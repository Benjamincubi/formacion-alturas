import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# Configuración de página
st.set_page_config(page_title="Gestor de Alturas - Formación", layout="wide")

# AUTO-RECARGA EN VIVO (Cada 3000 ms = 3 segundos) de forma limpia sin duplicar la grilla
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
            requests.patch(url_node, json={"altura": nueva_alt})
            st.success("Altura guardada.")
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

# Orden descendente por altura
presentes.sort(key=lambda x: x[2], reverse=True)

if not presentes:
    st.info("No hay personas marcadas como presentes aún.")
else:
    num_columnas = frente
    total_p = len(presentes)
    num_filas = (total_p + num_columnas - 1) // num_columnas

    # Contenedor limpio para evitar elementos en caché
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
