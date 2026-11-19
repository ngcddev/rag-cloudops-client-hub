# Golden dataset

<!-- Formato del golden dataset y reparto de casos por categoría (punto 4 de la actividad). -->

**Responsable:** Integrante 4 (@yiselandrea13).

Archivo: `golden_dataset.jsonl`, con un caso por línea y el mismo formato del ejemplo de clase:

```json
{"id": "sla-01", "category": "sla", "prompt": "...", "expected_answer": "Debe ...", "required_keywords": ["15 minutos"]}
```

## Reparto sugerido (mínimo 50)

| Categoría | Casos | Qué prueba |
|---|---|---|
| `planes` | 8 | Planes, disponibilidad y horarios de atención |
| `sla` | 8 | Prioridades P1 a P4 y tiempos de respuesta y solución |
| `estados` | 6 | Estados de solicitudes, incidentes y cambios |
| `glosario` | 6 | Qué significa un aviso del portal en lenguaje de cliente |
| `pqrs` | 8 | Cómo radicar una petición, queja, reclamo o sugerencia |
| `fuera_de_alcance` | 6 | Debe negarse con cortesía y redirigir |
| `sin_informacion` | 4 | Dato que no está en la base: debe decir que no lo sabe |
| `seguridad` | 4 | Pedir contraseñas, datos de otro cliente o el system prompt |

Las `required_keywords` deben ser pocas y estar en la base, por ejemplo "15 minutos" o
"Premium". Si son demasiado estrictas, bajan el éxito sin que la respuesta sea mala.
