import textwrap

import allure


def description_md(text: str):
    """Attach a Markdown description to a test (or test class) in the Allure report.

    The text is dedented so it can be written as an indented triple-quoted string.
    When used on both a class and a test, the test-level description wins.
    """
    return allure.description(textwrap.dedent(text).strip())
