import sys
import xml.etree.ElementTree as ET
import re

constants = {}


def parse_xml_to_config(xml_input):
    try:
        root = ET.fromstring(xml_input)
        return process_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Ошибка разбора XML: {e}")


def process_element(element):
    if not element.attrib and not element:
        return f'"{element.text.strip()}"' if element.text else '""'
    elif len(element) == 0 and element.text:
        return f'"{element.text.strip()}"'
    # Массив или словарь
    elif len(element) > 0:
        if all(child.tag == element[0].tag for child in element):
            # Массив
            values = " ".join(process_element(child) for child in element)
            return f"[ {values} ]"
        else:
            # Словарь
            items = ";\n".join(
                f'{child.tag} = {process_element(child)}' for child in element
            )
            return f"{{\n{items};\n}}"


# Функции для обработки констант и выражений
def evaluate_expression(expr):
    if expr.startswith("?(") and expr.endswith(")"):
        expr_content = expr[2:-1].strip()

        # Разбиваем строку на токены, учитывая строки в кавычках
        tokens = re.findall(r'"[^"]*"|[^\s"]+', expr_content)

        # Первая часть — оператор
        operator = tokens[0]
        operands = [resolve_value(token) for token in tokens[1:]]

        if operator == "+":
            print(sum(operands))
            return sum(operands)
        elif operator == "print":
            # Вывод на экран
            print(" ".join(map(str, operands)))
            return


def resolve_value(token):
    if token.isdigit():
        return int(token)
    elif token.startswith('"') and token.endswith('"'):
        return token[1:-1]
    elif token in constants:
        return constants[token]


def handle_constant_declaration(line):
    match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*) is (.+)$", line)
    if match:
        name = match.group(1)
        value = resolve_value(match.group(2))
        constants[name] = value


# Основной обработчик строк
def process_line(line):
    line = line.strip()
    if not line or line.startswith("::"):
        # комментарий
        return
    elif " is " in line:
        # oбъявление константы
        handle_constant_declaration(line)
        return
    elif line.startswith("?("):
        # вычисление выражения
        return evaluate_expression(line)


def main():
    xml_mode = True
    input_data = []

    for line in sys.stdin:
        if line.strip() == "---":
            xml_mode = False
            # Обрабатываем XML
            try:
                config_output = parse_xml_to_config("\n".join(input_data))
                print(config_output)
            except ValueError as e:
                print(f"Ошибка: {e}", file=sys.stderr)
                sys.exit(1)
            input_data = []
        else:
            if xml_mode:
                input_data.append(line)
            else:
                try:
                    process_line(line)
                except ValueError as e:
                    print(f"Ошибка: {e}", file=sys.stderr)
                    sys.exit(1)


if __name__ == "__main__":
    main()
