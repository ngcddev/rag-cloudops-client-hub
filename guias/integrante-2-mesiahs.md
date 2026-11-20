# Guía · Integrante 2 · @Mesiahs

<!-- Pasos para la base de conocimiento y la estrategia de corte (issues #2 y #3). -->

**Tu parte:** el servicio propuesto, los documentos de la base de conocimiento y la estrategia de
corte. **Vas primero:** el modelo, el golden dataset y la evaluación dependen de tus documentos.
Meta: **documentos en `main` a la hora 2 del cronograma** (ver `guias/README.md`).

## Paso 1 · Servicio propuesto (15 min)

Crear `conocimiento/servicio-propuesto.md` con:

- **Servicio:** asistente de soporte y PQRS para los clientes (PyMEs) de la agencia Forja Digital.
- **Usuario:** el dueño o empleado de la PyME (restaurante, ferretería, consultorio).
- **Necesidad:** resolver dudas frecuentes sin esperar a un técnico: planes, horarios de
  atención, tiempos de respuesta, estados de una solicitud, qué significa un aviso del portal y
  cómo radicar una PQRS.
- **Fuera de alcance:** datos de otros clientes, precios no publicados, cambios técnicos en el
  sitio y temas ajenos a la agencia.

## Paso 2 · Documentos de la base (1 h 30 min, con IA)

Fuentes en el repo del proyecto (público):

- Planes, prioridades y estados: https://github.com/ngcddev/CloudOps#agencia-clientes-y-planes
- Glosario para clientes: https://github.com/ngcddev/CloudOps/blob/main/docs/glosario.md
- Prioridades: https://github.com/ngcddev/CloudOps/blob/main/docs/prioridades.md
- Proceso de atención: https://github.com/ngcddev/CloudOps/blob/main/docs/proceso.md

Crear en `conocimiento/documentos/` (Markdown):

| Archivo | Contenido |
|---|---|
| `01-planes-y-horarios.md` | Planes Básico, Estándar y Premium: disponibilidad mensual y horario de atención |
| `02-prioridades-y-tiempos.md` | P1 a P4: qué significa cada una y los tiempos de respuesta y solución |
| `03-estados-de-solicitudes.md` | Estados de solicitudes, incidentes, cambios y del sitio, explicados al cliente |
| `04-glosario-para-clientes.md` | Qué significa cada aviso que ve el cliente (columna "Cómo lo ve el cliente") |
| `05-politica-pqrs.md` | Qué es una petición, queja, reclamo y sugerencia; cómo se radica; plazos |
| `06-preguntas-frecuentes.md` | 15 a 25 preguntas frecuentes con su respuesta |

Reglas para que el RAG funcione bien:

- Un `#` título por archivo y secciones `##` cortas, **un solo tema por sección**.
- Repetir el dato completo en cada sección ("En el plan Premium la atención es 24/7"), sin
  depender de "como se dijo arriba": el corte separa las secciones.
- Lenguaje de cliente: nunca Pod, namespace, clúster ni Argo CD.
- No inventar datos que contradigan las fuentes. Si inventas algo nuevo (por ejemplo, los plazos de
  PQRS), escríbelo una sola vez y de forma clara.

Sube los documentos en un PR **apenas estén** (`Closes #2`) y avisa al grupo.

## Paso 3 · Cargar en Open WebUI

1. *Workspace → Knowledge → +*: nombre `base-soporte-forja`, visibilidad **Public**.
2. Subir los 6 archivos.
3. Captura de pantalla en `evidencias/interfaz/01-base-de-conocimiento.png`.

## Paso 4 · Estrategia de corte (issue #3)

En *Admin Panel → Settings → Documents*:

1. **Text Splitter: Token (Tiktoken)**, para que el corte se mida en **tokens**, como pide la
   actividad.
2. Valores: **Chunk Size 500**, **Chunk Overlap 50**, **Top K 4**, división por encabezados Markdown activada y embeddings **Ollama · `bge-m3`** (todos usan la misma configuración; ver `conocimiento/estrategia-de-corte.md`).
3. Guardar y **volver a subir los documentos** (el corte se aplica al cargar).
4. Captura en `evidencias/interfaz/02-ajustes-de-corte.png`.

Crear `conocimiento/estrategia-de-corte.md` con una tabla de cada valor y su razón: tamaño de las
secciones de tus documentos, por qué el solapamiento evita cortar un dato a la mitad, por qué
top-k 4 y qué modelo de embeddings usa Open WebUI. Si Andrés prueba otra combinación (por ejemplo
400/40), se agrega a la tabla con su resultado.

## Paso 5 · Tu parte del informe y del README

- `informe/secciones/d-problema.md` y `informe/secciones/e1-conocimiento.md`, con las capturas.
- Tu línea en la tabla de aportes del README (issue #10).

## Terminado cuando

- [ ] `servicio-propuesto.md`, 6 documentos y `estrategia-de-corte.md` en `main`
- [ ] Capturas 01 y 02 en `evidencias/interfaz/`
- [ ] Secciones D y E.1 del informe

## Prompt para tu IA

```text
Voy a crear la base de conocimiento de un asistente RAG de soporte al cliente (Open WebUI + Ollama).
Contexto: "Forja Digital" es una agencia digital ficticia que administra los sitios web de PyMEs
(Restaurante La Sazón, Ferretería El Tornillo, Consultorio Dental Popayán). Los clientes tienen
planes Básico, Estándar y Premium, abren solicitudes y PQRS, y reciben avisos sobre su sitio.

Te paso el material fuente (planes, prioridades, estados, glosario y proceso). A partir de él,
redacta 6 documentos Markdown para la base: 01-planes-y-horarios, 02-prioridades-y-tiempos,
03-estados-de-solicitudes, 04-glosario-para-clientes, 05-politica-pqrs, 06-preguntas-frecuentes.

Reglas:
- Español, dirigido al cliente, sin jerga técnica (nunca Pod, namespace, clúster, Argo CD).
- Un título # por documento y secciones ## cortas, cada una con un solo tema y autocontenida
  (repite el dato completo, sin decir "como se dijo arriba"), porque se cortará en trozos de unos
  500 tokens.
- No cambies ningún dato de la fuente. Lo que no esté en la fuente (por ejemplo, los plazos de
  PQRS) propónmelo marcado con [PROPUESTA] para que yo lo revise.
- En 06 incluye 20 preguntas frecuentes reales de un cliente de PyME, con la respuesta.

Material fuente:
<pega aquí el contenido de las fuentes>
```
