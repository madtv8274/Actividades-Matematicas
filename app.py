import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="MathKahoot Secundaria", page_icon="🏆", layout="wide")

# Inicializar estados de la aplicación
if "score" not in st.session_state:
    st.session_state.score = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = [
        {"Nombre": "Sofía ⭐", "Puntaje": 950},
        {"Nombre": "Mateo", "Puntaje": 800},
        {"Nombre": "Valentina", "Puntaje": 650}
    ]
if "quiz_terminado" not in st.session_state:
    st.session_state.quiz_terminado = False

st.title("🏆 MathKahoot: ¡El Desafío de Matemáticas!")
st.write("Demuestra tus habilidades matemáticas y conquista el podio.")

# BASE DE DATOS DE 10 PREGUNTAS POR GRADO
preguntas_db = {
    "1º de Secundaria": [
        {"p": "¿Cuál es el resultado de -12 + 7?", "o": ["-5", "5", "-19", "19"], "c": "-5"},
        {"p": "Si 3x = 15, ¿cuánto vale x?", "o": ["3", "5", "12", "45"], "c": "5"},
        {"p": "¿Cuál es el 20% de 150?", "o": ["15", "20", "30", "45"], "c": "30"},
        {"p": "Convierte 3/4 a número decimal:", "o": ["0.34", "0.75", "0.60", "3.4"], "c": "0.75"},
        {"p": "El resultado de (-5) × (-4) es:", "o": ["-20", "20", "-9", "9"], "c": "20"},
        {"p": "Si un pantalón cuesta $500 y tiene el 10% de descuento, ¿cuánto pagas?", "o": ["$450", "$400", "$490", "$495"], "c": "$450"},
        {"p": "¿Cuál es el perímetro de un cuadrado si uno de sus lados mide 6 cm?", "o": ["12 cm", "36 cm", "24 cm", "18 cm"], "c": "24 cm"},
        {"p": "¿Qué número falta en la serie? 2, 5, 8, __, 14", "o": ["10", "11", "12", "13"], "c": "11"},
        {"p": "Si reparto 35 dulces entre 5 niños equitativamente, ¿cuántos recibe cada uno?", "o": ["5", "6", "7", "8"], "c": "7"},
        {"p": "¿Cuál es el resultado de la operación: 4 + 5 × 2?", "o": ["18", "14", "22", "13"], "c": "14"}
    ],
    "2º de Secundaria": [
        {"p": "Resuelve: 2x + 5 = 15", "o": ["x = 5", "x = 10", "x = 7.5", "x = 2"], "c": "x = 5"},
        {"p": "¿Cuánto mide la suma de los ángulos internos de cualquier triángulo?", "o": ["90°", "180°", "360°", "270°"], "c": "180°"},
        {"p": "Calcula el volumen de un cubo cuyo lado mide 3 cm:", "o": ["9 cm³", "18 cm³", "27 cm³", "12 cm³"], "c": "27 cm³"},
        {"p": "Si 2 obreros tardan 6 días en hacer una barda, ¿cuánto tardarán 4 obreros?", "o": ["12 días", "3 días", "4 días", "8 días"], "c": "3 días"},
        {"p": "Simplifica la expresión: a⁴ × a³", "o": ["a⁷", "a¹²", "2a⁷", "a¹"], "c": "a⁷"},
        {"p": "¿Cuál es la raíz cuadrada de 144?", "o": ["12", "14", "16", "11"], "c": "12"},
        {"p": "En el sistema 2x2: x + y = 10 y x - y = 2. ¿Cuánto vale x?", "o": ["x = 5", "x = 6", "x = 4", "x = 8"], "c": "x = 6"},
        {"p": "¿Cuál es el área de un círculo con radio de 2 cm? (usa π ≈ 3.14)", "o": ["6.28 cm²", "12.56 cm²", "25.12 cm²", "4 cm²"], "c": "12.56 cm²"},
        {"p": "El resultado de (x + 3)(x + 2) es:", "o": ["x² + 5x + 6", "x² + 6", "x² + 6x + 5", "2x + 5"], "c": "x² + 5x + 6"},
        {"p": "Si lanzas un dado común, ¿cuál es la probabilidad de que salga un número par?", "o": ["1/6", "1/2", "1/3", "2/3"], "c": "1/2"}
    ],
    "3º de Secundaria": [
        {"p": "Teorema de Pitágoras: Catetos de 6 y 8 cm. ¿Cuánto mide la hipotenusa?", "o": ["10 cm", "14 cm", "100 cm", "12 cm"], "c": "10 cm"},
        {"p": "¿Cuáles son las soluciones de la ecuación cuadrática x² - 25 = 0?", "o": ["5", "-5", "5 y -5", "25"], "c": "5 y -5"},
        {"p": "En un triángulo rectángulo, el seno de un ángulo se define como:", "o": ["Cat. Opuesto / Hipotenusa", "Cat. Adyacente / Hipotenusa", "Cat. Opuesto / Cat. Adyacente", "Hipotenusa / Cat. Opuesto"], "c": "Cat. Opuesto / Hipotenusa"},
        {"p": "Si la función es y = 3x - 2, ¿cuál es la pendiente de la recta?", "o": ["3", "-2", "x", "2"], "c": "3"},
        {"p": "Aplica el Teorema de Tales: Si una línea paralela corta un triángulo, los segmentos son:", "o": ["Iguales", "Proporcionales", "Perpendiculares", "Asimétricos"], "c": "Proporcionales"},
        {"p": "¿Cuál es la solución de la ecuación (x - 3)² = 0?", "o": ["x = 3", "x = -3", "x = 9", "No tiene"], "c": "x = 3"},
        {"p": "En la ecuación cuadrática ax² + bx + c = 0, si el discriminante es 0, ¿cuántas soluciones hay?", "o": ["Dos distintas", "Una única solución", "Ninguna solución real", "Infinitas"], "c": "Una única solución"},
        {"p": "Si el área de un cuadrado es 49 cm², ¿cuánto mide su diagonal aproximadamente?", "o": ["7 cm", "9.9 cm", "14 cm", "8.5 cm"], "c": "9.9 cm"},
        {"p": "¿Cuál es el valor del ángulo inscrito que subtiende un arco de 80° en una circunferencia?", "o": ["80°", "40°", "160°", "20°"], "c": "40°"},
        {"p": "¿Cuál es la razón trigonométrica equivalente a Cateto Adyacente / Cateto Opuesto?", "o": ["Tangente", "Cotangente", "Secante", "Coseno"], "c": "Cotangente"}
    ]
}

