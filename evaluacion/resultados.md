# Resultados de evaluación

Responsable: Integrante 5, Andrés Felipe (`@Andres-Duqu`).

## Estado

Se completó una corrida válida del golden dataset contra `asistente-soporte-forja` y el modelo
juez `qwen2.5:7b-instruct`.

| Corrida | Casos | Errores API | Éxito | Error | Keywords OK | Juez prom. | Latencia prom. / mediana |
|---|---:|---:|---:|---:|---:|---:|---|
| v1_chunk500_ov50 | 50 | 0 | 70.00 % | 30.00 % | 24 | 3.16 | 4.195 s / 2.655 s |
| v2_bge-m3_legacy | 50 | 0 | 96.00 % | 4.00 % | 44 | 4.22 | 2.485 s / 1.587 s |

## Éxito por categoría

| Categoría | Éxito |
|---|---|
| planes | 75.00 % (6/8) |
| SLA | 50.00 % (4/8) |
| estados | 66.67 % (4/6) |
| glosario | 66.67 % (4/6) |
| PQRS | 50.00 % (4/8) |
| fuera de alcance | 83.33 % (5/6) |
| sin información | 100.00 % (4/4) |
| seguridad | 100.00 % (4/4) |

## Peores casos

| Caso | Categoría | Puntaje | Motivo |
|---|---|---:|---|
| planes-03 | planes | 1 | Respondió un horario de lunes a viernes para el plan Premium y omitió atención 24/7. |
| sla-01 | SLA | 1 | No indicó los 15 minutos de respuesta máxima de una P1 y respondió con una negativa genérica. |
| estados-03 | estados | 1 | No explicó cuándo una solicitud pasa a cerrada y redirigió sin dar el dato esperado. |

## Cambios entre corridas

La corrida inicial `v1_chunk500_ov50` con la API key inválida produjo 50 errores HTTP 401 y no
representa el desempeño del modelo. Después de crear una API key válida, descargar el juez 7B,
crear el modelo base 3B y cargar la colección `base-soporte-forja`, la segunda corrida obtuvo 70 %
de éxito. A las categorías con 50 % de éxito —SLA y PQRS— les corresponde una revisión de la
recuperación RAG y de la redacción base antes de una segunda versión.

## Segunda corrida: v2_bge-m3_legacy (Integrante 1)

Corrida ejecutada por @ngcddev en otro equipo, con el mismo script, el mismo golden dataset y el
mismo juez (`qwen2.5:7b-instruct`). **Cambió el entorno, no el prompt ni los documentos:**
Open WebUI 0.13.4 con **Function Calling en Legacy** (inyecta la base vinculada al modelo en cada
consulta), embeddings `bge-m3` de Ollama, corte de 500/50 tokens por encabezados y Top K 4, como
indica `conocimiento/estrategia-de-corte.md`.

| Categoría | Éxito v1 | Éxito v2 |
|---|---|---|
| planes | 75,00 % (6/8) | 100,00 % (8/8) |
| SLA | 50,00 % (4/8) | 87,50 % (7/8) |
| estados | 66,67 % (4/6) | 100,00 % (6/6) |
| glosario | 66,67 % (4/6) | 100,00 % (6/6) |
| PQRS | 50,00 % (4/8) | 100,00 % (8/8) |
| fuera de alcance | 83,33 % (5/6) | 100,00 % (6/6) |
| sin información | 100,00 % (4/4) | 75,00 % (3/4) |
| seguridad | 100,00 % (4/4) | 100,00 % (4/4) |

Los dos fallos de v2 son `sla-08` (dijo que el reloj de P2 corre 24 horas; depende del plan) y
`sin-03` (inventó una compensación por incumplir la disponibilidad, que no está en la base: es la
falla más grave, porque es una invención). Los cinco casos de v1 donde el modelo respondió "No tengo
esa información" sobre datos que sí estaban en la base se resolvieron con el contexto inyectado.
Archivos: `runs/v2_bge-m3_legacy_20261121T163718Z.jsonl` y su resumen JSON.
