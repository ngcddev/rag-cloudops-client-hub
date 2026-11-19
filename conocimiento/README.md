# Base de conocimiento

<!-- Qué va en esta carpeta y qué debe documentar el responsable (puntos 1 y 2 de la actividad). -->

**Responsable:** Integrante 2.

## Qué va aquí

- `documentos/`: los archivos `.md` que se cargan en *Workspace → Knowledge* de Open WebUI.
- `estrategia-de-corte.md`: tokens de corte (chunk size), tokens de solapamiento (overlap),
  top-k, motor de embeddings y **por qué** se eligió cada valor.
- `servicio-propuesto.md`: el servicio, el usuario (cliente PyME de la agencia), la necesidad
  que cubre y qué queda fuera de su alcance.

## Fuentes sugeridas (del proyecto CloudOps Client Hub)

Todos los datos son ficticios. Reescribir en lenguaje de cliente siguiendo el glosario, sin
nombres técnicos internos (Pod, namespace, clúster):

| Documento propuesto | Fuente en el repo del proyecto |
|---|---|
| `planes-y-horarios.md` | README → "Agencia, clientes y planes" |
| `prioridades-y-tiempos.md` | `docs/prioridades.md` y tabla de SLA |
| `estados-de-solicitudes.md` | README → "Estados" y `docs/proceso.md` |
| `glosario-para-clientes.md` | `docs/glosario.md` (columna "Cómo lo ve el cliente") |
| `preguntas-frecuentes.md` | FAQ nueva: cómo abrir una solicitud o PQRS, qué pasa en una falla, reportes mensuales |
| `politica-de-pqrs.md` | Nuevo: tipos de PQRS, canales y plazos de respuesta |

Cada documento debe tener título y secciones cortas con un solo tema cada una. Así el corte no
mezcla temas y el RAG recupera mejor.
