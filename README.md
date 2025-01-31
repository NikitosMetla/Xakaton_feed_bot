# 🐾 Telegram Бот для Учёта и Распределения Корма – "Накорми"

## 📌 Описание проекта

Данный Telegram-бот предназначен для автоматизированного учёта, передачи и распределения корма среди благополучателей и волонтёров. Он оптимизирует процессы управления точками сбора, складским учетом и заявками, помогая зоозащитным организациям эффективнее координировать свою работу.

## 🚀 Функциональные возможности

- 📋 **Создание личных кабинетов** волонтёров и благополучателей с учётом количества животных.
- 🏢 **Управление точками сбора** корма и складским учетом.
- 🚚 **Прием и распределение заявок** на вывоз корма.
- 📦 **Учёт и отгрузка корма** благополучателям.
- 📊 **Генерация отчетов** и анализ данных в PDF.
- 📸 **Прикрепление фотоотчетов** к событиям передачи корма.
- 🛠 **Функции для разных ролей:** администратора, волонтёра, администратора точки.

## 🌐 Запуск проекта

### 1. Склонируйте репозиторий
```bash
git clone https://github.com/NikitosMetla/Xakaton_feed_bot.git
cd Xakaton_feed_bot
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Запуск бота
```bash
python main_bot.py
```

## 🔧 Переменные окружения (`.env`)

```ini
MAIN_BOT_TOKEN=your_telegram_bot_token
POSTGRES_DB=nakormi_db
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_PORT=5432
POSTGRES_HOST=db_host
```

## 💪 Используемые технологии
- **Python 3.11**
- **Aiogram 3.0.0b7**
- **PostgreSQL + SQLAlchemy**
- **Pydantic**
- **ReportLab (генерация PDF-отчётов)**

## 🎲 `requirements.txt`
```ini
SQLAlchemy~=2.0.30
python-dotenv~=1.0.1
aiogram~=3.0.0b7
pydantic~=1.10.16
reportlab~=4.2.0
```

## 💬 Обратная связь

📧 Email: romazanov04@mail.ru  
👉 Telegram: [@Nikita_rom04](https://t.me/Nikita_rom04)  
📚 GitHub: [NikitosMetla](https://github.com/NikitosMetla)  

