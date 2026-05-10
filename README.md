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
> Contiene toda la información relevante del proyecto </br>
>
>    * En la variable GEMINI_API_KEY se debe insertar el nombre de la api key guardada en el secreto anteriormente.
>      
>    * Tras varias pruebas se define un tamaño de chunk de 800, si se disminuye el tamaño, aumenta la precisión pero se agotan antes los créditos de Gemini, limitados para poder usar la aplicación en modo gratuito.
>      
>    * chunk overlap contiene los chunks que se comparten con el anterior extracto para que se mantenga el contexto en la mayor medida posible.
>      
>    * K se refiere al número de chunks que recupera el sistema para contestar a cada pregunta que se le haga.
>      
>    * Se utiliza el modelo de embedding de 'embedding-001'.
>      
>    * Se utiliza el modelo de LLM 'Gemini 2.5 Flash Lite' aunque también funciona con otros modelos como el 2.0
</br>

####  Definición del tema experto
> El tema sobre el que trata el proyecto es la filmografía del director de cine Quentin Tarantino. Se han extraído todas las entradas de wikipedia de sus películas, para que se puedan encontrar datos de argumento, reparto, anécdotas, etc.
> Al ejecutar la celda de 'Subida de documentación' se activa un botón llamado 'Elegir archivos', que nos permite subir todos los archivos que están dentro de la carpeta pdfs incluida en el proyecto. En total se trata de 10 documentos pdf, que engloban toda su filmografía.

#### Creación de la base de conocimiento
> Función de limpieza exhaustiva de los pdfs (clean_text), que al ser obtenidos de wikipedia tenían bastante ruido.
> Función load_pdfs, carga todos los pdfs de la carpeta página a página y crea los chunking de 800 palabras con 100 de solapamiento, como hemos predefinido en la celda de configuración.
> Devuelve por pantalla las páginas de cada pdf, y el total de chunks obtenidos.
> Carga de documentos en ChromaDB con Gemini Embeddings, los embeddings son vectores obtenidos de los chunks generados anteriormente, una vez obtenidos los embeddings, se crea la base de datos vectorial en ChromaDB.
> Para la creación de la base de conocimiento se hace en fragmentos pequeños y con pausas de tiempo entre uno y otro, para evitar que aparezca un error que me aparecía si queria indexar elementos demasiado grandes de golpe, por eso es un proceso algo más lento en comparación con los demás.
<img width="714" height="493" alt="Captura de pantalla 2026-05-10 a las 12 44 10" src="https://github.com/user-attachments/assets/e6d1f0e0-21f6-462a-af9e-b917851a53b7" />

#### Definición del system prompt
> Una vez creada la base de datos vectorial en ChromaDB, se genera un system prompt para dar personalidad al agente, para definir como tiene que ser el agente, la foramción que debe tener, cómo deben ser sus respuestas, idioma y formato. Y lo que tiene que decir en caso de que no encuentre la respuesta en la base de conocimiento que hemos creado anteriormente.
> <img width="725" height="370" alt="Captura de pantalla 2026-05-10 a las 12 39 37" src="https://github.com/user-attachments/assets/c2173e8f-f500-4204-9503-ce21e172cae5" />


#### Agente LangGraph
> El agente se encarga de congufirar el buscador con mmr (Maximal Marginal Relevance), con lo que se consigue encontrar el chunk que más se parezca a lo que busca la pregunta, buscando siempre que los chunks no sean repetitivos entre sí para sacar la máximo información posible para preparar la respuesta de la pregunta solicitada por el usuario.
> Monta el grafo que define el flujo a seguir por el agente, con retrieve busca en la base de datos vectorial los chunks relevantes y con generate, se genera la respuesta con Gemini

#### Memoria de conversación
> Esta celda es la que da memoria al chatbot, sin ella, cada pregunta del usuario sería independiente y el agente no recordaría nada de lo dicho anteriormente.
> Para probar que la memoria funciona, se hacen una serie de preguntas (5 concretamente) y una de ellas se pregunta algo relacionado con otra pregunta hecha anteriormente, la respuesta que se obtiene, muestra que el agente tenía conocimiento de que esta pregunta o alguna relacionada se había hecho anteriormente.

#### Interación en el notebook
> Implementación de un chatbot en el que el usuario inserta la pregunra que quiere resolver, y el agente devuelve la información solicitada si es que la tiene, en caso de preguntarle algo extraño que no tenga en la base de datos, contesta que no tiene esa información solicitada y que por tanto no puede responder a la pregunta en cuestión.

#### Despliegue en Streamlit
> Aplicación desplegada en streamlit que incluye un chatbot parecido al del ejercicio anterior, que contesta lo que deseemos sobre las películas de la filmografía de Quentin Tarantino.
> Este es el enlace que lleva a la aplicación en streamlit 
https://drill-blocks-reasoning-cooperative.trycloudflare.com
> Y, a continuación, unos ejemplos para probar el agente y el conocimiento específico adquirido
<img width="1328" height="540" alt="Captura de pantalla 2026-05-10 a las 18 00 12" src="https://github.com/user-attachments/assets/55c7cbd3-6d20-450b-9777-ca77ed2e52e0" />


