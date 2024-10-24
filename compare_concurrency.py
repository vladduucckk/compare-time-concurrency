import time
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# URL для тестування
url = "https://httpbin.org/get"


# Синхронний режим
def sync_requests(n):
    for _ in range(n):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Викине помилку, якщо статус-код не 200
            _ = response.json()  # Спроба отримати JSON
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            print(f"Request error occurred: {e}")  # Вивести помилку
        except ValueError:
            print(f"JSON decode error: {response.text}")  # Вивести текст відповіді, якщо JSON не дійсний


# Багатопотоковий режим
def thread_requests(n):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for _ in range(n)]
        for future in futures:
            try:
                response = future.result()
                response.raise_for_status()  # Перевірка статус-коду
                _ = response.json()
            except (requests.exceptions.HTTPError, ValueError) as e:
                print(f"Error occurred: {e}")


# Багатопроцесорний режим
def fetch(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.HTTPError, ValueError) as e:
        return str(e)


def process_requests(n):
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fetch, url) for _ in range(n)]
        for future in futures:
            result = future.result()
            if isinstance(result, dict):  # Assuming JSON returns a dictionary
                print(result)
            else:
                print(f"Error occurred: {result}")


# Асинхронний режим
async def async_requests(n):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(n):
            task = asyncio.create_task(session.get(url))
            tasks.append(task)

        for task in tasks:
            response = await task
            if response.status == 200:
                try:
                    _ = await response.json()
                except ValueError:
                    text = await response.text()
                    print(f"JSON decode error: {text}")


# Головна функція для вимірювання часу виконання
async def main():
    n = 5  # 500 запитів дуже довго виконуються в синхронному режимі, тому я зробив 5))

    # Синхронний
    start_time = time.time()
    sync_requests(n)
    print(f"Синхронний: {time.time() - start_time:.2f} секунд")

    # Багатопотоковий
    start_time = time.time()
    thread_requests(n)
    print(f"Багатопотоковий: {time.time() - start_time:.2f} секунд")

    # Багатопроцесорний
    start_time = time.time()
    process_requests(n)
    print(f"Багатопроцесорний: {time.time() - start_time:.2f} секунд")

    # Асинхронний
    start_time = time.time()
    await async_requests(n)
    print(f"Асинхронний: {time.time() - start_time:.2f} секунд")


# Запуск
if __name__ == "__main__":
    asyncio.run(main())
