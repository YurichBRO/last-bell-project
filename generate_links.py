import os

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "kids_photos": "детские_фото"
    },
    "output": {
        "links_folder": "ссылки",  # Папка для сохранения ссылок
        "base_url": "https://yur-itch.github.io/last-bell-project/"  # Базовый URL сайта
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def generate_links():
    # Создаем папку для ссылок
    os.makedirs(SETTINGS['output']['links_folder'], exist_ok=True)
    
    # Находим всех учеников по детским фото
    kids = find_files(SETTINGS['input']['kids_photos'], '.jpg')
    
    # Генерируем ссылки для каждого ученика
    for name in kids:
        # Формируем имя файла для ссылки (оставляем пробелы)
        link_filename = f"{name}.txt"  # Имя файла с пробелами
        link_path = os.path.join(SETTINGS['output']['links_folder'], link_filename)
        
        # Формируем полную ссылку
        student_page = f"{name.replace(' ', '_')}.html"  # Имя HTML-страницы ученика (с подчеркиваниями)
        full_url = SETTINGS['output']['base_url'] + student_page
        
        # Сохраняем ссылку в файл
        with open(link_path, 'w', encoding='utf-8') as f:
            f.write(full_url)
        
        print(f"Создана ссылка: {link_path} -> {full_url}")

if __name__ == "__main__":
    generate_links()