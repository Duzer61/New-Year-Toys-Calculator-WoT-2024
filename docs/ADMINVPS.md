# Развёртывание и обслуживание Calculator

Сайт: https://collider.hopto.org. Production-ветка — `main`, рабочая ветка — `adminvps-migration`.

## Конфигурация сервера

| Компонент | Настройка |
| --- | --- |
| Сервер | AdminVPS, `155.212.246.84` |
| Администратор | `dan`, привилегированные команды через sudo |
| Каталог проекта | `/srv/projects/calculator` |
| Compose | `/etc/calculator/compose.yml`, project name `calculator` |
| Приложение | Python 3.12, Django 4.2.7, образ `duzer61/calculator` |
| База данных | PostgreSQL 16, сервис `db_django` |
| Сеть | `calculator_default` |
| Тома | `calculator_pg_data`, `calculator_static_volume`, `calculator_media` |
| Внутренний Nginx | `/etc/calculator/nginx.conf`, порт `127.0.0.1:9000` |
| Nginx хоста | `/etc/nginx/sites-available/collider.hopto.org`, ссылка в `sites-enabled` |
| Секреты приложения | `/srv/projects/calculator/.env`, владелец root, права `600` |
| Состояние деплоя и резервные копии | `/var/lib/calculator`, доступ только root |

Приложение и PostgreSQL не публикуют порты на хосте. Внешние запросы принимает Nginx на 80/443.
У всех трёх сервисов задано `restart: unless-stopped`; контейнеры, остановленные вручную,
после перезагрузки остаются остановленными. Для логов используется драйвер `local`.

## Автоматический деплой

1. Подготовить изменения в рабочей ветке и открыть PR в `main`.
2. Дождаться успешного `checks`: сборка образа, проверки Django, миграции на отдельной тестовой БД и HTTP-проверки.
3. Слить PR в `main`. GitHub Actions соберёт образ, опубликует его в Docker Hub и передаст серверу точный digest.
4. Сервер сохранит дамп БД, остановит приложение и внутренний Nginx, выполнит готовые миграции и сборку статики.
5. После запуска контейнеров сервер проверит health и HTTP. Результат доступен в GitHub Actions.

Деплой включён при repository variable `CALCULATOR_DEPLOY_ENABLED=true`.
Значение `false` отключает автоматическое обновление сервера, сохраняя проверки и публикацию образа.
Push, содержащий только Markdown-документацию или LICENSE, workflow не запускает.
Для ручного запуска в GitHub Actions выбрать **Run workflow** и ветку `main`.

Сценарий выполняет `check`, `migrate --noinput`, `migrate --check`, `collectstatic`
и копирование проектной статики из образа. Новые миграции на сервере не создаются.
Статика и media хранятся в отдельных томах и сохраняются при обновлении приложения.
Автоматического отката БД нет: при ошибке деплой завершается, данные и резервная копия сохраняются.

Ручной деплой фиксированного образа:

```bash
sudo /usr/local/sbin/calculator-deploy 'deploy sha256:<64 lowercase hex>'
```

## SSH-доступ CI

Для GitHub используется отдельный пользователь `calculator-deploy` без группы `docker`
и без произвольного sudo. SSH-ключ ограничен параметрами
`restrict,command="/usr/local/sbin/calculator-deploy-entry"`.
Разрешена только команда `deploy sha256:<64 lowercase hex>` для образа из `duzer61/calculator`.

Compose, сценарии и `authorized_keys` принадлежат root. Публичный `authorized_keys` имеет права `644`:
SSH может читать его, но пользователь деплоя не может менять ограничения.
Приватный ключ хранится в GitHub Secrets. Секреты приложения остаются на VPS.
Для restore и deploy используется общий lock `/run/lock/calculator-deploy.lock`.

| GitHub Secret | Назначение |
| --- | --- |
| `HOST` | `155.212.246.84` |
| `USER` | `calculator-deploy` |
| `SSH_KEY` | Полный приватный Ed25519-ключ CI, включая строки BEGIN/END; файл `.pub` не подходит |
| `SSH_KNOWN_HOSTS` | Доверенная публичная запись сервера; хешированный формат `\|1\|` допустим |
| `DOCKER_USERNAME` | `duzer61` |
| `DOCKER_PASSWORD` | Docker Hub Personal Access Token с правами Repo Read & Write, не пароль аккаунта |

