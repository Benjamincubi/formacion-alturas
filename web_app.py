import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuración de página
st.set_page_config(page_title="Gestor de Alturas - Formación", layout="wide")

# Auto-recarga automática cada 3 segundos
st_autorefresh(interval=3000, limit=None, key="formacion_autorefresh")

FIREBASE_URL = "https://formacion-cupro-alfa-default-rtdb.firebaseio.com/personas.json"

DATOS_INICIALES = {
    "01": {"nombre": "OP Lopez Federico", "altura": 1.75, "presente": False, "novedad": ""},
    "02": {"nombre": "OP Fernandez Octavio", "altura": 1.85, "presente": False, "novedad": ""},
    "03": {"nombre": "OP Cassol Santiago", "altura": 1.73, "presente": False, "novedad": ""},
    "04": {"nombre": "OP Nuñez Claudio", "altura": 1.70, "presente": False, "novedad": ""},
    "05": {"nombre": "OP Oribe Maria Pia", "altura": 1.57, "presente": False, "novedad": ""},
    "06": {"nombre": "OP Brunel Julieta", "altura": 1.74, "presente": False, "novedad": ""},
    "07": {"nombre": "OP Merino Daiana", "altura": 1.65, "presente": False, "novedad": ""},
    "08": {"nombre": "OP Gimenez Lorena", "altura": 1.67, "presente": False, "novedad": ""},
    "09": {"nombre": "OP Diaz Varsi Maria", "altura": 1.54, "presente": False, "novedad": ""},
    "10": {"nombre": "OP Medina Maria", "altura": 1.50, "presente": False, "novedad": ""},
    "11": {"nombre": "OP Andrade Florencia", "altura": 1.63, "presente": False, "novedad": ""},
    "12": {"nombre": "OP Ramos Agñel", "altura": 1.56, "presente": False, "novedad": ""},
    "13": {"nombre": "OP Sanchez Paula", "altura": 1.67, "presente": False, "novedad": ""},
    "14": {"nombre": "OP Toledo Emilia", "altura": 1.58, "presente": False, "novedad": ""},
    "15": {"nombre": "OP Neira Rocio", "altura": 1.65, "presente": False, "novedad": ""},
    "16": {"nombre": "OP Aguero Luciana", "altura": 1.58, "presente": False, "novedad": ""},
    "17": {"nombre": "OP Arias Ariel", "altura": 1.67, "presente": False, "novedad": ""},
    "18": {"nombre": "OP Pereyra Herrera Micaela", "altura": 1.56, "presente": False, "novedad": ""},
    "19": {"nombre": "OP Iglesias Exequiel", "altura": 1.80, "presente": False, "novedad": ""},
    "20": {"nombre": "OP Mars Ivana", "altura": 1.70, "presente": False, "novedad": ""},
    "21": {"nombre": "OP Escalante Maria Celeste", "altura": 1.67, "presente": False, "novedad": ""},
    "22": {"nombre": "OP Michaluk Martina", "altura": 1.65, "presente": False, "novedad": ""},
    "23": {"nombre": "OP Gonzalez Agustina", "altura": 1.62, "presente": False, "novedad": ""},
    "24": {"nombre": "OP Otero Verónica", "altura": 1.57, "presente": False, "novedad": ""},
    "25": {"nombre": "OP Fernández Ruben", "altura": 1.75, "presente": False, "novedad": ""},
    "26": {"nombre": "OP Signorio Belen", "altura": 1.60, "presente": False, "novedad": ""},
    "27": {"nombre": "OP Pereira Paola", "altura": 1.68, "presente": False, "novedad": ""},
    "28": {"nombre": "OP Luft Melina", "altura": 1.60, "presente": False, "novedad": ""},
    "29": {"nombre": "OP Peloso Santiago", "altura": 1.80, "presente": False, "novedad": ""},
    "30": {"nombre": "OP Meli Carolina", "altura": 1.60, "presente": False, "novedad": ""},
    "31": {"nombre": "OP Brizuela Karen", "altura": 1.57, "presente": False, "novedad": ""},
    "32": {"nombre": "OP Acuña Diego", "altura": 1.76, "presente": False, "novedad": ""},
    "33": {"nombre": "OP Flores Federico", "altura": 1.60, "presente": False, "novedad": ""},
    "34": {"nombre": "OP Cubi Benjamin", "altura": 1.70, "presente": False, "novedad": ""},
    "35": {"nombre": "OP Capella Tomas", "altura": 1.68, "presente": False, "novedad": ""},
    "36": {"nombre": "OP Soto Lucia", "altura": 1.66, "presente": False, "novedad": ""}
}

