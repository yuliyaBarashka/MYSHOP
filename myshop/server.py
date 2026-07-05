#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой веб-сервер для интернет-магазина.
Обрабатывает GET и POST запросы.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os


class MyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов"""

    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # Словарь маршрутов
        routes = {
            '/': 'index.html',
            '/catalog': 'catalog.html',
            '/contacts': 'contacts.html',
        }

        if path in routes:
            self.serve_html(routes[path])
        else:
            # Страница 404 для несуществующих маршрутов
            self.send_error_response(404, 'Страница не найдена')

    def do_POST(self):
        """Обработка POST запросов"""
        if self.path == '/contacts':
            try:
                # Получаем длину содержимого
                content_length = int(self.headers.get('Content-Length', 0))

                # Читаем данные из запроса
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Парсим данные
                parsed_data = urllib.parse.parse_qs(post_data)

                # Выводим данные в консоль с красивым форматированием
                print("\n" + "=" * 60)
                print("📨 ПОЛУЧЕНЫ ДАННЫЕ ОТ ПОЛЬЗОВАТЕЛЯ")
                print("=" * 60)
                for key, value in parsed_data.items():
                    print(f"  {key.capitalize()}: {value[0] if value else ''}")
                print("=" * 60 + "\n")

                # Отправляем ответ с перенаправлением
                self.send_response(303)
                self.send_header('Location', '/contacts')
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()

                # Показываем сообщение об успехе
                success_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="refresh" content="2;url=/contacts">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css&quot; rel="stylesheet">
                </head>
                <body>
                    <div class="container text-center mt-5">
                        <div class="alert alert-success">
                            <h4>✅ Сообщение отправлено!</h4>
                            <p>Вы будете перенаправлены на страницу контактов...</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode('utf-8'))

            except Exception as e:
                self.send_error_response(500, f'Ошибка обработки запроса: {str(e)}')
        else:
            self.send_error_response(404, 'Страница не найдена')

    def serve_html(self, filename):
        """Отправка HTML файла"""
        try:
            # Читаем файл с помощью контекстного менеджера
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error_response(404, f'Файл {filename} не найден')
        except Exception as e:
            self.send_error_response(500, f'Внутренняя ошибка сервера: {str(e)}')

    def send_error_response(self, code, message):
        """Отправка ответа с ошибкой"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        error_html = f"""


<!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ошибка {code}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css&quot; rel="stylesheet">
        </head>
        <body>
            <div class="container text-center mt-5">
                <h1 class="display-1 text-danger">{code}</h1>
                <div class="display-4 mb-3">😕</div>
                <h2 class="mb-3">Что-то пошло не так</h2>
                <p class="lead">{message}</p>
                <div class="mt-4">
                    <a href="/" class="btn btn-primary">На главную</a>
                    <a href="/catalog" class="btn btn-outline-secondary">В каталог</a>
                </div>
                <hr class="my-4">
                <p class="text-muted small">Попробуйте перейти на другую страницу или вернуться позже</p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode('utf-8'))

    def log_message(self, format, *args):
        """Переопределяем метод логирования для более читаемого вывода"""
        print(f"[{self.address_string()}] {format % args}")


def run_server(port=8000):
    """Запуск сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)

    print("=" * 60)
    print("🛒 ИНТЕРНЕТ-МАГАЗИН - ВЕБ-СЕРВЕР")
    print("=" * 60)
    print(f"✅ Сервер запущен на порту {port}")
    print(f"🌐 Откройте в браузере: http://localhost:{port}")
    print("\n📄 Доступные страницы:")
    print(f"   • http://localhost:{port}/        - Главная")
    print(f"   • http://localhost:{port}/catalog  - Каталог")
    print(f"   • http://localhost:{port}/contacts - Контакты")
    print("\n💡 Нажмите Ctrl+C для остановки сервера")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Сервер остановлен")
        print("=" * 60)
        httpd.shutdown()


if __name__ == '__main__':
    run_server()