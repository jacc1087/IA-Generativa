# 🎬 IA-Generativa — Asistente Experto con Gemini, RAG y Agentes

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash%20Lite-4285F4)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-6E56CF)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Status](https://img.shields.io/badge/Estado-Finalizado-brightgreen)

Asistente conversacional experto construido con **RAG (Retrieval-Augmented Generation)** y un **agente LangGraph**, especializado en la filmografía de **Quentin Tarantino**. El sistema indexa documentación extraída de Wikipedia, recupera el contexto más relevante para cada pregunta y genera respuestas con memoria conversacional a través del modelo **Gemini**.

> ⚠️ **Aviso de spoilers**
> Este proyecto contiene información detallada sobre el argumento y los finales de las películas de Quentin Tarantino. Continúa bajo tu propia responsabilidad.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jacc1087/IA-Generativa/blob/main/Proyecto.ipynb) &nbsp; [**🎥 Ver demo en Streamlit →**](https://drill-blocks-reasoning-cooperative.trycloudflare.com)

---

## 🎥 Demo

**App en Streamlit:** [drill-blocks-reasoning-cooperative.trycloudflare.com](https://drill-blocks-reasoning-cooperative.trycloudflare.com)

| Base de conocimiento | System prompt | Interfaz Streamlit |
|---|---|---|
| ![Base de conocimiento](https://private-user-images.githubusercontent.com/231539012/590089631-e6d1f0e0-21f6-462a-af9e-b917851a53b7.png) | ![System prompt](https://private-user-images.githubusercontent.com/231539012/590089217-c2173e8f-f500-4204-9503-ce21e172cae5.png) | ![Streamlit](https://private-user-images.githubusercontent.com/231539012/590118593-55c7cbd3-6d20-450b-9777-ca77ed2e52e0.png) |

---

## 📑 Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Arquitectura del sistema](#-arquitectura-del-sistema)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Configuración](#-configuración)
- [Cómo funciona](#-cómo-funciona)
- [Tecnologías](#-tecnologías)
- [Autor](#-autor)

---

## 📖 Descripción general

El proyecto construye un asistente experto sobre un dominio muy concreto: **la filmografía de Quentin Tarantino**. A partir de las entradas de Wikipedia de sus 10 películas (en formato PDF), el sistema:

1. Limpia y fragmenta (*chunking*) la documentación.
2. Genera embeddings y los indexa en una base de datos vectorial.
3. Recupera los fragmentos más relevantes para cada pregunta mediante un agente.
4. Genera una respuesta contextualizada y mantiene memoria de la conversación.
5. Expone el asistente a través de una interfaz conversacional en Streamlit.

## 🏗️ Arquitectura del sistema

```
PDFs (Wikipedia)
      │
      ▼
Limpieza de texto (clean_text)
      │
      ▼
Chunking (800 palabras / 100 solapamiento)
      │
      ▼
Embeddings (Gemini embedding-001)
      │
      ▼
Base de datos vectorial (ChromaDB)
      │
      ▼
Agente LangGraph  ──►  Retriever (MMR)  ──►  Generación (Gemini 2.5 Flash Lite)
      │
      ▼
Memoria de conversación
      │
      ▼
Interfaz (Notebook / Streamlit)
```

## 📂 Estructura del repositorio

| Archivo / carpeta   | Descripción                                                              |
|----------------------|---------------------------------------------------------------------------|
| `pdfs/`             | Documentación de las películas de Tarantino extraída de Wikipedia (10 PDFs) |
| `Proyecto.ipynb`    | Notebook principal, ejecutable en Google Colab                            |
| `README.md`         | Este documento                                                             |

## 🚀 Instalación y ejecución

Este proyecto se ha desarrollado y probado en **Google Colab**, por lo que se recomienda ejecutarlo en ese mismo entorno.

1. Abre `Proyecto.ipynb` en Google Colab.
2. Sube la carpeta `pdfs/` cuando el notebook lo solicite (celda **"Subida de documentación"** → botón *"Elegir archivos"*). Son 10 documentos que cubren toda la filmografía.
3. Configura tu API Key de Gemini (ver [Configuración](#-configuración)).
4. Ejecuta las celdas en orden. La primera ejecución tarda algo más al construir la base de datos vectorial por lotes.

## ⚙️ Configuración

Todos los parámetros relevantes se definen en la celda de configuración inicial:

| Parámetro           | Valor                        | Descripción                                                                 |
|---------------------|------------------------------|------------------------------------------------------------------------------|
| `GEMINI_API_KEY`    | *(tu API key)*                | Se recomienda guardarla como secreto en Colab e insertar aquí su nombre     |
| Tamaño de chunk     | `800`                         | A menor tamaño, mayor precisión, pero se consumen antes los créditos de Gemini |
| Chunk overlap       | `100`                         | Palabras compartidas entre chunks consecutivos para mantener el contexto    |
| `K`                 | *(nº de chunks)*              | Número de fragmentos que recupera el sistema para responder cada pregunta  |
| Modelo de embedding | `embedding-001`               | Modelo de Gemini usado para generar los embeddings                          |
| Modelo LLM          | `Gemini 2.5 Flash Lite`       | También compatible con otras versiones, como Gemini 2.0                    |

## 🔍 Cómo funciona

### Creación de la base de conocimiento
Función `clean_text` para limpiar el ruido propio de los textos extraídos de Wikipedia, y `load_pdfs` para cargar cada PDF página a página y generar los chunks (800 palabras / 100 de solapamiento). El proceso indexa los embeddings en ChromaDB por lotes pequeños con pausas entre ellos, para evitar errores al indexar volúmenes grandes de una vez.

### Definición del system prompt
Se define la personalidad del agente: su formación, el tono de sus respuestas, el idioma y el formato de salida, así como el comportamiento cuando la pregunta no tiene respuesta en la base de conocimiento.

### Agente LangGraph
El agente configura un retriever con **MMR (Maximal Marginal Relevance)**, que prioriza fragmentos relevantes y no redundantes entre sí para maximizar la información disponible. El grafo define el flujo: `retrieve` (búsqueda en la base vectorial) → `generate` (generación de la respuesta con Gemini).

### Memoria de conversación
El agente mantiene el contexto entre preguntas. Se ha validado realizando una batería de 5 preguntas donde una de ellas hace referencia a una anterior, confirmando que el agente recuerda el histórico de la conversación.

### Interacción
Disponible tanto en el propio notebook (chatbot interactivo) como desplegado en **Streamlit**.

## 🛠️ Tecnologías

- **Lenguaje:** Python (Jupyter Notebook / Google Colab)
- **LLM:** Gemini 2.5 Flash Lite
- **Embeddings:** Gemini `embedding-001`
- **Base de datos vectorial:** ChromaDB
- **Orquestación del agente:** LangGraph
- **Interfaz:** Streamlit

## 👤 Autor

**José Ángel Contreras Caño**
[GitHub](https://github.com/jacc1087) · [LinkedIn](https://linkedin.com/in/jose-angel-contreras-caño-7867a193)
