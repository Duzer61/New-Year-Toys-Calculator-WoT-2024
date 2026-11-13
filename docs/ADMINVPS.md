# Calculator: перенос на AdminVPS

13 ноября 2026: root-owned файлы и отдельный пользователь установлены на VPS. Пользователь заполнил .env,
метаданные проверены: root:root 600; содержимое агент не читал. calculator-restore завершился успешно,
сверены все 13 таблиц, 13 пользователей, 13 альбомов, 10 настроек выбора и 23 миграции.
Приложение на VPS ещё не запускалось; GitHub build/deploy, DNS и HTTPS ещё не проверены.

## Область изменений

Рабочая ветка `adminvps-migration` от актуальной `origin/main` (`0aa7b4e`), production `main`.
Код, модели, формулы, настройки cookie/CAPTCHA, миграции и зависимости приложения не меняются.
В main ранее было слито обновление Pillow 13.0.0; оно сохранено. Python 3.12 и Django 4.2.7 сохранены.
Django 4.2 больше не получает поддержку; обновление зависимостей не входит в текущий перенос.
Dockerfile приложения сохранён. Расширен `.dockerignore`, исключающий секреты и локальные артефакты из контекста сборки.
В development Compose добавлен только `restart: unless-stopped` для трёх сервисов.

## Проверка исходных данных

Исходный том: `backup/var/lib/docker/volumes/calculator_pg_data/_data` в рабочей папке восстановления.
PG_VERSION=13, база `django`, UTF8, en_US.utf8. Исходный бэкап не изменялся.
Данные PostgreSQL скопированы по списку каталогов движка; старые конфиги, ключи, окружение и приложения не переносились.
Чистый PostgreSQL 13 запущен без сети на отдельной копии. Создан дамп custom без владельцев/ACL.
Дамп: `/home/dan/Dev/beget_backup/recovery/calculator/calculator_db.dump`.
SHA256: `b8cf743b6ab61964b97d0ec819ba02913fc62b19a59f356413173e77ddca754e`.
В отдельной пустой PostgreSQL 16 импорт одной транзакцией выполнен успешно.
Совпали все 13 таблиц по количеству строк, 23 Django-миграции и список расширений (`plpgsql`).
Пользователей 13, альбомов 13, настроек выбора альбомов 10. Пользовательские записи не выводились.
Полный безопасный отчёт: `/home/dan/Dev/beget_backup/recovery/calculator/verification.json`.
Том `calculator_media` пуст: 0 файлов. В моделях нет ImageField/FileField. Старую статику не переносим;
`collectstatic` и отдельное копирование каталога `static` из образа воспроизводят прежнюю схему.
Проверка устанавливает целостность сохранённой копии, а не полноту данных непосредственно перед инцидентом.

## Изоляция на сервере

- Администратор: `dan@155.212.246.84`, привилегированные действия выполняет пользователь через sudo.
- Проект: `/srv/projects/calculator`, секретный файл `.env` создаёт администратор вручную, root:root 600.
- Compose: `/etc/calculator/compose.yml`, project name `calculator`.
- Тома: `calculator_pg_data`, `calculator_static_volume`, `calculator_media`; отдельная сеть `calculator_default`.
- PostgreSQL 16 и стандартный Nginx закреплены по digest. PostgreSQL 13 используется только для извлечения дампа.
- Приложение: `duzer61/calculator@sha256:<digest>`; версия определяется результатом сборки CI.
- Приложение и БД не имеют опубликованных портов. Контейнерный Nginx: только `127.0.0.1:9000`.
- Хостовый Nginx: отдельный сайт `collider.hopto.org`, proxy_pass на loopback 9000. Подготовлен шаблон без SSL.
- `restart: unless-stopped` у всех трёх сервисов; намеренно остановленные контейнеры после reboot остаются остановленными.
- Везде logging driver `local`. Все проверки Compose — `config -q`.
- Career Tracker, Funny_recipes, общие SSH/firewall/Certbot настройки не меняются.

## Установка и восстановление

`install-adminvps.sh` отказывается перезаписывать существующие каталоги, сценарии, пользователя,
Compose-контейнеры/тома Calculator. Проверяет порт 9000 и контрольную сумму дампа.
Устанавливает root-owned сценарии и конфиги; не создаёт реальный `.env`, не запускает контейнеры,
не подключает SSH-ключ, не изменяет Nginx хоста.

После установки создать `.env` из `.env.example`, права 600, заполнить новые DJANGO_KEY и POSTGRES_PASSWORD локально.
POSTGRES_DB=calculator, POSTGRES_USER=calculator, DB_HOST=db_django, DB_PORT=5432,
DEBUG=False, ALLOWED_HOSTS=collider.hopto.org,127.0.0.1,localhost.
Новый DJANGO_KEY аннулирует старые подписанные сессии; пользовательские учётные записи и пароли остаются в восстановленной БД.
Внешнего CAPTCHA-сервиса нет: django-simple-captcha генерирует изображения внутри приложения.