CRONOGRAMA_ENCARGADOS = [
    {"fecha": "14/07/2026", "encargada": "OP María Pia ORIBE", "encargado": "OP Claudio NUÑEZ"},
    {"fecha": "04/08/2026", "encargada": "OP Daiana Elizabeth MERINO", "encargado": "OP Tomas CAPELLA"},
    {"fecha": "18/08/2026", "encargada": "OP Florencia ANDRADE", "encargado": "OP Federico LÓPEZ"},
    {"fecha": "25/08/2026", "encargada": "OP María Belén SIGNORIO", "encargado": "OP Rubén FERNÁNDEZ"},
    {"fecha": "01/09/2026", "encargada": "OP Luciana AGÜERO", "encargado": "OP Federico FLORES"},
    {"fecha": "08/09/2026", "encargada": "OP Micaela PEREYRA HERRERA", "encargado": "OP Diego Nicolas ACUÑA"},
    {"fecha": "15/09/2026", "encargada": "OP Ivana Nazarena MARS", "encargado": "OP Benjamin CUBI"},
    {"fecha": "22/09/2026", "encargada": "OP Agñel RAMOS", "encargado": "OP Octavio FERNÁNDEZ"},
    {"fecha": "29/09/2026", "encargada": "OP María DIAZ VARSI", "encargado": "OP Santiago PELOSO"},
    {"fecha": "06/10/2026", "encargada": "OP Martina Belen MICHALUK", "encargado": "OP Exequiel IGLESIAS"},
    {"fecha": "13/10/2026", "encargada": "OP Rocio NEIRA", "encargado": "OP Claudio NUÑEZ"},
    {"fecha": "20/10/2026", "encargada": "OP Maria Celeste ESCALANTE", "encargado": "OP Tomas CAPELLA"},
    {"fecha": "27/10/2026", "encargada": "OP Paula Vanesa SANCHEZ", "encargado": "OP Federico LÓPEZ"},
    {"fecha": "03/11/2026", "encargada": "OP Melina Gisel LUFT", "encargado": "OP Rubén FERNÁNDEZ"},
    {"fecha": "10/11/2026", "encargada": "OP Lorena N. GIMENEZ BAUTISTA", "encargado": "OP Federico FLORES"},
    {"fecha": "17/11/2026", "encargada": "OP Emilia Alejandra TOLEDO", "encargado": "OP Diego Nicolas ACUÑA"},
    {"fecha": "24/11/2026", "encargada": "OP Carolina A. MELI", "encargado": "OP Benjamin CUBI"},
    {"fecha": "02/03/2027", "encargada": "OP Agustina Gisele GONZALEZ", "encargado": "OP Octavio FERNÁNDEZ"},
    {"fecha": "09/03/2027", "encargada": "OP Paola Margarita PEREIRA", "encargado": "OP Ucedo Ariel ARIAS"},
    {"fecha": "16/03/2027", "encargada": "OP Verónica Ayelén OTERO", "encargado": "OP Santiago PELOSO"},
    {"fecha": "23/03/2027", "encargada": "OP Karen BRIZUELA", "encargado": "OP Diego Nicolas ACUÑA"},
    {"fecha": "30/03/2027", "encargada": "OP Maria Isabel MEDINA", "encargado": "OP Santiago CASSOL"},
    {"fecha": "06/04/2027", "encargada": "OP Lucia SOTO", "encargado": "OP Ucedo Ariel ARIAS"},
    {"fecha": "13/04/2027", "encargada": "OP María Pia ORIBE", "encargado": "OP Claudio NUÑEZ"},
    {"fecha": "20/04/2027", "encargada": "OP Julieta Brunel", "encargado": "OP Tomas CAPELLA"},
    {"fecha": "27/04/2027", "encargada": "OP Daiana Elizabeth MERINO", "encargado": "OP Santiago CASSOL"},
    {"fecha": "04/05/2027", "encargada": "OP Florencia ANDRADE", "encargado": "OP Federico LÓPEZ"},
    {"fecha": "11/05/2027", "encargada": "OP María Belén SIGNORIO", "encargado": "OP Rubén FERNÁNDEZ"},
    {"fecha": "18/05/2027", "encargada": "OP Luciana AGÜERO", "encargado": "OP Federico FLORES"},
    {"fecha": "01/06/2027", "encargada": "OP Micaela PEREYRA HERRERA", "encargado": "OP Exequiel IGLESIAS"},
    {"fecha": "08/06/2027", "encargada": "OP Ivana Nazarena MARS", "encargado": "OP Benjamin CUBI"},
    {"fecha": "15/06/2027", "encargada": "OP Agñel RAMOS", "encargado": "OP Octavio FERNÁNDEZ"},
    {"fecha": "22/06/2027", "encargada": "OP María DIAZ VARSI", "encargado": "OP Santiago PELOSO"},
    {"fecha": "29/06/2027", "encargada": "OP Martina Belen MICHALUK", "encargado": "OP Exequiel IGLESIAS"},
    {"fecha": "06/07/2027", "encargada": "OP Rocio NEIRA", "encargado": "OP Santiago CASSOL"},
    {"fecha": "13/07/2027", "encargada": "OP María Pia ORIBE", "encargado": "OP Ucedo Ariel ARIAS"},
    {"fecha": "20/07/2027", "encargada": "OP Daiana Elizabeth MERINO", "encargado": "OP Claudio NUÑEZ"}
]

