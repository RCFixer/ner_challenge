import logging
import json
from simpletransformers.ner import NERModel, NERArgs
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# 1. Подготовка данных
def create_sample_data():
    with open('bulgarian_addresses_dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def convert_to_simpletransformers_format_bio(data):
    """
    Конвертирует данные в формат B-I (Beginning-Inside)
    Для сущностей, состоящих из нескольких слов, первый токен получает метку B-, остальные I-

    Args:
        data: список словарей в вашем формате

    Returns:
        pandas DataFrame с колонками: sentence_id, words, labels
    """
    converted_data = []

    for sentence_id, item in enumerate(data):
        text = item["text"]
        labels_info = item["labels"]

        # Сортируем сущности по начальной позиции
        labels_info.sort(key=lambda x: x["start"])

        # Создаем словарь для хранения меток по позициям символов
        label_dict = {}
        for label_info in labels_info:
            start = label_info["start"]
            end = label_info["end"]
            label = label_info["label"]
            if start == -1:
                continue

            # Помечаем все символы в диапазоне
            for pos in range(start, end):
                label_dict[pos] = label

        # Разбиваем текст на слова по пробелам и определяем их позиции
        words = []
        word_positions = []

        current_word = ""
        word_start = None

        for pos, char in enumerate(text):
            if char == ' ':
                if current_word:
                    words.append(current_word)
                    word_positions.append((word_start, pos))
                    current_word = ""
                    word_start = None
            else:
                if not current_word:
                    word_start = pos
                current_word += char

        # Добавляем последнее слово
        if current_word:
            words.append(current_word)
            word_positions.append((word_start, len(text)))

        # Определяем метки для каждого слова в формате B-I
        labels = []
        previous_label = "O"

        for i, (word, (start, end)) in enumerate(zip(words, word_positions)):
            # Определяем основную метку для слова (по первому символу)
            word_label = label_dict.get(start, "O")

            if word_label == "O":
                labels.append("O")
            else:
                # Проверяем, продолжается ли сущность с предыдущего слова
                if previous_label == word_label:
                    labels.append(f"I-{word_label}")
                else:
                    labels.append(f"B-{word_label}")

            previous_label = word_label

        # Добавляем в результат
        for word, label in zip(words, labels):
            converted_data.append({
                "sentence_id": sentence_id,
                "words": word,
                "labels": label
            })

    return pd.DataFrame(converted_data)


# 2. Конфигурация
model_args = NERArgs()
model_args.num_train_epochs = 5
model_args.learning_rate = 3e-5
model_args.overwrite_output_dir = True
model_args.output_dir = "./result_model/"
model_args.best_model_dir = "./result_model/best_model/"
model_args.save_model_every_epoch = False
model_args.save_steps = -1  # ⭐ не сохранять промежуточные чекпоинты
model_args.save_eval_checkpoints = False


# ⭐ КРИТИЧЕСКИ ВАЖНЫЕ НАСТРОЙКИ ДЛЯ ПАМЯТИ ⭐
model_args.train_batch_size = 2           # Очень маленький батч
model_args.eval_batch_size = 2
model_args.gradient_accumulation_steps = 4 # Эмулирует большой батч
model_args.max_seq_length = 128           # Укоротить последовательности
model_args.save_steps = -1                # Не сохранять чекпоинты
model_args.save_model_every_epoch = False
model_args.no_cache = True               # Не кешировать данные в памяти
model_args.use_multiprocessing = False    # Отключить многопроцессорность

# 3. Обучение

model = NERModel(
     "distilbert",
    "distilbert-base-multilingual-cased",
    labels=['B-COUNTRY', 'O', 'B-POSTAL_CODE', 'B-CITY', 'I-CITY', 'O', 'B-STREET_NUM', 'B-STREET', 'O', 'I-STREET', 'O', 'B-PHONE', 'I-PHONE', 'B-EMAIL', 'I-EMAIL', 'O', 'B-WEB', 'I-WEB'],
    args=model_args,
    use_cuda=True  # Использовать GPU если доступен
)

train_data = create_sample_data()
train_df = convert_to_simpletransformers_format_bio(train_data)

model.train_model(train_df)

model.save_model()
print("✅ Модель сохранена в папке './result_model/'")

# 4. Использование
predictions, _ = model.predict(["""BULGARIA, Sofia 1000, 1 Dyakon Ignatiy  Str., 10 Stefan Karadja Str.
tel: + 359 2 93 06 333
fax: +359 2 930 63 21,
E-mail: office@bdbank.bg,
WEB: www.bdbank.bg WEB www.bdbank.bg"""])
print(predictions)
