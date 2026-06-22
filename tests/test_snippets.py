from plugins.latex.snippets import list_available_snippets, render_snippet


def test_lists_bundled_snippets():
    names = {snippet["name"] for snippet in list_available_snippets()}
    assert {"equation", "figure", "multiple_choice"} <= names


def test_renders_equation_with_optional_label():
    rendered = render_snippet("equation", equation="x^2", label="square")
    assert "x^2" in rendered
    assert r"\label{eq:square}" in rendered


def test_omits_empty_optional_label():
    rendered = render_snippet("equation", equation="x^2")
    assert r"\label" not in rendered
