from extractcontentfrompdf.sanitizer import TextSanitizer


def test_sanitize_remove_ruidos_e_normaliza_espacos() -> None:
    sanitizer = TextSanitizer()

    texto = "  Linha  1\t\tcom\x00 ruido \n\n\n Linha \ud8002  "

    resultado = sanitizer.sanitize(texto)

    assert resultado == "Linha 1 com ruido\n\nLinha 2"
