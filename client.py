import os
import sys
import requests
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QLabel, QListWidget, QWidget, QMessageBox, QInputDialog
)

# Путь для загрузки файлов
DOWNLOAD_FOLDER = r"C:\DownloadedApps"


class AppStore(QMainWindow):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url
        self.setWindowTitle("Магазин приложений")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Доступные приложения:")
        self.layout.addWidget(self.label)

        self.app_list = QListWidget()
        self.layout.addWidget(self.app_list)

        self.download_button = QPushButton("Скачать и запустить")
        self.download_button.clicked.connect(self.download_and_run_app)
        self.layout.addWidget(self.download_button)

        self.apps = []
        self.load_apps()

    def load_apps(self):
        """Загружает список приложений с указанного сервера"""
        try:
            response = requests.get(f"{self.api_url}/api/apps")
            response.raise_for_status()
            self.apps = response.json()
            for app in self.apps:
                self.app_list.addItem(f"{app['name']} - {app['description']} (ID: {app['id']})")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список приложений: {e}")

    def download_and_run_app(self):
        """Скачивает выбранное приложение и запускает его"""
        selected_item = self.app_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Внимание", "Выберите приложение для скачивания.")
            return

        app_index = self.app_list.currentRow()
        app = self.apps[app_index]

        try:
            # Создаем папку для загрузки, если ее нет
            os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

            # Скачиваем файл
            file_path = os.path.join(DOWNLOAD_FOLDER, app['file'])
            response = requests.get(f"{self.api_url}/download/{app['file']}", stream=True)
            response.raise_for_status()

            # Сохраняем файл
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            QMessageBox.information(self, "Успех", f"Приложение {app['name']} загружено в {file_path}!")

            # Автоматически запускаем скачанное приложение
            if file_path.endswith(".exe"):  # Если это исполняемый файл
                subprocess.Popen(file_path, shell=True)
            else:
                QMessageBox.information(self, "Информация", f"Скачанный файл сохранен, но не является исполняемым: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось скачать или запустить приложение: {e}")


def format_server_ip(ip_input):
    """Добавляет http:// и стандартный порт 5000, если они не указаны"""
    ip_input = ip_input.strip()
    if not ip_input.startswith("http://") and not ip_input.startswith("https://"):
        ip_input = "http://" + ip_input

    # Проверяем наличие порта, добавляем стандартный порт 5000, если он отсутствует
    if ":" not in ip_input.split("//")[-1]:
        ip_input += ":5000"
    
    return ip_input


def get_server_ip():
    """Запрашивает у пользователя IP-адрес сервера"""
    ip, ok = QInputDialog.getText(None, "Укажите сервер", "Введите IP-адрес сервера (например, 127.0.0.1:5000):")
    if ok and ip.strip():
        return format_server_ip(ip.strip())
    else:
        QMessageBox.critical(None, "Ошибка", "Вы не указали IP-адрес сервера.")
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Получаем IP-адрес сервера от пользователя
    server_ip = get_server_ip()

    # Создаем и запускаем приложение
    window = AppStore(server_ip)
    window.show()
    sys.exit(app.exec_())
