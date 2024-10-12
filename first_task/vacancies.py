import requests
import pandas as pd
import matplotlib.pyplot as plt

# Создаем список регионов с их id и именами
regions = [
    {"id": "78", "name": "Самара"},
    {"id": "41", "name": "Калининград"}
]

# Список специальностей и грейдов
specialties = ["Data Analyst", "Data Science", "Data Engineer"]
grades = ["Junior", "Middle", "Senior"]

data = []

# Функция для получения вакансий
def get_vacancies(area_id, specialty, level):
    params = {
        "text": specialty + " " + level,
        "area": area_id,
        "per_page": 50,
        "page": 0
    }
    response = requests.get("https://api.hh.ru/vacancies", params=params)
    return response.json()

# Сбор данных
for region in regions:
    for specialty in specialties:
        for grade in grades:
            vacancies = get_vacancies(region["id"], specialty, grade)
            count = vacancies.get("found", 0)
            # Проверка на дублирование с использованием словаря
            data.append({
                "region": region["name"],
                "specialty": specialty,
                "grade": grade,
                "count": count
            })

# Создание датафрейма
df = pd.DataFrame(data)

# Удаление дубликатов, если они есть
df = df.drop_duplicates()

# Вывод таблицы
print(df)

# Сводная таблица
pivot_table = df.pivot_table(values='count', index=['region', 'specialty'], columns='grade', fill_value=0)

# Построение графика
pivot_table.plot(kind='bar', stacked=True)
plt.title('Количество вакансий по регионам и уровням')
plt.xlabel('Регион и специальность')
plt.ylabel('Количество вакансий')
plt.xticks(rotation=45)
plt.legend(title='Уровень')
plt.tight_layout()
plt.show()
