import os
from PIL import Image
import qrcode

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "kids_photos": "детские_фото",
        "links": "ссылки"
    },
    "output": {
        "folder": "готовые_фото",
        "size": (800, 600),  # Желаемый размер фото (ширина, высота)
        "qr_position": (50, 50),  # Отступ QR-кода от правого нижнего угла
        "qr_size": 200,  # Размер стороны QR-кода
        "padding": 20  # Отступ при масштабировании
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def process_images():
    os.makedirs(SETTINGS['output']['folder'], exist_ok=True)
    
    # Собираем только нужные файлы
    kids = find_files(SETTINGS['input']['kids_photos'], '.jpg')
    links = find_files(SETTINGS['input']['links'], '.txt')
    
    for name in kids:
        try:
            # Проверяем наличие только ссылки
            if name not in links:
                print(f"Нет ссылки для {name}")
                continue
            
            # Загружаем данные
            kid_img = Image.open(kids[name])
            with open(links[name], 'r', encoding='utf-8') as f:
                link = f.read().strip()
            
            # Генерируем QR-код
            qr = qrcode.QRCode(box_size=5)
            qr.add_data(link)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((SETTINGS['output']['qr_size'],)*2)
            
            # Масштабируем фото с сохранением пропорций
            target_width, target_height = SETTINGS['output']['size']
            kid_ratio = kid_img.width / kid_img.height
            target_ratio = target_width / target_height
            
            if kid_ratio > target_ratio:
                new_width = target_width
                new_height = int(target_width / kid_ratio)
            else:
                new_height = target_height
                new_width = int(target_height * kid_ratio)
            
            kid_resized = kid_img.resize((new_width, new_height), Image.LANCZOS)
            
            # Создаем финальное изображение
            final_img = Image.new('RGB', SETTINGS['output']['size'], (255,255,255))
            pos_x = (target_width - new_width) // 2
            pos_y = (target_height - new_height) // 2
            final_img.paste(kid_resized, (pos_x, pos_y))
            
            # Вставляем QR-код
            qr_pos_x = final_img.width - qr_img.width - SETTINGS['output']['qr_position'][0]
            qr_pos_y = final_img.height - qr_img.height - SETTINGS['output']['qr_position'][1]
            final_img.paste(qr_img, (qr_pos_x, qr_pos_y))
            
            # Сохраняем результат
            output_path = os.path.join(SETTINGS['output']['folder'], f"{name}_qr.jpg")
            final_img.save(output_path)
            print(f"Обработано: {name}")
        
        except Exception as e:
            print(f"Ошибка при обработке {name}: {str(e)}")

if __name__ == "__main__":
    process_images()