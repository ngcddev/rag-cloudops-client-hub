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
