from package_template.example import print_text


def test_print_text():
    text = "hello"
    assert text == print_text(text)
