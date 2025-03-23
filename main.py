import sys
import json
from processor import RoundProcessor


def main():
    input_file = 'input.json'

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден в текущей директории.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Файл '{input_file}' содержит некорректный JSON.")
        sys.exit(1)

    processor = RoundProcessor()
    first_round = True

    output = processor.process_round(data, first_round)
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()