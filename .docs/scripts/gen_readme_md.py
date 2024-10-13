import os
import platform
import re


# Определяем путь к файлам
docs_index_md = 'docs/index.md'
readme_md = 'README.md'


def parse_hero(content):
    """Извлекает блок highlights из файла"""
    hero = []
    in_hero = False
    # is_description = False

    for line in content.splitlines():
        
        if line.startswith('hero:'):
            in_hero = True
            continue
        
        if in_hero:
            
            # Парсим до строки "highlights:"
            if line.strip() == "highlights:":
                break
            
            # Ищем заголовок
            if line.count(" title:"):
                title = f'Добро пожаловать в {line.split(":")[1].strip()}!'
                hero.append(f"# {title}")

            # Ищем подзаголовок
            if line.count("subtitle:"):
                subtitle = line.split(":")[1].strip()
                hero.append(f"{subtitle.capitalize()}")

    return "\n".join(hero)


def parse_highlights(content):
    """Извлекает блок highlights из файла"""
    highlights = []
    in_highlights = False
    is_description = False

    for line in content.splitlines():
        
        if line.startswith('highlights:'):
            in_highlights = True
            continue
        
        if in_highlights:
            
            # Парсим до строки "---""
            if line.strip() == "---":
                break
            
            # Ищем заголовок
            if line.count("- title:"):
                title = (
                    '<div style="flex: 1; padding-right: 10px;">\n\n'
                    f'### {line.split(":")[1].strip().capitalize()}'
                )
                highlights.append(title)
            
            # Ищем описание
            elif line.count("description:"):
                is_description = True
                continue
            if is_description:
                description = (
                    f"{line.strip()}\n\n"
                    "</div>\n\n"
                )
                highlights.append(description)
                is_description = False

    return "\n".join(highlights)


def main():
    # Читаем содержимое файла docs/index.md
    with open(docs_index_md, 'r', encoding='utf-8') as file:
        index_content = file.read()

    # Извлекаем блок highlights
    hero = parse_hero(index_content)
    print(hero)

    screenshots = (
        "![](docs/assets/images/cpanel.jpg)"
    )
    
    # # Извлекаем блок highlights
    highlights = (
        "## Основные возможности NotiLog\n\n"
        '<div style="display: flex;">\n\n'
            f"{parse_highlights(index_content)}"
        "</div>\n\n"
    )
    print(highlights)

    readme = hero + "\n\n" + screenshots + "\n\n" + highlights + (
        "## Сообщество\n\n"
        "Участие в сообществе NotiLog предоставляет вам прямой путь к установлению связей с другими единомышленниками. Узнайте больше о том, как вы можете участвовать в нашем сообществе, ознакомившись с нашим [руководством по сообществу](https://github.com/ForceFledgling/notilog/blob/main/docs/g/community.md).\n\n"
        "## Лицензия\n\n"
        "NotiLog является программным обеспечением с открытым исходным кодом и лицензируется по условиям лицензии [MIT License](https://github.com/ForceFledgling/notilog/blob/main/LICENSE)."
    )

    # Записываем обновленный README.md
    with open(readme_md, 'w', encoding='utf-8') as file:
        file.write(readme)


if __name__ == "__main__":
    main()
