from .parser import Parser, TokenType

success_test_map = {
    "{}": [],
    "\{": [(TokenType.NOT_webshake, 1, "{")],  # NOQA: W605 invalid escape sequence
    "\{\}": [(TokenType.NOT_webshake, 2, "{}")],  # NOQA: W605 invalid escape sequence
    "abc": [(TokenType.NOT_webshake, 0, "abc")],
    "abc{xp}": [(TokenType.NOT_webshake, 0, "abc"), (TokenType.webshake, 4, "xp")],
    "abc{{xp}}": [(TokenType.NOT_webshake, 0, "abc"), (TokenType.webshake, 4, "{xp}")],
    "abc{xp}to": [
        (TokenType.NOT_webshake, 0, "abc"),
        (TokenType.webshake, 4, "xp"),
        (TokenType.NOT_webshake, 7, "to"),
    ],
    "{ab}{cde}": [(TokenType.webshake, 1, "ab"), (TokenType.webshake, 5, "cde")],
}


def pytest_generate_tests(metafunc):
    id_list = []
    argvalues = []
    argnames = ["text", "expected_result"]
    for text, expected_result in success_test_map.items():
        id_list.append(text)
        argvalues.append(([text, expected_result]))
    metafunc.parametrize(argnames, argvalues, ids=id_list)


def test_parse(text, expected_result):
    parser = Parser()
    result = parser.tokenize(text)
    assert expected_result == result
