# IA-Generativa

## Asistente experto con Gemini, RAG y agentes
> ⚠️ **ADVERTENCIA DE SPOILERS** ⚠️
> </br>
> Este notebook contiene información detallada sobre el argumento y los finales de las películas de Quentin Tarantino.
> </br>
> **Continúa bajo tu propia responsabilidad.**

#### Instrucciones de instalación y ejecución
> Este proyecto se ha desarrollado en Google Colab, por lo que se recomienda su ejecución en el mismo entorno
> </br>
> Contiene dos archivos con las siguientes funciones:
>   * Carpeta pdfs: Contiene toda la información sobre películas de Tarantino descargada de Wikipedia
>   * Proyecto.ipynb: Contiene el código del proyecto en Google Colab, es el ejecutable
> </br>
> Celda de configuración y API Key
> Contiene toda la información relevante del proyecto
> </br>
* En la variable GEMINI_API_KEY se debe insertar el nombre de la api key guardada en el secreto anteriormente.

* Tras varias pruebas se define un tamaño de chunk de 800, si se disminuye el tamaño, aumenta la precisión pero se agotan antes los créditos de Gemini, limitados para poder usar la aplicación en modo gratuito.

* chunk overlap contiene los chunks que se comparten con el anterior extracto para que se mantenga el contexto en la mayor medida posible.

* K se refiere al número de chunks que recupera el sistema para contestar a cada pregunta que se le haga.

* Se utiliza el modelo de embedding de 'embedding-001'

* Se utiliza el modelo de LLM 'Gemini 2.5 Flash Lite' aunque también funciona con otros modelos como el 2.0


#### Definición del tema experto
> 

#### Diseño del system prompt

#### Creación de la base de conocimiento

#### Agente LangGraph

#### Memoria de conversación

#### Interación en el notebook

#### Despliegue en Streamlit
