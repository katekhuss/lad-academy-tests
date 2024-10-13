import requests
import pandas as pd
import matplotlib.pyplot as plt

# Создаем список регионов с их id и именами
regions = [
    {"id": "78", "name": "Самара"},
    {"id": "41", "name": "Калининград"}
]

# Список специальностей и грейдов + c русскоязычными вариантами
specialties = [
    {"name": "Data Analyst", "keywords": ["Data Analyst", "Дата аналитик", "Аналитик по данным"]},
    {"name": "Data Science", "keywords": ["Data Science", "Дата сайентист"]},
    {"name": "Data Engineer", "keywords": ["Data Engineer", "Инженер по данным", "Дата инженер"]}
]
grades = ["Junior", "Middle", "Senior"]

data = []

# Функция для получения вакансий
def get_vacancies(area_id, keyword, level):
    params = {
        "text": keyword + " " + level,
        "area": area_id,
        "per_page": 50,
        "page": 0
    }
    response = requests.get("https://api.hh.ru/vacancies", params=params)
    return response.json()

# Сбор данных
for region in regions:
    for specialty in specialties:
        total_count = 0
        # Получаем данные по всем ключевым словам (английские и русские варианты)
        for keyword in specialty["keywords"]:
            for grade in grades:
                vacancies = get_vacancies(region["id"], keyword, grade)
                count = vacancies.get("found", 0)
                total_count += count
                # Сохраняем результаты по каждой специальности и грейду
                data.append({
                    "region": region["name"],
                    "specialty": specialty["name"],
                    "grade": grade,
                    "keyword": keyword,
                    "count": count
                })
        
        # Суммируем результаты для всех вариантов названий специальности
        for grade in grades:
            data.append({
                "region": region["name"],
                "specialty": specialty["name"],
                "grade": grade,
                "keyword": "Total",
                "count": total_count
            })

# Создание датафрейма
df = pd.DataFrame(data)

# Удаление дубликатов, если они есть
df = df.drop_duplicates()

# Вывод таблицы
print(df)

# Сводная таблица для общего количества вакансий по всем названиям
pivot_table = df[df['keyword'] == "Total"].pivot_table(values='count', index=['region', 'specialty'], columns='grade', fill_value=0)

# Построение графика
pivot_table.plot(kind='bar', stacked=True)
plt.title('Количество вакансий по регионам и уровням')
plt.xlabel('Регион и специальность')
plt.ylabel('Количество вакансий')
plt.xticks(rotation=45)
plt.legend(title='Уровень')
plt.tight_layout()
plt.show()
