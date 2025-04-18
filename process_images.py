import os
from PIL import Image

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "kids_photos": "необрезанные_детские",
        "adults_photos": "необрезанные_взрослые"
    },
    "output": {
        "kids_photos": "детские_фото",
        "adults_photos": "взрослые_фото",
        "size": (600, 800)  # Желаемый размер фото (ширина, высота)
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def process_image(input_path, output_path, target_size):
    try:
        # Открываем изображение
        img = Image.open(input_path)
        
        target_width, target_height = target_size
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        # Определяем новые размеры для масштабирования
        if img_ratio > target_ratio:
            # Широкое изображение: масштабируем по высоте до target_height
            new_height = target_height
            new_width = int(img.width * (new_height / img.height))
        else:
            # Узкое изображение: масштабируем по ширине до target_width
            new_width = target_width
            new_height = int(img.height * (new_width / img.width))
        
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Вычисляем координаты обрезки
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        # Обрезаем изображение
        img_cropped = img_resized.crop((left, top, right, bottom))
        
        # Сохраняем результат
        img_cropped.save(output_path)
        print(f"Обработано: {output_path}")
    
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {str(e)}")

def process_images():
    # Создаем выходные папки
    os.makedirs(SETTINGS['output']['kids_photos'], exist_ok=True)
    os.makedirs(SETTINGS['output']['adults_photos'], exist_ok=True)
    
    # Собираем файлы
    kids = find_files(SETTINGS['input']['kids_photos'], '.jpg')
    adults = find_files(SETTINGS['input']['adults_photos'], '.jpg')
    
    # Обрабатываем детские фото
    for name, input_path in kids.items():
        output_path = os.path.join(SETTINGS['output']['kids_photos'], f"{name}.jpg")
        process_image(input_path, output_path, SETTINGS['output']['size'])
    
    # Обрабатываем взрослые фото
    for name, input_path in adults.items():
        output_path = os.path.join(SETTINGS['output']['adults_photos'], f"{name}.jpg")
        process_image(input_path, output_path, SETTINGS['output']['size'])

if __name__ == "__main__":
    process_images()