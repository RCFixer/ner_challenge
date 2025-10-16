import json
import random

# -----------------------------
#  Расширенные списки данных
# -----------------------------

# Болгарские города (≈150)
cities = [
    "Sofia", "Plovdiv", "Varna", "Burgas", "Ruse", "Stara Zagora", "Pleven", "Sliven", "Dobrich", "Shumen",
    "Pernik", "Haskovo", "Yambol", "Blagoevgrad", "Veliko Tarnovo", "Vratsa", "Gabrovo", "Kazanlak", "Asenovgrad",
    "Vidin", "Kardzhali", "Kyustendil", "Montana", "Lovech", "Pazardzhik", "Silistra", "Targovishte", "Razgrad",
    "Smolyan", "Sandanski", "Gotse Delchev", "Dupnitsa", "Sevlievo", "Nova Zagora", "Karlovo", "Svishtov",
    "Troyan", "Botevgrad", "Petrich", "Pomorie", "Velingrad", "Samokov", "Kavarna", "Balchik", "Nessebar", "Sozopol",
    "Byala", "Obzor", "Etropole", "Elhovo", "Zlatograd", "Belene", "Devnya", "Lom", "Isperih", "Belovo", "Aytos",
    "Mezdra", "Tryavna", "Razlog", "Bankya", "Hisarya", "Chepelare", "Teteven", "Sopot", "Pirdop", "Berkovitsa",
    "Panagyurishte", "Karnobat", "Kostenets", "Septemvri", "Lyaskovets", "Knezha", "Gorna Oryahovitsa", "Provadia",
    "Kotel", "Pavlikeni", "Bansko", "Devin", "Dulovo", "Momchilgrad", "Belogradchik", "Ivaylovgrad", "Zlataritsa",
    "Rakitovo", "Bozhurishte", "Rudozem", "Shipka", "Dalgopol", "Yablanitsa", "Kuklen", "Loznitsa", "Tutrakan",
    "Kresna", "Levski", "Krivodol", "Nikopol", "Kostinbrod", "Dryanovo", "Bobov Dol", "General Toshevo", "Elena",
    "Tsarevo", "Pravets", "Lukovit", "Topolovgrad", "Chepelare", "Dolna Mitropoliya", "Sarnitsa", "Aksakovo",
    "Simeonovgrad", "Bratsigovo", "Dolni Chiflik", "Oryahovo", "Byala Slatina", "Glavinitsa", "Kotel", "Kaspichan",
    "Zemen", "Perushtitsa", "Suhindol", "Stamboliyski", "Peshtera", "Harmanli", "Beloslav", "Rakitovo", "Lesichovo"
]

# Улицы (≈200)
streets = [
    "Knyaz Boris I Blvd.", "Todor Aleksandrov Blvd.", "Vitosha Blvd.", "Tsar Osvoboditel Str.",
    "Hristo Botev Str.", "Cherni Vrah Blvd.", "Alexander Stamboliyski Blvd.", "Tsarigradsko Shose Blvd.",
    "Damyan Gruev Str.", "Gen. Totleben Blvd.", "Lyuben Karavelov Str.", "Patriarh Evtimiy Blvd.",
    "Shipka Str.", "Rakovski Str.", "Opalchenska Str.", "Moskovska Str.", "Maria Luiza Blvd.",
    "Graf Ignatiev Str.", "Evlogi Georgiev Blvd.", "Dragan Tsankov Blvd.", "Nikola Vaptsarov Blvd.",
    "Bacho Kiro Str.", "Ivan Vazov Str.", "San Stefano Str.", "Slivnitsa Blvd.", "Bregalnitsa Str.",
    "Skobelev Blvd.", "Saborna Str.", "Petko Karavelov Str.", "Hristo Smirnenski Blvd.", "Luben Karavelov Str.",
    "Parchevich Str.", "Krakra Str.", "Neofit Rilski Str.", "Oborishte Str.", "Vasil Levski Blvd.",
    "Slavyanska Str.", "6th September Blvd.", "Yanko Sakazov Blvd.", "Alabin Str.", "Simeon Str.",
    "Dondukov Blvd.", "Tsvetan Lazarov Blvd.", "Tsar Simeon Blvd.", "Kiril i Metodii Str.", "Boris III Blvd.",
    "Lozenets Str.", "Boyana Str.", "Belasitsa Str.", "Pirin Str.", "Struma Str.", "Maritsa Blvd.",
    "Yantra Str.", "Veliko Tarnovo Blvd.", "Pliska Blvd.", "Sevastopol Str.", "Primorski Blvd.", "Cherno More Blvd.",
    "Dragoman Str.", "Orlov Most Blvd.", "Kavala Str.", "Hemus Blvd.", "Kaloyan Str.", "Trakia Blvd.",
    "Izgrev Blvd.", "Rodopi Str.", "Sredets Blvd.", "Hristo G. Danov Str.", "Mladost Blvd.",
    "Mizia Str.", "Knyaginya Maria Luiza Blvd.", "Sveta Nedelya Str.", "Stamboliyski Blvd.",
    "Parensov Str.", "Veliko Tarnovo Str.", "Struma Blvd.", "Lomsko Shose Blvd.", "G.S. Rakovski Str.",
    "Vardar Blvd.", "Iskar Blvd.", "Pleven Str.", "Bulgaria Blvd.", "Patriarh German Blvd.", "Hadzhi Dimitar Str.",
    "Kalofer Str.", "Vihren Str.", "Kamenitza Blvd.", "Stara Planina Blvd.", "Opalchenska Blvd.",
    "Shipchenski Prohod Blvd.", "Kostinbrod Str.", "Rila Str.", "Balkan Str.", "Dunav Blvd.",
    "Rozhen Blvd.", "Orfeev Str.", "Sredna Gora Blvd.", "Zlaten Rog Blvd.", "Elin Pelin Str.", "Pirin Blvd."
]

