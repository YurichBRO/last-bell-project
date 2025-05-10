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
        
        # Форматируем цитату
        if not caption:
            caption = ""
        else:
            caption = f'<span class="quote-sign">«</span>{caption}<span class="quote-sign">»</span>'
        
        students.append({
            "name": name,
            "filename": name.replace(" ", "_"),  # Заменяем пробелы на подчеркивания
            "adult_photo": os.path.join(SETTINGS['input']['adults_photos'], os.path.basename(adults[name])),
            "caption": caption
        })
    
    return students

def generate_pages(students):
    # Загружаем шаблон из файла
    with open('student_template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    for student in students:
        html_content = template.replace('{{ title }}', student['name'])
        html_content = html_content.replace('{{ name }}', student['name'])
        html_content = html_content.replace('{{ photo }}', student['adult_photo'])
        html_content = html_content.replace('{{ caption }}', student['caption'])
        
        output_path = f"{student['filename']}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Создана страница: {student['filename']}.html")

def generate_index(students):
    # Генерируем ссылки на учеников, где каждый элемент списка — ссылка
    student_links = "\n".join(
        f'        <li class="list-group-item"><a href="{student["filename"]}.html">{student["name"]}</a></li>'
        for student in students
    )
    
    # Загружаем шаблон из файла
    with open('index_template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    html_content = template.replace('{{ student_links }}', student_links)
    
    output_path = SETTINGS['output']['index_file']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Создана главная страница: index.html")

if __name__ == "__main__":
    # Загружаем данные и генерируем сайт
    students = load_data()
    generate_pages(students)
    generate_index(students)