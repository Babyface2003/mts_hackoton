# README: Планировщик размещения виртуальных машин на физических серверах MWS Cloud Platform

## Описание проекта
Этот проект реализует алгоритм планирования размещения виртуальных машин (ВМ) на физических серверах (хостах) в облачной платформе MWS Cloud Platform. Целью является эффективное распределение ресурсов с учетом ограничений по CPU и RAM, минимизация количества активных серверов и поддержание загрузки хостов в оптимальном диапазоне (~80%).

## Структура входных данных
Программа получает на стандартный ввод JSON-документ со следующей структурой:

```json
{
  "hosts": {
    "host1": { "cpu": 24, "ram": 512 },
    "host2": { "cpu": 32, "ram": 768 }
  },
  "virtual_machines": {
    "vm1": { "cpu": 2, "ram": 4 },
    "vm2": { "cpu": 3, "ram": 7 }
  },
  "diff": {
    "add": { "virtual_machines": [ "vm3" ] }
  }
}
```

- `hosts` — список физических серверов с характеристиками CPU и RAM.
- `virtual_machines` — список ВМ с характеристиками CPU и RAM.
- `diff` — изменения с предыдущего раунда (добавление или удаление ВМ).

## Структура выходных данных
Программа должна вывести JSON-документ следующего формата:

```json
{
  "allocations": {
    "host1": [ "vm1" ],
    "host2": [ "vm2" ]
  },
  "allocation_failures": [ "vm3" ],
  "migrations": {
    "vm2": { "from": "host1", "to": "host2" }
  }
}
```

- `allocations` — распределение ВМ по хостам.
- `allocation_failures` — список ВМ, которые не удалось разместить.
- `migrations` — миграции ВМ между хостами.

## Алгоритм работы
1. Чтение входных данных из `stdin`.
2. Определение текущего состояния хостов и ВМ.
3. Распределение новых ВМ по хостам с учетом ограничений.
4. Принятие решений о миграции для оптимизации загрузки.
5. Формирование выходного JSON-документа.
6. Вывод результата в `stdout`.

## Оценка качества решения
Баллы начисляются за:
- Оптимальное распределение загрузки (~80%) → **10 баллов**.
- Полное использование хоста (100%) → **~3 балла**.
- Недогруженные хосты → **<10 баллов**.
- Отключенные хосты (5 раундов без нагрузки) → **8 баллов за каждый раунд**.

Штрафы:
- Невозможность размещения ВМ: `-5 * h`, где `h` — число хостов.
- Миграции ВМ: `m^2`, где `m` — количество перемещенных ВМ.

## Запуск программы
### Использование Docker
Рекомендуемый способ запуска — Docker-контейнер.
1. Соберите образ:
   ```bash
   docker build -t vm_scheduler .
   ```
2. Запустите контейнер:
   ```bash
   docker run --rm -i vm_scheduler < input.json
   ```

### Альтернативный вариант: архив с приложением
Если Docker не используется, можно создать `.zip` или `.tar.gz` архив:
- В корне архива должен быть исполняемый файл `run`.
- Все зависимости включены (кроме OpenJDK 8, 11, 17, 21 и Python 3.9—3.13).

Пример запуска:
```bash
./run < input.json
```

## Технологии
- Python 3.x
- JSON для ввода/вывода
- Docker для контейнеризации

## Авторы
- [Ваше имя]
- [Контакты]

Этот README-файл можно использовать для предоставления информации проверяющим. Если нужны правки, сообщите!

