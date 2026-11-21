# G. Conclusiones y trabajos futuros

## Integrante 2 · Eric Mesias

Aprendí que una base de conocimiento para RAG no consiste solo en reunir información: cada sección debe ser clara, autocontenida y fiel a las fuentes para que el asistente pueda recuperarla y explicarla correctamente. La carga de los seis documentos y la configuración visible de fragmentos de 500 tokens con 50 de superposición son un primer avance, pero la respuesta de prueba sobre Top-K mostró que todavía no se puede asumir que el sistema responde con precisión. Mejoraría la base separando los avisos y estados en temas más específicos, revisando los datos propuestos de PQRS con la agencia y verificando el valor de Top K, el modelo de embeddings y la recarga de los documentos; después repetiría pruebas con respuestas esperadas para detectar y corregir información incorrecta antes de usar el asistente con clientes.

## Integrante 1 · Nicolás Gaviria

Aprendí que un RAG puede fallar sin que nada parezca roto: al reproducir el entorno en otro equipo, el modelo respondía con seguridad datos que no estaban en la base porque la versión de Open WebUI no inyectaba la base vinculada al modelo, y solo se notó al comparar la respuesta con el documento. Desde entonces compruebo cada cambio con una pregunta cuya respuesta está en la base. La dificultad mayor fue la coordinación: cinco personas con equipos distintos necesitaban la misma configuración de corte y de embeddings, y la resolví dejándola escrita en el repositorio y usando ramas, PR y conflictos pequeños en carpetas separadas. Como mejora futura, un modelo base más grande o un reordenador de resultados reduciría las respuestas "no tengo esa información" sobre datos que sí están, y fijar la versión de Open WebUI evitaría diferencias entre equipos.
