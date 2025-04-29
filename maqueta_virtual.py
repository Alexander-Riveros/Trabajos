# --- Librerías necesarias ---
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# --- Configuración de la Página ---
st.set_page_config(page_title="Maqueta Virtual - Dinámica de Usuarios 🚀", page_icon="🚀", layout="wide")

# --- Estilos personalizados avanzados ---
st.markdown("""
    <style>
    /* Estilo general */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #F4F6F7;
        color: #2E4053;
    }

    /* Estilo para títulos */
    .title {
        font-size: 50px;
        font-weight: 700;
        color: #2980B9;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-size: 26px;
        color: #5D6D7E;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Estilo para los bloques */
    .block {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 40px;
        transition: transform 0.3s ease-in-out;
    }

    .block:hover {
        transform: translateY(-10px);
    }

    /* Centrado de métricas */
    .metric-box {
        text-align: center;
        background: #D5E8F3;
        border-radius: 12px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease-in-out;
    }

    .metric-box:hover {
        transform: scale(1.05);
    }

    /* Estilo para gráficos */
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #2E4053;
        padding: 10px;
        border-radius: 15px;
        background-color: #F0F3F4;
        width: 70%;  /* Reduce el tamaño de la gráfica */
        margin: 20px auto;
    }

    .chart-container img {
        max-width: 100%;  /* Hace que la gráfica se ajuste al contenedor */
        border: 1px solid #2E4053;  /* Borde negro alrededor de la gráfica */
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. Título Principal ---
st.markdown('<div class="title">Maqueta Virtual 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dinámica de Usuarios en un Sistema Web</div>', unsafe_allow_html=True)
st.write("---")

# --- 2. Parámetros de Simulación ---
with st.sidebar:
    st.header('⚙️ Configuración de Parámetros')
    U0 = st.number_input('Usuarios Iniciales (U₀)', min_value=0, value=20)
    C = st.number_input('Capacidad del Servidor (C)', min_value=1, value=10)
    llegada = st.number_input('Tasa de Llegada de Usuarios (λ)', min_value=0.0, value=5.0)
    p_abandono = st.slider('Probabilidad de Abandono (%)', 0, 100, 10) / 100
    T_respuesta = st.number_input('Tiempo de Respuesta Promedio (segundos)', min_value=1, value=5)
    Max_conexiones = st.number_input('Máximo de Conexiones Simultáneas', min_value=1, value=100)
    tiempo_simulacion = st.slider('⏳ Tiempo de Simulación (segundos)', 10, 600, 120)

# --- 3. Simulación Dinámica del Sistema ---
dt = 1
t = np.arange(0, tiempo_simulacion + dt, dt)
U = np.zeros_like(t)
procesados = np.zeros_like(t)
abandonados = np.zeros_like(t)

U[0] = U0

for i in range(1, len(t)):
    llegada_actual = llegada * dt
    capacidad_actual = min(C * dt, U[i-1])
    abandono_actual = p_abandono * (U[i-1] - capacidad_actual)

    U[i] = U[i-1] + llegada_actual - capacidad_actual - abandono_actual
    
    if U[i] > Max_conexiones:
        abandono_exceso = U[i] - Max_conexiones
        abandono_actual += abandono_exceso
        U[i] = Max_conexiones

    U[i] = max(U[i], 0)

    procesados[i] = capacidad_actual
    abandonados[i] = abandono_actual

# --- 4. Presentación de Resultados ---
st.markdown('<div class="block">', unsafe_allow_html=True)
st.subheader('📊 Resumen del Sistema')

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Usuarios Iniciales", U0)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Tasa de Llegada", f"{llegada} usuarios/seg")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("Probabilidad de Abandono", f"{p_abandono*100}%")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. Gráficas Dinámicas ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, U, label='Usuarios Activos', color='royalblue', linewidth=2)
ax.plot(t, procesados, label='Usuarios Procesados', color='seagreen', linestyle='--', linewidth=2)
ax.plot(t, abandonados, label='Usuarios que Abandonan', color='firebrick', linestyle='-.', linewidth=2)

ax.set_xlabel('Tiempo (segundos)', fontsize=12)
ax.set_ylabel('Cantidad de Usuarios', fontsize=12)
ax.set_title('Dinámica de Usuarios en el Sistema Web', fontsize=14, color='#154360')
ax.legend(loc='upper right')
ax.grid(True)
fig.tight_layout()

# Contenedor gráfico estilizado
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)
# --- 6. Información Pedagógica Final ---
with st.expander("🧠 ¿Cómo funciona este Modelo?"):
    st.write("""
    Esta maqueta utiliza un modelo simplificado de flujo de usuarios basado en tasas diferenciales:

    **Ecuación principal:**  
    `dU/dt = λ - µ - α`

    **Definiciones:**
    - `λ` = Tasa de llegada de nuevos usuarios.
    - `µ` = Tasa de procesamiento de usuarios.
    - `α` = Usuarios que abandonan el sistema.

    **Aspectos Destacados:**
    - Control de saturación de servidor.
    - Abandono proporcional a la congestión.
    - Evolución temporal gráfica de procesos simultáneos.
    """)

st.success("✅ ¡Simulación completa! Ajusta parámetros en la barra lateral para explorar diferentes escenarios.")