Доступ Cloud Sandboxes для Docker Hub PAT не требуется. SSH проверяет ключ хоста;
проверку нельзя отключать при настройке CI.

## Серверные файлы

| Исходник в репозитории | Установленный файл |
| --- | --- |
| `docker-compose-calc.production.yml` | `/etc/calculator/compose.yml` |
| `deployment/nginx-container.conf` | `/etc/calculator/nginx.conf` |
| `scripts/deploy-root.sh` | `/usr/local/sbin/calculator-deploy` |
| `scripts/deploy-entry.sh` | `/usr/local/sbin/calculator-deploy-entry` |
| `scripts/restore-root.sh` | `/usr/local/sbin/calculator-restore` |
| `scripts/authorize-key.sh` | `/usr/local/sbin/calculator-authorize-key` |
| `deployment/verify.sql` | `/etc/calculator/verify.sql` |
| `deployment/verification.sha256` | `/etc/calculator/verification.sha256` |

CI обновляет образ приложения и не заменяет эти файлы. Изменения серверной конфигурации
устанавливает администратор отдельно после проверки.
`deployment/nginx/collider.hopto.org.conf` — шаблон первоначальной HTTP-настройки.
Не заменять им работающий конфиг хоста: HTTPS-настройки добавлены Certbot.

## Первоначальная установка и восстановление

`scripts/install-adminvps.sh` предназначен для подготовленного установочного комплекта:
в его корне должны находиться `compose.yml`, `nginx.conf`, `.env.example`, `verify.sql`,
`verification.sha256`, каталог `scripts` и дамп `restore/calculator_db.dump`.
Повторная установка поверх существующего проекта запрещена самим сценарием.

После установки администратор создаёт `.env` из шаблона с правами `600`, задаёт новые
`DJANGO_KEY` и `POSTGRES_PASSWORD` и проверяет параметры подключения:
`POSTGRES_DB=calculator`, `POSTGRES_USER=calculator`, `DB_HOST=db_django`, `DB_PORT=5432`,
`DEBUG=False`, `ALLOWED_HOSTS=collider.hopto.org,127.0.0.1,localhost`.
CAPTCHA генерируется внутри приложения через django-simple-captcha и не требует внешних ключей.

До первого запуска приложения выполняется:

```bash
sudo /usr/local/sbin/calculator-restore
```

Восстановление разрешено только в пустую БД и до появления маркера
`/var/lib/calculator/database-restored`. Сценарий проверяет фиксированную контрольную сумму,
импортирует дамп одной транзакцией и сверяет таблицы, миграции и расширения.
Ожидаемые данные привязаны к исходному дампу; для другого дампа требуется отдельная проверка
и соответствующее обновление сценария. Повторять restore в работающую базу нельзя.

Для авторизации отдельного публичного ключа:

```bash
sudo /usr/local/sbin/calculator-authorize-key /path/to/calculator-deploy.pub
```

## Резервные копии и HTTPS

- Дампы перед миграциями: `/var/lib/calculator/backups/predeploy-*.dump`.
- Исходный дамп восстановления: `/var/lib/calculator/restore/calculator_db.dump`.
- Маркер восстановления: `/var/lib/calculator/database-restored`.
- Последний успешно развёрнутый образ: `/var/lib/calculator/current-image`.

Резервные копии доступны только root. Автоматическое удаление старых дампов не настроено.
HTTP перенаправляется на HTTPS; сертификат продлевается существующим `certbot.timer`.
Проверка продления:

```bash
sudo certbot renew --cert-name collider.hopto.org --dry-run
```

## Проверка после обновления

Проверить статусы jobs и steps в GitHub Actions, затем главную страницу, вход, статику и админку.
Ожидаемые ответы: главная и CSS — 200, HTTP → HTTPS — 301, `/admin` → `/admin/` — 301,
`/admin/` без авторизации — 302 на вход, неизвестный URL — 404.
При диагностике не публиковать сырые логи, содержимое `.env`, приватные ключи и токены.

[Проверенный запуск полного CI/CD](https://github.com/Duzer61/New-Year-Toys-Calculator-WoT-2024/actions/runs/43424654797).
