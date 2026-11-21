# Configuración del modelo personalizado

<!-- Decisiones del modelo en Open WebUI y su justificación (punto 3 de la actividad). -->

**Responsable:** Integrante 3 (@sebastianpaja-debug).

## Identificación en Open WebUI

| Campo | Valor |
|---|---|
| Name | Asistente Soporte Forja |
| ID | `asistente-soporte-forja` (exacto: lo usan los scripts de `api/` y `evaluacion/`) |
| Base model | `qwen2.5:3b-instruct` |
| Knowledge | `base-soporte-forja` |
| Visibility | Public |
| System prompt | [`system-prompt.md`](system-prompt.md) |

## Decisiones e hiperparámetros

| Decisión | Valor | Por qué |
|---|---|---|
| Modelo base | qwen2.5:3b-instruct | Buen español, sigue instrucciones y corre en CPU con unos 4 GB; es el que ya usa el proyecto |
| Temperatura | 0.2 | Respuestas consistentes y poca invención; el asistente debe ceñirse al contexto |
| top_p | 0.9 | Con temperatura baja, deja algo de variedad en la redacción sin salirse de las opciones probables |
| num_ctx | 4096 | Cabe el prompt, 4 trozos de 500 tokens y la pregunta |
| max_tokens | 400 | Las respuestas son de 150 palabras como máximo; deja margen y evita divagar |
| Function Calling | Legacy | En Open WebUI 0.13.x, con el valor nativo el modelo de 3B no llama a la herramienta de búsqueda y responde sin la base; con Legacy el contexto recuperado siempre se inyecta |

## Plantilla RAG

Open WebUI inserta el contexto recuperado con una plantilla (*Admin → Ajustes → Documentos*). La que
trae por defecto pide citas `[1]` y permite responder con conocimiento propio, lo que contradice la
política 1 y confundía al modelo de 3B. Se usa esta, más corta y en español:

```text
Use el siguiente contexto de la base de conocimiento para responder al cliente. No escriba números entre corchetes ni cite fuentes.

<context>
{{CONTEXT}}
</context>

Pregunta del cliente: {{QUERY}}
```

## Versiones del prompt

| Versión | Cambio | Resultado en la evaluación |
|---|---|---|
| v1 | Prompt inicial con 8 políticas | Cumple seguridad y alcance; falla en datos concretos (por ejemplo, el horario del Premium) |
| v2 (descartada) | v1 más una regla para no mezclar planes y un rechazo fijo fuera de tema | No mejoró los datos y añadió un rechazo innecesario a la falla crítica |

Si la evaluación (Integrante 5) encuentra fallas, se ajusta el prompt como v2, se anota aquí y se
vuelve a correr. La comparación v1 contra v2 va en el informe.

## Capturas

En `../evidencias/interfaz/`: `03-modelo-general.png`, `03b-modelo-conocimiento.png`, `04-modelo-parametros.png` y `04b-modelo-parametros.png`.
