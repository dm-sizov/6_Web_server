import socket
import os
from datetime import datetime

# Создание сокета для веб-сервера
sock = socket.socket()

# Попытка привязать сервер к порту 80
try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    # Если порт 80 занят, использовать порт 8080
    sock.bind(('', 8080))
    print("Using port 8080")

# Слушаем входящие соединения
sock.listen(5)

# Бесконечный цикл для обработки входящих соединений
while True:
    # Принятие соединения
    conn, addr = sock.accept()
    print("Connected", addr)

    # Получение данных от клиента
    data = conn.recv(8192)
    msg = data.decode()

    # Разбор запроса
    if msg:
        print("Received request:", msg)

        # Извлечение строки запроса из полученных данных
        request_line = msg.splitlines()[0]
        print("Request Line:", request_line)

        # Получение ресурса, запрашиваемого клиентом
        requested_resource = request_line.split()[1]

        # Если запрашиваемый ресурс корневой, используем index.html
        if requested_resource == '/':
            requested_resource = '/index.html'

        # Путь к запрашиваемому ресурсу в директории сервера
        filepath = '.' + requested_resource

        # Проверка на существование файла
        if not os.path.isfile(filepath):
            # Если файл не найден, отправляем 404 Not Found
            content = "<!DOCTYPE html><html lang=\"en\"><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
            response = """HTTP/1.1 404 Not Found
Date: {date}
Server: SelfMadeServer v0.0.1
Content-Type: text/html
Content-Length: {length}
Connection: close

{content}""".format(
                date=datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                length=len(content),
                content=content
            ).encode()
        else:
            # Если файл существует, читаем его содержимое
            with open(filepath, 'rb') as f:
                file_content = f.read()

            # Формируем ответ с содержимым запрашиваемого файла
            response_headers = f"""HTTP/1.1 200 OK
Date: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}
Server: SelfMadeServer v0.0.1
Content-Type: text/html
Content-Length: {len(file_content)}
Connection: close

"""
            # Отправляем содержимое файла вместе с заголовками
            response = response_headers.encode() + file_content

        # Отправляем ответ клиенту
        conn.send(response)

    # Закрытие соединения
    conn.close()
