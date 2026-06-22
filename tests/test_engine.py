import pytest

from plugins.latex.engine import validate_source


VALID_DOCUMENT = r"""
\documentclass{article}
\begin{document}
Hello
\end{document}
"""


def test_accepts_complete_document():
    validate_source(VALID_DOCUMENT)


@pytest.mark.parametrize(
    "source",
    [
        r"\documentclass{article}\begin{document}\write18{touch /tmp/x}\end{document}",
        r"\documentclass{article}\begin{document}\openout1=/tmp/x\end{document}",
        r"\documentclass{article}\begin{document}\input{/etc/passwd}\end{document}",
    ],
)
def test_rejects_known_dangerous_commands(source):
    with pytest.raises(ValueError, match="dangerous"):
        validate_source(source)


@pytest.mark.parametrize(
    "source",
    [
        r"\begin{document}Hello\end{document}",
        r"\documentclass{article}Hello\end{document}",
        r"\documentclass{article}\begin{document}Hello",
    ],
)
def test_requires_document_structure(source):
    with pytest.raises(ValueError):
        validate_source(source)
