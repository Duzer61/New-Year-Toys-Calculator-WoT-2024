# Calculator: перенос на AdminVPS

13 ноября 2026: Calculator восстановлен на AdminVPS и работает по https://collider.hopto.org.
Пользователь подтвердил вход, сайт и админку. БД восстановлена до первого запуска приложения;
проверены все 13 таблиц, 13 пользователей, 13 альбомов, 10 настроек выбора и 23 миграции.
HTTP перенаправляется на HTTPS, статика доступна. Сертификат действует до 11 февраля 2027;
`certbot renew --cert-name collider.hopto.org --dry-run` прошёл успешно, `certbot.timer` активен.
Отдельный ограниченный SSH-ключ установлен и проверен. Полный автоматический деплой из GitHub
предстоит подтвердить после включения CALCULATOR_DEPLOY_ENABLED; ручные деплои уже прошли успешно.

## Область изменений

Рабочая ветка `adminvps-migration` от актуальной `origin/main` (`0aa7b4e`), production `main`.
Модели, формулы, настройки cookie/CAPTCHA, миграции и зависимости приложения сохранены.
С разрешения пользователя исправлена одна ссылка в шаблоне 404: posts:index → calc:index.
Это устранило HTTP 500 на /admin без завершающего слеша и неизвестных URL (PR #28).
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
- Хостовый Nginx: отдельный сайт `collider.hopto.org`, proxy_pass на loopback 9000; HTTPS добавлен Certbot.
  /etc/nginx/sites-available/collider.hopto.org и ссылка в sites-enabled.
  Шаблон deployment/nginx/collider.hopto.org.conf предназначен только для первоначальной HTTP-настройки;
  не заменять им установленный конфиг с HTTPS.
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
Публичный authorized_keys имеет режим 644: SSH может читать его, deployment-пользователь не может менять.
Приватные ключи и .env имеют режим 600 и не входят в репозиторий.
Проверено: отдельный ключ аутентифицируется, произвольная команда id отклоняется с exit 2;
calculator-deploy не состоит в группе docker. Проверено подключение с точным публичным SSH_KNOWN_HOSTS
и StrictHostKeyChecking=yes. Приватный ключ читал только штатный SSH, содержимое агенту не раскрывалось.
Допускается только `deploy sha256:<64 lowercase hex>`; root-сценарий фиксирует репозиторий образа, Compose и пути.
Общий lock для restore/deploy: `/run/lock/calculator-deploy.lock`.
CI не может заменить root-owned файлы. Обновления этих файлов устанавливает администратор после проверки.

Workflow выполняет проверки на main/adminvps-migration/PR, затем build/push только из main.
Actions закреплены по commit SHA, права contents:read, persist-credentials:false.
Деплой сериализован; запускается только при `CALCULATOR_DEPLOY_ENABLED=true` и после сборки main.
До восстановления эту переменную не включать. Возможность workflow_dispatch предусмотрена.
Secrets: HOST=155.212.246.84, USER=calculator-deploy, SSH_KEY, SSH_KNOWN_HOSTS,
DOCKER_USERNAME=duzer61, DOCKER_PASSWORD (значение — Docker Hub PAT, не пароль аккаунта).
Отдельный PAT calculator-github-actions: Repo Read & Write, Cloud Sandboxes выключен.
SSH_KEY — полное содержимое отдельного приватного Ed25519-ключа без .pub, включая BEGIN/END;
SSH_KNOWN_HOSTS — доверенная публичная запись AdminVPS, допускается хешированный формат |1|.
Пользователь вводит секреты самостоятельно в интерфейсе GitHub; их значения агент не читает.
Секреты приложения остаются на VPS. Старые GitHub Secrets БД workflow больше не использует.
Telegram-отправка из старого workflow отсутствует; уведомления отдельно не настраивались.

## Локальные проверки

Образ собрался из чистых tracked-файлов main без реальных секретов. На отдельной восстановленной базе прошли
Django check, migrate --check, makemigrations --check --dry-run, collectstatic, HTTP главной/входа/регистрации.
Полный Compose проверен на 127.0.0.1:19000: health всех сервисов, HTTP, CSS, форма входа.
Проверочные сервисы явно остановлены, тестовый порт освобождён. На VPS проверены loopback и публичный HTTPS:
главная/вход/регистрация/CSS → 200; /admin → 301 /admin/; /admin/ → 302 на вход; неизвестный URL → 404.

## Подтверждённые запуски и текущее состояние

- PR #27: инфраструктура переноса. Main 53a97a24593afb42b79fb036b1131465f33576a6.
- Первый build/push: https://github.com/Duzer61/New-Year-Toys-Calculator-WoT-2024/actions/runs/43405453621.
  После замены пароля аккаунта на PAT вход в Docker Hub и публикация успешны, deploy был выключен.
- PR #28: одна ссылка шаблона 404. Main ebcaecd5874ec22684a6282ed11577b6589a55de.
- Build исправления: https://github.com/Duzer61/New-Year-Toys-Calculator-WoT-2024/actions/runs/43420837156.
  checks/build успешны, deploy штатно пропущен до включения gate.
- Последний вручную развёрнутый образ:
  duzer61/calculator@sha256:aa572771fdbbe9c06aaac82971ea5f930110ecc0a57ac317da174a9303dde3d5.
- No-IP: A collider.hopto.org = 155.212.246.84; проверены локальный resolver, 1.1.1.1, 8.8.8.8.
  Публичной AAAA-записи нет. CAPTCHA не требует внешних разрешённых доменов.
- До миграций каждого деплоя сохраняется отдельный root-only дамп в /var/lib/calculator/backups.
  Исходный проверенный дамп на VPS: /var/lib/calculator/restore/calculator_db.dump.
- Сохранённый marker восстановления: /var/lib/calculator/database-restored.

Осталось включить CALCULATOR_DEPLOY_ENABLED=true, проследить workflow checks → build/push → restricted SSH →
backup → Django migrate → healthy application, затем снова проверить HTTPS и записать итоговый workflow/digest.
Начинать диагностику с jobs/steps и безопасных аннотаций, не сырых логов.

Сертификаты/ключи в /etc/letsencrypt не читать и не копировать. Новую учётную запись Certbot/таймер не создавать.
Без отдельного согласования не выполнять down -v, prune, pg_restore --clean, сбросы БД или force Git.
