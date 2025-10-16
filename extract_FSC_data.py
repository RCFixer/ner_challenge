from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd
from simpletransformers.ner import NERModel


class CompanyParser:
    """Класс для парсинга данных компаний с веб-страниц."""

    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def parse(self) -> List[Dict[str, str]]:
        """
        Парсит таблицу компаний с указанного URL.

        Returns:
            Список словарей с данными компаний (name, info)
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.content, 'html.parser')
            table = self._find_table(soup)

            if not table:
                print("Таблица не найдена!")
                return []

            companies = self._extract_companies(table)
            return companies

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return []
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            return []

    def _find_table(self, soup: BeautifulSoup):
        """Находит таблицу с данными компаний."""
        figure = soup.find('figure', {'class': 'wp-block-table'})
        return figure.find('table') if figure else None

    def _extract_companies(self, table) -> List[Dict[str, str]]:
        """Извлекает данные компаний из таблицы."""
        companies = []
        rows = table.find_all('tr')

        for row in rows[1:]:  # Пропускаем заголовок
            cols = row.find_all('td')

            if len(cols) == 2:
                company_name = cols[0].get_text(strip=True)
                company_info = cols[1].get_text(separator=" ").replace('  ', ' ')

                if company_name and not company_name.startswith('BRANCHES'):
                    companies.append({
                        'name': company_name,
                        'info': company_info
                    })

        return companies


class CompanyAnalyzer:
    """Класс для анализа данных компаний с использованием NER модели."""

    def __init__(self, model_path: str = "./result_model/"):
        self.model = NERModel("distilbert", model_path, use_cuda=False)

    def analyze(self, companies: List[Dict[str, str]]) -> pd.DataFrame:
        """
        Анализирует данные компаний и извлекает структурированную информацию.

        Args:
            companies: Список словарей с данными компаний

        Returns:
            DataFrame с извлеченными данными
        """
        processed_data = self._preprocess_companies(companies)
        predictions = self._predict_entities(processed_data)
        extracted_data = self._extract_entities(predictions, list(processed_data.keys()))

        return self._create_dataframe(extracted_data)

    def _preprocess_companies(self, companies: List[Dict[str, str]]) -> Dict[str, str]:
        """Предобработка текста компаний."""
        processed = {}

        for company in companies:
            company_name = company['name']
            company_info = company['info']

            # Удаляем слова, заканчивающиеся на двоеточие
            words = company_info.split()
            filtered_words = [word for word in words if not word.endswith(':')]
            cleaned_text = ' '.join(filtered_words).replace(':', ' ')

            # Удаляем лишние пробелы в числах и телефонах
            cleaned_text = self._remove_math_spaces(cleaned_text)
            processed[company_name] = cleaned_text

        return processed

    def _remove_math_spaces(self, text: str) -> str:
        """Удаляет пробелы между цифрами и специальными символами."""
        if len(text) < 2:
            return text

        result = [text[0]]

        for i in range(1, len(text) - 1):
            current_char = text[i]
            prev_char = text[i - 1]
            next_char = text[i + 1]

            # Пропускаем пробел между цифрами и специальными символами
            if (current_char == ' ' and
                    prev_char in '0123456789+/' and
                    next_char in '0123456789/'):
                continue

            result.append(current_char)

        if len(text) > 1:
            result.append(text[-1])

        return ''.join(result)

    def _predict_entities(self, processed_data: Dict[str, str]) -> List:
        """Получает предсказания NER модели."""
        predictions, _ = self.model.predict(list(processed_data.values()))
        return predictions

    def _extract_entities(self, predictions: List, company_names: List[str]) -> List[Dict[str, str]]:
        """Извлекает именованные сущности из предсказаний модели."""
        results = []

        for prediction, company_name in zip(predictions, company_names):
            result = {'COMPANY_NAME': company_name}
            current_entity = None

            for item in prediction:
                for text, label in item.items():
                    if label.startswith('B-') or (label.startswith('I-') and label[2:] != current_entity):
                        entity_type = label[2:]
                        result[entity_type] = text
                        current_entity = entity_type
                    elif label.startswith('I-') and current_entity:
                        result[current_entity] += ' ' + text
                    elif label == 'O':
                        if '@' in text:
                            result['EMAIL'] = text
                            current_entity = 'EMAIL'
                        elif '+' in text:
                            result['PHONE'] = text
                            current_entity = 'PHONE'

            results.append(result)

        return results

    def _create_dataframe(self, data: List[Dict[str, str]]) -> pd.DataFrame:
        """Создает DataFrame с правильными названиями колонок."""
        df = pd.DataFrame(data)

        # Переименовываем колонки
        column_mapping = {
            'COMPANY_NAME': 'Company Name',
            'PHONE': 'Numbers',
            'WEB': 'Website',
            'EMAIL': 'Email',
            'STREET': 'Street Address',
            'COUNTRY': 'Country',
            'CITY': 'City',
            'POSTAL_CODE': 'Postal Code'
        }
        df = df.rename(columns=column_mapping)

        # Определяем порядок колонок
        columns_order = [
            'Company Name', 'Numbers', 'Website', 'Email',
            'Street Address', 'Country', 'City', 'Postal Code'
        ]

        # Оставляем только существующие колонки в нужном порядке
        existing_columns = [col for col in columns_order if col in df.columns]
        df = df[existing_columns]

        return df


def main():
    """Основная функция для запуска парсинга и анализа."""
    url = "https://www.fsc.bg/en/investment-avtivity/lists-of-supervised-entities/investment-firms/"

    # Парсинг данных
    parser = CompanyParser(url)
    companies = parser.parse()

    if not companies:
        print("Не удалось получить данные компаний")
        return

    # Анализ данных
    analyzer = CompanyAnalyzer()
    result_df = analyzer.analyze(companies)

    # Настройка отображения pandas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Вывод результата
    print(result_df)


if __name__ == "__main__":
    main()
