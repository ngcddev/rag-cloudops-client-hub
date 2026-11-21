"""Arma el PDF del informe a partir de las secciones Markdown de informe/secciones/.

Une portada, índice con números de página, secciones C a G y las imágenes de evidencias/, y lo
imprime con Chrome o Edge sin interfaz. Se puede volver a correr cada vez que cambie una sección.

Uso:
    pip install markdown pymupdf
    python informe/construir_pdf.py
"""

from pathlib import Path
import html
import re
import subprocess
import sys
import tempfile

import markdown
import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
SECCIONES = RAIZ / "informe" / "secciones"
SALIDA = RAIZ / "informe" / "Informe-modelo-rag-CloudOps-Client-Hub.pdf"
NAVEGADORES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

# (archivo, título de la parte que se antepone, si el encabezado # del archivo baja a nivel 2)
PARTES = [
    ("c-introduccion.md", None, False),
    ("d-problema.md", None, False),
    ("e1-conocimiento.md", "E. Definición del modelo", True),
    ("e2-modelo.md", None, True),
    ("f1-pruebas-ui-api.md", "F. Implementación y análisis de pruebas", True),
    ("f2-golden.md", None, True),
    ("f3-resultados.md", None, True),
    ("g-conclusiones.md", None, False),
]

CSS = """
@page { size: A4; margin: 22mm 18mm 20mm 18mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1a1a1a; }
h1 { font-size: 19pt; border-bottom: 2px solid #2ea043; padding-bottom: 4px; margin-top: 0; page-break-before: always; }
h2 { font-size: 13.5pt; margin-top: 18px; }
h3 { font-size: 11.5pt; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #c9d1d9; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #f0f3f6; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #f0f3f6; padding: 1px 3px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; padding: 8px; white-space: pre-wrap; word-wrap: break-word; font-size: 8.5pt; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
img { max-width: 100%; max-height: 118mm; display: block; margin: 10px auto; border: 1px solid #d0d7de; }
.portada { page-break-after: always; text-align: center; padding-top: 55mm; }
.portada h1 { border: 0; font-size: 28pt; page-break-before: avoid; }
.portada h2 { font-size: 14pt; }
.portada table { margin: 24px auto; width: auto; }
.indice { page-break-after: always; }
.indice h1 { page-break-before: avoid; }
.indice li { list-style: none; margin: 3px 0; }
.indice a { color: #1a1a1a; text-decoration: none; display: flex; }
.indice a span.p { margin-left: auto; padding-left: 10px; }
.indice li.n2 { margin-left: 18px; font-size: 9.5pt; }
.indice ul { padding-left: 0; }
"""


def convertir(texto: str) -> str:
    """Pasa Markdown a HTML con tablas y bloques de código."""
    return markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])


def identificador(texto: str, usados: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-") or "seccion"
    nuevo, n = base, 2
    while nuevo in usados:
        nuevo, n = f"{base}-{n}", n + 1
    usados.add(nuevo)
    return nuevo


def construir_html(paginas: dict) -> str:
    """Devuelve el HTML completo; `paginas` mapea título → página para el índice."""
    usados, entradas, cuerpo = set(), [], []

    portada = convertir((SECCIONES / "a-portada.md").read_text(encoding="utf-8"))
    cuerpo.append(f'<section class="portada">{portada}</section>')

    for archivo, antepuesto, bajar in PARTES:
        texto = (SECCIONES / archivo).read_text(encoding="utf-8")
        if antepuesto:
            ident = identificador(antepuesto, usados)
            entradas.append((1, antepuesto, ident))
            cuerpo.append(f'<h1 id="{ident}">{html.escape(antepuesto)}</h1>')
        if bajar:
            # Las subsecciones E.1, E.2, F.1… pasan a nivel 2 dentro de su parte.
            texto = re.sub(r"(?m)^# ", "## ", texto, count=1)
        salida = convertir(texto)

        def con_id(m):
            nivel, interior = int(m.group(1)), m.group(2)
            limpio = re.sub(r"<[^>]+>", "", interior)
            ident = identificador(limpio, usados)
            if nivel == 1 or (nivel == 2 and limpio.startswith(("E.", "F."))):
                entradas.append((1 if nivel == 1 else 2, html.unescape(limpio), ident))
            return f'<h{nivel} id="{ident}">{interior}</h{nivel}>'

        salida = re.sub(r"<h([12])>(.*?)</h\1>", con_id, salida)
        if antepuesto:
            # La primera subsección no debe forzar otra página: ya hay un h1 antes.
            salida = salida.replace("<h2 ", '<h2 style="margin-top:6px" ', 1)
        cuerpo.append(salida)

    items = []
    for nivel, titulo, ident in entradas:
        pagina = paginas.get(titulo, "")
        clase = "n2" if nivel == 2 else "n1"
        items.append(
            f'<li class="{clase}"><a href="#{ident}"><span>{html.escape(titulo)}</span>'
            f'<span class="p">{pagina}</span></a></li>'
        )
    indice = f'<section class="indice"><h1>Índice</h1><ul>{"".join(items)}</ul></section>'

    base = (SECCIONES).as_uri() + "/"
    return (
        f'<!doctype html><html lang="es"><head><meta charset="utf-8"><base href="{base}">'
        f"<title>Informe del modelo RAG: CloudOps Client Hub</title><style>{CSS}</style></head>"
        f'<body>{cuerpo[0]}{indice}{"".join(cuerpo[1:])}</body></html>'
    ), [e[1] for e in entradas]


def imprimir(html_texto: str, destino: Path) -> None:
    """Imprime el HTML a PDF con el navegador sin interfaz."""
    navegador = next((n for n in NAVEGADORES if n.exists()), None)
    if navegador is None:
        sys.exit("No encontré Chrome ni Edge para imprimir el PDF.")
    with tempfile.TemporaryDirectory() as tmp:
        archivo = Path(tmp) / "informe.html"
        archivo.write_text(html_texto, encoding="utf-8")
        perfil = Path(tmp) / "perfil"
        subprocess.run(
            [str(navegador), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={perfil}", f"--print-to-pdf={destino}", archivo.as_uri()],
            check=True, capture_output=True, timeout=180,
        )


def paginas_de(pdf: Path, titulos: list) -> dict:
    """Busca en qué página aparece cada título (después del índice)."""
    doc = pymupdf.open(pdf)
    resultado = {}
    for titulo in titulos:
        for numero in range(2, len(doc)):  # 0 portada, 1 índice
            texto = doc[numero].get_text()
            if re.search(r"(?m)^\s*" + re.escape(titulo) + r"\s*$", texto):
                resultado[titulo] = numero + 1
                break
    return resultado


def main() -> None:
    contenido, titulos = construir_html({})
    imprimir(contenido, SALIDA)
    paginas = paginas_de(SALIDA, titulos)
    contenido, _ = construir_html(paginas)
    imprimir(contenido, SALIDA)
    doc = pymupdf.open(SALIDA)
    print(f"{SALIDA.relative_to(RAIZ)}: {len(doc)} páginas, {len(paginas)}/{len(titulos)} títulos con página")


if __name__ == "__main__":
    main()
