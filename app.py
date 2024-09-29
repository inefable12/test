import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Función para agregar datos a Google Sheets
def add_data_to_gsheet(data):
    # Definir el alcance
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # Obtener credenciales de Streamlit Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    # Autenticar con las credenciales
    client = gspread.authorize(creds)
    # Abrir la hoja de cálculo
    sheet = client.open('Resultados Examen').sheet1  # Reemplaza con el nombre de tu hoja
    # Agregar los datos
    sheet.append_row(data)

# Título de la aplicación
st.title("Examen en Línea")

# Inicializar el estado de la sesión
if 'started' not in st.session_state:
    st.session_state.started = False

# Botón para iniciar el examen
if not st.session_state.started:
    if st.button("Iniciar Examen"):
        st.session_state.started = True

# Si el examen ha comenzado
if st.session_state.started:
    # Campos para nombre y palabra clave
    nombre = st.text_input("Nombre Completo")
    identificador = st.text_input("Palabra Clave (Proporcionada por el Profesor)")

    # Verificar que ambos campos estén llenos
    if nombre and identificador:
        st.write("Responde las siguientes preguntas:")

        # Lista de preguntas y opciones
        preguntas = [
            "1. ¿Cuál es la capital de Francia?",
            "2. ¿Cuál es el número atómico del Helio?",
            "3. ¿Quién escribió 'Don Quijote'?",
            "4. ¿Cuál es la fórmula del agua?"
        ]

        opciones = [
            ['A) Berlín', 'B) Madrid', 'C) París', 'D) Roma', 'E) Londres'],
            ['A) 1', 'B) 2', 'C) 3', 'D) 4', 'E) 5'],
            ['A) Lope de Vega', 'B) Miguel de Cervantes', 'C) Gabriel García Márquez', 'D) Mario Vargas Llosa', 'E) William Shakespeare'],
            ['A) CO2', 'B) H2O', 'C) O2', 'D) CH4', 'E) NH3']
        ]

        respuestas = []

        # Mostrar las preguntas y opciones
        for i, pregunta in enumerate(preguntas):
            respuesta = st.radio(pregunta, opciones[i], key=f"pregunta_{i+1}")
            respuestas.append(respuesta.split(')')[0])  # Obtener solo la letra de la opción

        # Botón para enviar las respuestas
        if st.button("ENVIAR"):
            # Datos a agregar
            data_to_append = [nombre, identificador] + respuestas
            # Agregar datos a Google Sheets
            add_data_to_gsheet(data_to_append)
            # Mensaje de éxito
            st.success("Respuestas enviadas correctamente.")
            # Reiniciar el examen
            st.session_state.started = False
