# E.1 Base de conocimiento y estrategia de corte

## Contenido de la base

Se prepararon seis documentos Markdown en español, dirigidos a los clientes de Forja Digital:

1. `01-planes-y-horarios.md`: disponibilidad mensual y horarios de los planes.
2. `02-prioridades-y-tiempos.md`: significado de P1–P4 y tiempos de respuesta y solución.
3. `03-estados-de-solicitudes.md`: estados de solicitudes, incidentes, cambios y sitios.
4. `04-glosario-para-clientes.md`: explicación de los avisos del portal en lenguaje de cliente.
5. `05-politica-pqrs.md`: tipos de PQRS, canal, información requerida, plazos y seguimiento.
6. `06-preguntas-frecuentes.md`: 20 preguntas frecuentes con sus respuestas.

El contenido se elaboró a partir de los documentos del proyecto CloudOps Client Hub sobre planes,
prioridades, glosario y proceso de atención, reescritos sin jerga técnica. La política de PQRS
(canal y plazos) se definió para este servicio y es coherente con los tiempos de las prioridades.

Cada documento se escribió pensando en el corte: un título por documento y secciones `##` cortas,
cada una con **un solo tema** y **autocontenida** (repite el dato completo en vez de remitir a
otra sección). Así, cualquier trozo recuperado basta por sí solo para responder.

## Carga en Open WebUI

Los seis archivos se cargaron en una base de conocimiento de Open WebUI (*Espacio de trabajo →
Conocimiento*), que luego se vincula al modelo personalizado.

![Archivos cargados en la base de conocimiento](../../evidencias/interfaz/01-base-de-conocimiento.png)

## Estrategia de corte

| Parámetro | Valor | Justificación |
|---|---|---|
| Divisor de texto | Token (Tiktoken) | El corte se mide en tokens, la misma unidad del modelo |
| División por encabezados Markdown | Activada | Cada sección `##` queda como un trozo de un solo tema |
| Tokens de corte (chunk size) | **500** | Techo por trozo; la sección más larga mide 141 tokens, así que ninguna se parte |
| Tokens de solapamiento (overlap) | **50** (10 %) | Si una sección supera 500 tokens, evita cortar un dato a la mitad |
| Top K | 4 | Cubre preguntas que necesitan 1 o 2 secciones, con margen, en unos 560 tokens de contexto |
| Embeddings | Ollama · `bge-m3` | Local y multilingüe: relaciona preguntas en español con distintas palabras |

![Ajustes de corte en Open WebUI: Tiktoken, 500 y 50 tokens, división por encabezados](../../evidencias/interfaz/02-ajustes-de-corte.png)

La base suma **3.367 tokens** en **62 secciones** (promedio de 53 tokens por sección), medidos con
Tiktoken. Como las secciones son cortas y de un tema, la división por encabezados produce unos 62
trozos coherentes. El valor de 500 tokens actúa como techo de seguridad si un documento crece. Con
4 trozos recuperados, el system prompt (404 tokens) y la respuesta (400), cada consulta usa unos
1.700 tokens, dentro de la ventana de 4.096 del modelo.

El detalle por documento y las variantes previstas para comparar están en
[`conocimiento/estrategia-de-corte.md`](../../conocimiento/estrategia-de-corte.md).
