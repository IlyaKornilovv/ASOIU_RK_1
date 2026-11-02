"""Рубежный контроль №1: вариант предметной области 12, запросы Б.

Предметная область: «Язык программирования — Средство разработки».
"""

from operator import itemgetter


class ProgrammingLanguage:
    """Язык программирования (сторона «много» связи один-ко-многим)."""

    def __init__(self, language_id, name, popularity, tool_id):
        self.id = language_id
        self.name = name
        self.popularity = popularity
        self.tool_id = tool_id


class DevelopmentTool:
    """Средство разработки (сторона «один» связи один-ко-многим)."""

    def __init__(self, tool_id, name):
        self.id = tool_id
        self.name = name


class LanguageTool:
    """Связь языков и средств разработки «многие-ко-многим»."""

    def __init__(self, language_id, tool_id):
        self.language_id = language_id
        self.tool_id = tool_id


# Средства разработки.
TOOLS = [
    DevelopmentTool(1, "PyCharm"),
    DevelopmentTool(2, "Visual Studio Code"),
    DevelopmentTool(3, "IntelliJ IDEA"),
    DevelopmentTool(4, "WebStorm"),
    DevelopmentTool(5, "Eclipse"),
]

# Языки программирования. Популярность — количественный признак (0–100).
# tool_id задаёт связь один-ко-многим с основным средством разработки.
LANGUAGES = [
    ProgrammingLanguage(1, "Python", 95, 1),
    ProgrammingLanguage(2, "Java", 85, 3),
    ProgrammingLanguage(3, "JavaScript", 90, 2),
    ProgrammingLanguage(4, "TypeScript", 88, 4),
    ProgrammingLanguage(5, "CoffeeScript", 55, 4),
]

# Допустимые сочетания языков и средств разработки: многие-ко-многим.
LANGUAGE_TOOLS = [
    LanguageTool(1, 1),
    LanguageTool(1, 2),
    LanguageTool(2, 2),
    LanguageTool(2, 3),
    LanguageTool(2, 5),
    LanguageTool(3, 2),
    LanguageTool(3, 4),
    LanguageTool(4, 2),
    LanguageTool(4, 4),
    LanguageTool(5, 2),
    LanguageTool(5, 4),
]


def build_one_to_many(languages, tools):
    """Соединяет данные по связи один-ко-многим."""
    return [
        (language.name, language.popularity, tool.name)
        for language in languages
        for tool in tools
        if language.tool_id == tool.id
    ]


def build_many_to_many(languages, tools, language_tools):
    """Соединяет данные по связи многие-ко-многим."""
    temporary = [
        (link.language_id, tool.name)
        for link in language_tools
        for tool in tools
        if link.tool_id == tool.id
    ]
    return [
        (language.name, tool_name)
        for language_id, tool_name in temporary
        for language in languages
        if language.id == language_id
    ]


def query_1(one_to_many):
    """Б1: связанные языки и средства, сортировка по языкам."""
    return sorted(one_to_many, key=itemgetter(0))


def query_2(tools, one_to_many):
    """Б2: число языков у каждого средства, по убыванию количества."""
    result = [
        (
            tool.name,
            len(list(filter(lambda row: row[2] == tool.name, one_to_many))),
        )
        for tool in tools
    ]
    return sorted(result, key=lambda row: (-row[1], row[0]))


def query_3(many_to_many):
    """Б3: языки с окончанием 'Script' и поддерживающие их средства."""
    script_languages = sorted(
        {language_name for language_name, _ in many_to_many
         if language_name.endswith("Script")}
    )
    return {
        language_name: sorted(
            tool_name
            for current_language, tool_name in many_to_many
            if current_language == language_name
        )
        for language_name in script_languages
    }


def run_self_checks(result_1, result_2, result_3):
    """Проверяет полноту и порядок результатов запросов."""
    assert [row[0] for row in result_1] == [
        "CoffeeScript", "Java", "JavaScript", "Python", "TypeScript"
    ]
    assert result_2 == [
        ("WebStorm", 2),
        ("IntelliJ IDEA", 1),
        ("PyCharm", 1),
        ("Visual Studio Code", 1),
        ("Eclipse", 0),
    ]
    assert set(result_3) == {"CoffeeScript", "JavaScript", "TypeScript"}
    assert all(tools == ["Visual Studio Code", "WebStorm"]
               for tools in result_3.values())


def print_results(result_1, result_2, result_3):
    """Печатает результаты в удобном для отчёта виде."""
    print("ЗАДАНИЕ Б1")
    print("Язык | Популярность | Основное средство разработки")
    for language_name, popularity, tool_name in result_1:
        print(f"{language_name} | {popularity} | {tool_name}")

    print("\nЗАДАНИЕ Б2")
    print("Средство разработки | Количество языков")
    for tool_name, language_count in result_2:
        print(f"{tool_name} | {language_count}")

    print("\nЗАДАНИЕ Б3")
    print("Язык с окончанием 'Script' | Средства разработки")
    for language_name, tool_names in result_3.items():
        print(f"{language_name} | {', '.join(tool_names)}")

    print("\nСАМОПРОВЕРКА: все проверки пройдены успешно.")


def main():
    """Выполняет соединения, три запроса и самопроверку."""
    one_to_many = build_one_to_many(LANGUAGES, TOOLS)
    many_to_many = build_many_to_many(LANGUAGES, TOOLS, LANGUAGE_TOOLS)

    result_1 = query_1(one_to_many)
    result_2 = query_2(TOOLS, one_to_many)
    result_3 = query_3(many_to_many)

    run_self_checks(result_1, result_2, result_3)
    print_results(result_1, result_2, result_3)


if __name__ == "__main__":
    main()
