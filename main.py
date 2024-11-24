import sys
import xml.etree.ElementTree as ET


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
    else:
        raise ValueError("Неизвестная структура")


def main():
    xml_input = sys.stdin.read()
    try:
        config_output = parse_xml_to_config(xml_input)
        print(config_output)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
