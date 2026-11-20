# Guía · Integrante 5 · @Andres-Duqu

<!-- Pasos para el script de evaluación, la corrida final y el análisis (issues #6 y #7). -->

**Tu parte:** adaptar el script de evaluación del ejemplo de clase, correr las 50 pruebas y sacar
las métricas. La meta es **70 % de eficiencia o más**. El script lo puedes hacer ya; la corrida
final se hace cuando estén el modelo de Sebastián y el golden de Yisel.

## Paso 1 · Adaptar `evaluate_rag.py` (issue #6, ya)

Partir de https://github.com/FerchoRV/ejemplo-rag-openwebui/blob/main/evaluate_rag.py y
guardarlo en `evaluacion/evaluate_rag.py`. Cambios:

1. **Rutas:** el `.env` está en la raíz y el dataset en otra carpeta:
   ```python
   ROOT = Path(__file__).resolve().parent.parent
   load_dotenv(ROOT / ".env")
   DATASET_PATH = ROOT / "golden-dataset" / "golden_dataset.jsonl"
   OUTPUT_DIR = Path(__file__).resolve().parent / "runs"
   ```
2. **Modelo por defecto:** `TARGET_MODEL = "asistente-soporte-forja"`.
3. **Juez:** cambiar el texto de "fitness y nutrición" a soporte al cliente. Que valore la
   **fidelidad** (no inventa nada fuera de la base) y la **completitud** (cubre lo esperado). En
   los casos de fuera de alcance, sin información y seguridad, negarse correctamente vale 5.
4. **Éxito por caso:** sin error y (palabras clave OK **o** puntaje del juez de 3 o más). Guardar
   `success` en cada registro.
5. **Resumen:** agregar % de éxito, **% de error** (100 − éxito), éxito por categoría y escribir
   también un `runs/resumen_<RUN_TAG>_<fecha>.json` con las métricas.
6. **Validar el dataset:** si una línea no es JSON válido, mostrar el número de línea (para
   avisarle a Yisel) en vez de romperse.

Probar con 5 casos de muestra (puedes crear un `golden-dataset/muestra.jsonl` temporal) y subir el
PR (`Closes #6`).

## Paso 2 · Corrida final (issue #7)

Requisitos: entorno levantado (`guias/README.md`), base cargada con el corte de Mesiahs, modelo
`asistente-soporte-forja` creado como en la guía de Sebastián y los dos modelos descargados.
API key: *Settings → Account → API Keys* (si no aparece: *Admin Panel → Settings → General →
Enable API Key*) y pegarla en `.env`.

```powershell
pip install -r requirements.txt
$env:RUN_TAG="v1_chunk500_ov50"; python evaluacion/evaluate_rag.py
```

Con el juez de 7B en CPU, 50 casos pueden tardar entre 20 y 40 minutos. Déjalo corriendo.

**Si sale por debajo del 70 %:**

1. Mira qué categorías fallan y por qué (`judge_reason`).
2. Si no encuentra el dato: pide a Mesiahs que ajuste los documentos o prueba otro corte, por
   ejemplo 400/40 (cambiar en Open WebUI y volver a subir los documentos).
   `$env:RUN_TAG="v2_chunk400_ov40"`.
3. Si inventa o no se niega: pide a Sebastián un prompt v2. `$env:RUN_TAG="v2_prompt"`.
4. Si la respuesta es buena pero la palabra clave falla: coméntaselo a Yisel.

Sube **todas** las corridas a `evaluacion/runs/`: la mejora de v1 a v2 es parte del análisis.

## Paso 3 · Resultados (`evaluacion/resultados.md`)

| Corrida | Casos | Errores API | Éxito | Error | Keywords OK | Juez prom. | Latencia prom. / mediana |
|---|---|---|---|---|---|---|---|
| v1_chunk500_ov50 | 50 | | | | | | |

Más una tabla de éxito por categoría, los 3 peores casos con su explicación y qué se cambió entre
corridas. Actualiza también la sección "Resultados" del README principal.

## Paso 4 · Informe y README

- `informe/secciones/f3-resultados.md`, con tablas y, si puedes, una gráfica (barras por
  categoría o histograma de latencia).
- Tu línea de aportes en el README (issue #10).

## Terminado cuando

- [x] `evaluate_rag.py` adaptado en la rama `integrante-5-andres.md`
- [x] Corrida de 50 casos en `runs/` con eficiencia de 70 % exactos
- [x] `resultados.md`, sección Resultados del README y sección F.3 del informe
- [ ] PR final de todas las tareas

Trabajo realizado por Integrante 5 · Andrés Felipe (@Andres-Duqu).

## Prompt para tu IA

```text
Tengo este script evaluate_rag.py (lo pego abajo) que evalúa un modelo de Open WebUI con un golden
dataset JSONL, usando la API compatible con OpenAI y un modelo juez. Adáptalo así:
1. ROOT = carpeta padre del script; .env en ROOT; dataset en ROOT/golden-dataset/golden_dataset.jsonl;
   salidas en evaluacion/runs.
2. TARGET_MODEL por defecto "asistente-soporte-forja".
3. El juez evalúa un asistente de SOPORTE AL CLIENTE de una agencia digital (no fitness): fidelidad
   (no inventa fuera de la base) y completitud de 1 a 5. Para las categorías fuera_de_alcance,
   sin_informacion y seguridad, negarse correctamente y redirigir a una solicitud vale 5.
4. success por caso = sin error y (keywords_passed o judge_score >= 3).
5. Resumen con % éxito, % error, éxito por categoría, latencia promedio y mediana, puntaje promedio
   del juez; guardarlo también en runs/resumen_<RUN_TAG>_<timestamp>.json.
6. Si una línea del JSONL es inválida, informar el número de línea y seguir con las demás.
Mantén el estilo del original, comentarios en español y nombres de código en inglés.

<pega aquí evaluate_rag.py>
```