# Компании и домены (≈300)
companies = [
    "abvinvest", "abc-finance", "acp", "alaricsecurities", "allianz", "dfcoad", "bac", "mkb", "benchmark",
    "gfex", "bnpparibas", "bulbrokers", "bacb", "bdbank", "investcapital", "capman", "ccbank", "citibank",
    "dbank", "denovo", "deltastock", "dvinvest", "dskbank", "elana", "eurofinance", "postbank", "grandcapital",
    "unicredit", "fibank", "sgebank", "ubb", "procredit", "raiffeisen", "tokuda", "tbi", "otpbank",
    "expressbank", "teximbank", "levins", "piraeus", "alphabank", "bulstrad", "arco", "smartfinance",
    "finbroker", "easymoney", "creditplus", "investgroup", "finconsult", "capitaladvisors", "balkantrade",
    "metafinance", "eurotrust", "novafin", "futureinvest", "avangardfinance", "maxtrade", "solarinvest",
    "euroline", "eastcapital", "bulgariafund", "bgfinance", "smartinvest", "futurebank", "sofinvest", "greenfinance",
    "bluecapital", "financegroup", "alphainvest", "investtrade", "trustbank", "globalfund", "primeinvest",
    "goldfinance", "platinumfund", "credittrust", "bizcapital", "firstinvest", "capitalonebg", "fintechbg",
    "bulgariatrust", "smartcredit", "lendify", "microcredit", "megafinance", "minibank", "maxfinance"
]

domains = [".bg", ".eu", ".com", ".net", ".info", ".org"]

# -----------------------------
#  Генераторы случайных полей
# -----------------------------
def random_postal():
    return str(random.randint(1000, 9999))

def random_street():
    # Форматы: "1 Dyakon Ignatiy Str.", "10 Stefan Karadja Str., fl. 3, office 7"
    number = random.randint(1, 50)
    name = random.choice(streets)
    suffix = random.choice(["Str.", "Blvd.", "Ave."])
    extra = []
    if random.random() < 0.3:
        extra.append(f"fl. {random.randint(1, 5)}")
    if random.random() < 0.3:
        extra.append(f"office {random.randint(1, 20)}")
    return f"{number} {name} {suffix}" + (", " + ", ".join(extra) if extra else "")




def random_phone():
    # Все возможные форматы болгарских телефонных номеров
    choice = random.choice(["mobile", "short1", "short2", "mobile2", "mobile3",
                            "sofia_full", "sofia_spaced", "regional", "simple_mobile",
                            "international", "domestic", "brackets"])

    if choice == "mobile":
        return f"+359{random.randint(2_800_0000, 2_999_9999)}"
    elif choice == "short1":
        return f"02/{random.randint(4000000, 4999999)}"
    elif choice == "short2":
        return f"02/{random.randint(400, 499)} {random.randint(10, 99)} {random.randint(10, 99)}"
    elif choice == "mobile2":
        return f"+ 359 {random.choice(['2', '52', '32', '42', '62'])} {random.randint(100000, 999999)}"
    elif choice == "mobile3":
        return f"+359 {random.choice(['2', '52', '32', '42', '62'])} {random.randint(100000, 999999)}"
    elif choice == "sofia_full":
        # Формат: + 359 2 81 64 370
        return f"+ 359 2 {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(100, 999)}"
    elif choice == "sofia_spaced":
        # Формат: + 359 2 439 81 50
        return f"+ 359 2 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"
    elif choice == "regional":
        # Формат: +  032/ 62 54 01
        region = random.choice(['32', '52', '42', '62', '38'])
        return f"+ {region}/{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"
    elif choice == "simple_mobile":
        # Формат: +359 896 757 855
        return f"+359 {random.randint(87, 89)}{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(100, 999)}"
    elif choice == "international":
        # Формат: +359 (0) 700 156 56
        return f"+359 (0) {random.randint(700, 799)} {random.randint(100, 999)} {random.randint(10, 99)}"
    elif choice == "domestic":
        # Формат: 02/8186182 или 02/ 8186 128
        if random.random() > 0.5:
            return f"02/{random.randint(1000000, 9999999)}"
        else:
            return f"02/ {random.randint(1000, 9999)} {random.randint(100, 999)}"
    elif choice == "brackets":
        # Формат: (02) 4893 715
        return f"(02) {random.randint(1000, 9999)} {random.randint(100, 999)}"
    else:
        # Универсальный формат с различными разделителями
        formats = [
            f"+359 2 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
            f"+359 2/{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
            f"+359 2 {random.randint(1000, 9999)} {random.randint(100, 999)}",
            f"02/{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
            f"02/{random.randint(1000, 9999)} {random.randint(10, 99)}"
        ]
        return random.choice(formats)

