__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import re
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ── Configuración ────────────────────────────────────────────────
PDF_DIR         = "pdfs"          # carpeta del repo con los documentos de Tarantino
DOC_EXTENSION   = ".txt"          # los archivos del repo están en texto plano, no en PDF
COLLECTION_NAME = "tarantino_expert"
CHUNK_SIZE      = 800
CHUNK_OVERLAP   = 100
TOP_K           = 5
EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL       = "gemini-2.5-flash-lite"

SYSTEM_PROMPT = """
Eres un asistente experto en el cine de Quentin Tarantino.

Tu conocimiento proviene EXCLUSIVAMENTE de los fragmentos de documentos que se te
proporcionan en cada consulta. Sigue estas reglas sin excepción:

1. Basa tus respuestas únicamente en los fragmentos recuperados.
   No uses conocimiento externo ni inventes información.
2. Si los fragmentos no contienen información suficiente, dilo:
   "No tengo esa información en mi base de conocimiento."
3. MEMORIA: Tienes acceso al historial de conversación. Mantén coherencia con
   respuestas anteriores y haz referencia a ellas cuando sea relevante.
4. IDIOMA: Responde siempre en español.
5. FORMATO: Usa listas y negritas cuando mejore la legibilidad.
""".strip()

# ── Página ───────────────────────────────────────────────────────
st.set_page_config(page_title="Experto en Tarantino", page_icon="🎬", layout="wide")
st.title("🎬 Experto en el cine de Quentin Tarantino")
st.caption("Asistente RAG · LangChain + Gemini + ChromaDB")

with st.expander("⚠️ Aviso de spoilers", expanded=False):
    st.write(
        "Este asistente conoce el argumento y los finales de las películas "
        "de Quentin Tarantino. Pregunta bajo tu propia responsabilidad."
    )

# ── API Key (se configura como Secret en Streamlit Cloud, nunca en el código) ──
if "GEMINI_API_KEY" not in st.secrets:
    st.error(
        "Falta configurar GEMINI_API_KEY en los Secrets de la app "
        "(Settings → Secrets en Streamlit Community Cloud)."
    )
    st.stop()

os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]


def clean_text(text: str) -> str:
    """Limpieza exhaustiva para PDFs de Wikipedia (idéntica a la del notebook)."""
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[cita requerida\]', '', text)
    text = re.sub(r'\[nota \d+\]', '', text)
    text = re.sub(
        r'^\d{1,3}\.\s+.{0,20}(Consultado|Archivado|ISBN|doi:).*$',
        '', text, flags=re.MULTILINE,
    )
    text = re.sub(r'^\s*[\d\.\-\+]+\s*$', '', text, flags=re.MULTILINE)
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 15 or l.strip() == '']
    text = '\n'.join(lines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\.{4,}', '...', text)
    return text.strip()


@st.cache_resource(show_spinner="Construyendo la base de conocimiento (solo la primera vez)...")
def load_agent():
    # 1. Cargar y limpiar los documentos del repo
    docs = []
    for fname in sorted(os.listdir(PDF_DIR)):
        if not fname.lower().endswith(DOC_EXTENSION):
            continue
        loader = TextLoader(os.path.join(PDF_DIR, fname), encoding="utf-8")
        docs.extend(loader.load())

    if not docs:
        st.error(
            f"No se ha encontrado ningún archivo {DOC_EXTENSION} dentro de la "
            f"carpeta '{PDF_DIR}/'. Revisa que los documentos estén subidos al repo."
        )
        st.stop()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
    docs = [d for d in docs if len(d.page_content.strip()) > 50]

    # 2. Chunking (mismos parámetros que en el notebook)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    if not chunks:
        st.error("Los documentos se cargaron pero no se generó ningún chunk. Revisa el contenido de los archivos.")
        st.stop()

    # 3. Embeddings + indexado en ChromaDB (en memoria del contenedor)
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        task_type="retrieval_document",
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K, "fetch_k": TOP_K * 3},
    )
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0.2,
        convert_system_message_to_human=True,
    )
    return retriever, llm, len(chunks)


retriever, llm, total_chunks = load_agent()

# ── Barra lateral ────────────────────────────────────────────────
with st.sidebar:
    st.metric("Chunks indexados", total_chunks)
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

# ── Historial de chat ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Pregunta sobre Tarantino...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos..."):
            # Fragmentos relevantes
            docs = retriever.invoke(prompt)
            context = "\n\n".join(d.page_content for d in docs)

            # Historial para dar memoria al agente
            history = []
            for m in st.session_state.messages[:-1]:
                if m["role"] == "user":
                    history.append(HumanMessage(content=m["content"]))
                else:
                    history.append(AIMessage(content=m["content"]))

            mensajes = [
                SystemMessage(content=SYSTEM_PROMPT),
                *history,
                HumanMessage(content=f"Contexto:\n{context}\n\nPregunta: {prompt}"),
            ]
            answer = llm.invoke(mensajes).content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
