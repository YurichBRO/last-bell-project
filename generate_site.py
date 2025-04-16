import os

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "adults_photos": "взрослые_фото",  # Папка с фотографиями взрослых учеников
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
    adults = find_files(SETTINGS['input']['adults_photos'], '.jpg')
    captions = find_files(SETTINGS['input']['captions'], '.txt')
    
    # Создаем список учеников
    students = []
    for name in adults:
        if name not in captions:
            print(f"Пропущен: {name} (нет подписи)")
            continue
        
        with open(captions[name], 'r', encoding='utf-8') as f:
            caption = f.read().strip()
        
        students.append({
            "name": name,
            "filename": name.replace(" ", "_"),  # Заменяем пробелы на подчеркивания
            "adult_photo": os.path.join(SETTINGS['input']['adults_photos'], os.path.basename(adults[name])),
            "caption": caption
        })
    
    return students

def generate_pages(students):
    # Генерируем страницы для каждого ученика
    for student in students:
        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{student['name']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: #f9f9f9;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        a {{
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            color: blue;
            font-size: 18px;
        }}
        p {{
            font-size: 16px;
            color: #333;
        }}
        @media (max-width: 600px) {{
            img {{
                width: 90%;
            }}
        }}
    </style>
</head>
<body>
    <h1>{student['name']}</h1>
    <img src="{student['adult_photo']}" alt="{student['name']} (11 класс)">
    <p>{student['caption']}</p>
    <a href="index.html">На главную</a>
</body>
</html>
"""
        output_path = f"{student['filename']}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Создана страница: {student['filename']}.html")

def generate_index(students):
    # Генерируем главную страницу
    student_links = "\n".join(
        f'        <li><a href="{student["filename"]}.html">{student["name"]}</a></li>'
        for student in students
    )
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ученики</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: #f9f9f9;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
        }}
        a {{
            text-decoration: none;
            color: blue;
            font-size: 18px;
        }}
        @media (max-width: 600px) {{
            a {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <h1>Наши ученики</h1>
    <ul>
{student_links}
    </ul>
</body>
</html>
"""
    output_path = SETTINGS['output']['index_file']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Создана главная страница: index.html")

if __name__ == "__main__":
    # Загружаем данные и генерируем сайт
    students = load_data()
    generate_pages(students)
    generate_index(students)