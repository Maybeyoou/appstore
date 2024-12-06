import os
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Абсолютный путь к папке, где хранятся приложения
BASE_DIR = r"C:\prog\webstoreserver"
APPS_DIR = os.path.join(BASE_DIR, "apps")

# Список приложений
APPS = [
    {"id": 1, "name": "amneziaVPN", "description": "VPN сервис", "file": "AmneziaVPN.exe"},
    {"id": 2, "name": "anydesk", "description": "програма удаленого доступа", "file": "anydesk.exe"},
    {"id": 3, "name": "discord", "description": "приложение для разговоров поинтернету на пк", "file": "discord.exe"},
    {"id": 4, "name": "java17", "description": "", "file": "java17.msi"},
    {"id": 5, "name": "java21", "description": "Читалка PDF-документов.", "file": "java21.msi"},
    {"id": 6, "name": "nvidia_app", "description": "приложение от nvidia для загрузки драйверов.", "file": "nvidia_app.exe"},
    {"id": 7, "name": "obs_studio", "description": "Приложение для записи и стрима экрана.", "file": "obs_studio.exe"},
    {"id": 8, "name": "radminVPN", "description": "Простой файловый менеджер.", "file": "radmin_vpn.exe"},
    {"id": 9, "name": "steam", "description": "самый популярный магазин игр.", "file": "steam.exe"},
    {"id": 10, "name": "telegram", "description": "месенджер.", "file": "telegram.exe"},
    {"id": 11, "name": "visualstudiacode", "description": "програма для програмирования на которой написана эта програма .", "file": "visualstudiacode.exe"},
    {"id": 12, "name": "vlcmediaplaer", "description": "медиа плаер с открытым исходным кодом .", "file": "vlcmediaplaer.exe"},
    {"id": 13, "name": "yandexbrouser", "description": "браузер от яндекс", "file": "yandexbrouser.exe"},
]



@app.route('/api/apps', methods=['GET'])
def get_apps():
    """Возвращает список приложений"""
    return jsonify(APPS)


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Отдает файл из папки apps"""
    return send_from_directory(APPS_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    # Убедитесь, что папка apps существует
    if not os.path.exists(APPS_DIR):
        os.makedirs(APPS_DIR)
        print(f"Создана папка: {APPS_DIR}")
    print(f"Приложения хранятся в: {APPS_DIR}")
    # Запуск сервера
    app.run(host="0.0.0.0", port=5000)
