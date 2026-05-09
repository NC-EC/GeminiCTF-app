import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Ciber-Sensei | CTF Companion", page_icon="🛡️", layout="wide")

# --- BARRA LATERAL (API KEY Y MENÚ) ---
with st.sidebar:
    st.title("🛡️ Ciber-Sensei")
    st.write("Tu aliado socrático para retos CTF.")
    api_key = st.text_input("Ingresa tu Google Gemini API Key:", type="password").strip()
    
    st.divider()
    app_mode = st.radio("Selecciona una herramienta:", 
                        ["🧠 Mentor Socrático", "📝 Generador de Write-ups", "🕸️ Visualizador de Amenazas"])
    
    st.divider()
    st.caption("Creado para el Google Gemini API Challenge 🏆")

# Verifica que haya una API Key antes de continuar
if not api_key:
    st.warning("⚠️ Por favor, ingresa tu API Key de Gemini en la barra lateral para comenzar.")
    st.stop()

# Configurar el SDK
genai.configure(api_key=api_key)
# Usaremos gemini-1.5-flash por su rapidez y excelente manejo de contexto
model = genai.GenerativeModel('gemini-2.0-flash')

# --- MÓDULO 1: MENTOR SOCRÁTICO ---
if app_mode == "🧠 Mentor Socrático":
    st.header("🧠 El Mentor Socrático")
    st.write("Pega el output de tu herramienta (Nmap, Burp, etc.) o describe tu bloqueo. **No te daré la respuesta, te ayudaré a pensar.**")
    
    user_input = st.text_area("Logs o descripción del problema:", height=200)
    
    if st.button("Pedir Consejo al Sensei"):
        if user_input:
            with st.spinner("Analizando tu situación..."):
                prompt = f"""
                Eres 'Ciber-Sensei', un mentor experto en ciberseguridad y CTFs.
                REGLA ESTRICTA: NUNCA des la respuesta directa, no escribas el comando final que soluciona el reto, ni reveles la 'flag'.
                TU OBJETIVO: Analizar los datos provistos y hacer 2 o 3 preguntas socráticas que guíen al estudiante hacia la respuesta correcta por sí mismo. 
                Si ves un vector de ataque obvio, pregúntale por los conceptos detrás de ese vector.
                
                Datos del usuario:
                {user_input}
                """
                response = model.generate_content(prompt, generation_config={"temperature": 0.3})
                st.info(response.text)
        else:
            st.error("Por favor, ingresa algún texto o log.")

# --- MÓDULO 2: GENERADOR DE WRITE-UPS ---
elif app_mode == "📝 Generador de Write-ups":
    st.header("📝 Generador Automático de Write-ups")
    st.write("Pega tu historial de comandos bash o tus notas desordenadas. Yo lo convertiré en un reporte profesional.")
    
    logs_input = st.text_area("Historial de comandos o notas brutas:", height=200)
    
    if st.button("Generar Reporte Markdown"):
        if logs_input:
            with st.spinner("Redactando reporte profesional..."):
                prompt = f"""
                Eres un analista técnico de seguridad. Tu trabajo es documentar la resolución de un reto CTF.
                Toma los siguientes comandos/notas y redacta un 'Write-up' profesional en formato Markdown.
                Ignora los comandos que fallaron o son ruido (como 'ls' repetidos sin contexto).
                Estructura el documento con: 1. Resumen Ejecutivo, 2. Reconocimiento, 3. Explotación, 4. Post-Explotación (si aplica), 5. Conceptos clave aprendidos.
                
                Notas del usuario:
                {logs_input}
                """
                response = model.generate_content(prompt, generation_config={"temperature": 0.2})
                st.markdown(response.text)
                st.download_button("⬇️ Descargar Markdown", response.text, file_name="writeup.md")
        else:
            st.error("Necesito datos para generar el reporte.")

# --- MÓDULO 3: VISUALIZADOR DE AMENAZAS ---
elif app_mode == "🕸️ Visualizador de Amenazas":
    st.header("🕸️ Visualizador de Vectores de Ataque")
    st.write("Describe la red o el servicio al que te enfrentas. Generaré un diagrama Mermaid.js para que visualices la superficie de ataque.")
    
    infra_input = st.text_area("Describe la infraestructura (Ej: 'Hay un firewall que filtra el puerto 80, detrás hay un Nginx que conecta a una app Flask y una BD PostgreSQL interna'):", height=150)
    
    if st.button("Mapear Infraestructura"):
        if infra_input:
            with st.spinner("Diseñando diagrama..."):
                prompt = f"""
                Eres un arquitecto de seguridad. A partir de la siguiente descripción, genera un diagrama de flujo de datos usando código 'Mermaid.js'.
                El diagrama debe mostrar la relación entre los componentes y posibles vectores de ataque (etiquetados).
                SOLO devuelve el bloque de código Mermaid, sin texto adicional introductorio.
                
                Descripción:
                {infra_input}
                """
                response = model.generate_content(prompt, generation_config={"temperature": 0.1})
                
                # Renderizando el código de Mermaid
                mermaid_code = response.text.replace("```mermaid", "").replace("```", "").strip()
                st.components.v1.html(
                    f"""
                    <div class="mermaid">
                        {mermaid_code}
                    </div>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <script>mermaid.initialize({{startOnLoad:true}});</script>
                    """, height=500
                )
                
                with st.expander("Ver código fuente Mermaid"):
                    st.code(mermaid_code, language="mermaid")
        else:
            st.error("Por favor, describe la infraestructura.")
