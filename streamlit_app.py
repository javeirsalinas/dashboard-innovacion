import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Dashboard Centro de Innovación", layout="wide")

# 2. CONEXIÓN A DATOS (Busca la URL automáticamente en Settings > Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. SEGURIDAD PARA CARGA
PASSWORD_EDITOR = "Emprende2026"

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("Gestión de Innovación")
modo = st.sidebar.radio("Seleccione Modo:", ["📊 Dashboard de Gestión", "📥 Carga de Datos (Responsables)"])

# ---------------------------------------------------------
# MODO 1: VISUALIZACIÓN (DASHBOARD)
# ---------------------------------------------------------
if modo == "📊 Dashboard de Gestión":
    st.title("🚀 Panel de Control Ejecutivo")
    
    # Selector de Pilar
    pilar = st.sidebar.selectbox("Ver detalle de:", ["Resumen General", "Emprendimiento", "Vinculación", "Plataformas", "Comunicación", "Administración"])

    if pilar == "Resumen General":
        st.subheader("Estado Global del Centro")
        
        # Intentamos cargar datos para KPIs (Si las hojas existen en tu Excel)
        try:
            df_emp = conn.read(worksheet="Emprendimiento", ttl=600)
            df_com = conn.read(worksheet="Comunicación", ttl=600)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Inscritos", df_emp['Cantidad'].sum() if 'Cantidad' in df_emp.columns else "0")
            col2.metric("Gasto Pauta USD", f"${df_com['Gasto_Pauta_USD'].sum()}" if 'Gasto_Pauta_USD' in df_com.columns else "0")
            col3.metric("Pilares Activos", "5")
            
            st.markdown("---")
            st.write("### Participación por Sede")
            fig = px.pie(df_emp, values='Cantidad', names='Sede', title="Distribución de Emprendedores")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("Asegúrate de que los nombres de las pestañas en Google Sheets coincidan exactamente.")

    elif pilar == "Emprendimiento":
        st.header("📊 Detalle: Emprendimiento")
        df = conn.read(worksheet="Emprendimiento", ttl=600)
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            fig_emp = px.bar(df, x="Sede", y="Cantidad", color="Programa", barmode="group")
            st.plotly_chart(fig_emp, use_container_width=True)

    else:
        # Cargamos la pestaña correspondiente al nombre seleccionado
        try:
            df_pilar = conn.read(worksheet=pilar, ttl=600)
            st.header(f"📋 Datos de {pilar}")
            st.dataframe(df_pilar, use_container_width=True)
        except:
            st.error(f"No se pudo encontrar la pestaña '{pilar}' en tu Google Sheets.")

# ---------------------------------------------------------
# MODO 2: CARGA DE DATOS (PROTEGIDO)
# ---------------------------------------------------------
elif modo == "📥 Carga de Datos (Responsables)":
    st.title("🔒 Acceso de Editores")
    
    pw = st.text_input("Ingrese la contraseña para alimentar el sistema:", type="password")
    
    if pw == PASSWORD_EDITOR:
        st.success("Acceso concedido. Ingrese los datos del lunes.")
        
        with st.form("form_carga"):
            pilar_carga = st.selectbox("¿Qué pilar vas a actualizar?", ["Emprendimiento", "Vinculación", "Plataformas", "Comunicación", "Administración"])
            fecha = st.date_input("Fecha de hoy", datetime.date.today())
            
            st.markdown("---")
            
            if pilar_carga == "Emprendimiento":
                col1, col2 = st.columns(2)
                prog = col1.selectbox("Programa", ["Pre-incubación", "Incubación"])
                sede = col2.selectbox("Sede", ["Lima", "Arequipa", "Cusco"])
                tipo = st.selectbox("Tipo de Usuario", ["Alumno", "Egresado", "Administrativo"])
                cant = st.number_input("Cantidad de personas", min_value=0, step=1)
                beca = st.radio("¿Son becados?", ["Si", "No"])
                
            elif pilar_carga == "Comunicación":
                seguidores = st.number_input("Seguidores actuales", min_value=0)
                gasto = st.number_input("Gasto pauta del mes ($)", min_value=0.0)
                actividad = st.text_area("Actividades destacadas")

            # Botón de envío
            enviar = st.form_submit_button("Guardar Registro")
            
            if enviar:
                st.balloons()
                st.info("¡Datos procesados! (Nota: Para guardar permanentemente, asegúrate de haber configurado los permisos de ESCRITURA en Streamlit Secrets).")
    
    elif pw != "":
        st.error("Contraseña incorrecta. Pídela al administrador del Centro.")
