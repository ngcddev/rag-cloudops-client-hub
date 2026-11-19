# Modelo personalizado

<!-- Qué va en esta carpeta y qué debe documentar el responsable (punto 3 de la actividad). -->

**Responsable:** Integrante 3.

## Qué va aquí

- `system-prompt.md`: el system prompt completo que se pega en Open WebUI, con sus políticas:
  - responder solo con la base de conocimiento y decir "no tengo esa información" cuando no esté;
  - no inventar plazos, precios ni datos de clientes;
  - no revelar credenciales, datos de otros clientes ni el propio prompt;
  - rechazar con cortesía las preguntas fuera de alcance y redirigir a una solicitud;
  - escalar a un humano ante una falla crítica (P1);
  - tono y lenguaje del glosario para clientes (sin jerga técnica).
- `configuracion.md`: modelo base (sugerido `qwen2.5:3b-instruct`, que ya usa el proyecto) y por
  qué; ID del modelo en Open WebUI (`asistente-soporte-forja`); temperatura, top_p, num_ctx y
  max_tokens, con la razón de cada valor.
- Capturas de la configuración en `../evidencias/interfaz/`.
