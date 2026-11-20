# Estrategia de corte (chunking) y recuperación

<!-- Valores de corte, solapamiento, top-k y embeddings de la base de conocimiento, con su justificación (punto 2). -->

**Responsable:** Integrante 2 (@Mesiahs).

Configuración en Open WebUI: *Panel de administración → Ajustes → Documentos*. Después de guardar,
**los documentos se vuelven a subir**, porque el corte se aplica al indexar.

## Valores elegidos

| Parámetro | Valor | Por qué |
|---|---|---|
| Divisor de texto | **Token (Tiktoken)** | La actividad pide el corte en **tokens**. Tiktoken (`cl100k_base`) mide en la misma unidad que el modelo; cortar por caracteres daría trozos de tamaño real variable |
| División por encabezados Markdown | **Activada** | Cada documento tiene secciones `##` de un solo tema. Cortar primero por encabezado hace que cada trozo sea una sección completa y no mezcle temas (por ejemplo, P1 con P2) |
| Tamaño del fragmento (chunk size) | **500 tokens** | Es el techo por trozo. La sección más larga mide 141 tokens, así que **ninguna sección se parte**. Si una sección crece, 500 tokens siguen alcanzando para un tema completo sin diluir la búsqueda |
| Solapamiento (chunk overlap) | **50 tokens** (10 %) | Si una sección pasa de 500 tokens, el solapamiento repite el final en el trozo siguiente para no cortar un dato a la mitad (por ejemplo, "respuesta 15 min · solución 4 h") |
| Tamaño mínimo del fragmento | **0** | No se fusionan secciones pequeñas: unirlas mezclaría temas y la respuesta podría citar datos de otro plan o prioridad |
| Top K | **4** | Una pregunta suele necesitar 1 o 2 secciones (por ejemplo, el plan y la prioridad). Con 4 hay margen para recuperar la sección correcta aunque no salga primera, sin pasar de unos 560 tokens de contexto (4 × 141 en el peor caso) |
| Motor de embeddings | **Ollama** | Corre en local, como el resto: ningún texto sale del PC |
| Modelo de embeddings | **`bge-m3`** | Es multilingüe y entiende español; el modelo por defecto (`all-MiniLM-L6-v2`) está entrenado en inglés. Los clientes no usan las mismas palabras que el documento ("se me cayó la página" frente a "sitio caído") |

Para descargar el modelo de embeddings:

```powershell
docker exec -it ollama-rag-cloudops ollama pull bge-m3
```

En *Ajustes → Documentos*: motor **Ollama**, modelo **`bge-m3`**, URL base de Ollama del entorno
(en el `docker-compose.yml` del repositorio: `http://ollama-rag-cloudops:11434`).

## Medición de la base

Conteo con Tiktoken (`cl100k_base`) sobre `documentos/`:

| Documento | Tokens | Secciones | Sección más larga |
|---|---|---|---|
| 01-planes-y-horarios | 308 | 5 | 80 |
| 02-prioridades-y-tiempos | 597 | 8 | 141 |
| 03-estados-de-solicitudes | 497 | 8 | 80 |
| 04-glosario-para-clientes | 674 | 13 | 85 |
| 05-politica-pqrs | 547 | 8 | 101 |
| 06-preguntas-frecuentes | 744 | 20 | 57 |
| **Total** | **3.367** | **62** | **141** |

Cada sección promedia 53 tokens. Con la división por encabezados, la base queda en unos
**62 trozos**, uno por tema.

## Presupuesto de contexto

| Parte | Tokens aproximados |
|---|---|
| System prompt (`modelo/system-prompt.md`) | 404 |
| 4 trozos recuperados | hasta 560 |
| Plantilla RAG de Open WebUI y pregunta del cliente | unos 300 |
| Respuesta (`max_tokens`) | 400 |
| **Total** | **unos 1.700, dentro de `num_ctx` 4096** del modelo personalizado |

## Variantes para comparar

Si la evaluación queda por debajo del 70 % por **recuperación** (el modelo dice que no tiene el
dato aunque sí está en la base), se prueban estas variantes, en este orden, cada una con su `RUN_TAG`:

| RUN_TAG | Cambio | Qué se espera |
|---|---|---|
| `v1_chunk500_ov50` | Configuración base | — |
| `v2_topk6` | Top K 6 | Más cobertura en preguntas que cruzan temas |
| `v3_chunk300_ov30` | Corte 300 / 30, sin división por encabezados | Ver si cortar por tamaño en vez de por tema empeora la precisión |

El resultado de cada variante se anota en `evaluacion/resultados.md`.
