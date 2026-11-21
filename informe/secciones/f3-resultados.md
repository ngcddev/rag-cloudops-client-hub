# F.3 Resultados y análisis

Responsable: Integrante 5, Andrés Felipe (`@Andres-Duqu`).

## Estado de la corrida

El script de evaluación se ejecutó sobre los 50 casos válidos contra el modelo
`asistente-soporte-forja`, con `qwen2.5:7b-instruct` como juez.

## Métricas previstas

| Métrica | Resultado |
|---|---|
| Casos evaluados | 50 |
| Porcentaje de éxito | 70.00 % |
| Porcentaje de error | 30.00 % |
| Casos que aprobaron palabras clave | 24 |
| Errores API | 0 |
| Éxito por categoría | Ver tabla siguiente |
| Latencia promedio | 4.195 s |
| Latencia mediana | 2.655 s |
| Puntaje promedio del juez | 3.16 |

| Categoría | Éxito |
|---|---|
| planes | 75.00 % |
| SLA | 50.00 % |
| estados | 66.67 % |
| glosario | 66.67 % |
| PQRS | 50.00 % |
| fuera de alcance | 83.33 % |
| sin información | 100.00 % |
| seguridad | 100.00 % |

## Análisis

La meta del 70 % se alcanzó exactamente. Las categorías de seguridad y ausencia de información
alcanzaron 100 %. Los resultados más débiles fueron SLA y PQRS, con 50 % de éxito. El modelo
presentó fallas de recuperación de datos concretos, por ejemplo 15 minutos en P1, 24 horas en P3
o el cierre de una solicitud.

Los tres peores casos fueron `planes-03`, `sla-01` y `estados-03`, con puntaje 1 del juez.
No hubo errores de API en la corrida válida.

## Segunda corrida (v2) y comparación

Con el mismo golden dataset y el mismo juez se repitió la evaluación con el contexto de la base
realmente inyectado (Function Calling en Legacy) y embeddings `bge-m3` (detalle en
`evaluacion/resultados.md`):

| Métrica | v1 (`v1_chunk500_ov50`) | v2 (`v2_bge-m3_legacy`) |
|---|---|---|
| Porcentaje de éxito | 70,00 % | **96,00 %** |
| Porcentaje de error | 30,00 % | **4,00 %** |
| Casos que aprobaron palabras clave | 24 | 44 |
| Puntaje promedio del juez | 3,16 | 4,22 |
| Latencia promedio / mediana | 4,195 s / 2,655 s | 2,485 s / 1,587 s |

La mejora de 26 puntos viene de la recuperación, no del modelo: el prompt, los documentos y el modelo
base son los mismos. Todas las categorías con datos de la base llegan a 100 %, salvo SLA (87,5 %).
Los dos fallos restantes son `sla-08` y `sin-03`; este último es una invención (el modelo ofreció una
compensación que no existe), el riesgo más importante de un asistente RAG y el primer punto a corregir
en una versión siguiente, por ejemplo con una política más estricta contra datos que no estén en el
contexto.
