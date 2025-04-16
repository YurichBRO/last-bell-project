import os
from jinja2 import Template

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "kids_photos": "детские_фото",
        "adults_photos": "взрослые_фото",
        "captions": "подписи"
    },
    "output": {
        "index_file": "index.html"  # Главная страница будет в корне
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def load_data():
    # Загружаем данные из папок
    kids = find_files(SETTINGS['input']['kids_photos'], '.jpg')
    adults = find_files(SETTINGS['input']['adults_photos'], '.jpg')
    captions = find_files(SETTINGS['input']['captions'], '.txt')
    
    # Создаем список учеников
    students = []
    for name in kids:
        if name not in adults or name not in captions:
            print(f"Пропущен: {name} (не хватает данных)")
            continue
        
        with open(captions[name], 'r', encoding='utf-8') as f:
            caption = f.read().strip()
        
        students.append({
            "name": name,
            "filename": name.replace(" ", "_"),  # Заменяем пробелы на подчеркивания
            "kid_photo": os.path.basename(kids[name]),
            "adult_photo": os.path.basename(adults[name]),
            "caption": caption
        })
    
    return students

def generate_pages(students):
    # Шаблон для страницы ученика
    student_template = Template("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ student.name }}</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        img { max-width: 100%; height: auto; margin: 10px; }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: blue; }
    </style>
</head>
<body>
    <h1>{{ student.name }}</h1>
    <img src="{{ student.kid_photo }}" alt="{{ student.name }} (1 класс)">
    <img src="{{ student.adult_photo }}" alt="{{ student.name }} (11 класс)">
    <p>{{ student.caption }}</p>
    <a href="index.html">На главную</a>
</body>
</html>
    """)
    
    # Генерируем страницы для каждого ученика
    for student in students:
        output_path = f"{student['filename']}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(student_template.render(student=student))
        print(f"Создана страница: {student['filename']}.html")

def generate_index(students):
    # Шаблон для главной страницы
    index_template = Template("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ученики</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; }
        a { text-decoration: none; color: blue; font-size: 18px; }
    </style>
</head>
<body>
    <h1>Наши ученики</h1>
    <ul>
        {% for student in students %}
        <li><a href="{{ student.filename }}.html">{{ student.name }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
    """)
    
    # Генерируем главную страницу
    output_path = SETTINGS['output']['index_file']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(index_template.render(students=students))
    print("Создана главная страница: index.html")

if __name__ == "__main__":
    # Загружаем данные и генерируем сайт
    students = load_data()
    generate_pages(students)
    generate_index(students)