# --- BARRA LATERAL (Leaderboard y Configuración) ---
with st.sidebar:
    st.header("👤 Registro de Jugador")
    nombre_usuario = st.text_input("Ingresa tu nombre para el podio:", value="Invitado")
    
    st.header("📊 Tabla de Posiciones")
    df_leaderboard = pd.DataFrame(st.session_state.leaderboard)
    st.table(df_leaderboard.sort_values(by="Puntaje", ascending=False))

# --- FLUJO PRINCIPAL ---
grado = st.selectbox("🎯 Elige tu Grado Escolar:", list(preguntas_db.keys()))

# Temporizador visual animado (Simulación de estrés tipo Kahoot)
progreso_tiempo = st.progress(1.0)
status_tiempo = st.empty()

# Cuenta regresiva simulada al cambiar de grado o cargar
for percent_complete in range(100, 0, -10):
    time.sleep(0.05)
    progreso_tiempo.progress(percent_complete / 100)
status_tiempo.caption("⏱️ ¡Tiempo corriendo para responder el bloque entero!")

# Formulario de envío
with st.form("quiz_form"):
    respuestas_alumno = {}
    
    for idx, item in enumerate(preguntas_db[grado]):
        st.markdown(f"#### 📝 Pregunta {idx+1}")
        st.write(item["p"])
        respuestas_alumno[idx] = st.radio(
            "Selecciona la opción correcta:", 
            item["o"], 
            key=f"ans_{grado}_{idx}"
        )
        st.write("---")
        
    enviar_respuestas = st.form_submit_form("¡Terminar Cuestionario y Enviar al Podio!")

if enviar_respuestas:
    puntaje_obtenido = 0
    for idx, item in enumerate(preguntas_db[grado]):
        if respuestas_alumno[idx] == item["c"]:
            puntaje_obtenido += 100 # 100 puntos por respuesta correcta
            
    st.session_state.score = puntaje_obtenido
    
    # Agregar a la tabla de posiciones si no se ha agregado ya
    nuevo_registro = {"Nombre": nombre_usuario, "Puntaje": puntaje_obtenido}
    st.session_state.leaderboard.append(nuevo_registro)
    
    st.balloons()
    st.success(f"🎉 ¡Felicidades {nombre_usuario}! Has terminado el bloque con **{puntaje_obtenido} puntos**.")
    st.info("Revisa la barra lateral para ver tu lugar en la Tabla de Posiciones.")
