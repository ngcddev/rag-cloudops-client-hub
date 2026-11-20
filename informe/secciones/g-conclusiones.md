# G. Conclusiones y trabajos futuros

## Integrante 2 · Eric Mesias

Aprendí que una base de conocimiento para RAG no consiste solo en reunir información: cada sección debe ser clara, autocontenida y fiel a las fuentes para que el asistente pueda recuperarla y explicarla correctamente. La carga de los seis documentos y la configuración visible de fragmentos de 500 tokens con 50 de superposición son un primer avance, pero la respuesta de prueba sobre Top-K mostró que todavía no se puede asumir que el sistema responde con precisión. Mejoraría la base separando los avisos y estados en temas más específicos, revisando los datos propuestos de PQRS con la agencia y verificando el valor de Top K, el modelo de embeddings y la recarga de los documentos; después repetiría pruebas con respuestas esperadas para detectar y corregir información incorrecta antes de usar el asistente con clientes.
