from .parser import Parser

# Unbalanced open/close cases
fail_test_cases = ["{", "}", "{{}", "{}}"]


def pytest_generate_tests(metafunc):
    id_list = []
    argvalues = []
    argnames = ["text"]

    for text in fail_test_cases:
        id_list.append(text)
        argvalues.append(([text]))
    metafunc.parametrize(argnames, argvalues, ids=id_list)


def test_parse(text):
    parser = Parser()
    try:
        parser.tokenize(text)
    except ValueError:
        pass
    else:
        assert False
