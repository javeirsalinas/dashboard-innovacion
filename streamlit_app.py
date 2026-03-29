import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Dashboard Centro de Innovación", layout="wide")

# 2. CONEXIÓN A DATOS (Google Sheets)
# Reemplaza con tu URL real en el Secrets de Streamlit o aquí
URL_SHEET = "https://docs.google.com/spreadsheets/d/10mc_pk6QHWwia1njPo6uftI7eleHGZmdhgUW6yvJZ20/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. SEGURIDAD
PASSWORD_EDITOR = "Emprende2026"

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/606/606112.png", width=100)
st.sidebar.title("Gestión de Innovación")
modo = st.sidebar.radio("Ir a:", ["📊 Visualización General", "📥 Carga de Datos (Lunes)"])

# ---------------------------------------------------------
# MODO 1: VISUALIZACIÓN (DASHBOARD)
# ---------------------------------------------------------
if modo == "📊 Visualización General":
    st.title("🏛️ Panel de Control Ejecutivo")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["General", "Emprendimiento", "Vinculación", "Plataformas", "Comunicación"])

    with tab1:
        st.subheader("Resumen de Impacto")
        # Aquí cargaríamos datos de todas las hojas para KPIs globales
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Inscritos", "150", "+5%")
        col2.metric("Aliados Activos", "12")
        col3.metric("Seguidores Totales", "25,400")
        
        # Ejemplo de gráfico de barras global
        st.markdown("---")
        st.write("Distribución de actividad por Sedes")
        # Simulación de data para el gráfico
        data_mock = pd.DataFrame({"Sede": ["Lima", "Arequipa", "Cusco"], "Actividad": [45, 30, 25]})
        fig = px.bar(data_mock, x="Sede", y="Actividad", color="Sede")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("🚀 Pilar: Emprendimiento")
        df_emp = conn.read(spreadsheet=URL_SHEET, worksheet="Emprendimiento", ttl=600)
        st.dataframe(df_emp, use_container_width=True)

# ---------------------------------------------------------
# MODO 2: CARGA DE DATOS (PROTEGIDO)
# ---------------------------------------------------------
elif modo == "📥 Carga de Datos (Lunes)":
    st.title("🔒 Acceso de Responsables")
    
    pw = st.text_input("Ingrese la contraseña para editar:", type="password")
    
    if pw == PASSWORD_EDITOR:
        st.success("Acceso autorizado. Complete los campos de su pilar.")
        
        with st.form("form_carga"):
            pilar = st.selectbox("¿Qué pilar vas a alimentar?", 
                                ["Emprendimiento", "Vinculación", "Plataformas", "Comunicación", "Administración"])
            
            fecha = st.date_input("Fecha de registro", datetime.date.today())
            
            # CAMPOS DINÁMICOS
            if pilar == "Emprendimiento":
                prog = st.selectbox("Programa", ["Pre-incubación", "Incubación"])
                cant = st.number_input("Cantidad de nuevos inscritos", min_value=0)
                sede = st.selectbox("Sede", ["Lima", "Arequipa", "Cusco"])
                
            elif pilar == "Comunicación":
                seg = st.number_input("Nuevos seguidores", min_value=0)
                pauta = st.number_input("Gasto pauta USD", min_value=0.0)
                desc = st.text_area("Hito o actividad del mes")

            enviar = st.form_submit_button("Guardar en la Base de Datos")
            
            if enviar:
                # Lógica para escribir en Google Sheets
                # Nota: st-gsheets-connection requiere configuración de escritura
                st.info("Simulación: Datos enviados a la nube correctamente.")
                st.balloons()
    
    elif pw != "":
        st.error("Contraseña incorrecta.")
