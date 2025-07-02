# Вопрос по pytest 

### Создание базы данных:

Поменяйте `owner`, если я ошибся в вашем:)

```sql
create database test_wine_database with
encoding="UTF-8"
lc_collate="ru_RU.utf8"
lc_ctype="ru_RU.utf8"
owner sterx;
```

### Запуск тестов:

```bash
uv run pytest
```