def random_email(company):
    user = random.choice(["office", "info", "contact", "admin", "sales"])
    return f"{user}@{company}{random.choice(domains)}"

def random_web(company):
    prefix = random.choice(["www.", "https://www.", "http://"])
    return f"{prefix}{company}{random.choice(domains)}"

# -----------------------------
#  Создание одного примера
# -----------------------------
def make_example():
    city = random.choice(cities)
    postal = random_postal()
    streets = [random_street() for _ in range(random.randint(1, 2))]
    company = random.choice(companies)

    # Несколько телефонов, emails, web-сайтов
    phones = [random_phone() for _ in range(random.randint(1, 3))]
    emails = [random_email(company) for _ in range(random.randint(1, 2))]
    webs = [random_web(company) for _ in range(random.randint(1, 2))]

    # --- новое: вариативные шаблоны адресов ---
    patterns = [
        # классические адреса
        "BULGARIA, {postal} {city}, {streets}, tel: {phones}; E-mail: {emails} WEB: {webs}",
        "{city} {postal}, {streets}, BULGARIA, tel: {phones}; WEB: {webs}; E-mail: {emails}",
        "BULGARIA, {city}, {streets}, tel.: {phones}, fax: {phones2}; E-mail: {emails} WEB: {webs}",
        "{streets}, {postal} {city}, BULGARIA. Tel: {phones}. {webs} {emails}",
        "BULGARIA, {postal} {city}, {streets}. Phones: {phones}. Emails: {emails}. Web: {webs}",
        "{city}, {streets}, BULGARIA {postal}. Contact: {phones}; {emails}; {webs}",
        "BULGARIA, {city}, {streets}, tel: {phones}; fax: {phones2} {emails} {webs}",

        # варианты без страны
        "{postal} {city}, {streets}. Tel: {phones}. {emails} {webs}",
        "{city}, {streets}, {postal}. Phones: {phones}. {webs}",
        "{streets}, {city} {postal}. E-mail: {emails}; Web: {webs}",
        "{streets}, {city}. tel: {phones} / fax: {phones2}, {emails}",

        # минималистичные
        "{city}, {streets}. {emails}",
        "{streets}, {city}. tel: {phones}",
        "{city}, {streets}. {webs}",
        "{streets}, {city}. Contact: {phones}",

        # с разными словами и разделителями
        "Address: {streets}, {city}, {postal}, BULGARIA | Phone: {phones} | E-mail: {emails} | Web: {webs}",
        "Head Office – {city}, {streets}, BULGARIA {postal}. Tel.: {phones} / Fax: {phones2} / {emails}",
        "Office: {streets}, {city}, {postal}. For info call: {phones}, or visit {webs}",
        "{streets}, {postal} {city}, tel: {phones}. For contact: {emails}",
        "BULGARIA – {city}, {streets}. Tel/Fax: {phones}, {phones2}. {webs}",
        "Registered office: {streets}, {city}, {postal}. E-mail: {emails}. Web: {webs}",
        "{city}, {streets}, {postal}. Tel.: {phones} / {phones2} / {emails}",
        "Main branch: {streets}, {city}. Contacts: {phones}, {emails}, {webs}",
        "BULGARIA, {city}, {streets}. {emails}. {webs}",
        "Postal code {postal}, {city}, {streets}. Tel: {phones}. {webs}"
    ]

    # дополнительный список телефонов для факсов/вторичных номеров
    phones2 = [random_phone() for _ in range(random.randint(0, 2))]

    # выбираем случайный шаблон
    pattern = random.choice(patterns)

    text = pattern.format(
        postal=postal,
        city=city,
        streets=", ".join(streets),
        phones=", ".join(phones),
        phones2=", ".join(phones2) if phones2 else "",
        emails=", ".join(emails),
        webs=" ".join(webs)
    ).strip()

    def span(term, label):
        start = text.find(term)
        return {"text": term, "start": start, "end": start + len(term), "label": label}

    labels = [
        span("BULGARIA", "COUNTRY"),
        span(postal, "POSTAL_CODE"),
        span(city, "CITY")
    ]

    for s in streets:
        labels.append(span(s, "STREET"))
    for p in phones:
        labels.append(span(p, "PHONE"))
    for p2 in phones2:
        labels.append(span(p2, "PHONE"))
    for e in emails:
        labels.append(span(e, "EMAIL"))
    for w in webs:
        labels.append(span(w, "WEB"))

    return {"text": text.strip(), "labels": labels}

# -----------------------------
#  Генерация датасета
# -----------------------------
dataset = [make_example() for _ in range(20000)]

with open("bulgarian_addresses_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print(f"✅ Generated {len(dataset)} examples with complex addresses → 'bulgarian_addresses_dataset.json'")
