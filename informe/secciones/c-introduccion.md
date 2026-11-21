# C. Introducción

Este documento describe el diseño, la implementación y la evaluación de un asistente de soporte y
PQRS (peticiones, quejas, reclamos y sugerencias) para los clientes de **Forja Digital**, una agencia
digital ficticia que administra los sitios web de pequeñas y medianas empresas. El asistente hace
parte del proyecto integrador **CloudOps Client Hub** del diplomado CloudForge AI 5.0 y responde
preguntas sobre planes, horarios de atención, prioridades y tiempos, estados de las solicitudes,
avisos del portal y radicación de PQRS.

El servicio usa **generación aumentada por recuperación (RAG)**: el modelo no responde de memoria,
sino con trozos recuperados de una base de conocimiento propia de seis documentos. Se ejecuta por
completo en local, con Ollama y Open WebUI, de modo que ningún dato sale a servicios de IA externos.
Sobre el modelo base `qwen2.5:3b-instruct` se creó un modelo personalizado con un system prompt de
ocho políticas que delimitan su comportamiento.

El informe sigue el orden de la actividad. La sección D explica el problema que resuelve el modelo.
La sección E define el modelo: la base de conocimiento y su estrategia de corte, el system prompt y
los hiperparámetros. La sección F reporta las pruebas desde la interfaz y la API y los resultados
con el golden dataset de 50 casos. La sección G recoge las conclusiones y los trabajos futuros.
El código, los documentos de la base y las evidencias están en el repositorio del equipo.
