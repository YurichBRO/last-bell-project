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
        "size": (800, 600),  # Желаемый размер фото (ширина, высота)
        "padding": 20  # Отступ при масштабировании
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def process_image(input_path, output_path, target_size):
    try:
        # Открываем изображение
        img = Image.open(input_path)
        
        # Масштабируем с сохранением пропорций
        target_width, target_height = target_size
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Широкое изображение - масштабируем по ширине
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            # Высокое изображение - масштабируем по высоте
            new_height = target_height
            new_width = int(target_height * img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Создаем финальное изображение с фоном
        final_img = Image.new('RGB', target_size, (255, 255, 255))
        pos_x = (target_width - new_width) // 2
        pos_y = (target_height - new_height) // 2
        final_img.paste(img_resized, (pos_x, pos_y))
        
        # Сохраняем результат
        final_img.save(output_path)
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