# Интернет-магазин на Django

Учебный проект интернет-магазина, разработанный в рамках курса по Django.

---

## 📋 О проекте

Проект представляет собой полноценный интернет-магазин с каталогом товаров, системой категорий, административной панелью и формами для добавления товаров.

### Основные возможности:

- 🏠 **Главная страница** с выводом товаров (пагинация, обрезка описания до 100 символов)
- 📦 **Каталог товаров** с фильтрацией по категориям
- 📄 **Детальная страница товара** с полной информацией
- 📞 **Страница контактов** с формой обратной связи
- ➕ **Добавление товаров** через форму
- 🔐 **Административная панель** для управления контентом
- 📊 **Пагинация** на главной странице
- 🗄️ **База данных PostgreSQL**

---

## 🛠️ Стек технологий

| Компонент | Технология |
|-----------|------------|
| Backend | Django 4.2+ |
| База данных | PostgreSQL 14+ |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Работа с БД | psycopg2-binary |
| Переменные окружения | python-dotenv |
| Изображения | Pillow |
| Shell | ipython |

---

## 📁 Структура проекта
myshop/  
├── catalog/ # Основное приложение  
│ ├── fixtures/ # Тестовые данные  
│ │ ├── categories.json  
│ │ └── products.json  
│ ├── management/ # Кастомные команды  
│ │ └── commands/  
│ │ └── load_test_data.py  
│ ├── migrations/ # Миграции БД  
│ ├── templates/ # HTML шаблоны  
│ │ └── catalog/  
│ │ ├── includes/  
│ │ │ └── sidebar.html  
│ │ ├── base.html  
│ │ ├── home.html  
│ │ ├── catalog.html  
│ │ ├── contacts.html  
│ │ ├── product_detail.html  
│ │ └── add_product.html  
│ ├── static/ # Статические файлы  
│ │ └── css/  
│ │ └── style.css  
│ ├── admin.py  
│ ├── models.py  
│ ├── urls.py  
│ └── views.py  
├── config/ # Настройки проекта  
│ ├── settings.py  
│ └── urls.py  
├── media/ # Загруженные изображения  
├── static/ # Собранная статика  
├── .env # Переменные окружения  
├── .env.example # Шаблон .env  
├── .gitignore  
├── manage.py  
├── requirements.txt  
└── README.md  


---

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
```
```bash
cd myshop
```
Windows
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
Linux/Mac
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```


