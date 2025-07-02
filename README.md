# Вопрос по pytest 

Тесты проверяются на локальной базе данных. Подключение настраивается в `.env`. 

### Клонировение репозитория:

```bash
git clone https://github.com/nikuIin/pytest_db_questition
```

### Создание базы данных:

1) Поменяйте `owner`-а, если я ошибся в вашем:)

```sql
create database test_wine_database with
encoding="UTF-8"
lc_collate="ru_RU.utf8"
lc_ctype="ru_RU.utf8"
owner sterx;
```

2) Также нужно изменить `DB_USER` в `.env`

### Запуск тестов:

Важно: 1 тест выполнится успешно, а второй упадет с `RuntimeError`

```bash
uv run pytest
```
