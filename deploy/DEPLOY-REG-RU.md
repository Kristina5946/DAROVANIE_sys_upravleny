# Деплой CRM «Дарование» на reg.ru

Инструкция для хостинга **reg.ru / ISPmanager** (Passenger, Python 3.11, MySQL).

---

## Шаблон — заполните перед деплоем

```
Логин хостинга:     u________
Домен:              ________________.ru
Путь к сайту:       /var/www/u________/data/www/________________.ru
Python для venv:    /opt/python/python-3.11/bin/python3

MySQL (из панели ISPmanager):
  DB_NAME:          u_________
  DB_USER:          u_________
  DB_PASSWORD:      ********
  DB_HOST:          localhost
  DB_PORT:          3306
```

---

## Что загружать на сервер

Загрузите **всю папку проекта** в `~/www/ВАШ-ДОМЕН.ru/`:

- `manage.py`, `config/`, `core/`, `accounts/`, `templates/`, `static/`
- `requirements.txt`, `passenger_wsgi.py.example`

**Не загружайте:**

- `.env` — создать на сервере
- `venv/` — создать на сервере
- `staticfiles/` — собрать на сервере
- `.git/`, `__pycache__/`, `app.py` (старый прототип, не нужен)

---

## Блок 1. ISPmanager (панель reg.ru)

1. **Сайты** → создать домен + псевдоним `www.`
2. **SSL** → Let's Encrypt, включить **HTTP → HTTPS**
3. **Базы данных** → MySQL → создать БД и пользователя, записать имя/логин/пароль
4. Загрузить файлы проекта в корень сайта
5. Скопировать `passenger_wsgi.py.example` → `passenger_wsgi.py` и **заменить пути** (см. блок 4)
6. **Сайты** → домен → **Изменить** → **Дополнительные возможности**:
   - ✅ CGI-скрипты
   - ✅ Python → `python-3.11`
7. Удалить пустые `index.html` / `index.php` из корня, если есть
8. **Не создавать** `.htaccess` с Passenger — панель настраивает сама

---

## Блок 2. Shell на сервере — venv и зависимости

Подставьте свой домен и логин:

```bash
DOMAIN="ВАШ-ДОМЕН.ru"
PYTHON="/opt/python/python-3.11/bin/python3"
SITE_ROOT="$HOME/www/$DOMAIN"

cd "$SITE_ROOT"

rm -rf venv
$PYTHON -m venv venv
source venv/bin/activate
python --version

pip install --upgrade pip
pip install -r requirements.txt
```

Если `python3.11: команда не найдена` — используйте полный путь `/opt/python/python-3.11/bin/python3`.

Список Python на сервере:

```bash
ls /opt/python/*/bin/python3
```

---

## Блок 3. Файл .env на сервере

```bash
cd ~/www/ВАШ-ДОМЕН.ru
nano .env
```

Вставьте (замените значения):

```env
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=ВСТАВЬТЕ_СГЕНЕРИРОВАННЫЙ_КЛЮЧ
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=ВАШ-ДОМЕН.ru,www.ВАШ-ДОМЕН.ru
DJANGO_CSRF_TRUSTED_ORIGINS=https://ВАШ-ДОМЕН.ru,https://www.ВАШ-ДОМЕН.ru

DB_ENGINE=django.db.backends.mysql
DB_NAME=uXXXXXX_darovanie
DB_USER=uXXXXXX_darovanie
DB_PASSWORD=ПАРОЛЬ_ИЗ_ПАНЕЛИ
DB_HOST=localhost
DB_PORT=3306

SITE_URL=https://ВАШ-ДОМЕН.ru
SITE_NAME=Дарование — CRM
```

Сохранить: `Ctrl+O`, Enter, `Ctrl+X`.

Сгенерировать SECRET_KEY:

```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Блок 4. passenger_wsgi.py

```bash
cd ~/www/ВАШ-ДОМЕН.ru

cat > passenger_wsgi.py << 'EOF'
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/uXXXXXX/data/www/ВАШ-ДОМЕН.ru')
sys.path.insert(1, '/var/www/uXXXXXX/data/www/ВАШ-ДОМЕН.ru/venv/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF
```

**Замените** `uXXXXXX` и `ВАШ-ДОМЕН.ru` на реальные значения.  
Версия `python3.11` должна совпадать с venv: `ls venv/lib/`

---

## Блок 5. Миграции, статика, администратор

```bash
cd ~/www/ВАШ-ДОМЕН.ru
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production

python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p media
chmod 755 media

python manage.py check --deploy

python manage.py createsuperuser
```

При создании суперпользователя в **admin** назначьте роль **Директор** (блок «Доступ в CRM»).

---

## Блок 6. Перезапуск и проверка

```bash
cd ~/www/ВАШ-ДОМЕН.ru
touch .restart-app
```

Логи ошибок:

```bash
tail -30 ~/logs/ВАШ-ДОМЕН.ru.error.log
```

В браузере:

- `https://ВАШ-ДОМЕН.ru`
- `https://ВАШ-ДОМЕН.ru/admin/`

---

## Чеклист

- [ ] Файлы в `~/www/ДОМЕН/`
- [ ] venv на Python 3.11
- [ ] `pip install -r requirements.txt` без ошибок
- [ ] `.env` на сервере, `DEBUG=False`
- [ ] `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` с доменом
- [ ] `migrate` + `collectstatic`
- [ ] `passenger_wsgi.py` с правильными путями
- [ ] CGI + Python 3.11 в панели
- [ ] SSL включён
- [ ] `createsuperuser` + роль Директор
- [ ] `touch .restart-app`

---

## Типичные ошибки

| Ошибка | Решение |
|--------|---------|
| `cryptography package is required` | `pip install cryptography` (уже в requirements.txt) |
| `can't start new thread` при collectstatic | production.py использует `StaticFilesStorage` — уже настроено |
| Сайт без CSS | `collectstatic --noinput` + `touch .restart-app` |
| `directory index forbidden` | Включить CGI + Python, проверить passenger_wsgi.py |
| Python сбрасывается в панели | Включить **CGI** вместе с Python; passenger_wsgi.py должен быть в корне |

---

## Локально перед загрузкой

```bash
pip install -r requirements.txt
python manage.py clear_business_data --yes
python manage.py check
```

## Импорт учеников и преподавателей из CSV

Файлы лежат в `data/import/`. На сервере после `migrate`:

```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py import_legacy_csv
```

Проверка без записи: `python manage.py import_legacy_csv --dry-run`

**Важно:** `passenger_wsgi.py` должен быть в корне сайта (не только `.example`).

---

*CRM «Дарование», Django 6, reg.ru Passenger.*