`sudo /usr/local/sbin/calculator-restore` запускает только БД. Импорт запрещён при наличии маркера
или любых пользовательских таблиц/последовательностей/представлений. Дамп сверяется по фиксированной SHA256.
Импорт выполняется `pg_restore --single-transaction --exit-on-error --no-owner --no-acl`.
Сверяются все числа строк, идентификаторы миграций и расширения; лишь затем создаётся root-only
`/var/lib/calculator/database-restored`. Приложение и миграции не запускаются в restore.
При ошибке проверки импортированные данные сохраняются, автодеплой остаётся заблокирован.

Первый запуск: после успешного восстановления вызвать `sudo /usr/local/sbin/calculator-deploy 'deploy sha256:<digest>'`.
Перед миграциями создаётся dump в `/var/lib/calculator/backups`, затем останавливаются только
Calculator и его gateway, выполняются `check`, `migrate --noinput`, `migrate --check`, `collectstatic`,
копирование проектной статики и проверка health/HTTP. `makemigrations` на production отсутствует.
Автоматического отката БД/удаления данных нет. Сырые ошибки подавляются для защиты секретов.
Последний успешный образ записывается в `/var/lib/calculator/current-image`.

## Ограниченный CI/CD

`calculator-deploy` без группы docker, без произвольного sudo. Отдельный Ed25519 SSH-ключ создаёт пользователь.
Приватный ключ сохраняется самостоятельно в GitHub Secret SSH_KEY. Личный ключ dan не используется для CI.
Публичный `.pub` файл устанавливается `sudo /usr/local/sbin/calculator-authorize-key /path/to/calculator-deploy.pub`.
Ключ ограничен `restrict,command="/usr/local/sbin/calculator-deploy-entry"`; home/authorized_keys принадлежат root.
Допускается только `deploy sha256:<64 lowercase hex>`; root-сценарий фиксирует репозиторий образа, Compose и пути.
Общий lock для restore/deploy: `/run/lock/calculator-deploy.lock`.
CI не может заменить root-owned файлы. Обновления этих файлов устанавливает администратор после проверки.

Workflow выполняет проверки на main/adminvps-migration/PR, затем build/push только из main.
Actions закреплены по commit SHA, права contents:read, persist-credentials:false.
Деплой сериализован; запускается только при `CALCULATOR_DEPLOY_ENABLED=true` и после сборки main.
До восстановления эту переменную не включать. Возможность workflow_dispatch предусмотрена.
Secrets: HOST=155.212.246.84, USER=calculator-deploy, SSH_KEY, SSH_KNOWN_HOSTS,
DOCKER_USERNAME, DOCKER_PASSWORD (Docker Hub PAT Read & Write).
Секреты приложения остаются на VPS. Старые GitHub Secrets БД workflow больше не использует.
Telegram-отправка из старого workflow отсутствует; уведомления отдельно не настраивались.

## Локальные проверки

Образ собрался из чистых tracked-файлов main без реальных секретов. На отдельной восстановленной базе прошли
Django check, migrate --check, makemigrations --check --dry-run, collectstatic, HTTP главной/входа/регистрации.
Полный Compose проверен на 127.0.0.1:19000: health всех сервисов, HTTP, CSS, форма входа.
Проверочные сервисы явно остановлены. Production на VPS ещё не запускался.

## Порядок оставшихся проверок

1. Установка, ручное заполнение `.env`, импорт БД и сверка маркера.
2. GitHub Docker Hub Secrets, сборка main без активированного деплоя; первый запуск по digest.
3. Loopback: HTTP, статика, вход/данные/админка с участием пользователя.
4. Отдельный Nginx server block, nginx -t, reload.
5. Пользователь обновляет No-IP A collider.hopto.org на 155.212.246.84; проверить AAAA и распространение DNS.
6. Выпустить отдельный сертификат Certbot, проверить HTTP→HTTPS и renew --cert-name collider.hopto.org --dry-run.
7. Настроить отдельный ограниченный ключ CI и GitHub Secrets; включить CALCULATOR_DEPLOY_ENABLED.
8. Проследить workflow до успеха и снова проверить сайт. Сначала смотреть статусы jobs/steps, не сырые логи.

Сертификаты/ключи в /etc/letsencrypt не читать и не копировать. Новую учётную запись Certbot/таймер не создавать.
Без отдельного согласования не выполнять down -v, prune, pg_restore --clean, сбросы БД или force Git.
