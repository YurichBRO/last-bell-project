import requests

def shorten_url(long_url):
    """
    Сокращает длинную ссылку с помощью TinyURL API.

    :param long_url: str - исходная длинная ссылка
    :return: str - сокращенная ссылка
    """
    api_url = "https://tinyurl.com/api-create.php"
    try:
        # Отправляем GET-запрос к TinyURL API
        response = requests.get(api_url, params={"url": long_url})
        # Проверяем успешность запроса
        if response.status_code == 200:
            return response.text  # Возвращаем сокращенную ссылку
        else:
            raise Exception(f"Ошибка при сокращении ссылки. Код: {response.status_code}")
    except requests.RequestException as e:
        # Обрабатываем ошибки сети или запроса
        raise Exception(f"Ошибка сети: {e}")

# Пример использования
if __name__ == "__main__":
    long_url = "https://www.example.com/very/long/url/that/needs/to/be/shortened"
    try:
        short_url = shorten_url(long_url)
        print(f"Сокращенная ссылка: {short_url}")
    except Exception as e:
        print(e)