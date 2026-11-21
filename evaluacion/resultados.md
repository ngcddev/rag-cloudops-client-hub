# Resultados de evaluación

Responsable: Integrante 5, Andrés Felipe Díaz (`@Andres-Duqu`).

## Estado

Se completaron dos corridas válidas del golden dataset contra `asistente-soporte-forja` con el
modelo juez `qwen2.5:7b-instruct`: `v1_chunk500_ov50` (70.00 % de éxito) y `v2_bge-m3_legacy`
(96.00 % de éxito). La primera ejecución de v1, hecha con una API key inválida, se conserva como
evidencia del error 401 y no se usa para el análisis.

| Corrida | Casos | Errores API | Éxito | Error | Keywords OK | Juez prom. | Latencia prom. / mediana |
|---|---:|---:|---:|---:|---:|---:|---|
| v1_chunk500_ov50 | 50 | 0 | 70.00 % | 30.00 % | 24 | 3.16 | 4.195 s / 2.655 s |
| v2_bge-m3_legacy | 50 | 0 | 96.00 % | 4.00 % | 44 | 4.22 | 2.485 s / 1.587 s |

## Éxito por categoría en v1_chunk500_ov50

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

## Peores casos de v1_chunk500_ov50

| Caso | Categoría | Puntaje | Motivo |
|---|---|---:|---|
| planes-03 | planes | 1 | Respondió un horario de lunes a viernes para el plan Premium y omitió atención 24/7. |
| sla-01 | SLA | 1 | No indicó los 15 minutos de respuesta máxima de una P1 y respondió con una negativa genérica. |
| estados-03 | estados | 1 | No explicó cuándo una solicitud pasa a cerrada y redirigió sin dar el dato esperado. |

El puntaje mínimo (1/5) apareció en siete casos: además de los tres anteriores, `planes-05`,
`sla-05`, `pqrs-04` y `pqrs-06`. `planes-05` y `sla-05` se contaron como éxito porque acertaron las
palabras clave aunque el juez les dio 1; conviene revisar ese criterio en la próxima corrida.

## Cambios entre corridas

La primera ejecución de `v1_chunk500_ov50` usó una API key inválida: produjo 50 errores HTTP 401 y
no representa el desempeño del modelo. La segunda ejecución, ya con una API key válida, el juez 7B
descargado, el modelo base 3B creado y la colección `base-soporte-forja` cargada, obtuvo 70 % de
éxito. Las categorías con 50 % —SLA y PQRS— concentraron las fallas de recuperación de datos
concretos. En lugar de cambiar el prompt o los documentos, la corrida siguiente cambió el entorno
de recuperación (ver abajo), y esa fue la variable que explicó la mejora.

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

Los dos fallos de v2 son `sla-08` (afirmó que el reloj de P2 corre 24 horas; en realidad P2, P3 y
P4 siguen el horario del plan y solo P1 es 24x7) y `sin-03` (inventó una compensación por
incumplir la disponibilidad, que no está en la base: es la falla más grave, porque es una
invención). Los 15 casos que fallaron en v1 aprobaron en v2; siete de ellos habían respondido "No
tengo esa información" sobre datos que sí estaban en la base, y el contexto inyectado los resolvió.
Archivos: `runs/v2_bge-m3_legacy_20261121T163718Z.jsonl` y su resumen JSON.

## Comentario del Integrante 5 sobre la corrida v2

La corrida v2 confirma que la mayor parte del error de v1 estaba en la recuperación: con el mismo
prompt, los mismos documentos y el mismo modelo base, el contexto inyectado y los embeddings
`bge-m3` subieron el éxito de 70 % a 96 % y bajaron la latencia promedio de 4.195 s a 2.485 s. Sin
embargo, el resultado no debe leerse como una mejora completa: `sla-08` y `sin-03` empeoraron
respecto de v1, y `sin-03` es una invención, el tipo de error más peligroso para un asistente de
soporte. También hay que tener en cuenta que el criterio de éxito (`keywords_passed` o juez ≥ 3)
puede contar como válida una respuesta con puntaje 1 si acierta la palabra clave, como ocurrió en
`planes-05` y `sla-05` de v1. Para una v3 propondría: (1) prohibir explícitamente compensaciones o
descuentos que no estén en la base; (2) reportar por separado el éxito por palabras clave y por
juez; (3) repetir la corrida con una muestra mayor o con variantes de redacción; y (4) fijar la
versión de Open WebUI y la configuración de Function Calling para que el resultado sea reproducible.
