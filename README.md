# Инструмент командной строки для учебного конфигурационного языка
## Преобразует XML синтаксис в конфигурационный язык
### Синтаксис
```Однострочные комментарии:
:: Это однострочный комментарий
Массивы:
[ значение значение значение ... ]
Словари:
{
 имя = значение;
 имя = значение;
 имя = значение;
 ...
}
Имена:
[a-zA-Z]+
Значения:
• Числа.
• Строки.
• Массивы.
146
• Словари.
Строки:
"Это строка"
Объявление константы на этапе трансляции:
имя is значение
Вычисление константного выражения на этапе трансляции (префиксная
форма), пример:
?(+ имя 1)
```
### Клонирование
```
git clone https://github.com/Avinar16/Configs
cd <директория проекта>
```
### Создание виртуального окружения python
```
python -m venv venv
venv/Scripts/activate
```

### Тестирование:
    python tests.py