def obtener_datos():
    try:
        res = requests.get(FIREBASE_URL, timeout=3)
        data = res.json()
        if not data:
            requests.put(FIREBASE_URL, json=DATOS_INICIALES)
            return DATOS_INICIALES
        return data
    except Exception:
        return {}

def obtener_encargados_actuales():
    hoy = datetime.now().date()
    encargado_vigente = CRONOGRAMA_ENCARGADOS[0]
    
    for item in CRONOGRAMA_ENCARGADOS:
        fecha_dt = datetime.strptime(item["fecha"], "%d/%m/%Y").date()
        if fecha_dt <= hoy:
            encargado_vigente = item
        else:
            break
            
    return encargado_vigente

personas_db = obtener_datos()

st.title("🔴 Gestor de Alturas - Formación")

# --- RESUMEN DE PRESENTES Y AUSENTES ---
total_efectivos = len(personas_db)
presentes_list = [v for v in personas_db.values() if v.get("presente", False)]
ausentes_list = [v for v in personas_db.values() if not v.get("presente", False)]

cant_presentes = len(presentes_list)
cant_ausentes = len(ausentes_list)

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Personal", total_efectivos)
col_m2.metric("Presentes", cant_presentes)
col_m3.metric("Ausentes", cant_ausentes)

st.divider()

# --- SECCIÓN: ENCARGADOS DE SEMANA (Ubicado por arriba de "Mi Estado") ---
encargados_hoy = obtener_encargados_actuales()

st.subheader("⭐ Encargados de Turno / Formación")

st.markdown(
    f"""
    <div style="
        background-color: #1E88E5;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    ">
        📅 Semana / Martes: {encargados_hoy['fecha']}<br>
        👩‍✈️ Encargada: <span style="color: #FFEB3B;">{encargados_hoy['encargada']}</span><br>
        👨‍✈️ Encargado: <span style="color: #FFEB3B;">{encargados_hoy['encargado']}</span>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("📅 Ver Cronograma Completo de Encargados"):
    st.dataframe(CRONOGRAMA_ENCARGADOS, use_container_width=True)

st.divider()

# --- PANEL DE CONTROL INDIVIDUAL ---
st.subheader("👤 Mi Estado")
nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
mi_nombre = st.selectbox("Seleccioná tu Nombre:", ["-- Seleccionar --"] + nombres)

if mi_nombre != "-- Seleccionar --":
    pid = [k for k, v in personas_db.items() if v["nombre"] == mi_nombre][0]
    pdata = personas_db[pid]

    col_a, col_b = st.columns(2)
    with col_a:
        es_presente = st.checkbox("Dar Presente", value=pdata.get("presente", False))
        if es_presente != pdata.get("presente", False):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"presente": es_presente})
            st.rerun()

    with col_b:
        nueva_alt = st.number_input("Mi Altura (m):", min_value=1.0, max_value=2.5, value=float(pdata["altura"]), step=0.01)
        if st.button("Guardar Altura"):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            # Actualiza tanto la base de datos como los registros en tiempo real
            requests.patch(url_node, json={"altura": nueva_alt})
            st.success("Altura guardada correctamente en la base de datos.")
            st.rerun()

st.divider()

# --- VISTA EN GRILLA (ORDENADA DE MAYOR A MENOR DERECHA A IZQUIERDA) ---
st.subheader("📐 Formación en Vivo")
frente = st.slider("Frente (Columnas):", min_value=1, max_value=12, value=6)

presentes = [
    (pid, p["nombre"], p["altura"])
    for pid, p in personas_db.items()
    if p.get("presente", False)
]

presentes.sort(key=lambda x: x[2], reverse=True)

if not presentes:
    st.info("No hay personas marcadas como presentes aún.")
else:
    num_columnas = frente
    total_p = len(presentes)
    num_filas = (total_p + num_columnas - 1) // num_columnas

    grilla_container = st.container()

    with grilla_container:
        for fila in range(num_filas):
            cols = st.columns(num_columnas)
            for col_index in range(num_columnas):
                idx = fila * num_columnas + col_index
                col_invertida = (num_columnas - 1) - col_index
                
                if idx < total_p:
                    posicion = idx + 1
                    _, nombre, altura = presentes[idx]
                    nombre_limpio = nombre.replace("OP ", "")
                    
                    with cols[col_invertida]:
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #E53935;
                                color: white;
                                border-radius: 50%;
                                width: 85px;
                                height: 85px;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                text-align: center;
                                font-size: 11px;
                                font-weight: bold;
                                margin: 5px auto;
                                box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
                            ">
                                <div>({posicion})</div>
                                <div>{nombre_limpio}</div>
                                <div>{altura:.2f}m</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

st.divider()

# --- NOVEDADES / JUSTIFICACIÓN DE AUSENTES ---
st.subheader("📋 Registro de Novedades (Ausentes)")

nombres_ausentes = [v["nombre"] for k, v in sorted(personas_db.items()) if not v.get("presente", False)]

if nombres_ausentes:
    col_aus1, col_aus2 = st.columns([1, 2])
    with col_aus1:
        ausente_sel = st.selectbox("Seleccionar Ausente:", ["-- Seleccionar --"] + nombres_ausentes)
    
    if ausente_sel != "-- Seleccionar --":
        pid_aus = [k for k, v in personas_db.items() if v["nombre"] == ausente_sel][0]
        nov_actual = personas_db[pid_aus].get("novedad", "")
        
        with col_aus2:
            nueva_nov = st.text_input("Motivo de ausencia / Novedad:", value=nov_actual, placeholder="Ej: Licencia médica, Servicio, Guardia...")
            if st.button("Guardar Novedad"):
                url_node = FIREBASE_URL.replace(".json", f"/{pid_aus}.json")
                requests.patch(url_node, json={"novedad": nueva_nov})
                st.success("Novedad guardada.")
                st.rerun()

    st.markdown("**Detalle de ausencias registradas:**")
    ausencias_con_motivo = [
        {"Nombre": v["nombre"], "Motivo / Novedad": v.get("novedad", "Sin registrar")}
        for v in personas_db.values() if not v.get("presente", False)
    ]
    st.dataframe(ausencias_con_motivo, use_container_width=True)
else:
    st.success("¡Personal completo! No hay ausentes.")

st.divider()

# --- ACCIONES GLOBALES PROTEGIDAS ---
with st.expander("⚙️ Acciones Globales (Reinicio de Formación / Carga Masiva)"):
    st.warning("⚠️ Cuidado: Estas opciones modifican el estado de TODO el personal.")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ Marcar a TODOS como Presentes"):
            datos_actualizados = {k: {**v, "presente": True} for k, v in personas_db.items()}
            requests.put(FIREBASE_URL, json=datos_actualizados)
            st.success("Se marcaron todos como presentes.")
            st.rerun()
            
    with col_btn2:
        if st.button("❌ REINICIAR: Marcar a TODOS como Ausentes"):
            datos_actualizados = {k: {**v, "presente": False, "novedad": ""} for k, v in personas_db.items()}
            requests.put(FIREBASE_URL, json=datos_actualizados)
            st.warning("Se reinició la lista. Todos marcados como ausentes.")
            st.rerun()
