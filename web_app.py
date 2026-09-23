import streamlit as st
import requests

# Configuración de página adaptable
st.set_page_config(page_title="Gestor de Alturas", layout="wide")

FIREBASE_URL = "https://formacion-cupro-alfa-default-rtdb.firebaseio.com/personas.json"

DATOS_INICIALES = {
    "01": {"nombre": "OP Lopez Federico", "altura": 1.75, "presente": False},
    "02": {"nombre": "OP Fernandez Octavio", "altura": 1.85, "presente": False},
    "03": {"nombre": "OP Cassol Santiago", "altura": 1.73, "presente": False},
    "04": {"nombre": "OP Nuñez Claudio", "altura": 1.70, "presente": False},
    "05": {"nombre": "OP Oribe Maria Pia", "altura": 1.57, "presente": False},
    "06": {"nombre": "OP Brunel Julieta", "altura": 1.74, "presente": False},
    "07": {"nombre": "OP Merino Daiana", "altura": 1.65, "presente": False},
    "08": {"nombre": "OP Gimenez Lorena", "altura": 1.67, "presente": False},
    "09": {"nombre": "OP Diaz Varsi Maria", "altura": 1.54, "presente": False},
    "10": {"nombre": "OP Medina Maria", "altura": 1.50, "presente": False},
    "11": {"nombre": "OP Andrade Florencia", "altura": 1.63, "presente": False},
    "12": {"nombre": "OP Ramos Agñel", "altura": 1.56, "presente": False},
    "13": {"nombre": "OP Sanchez Paula", "altura": 1.67, "presente": False},
    "14": {"nombre": "OP Toledo Emilia", "altura": 1.58, "presente": False},
    "15": {"nombre": "OP Neira Rocio", "altura": 1.65, "presente": False},
    "16": {"nombre": "OP Aguero Luciana", "altura": 1.58, "presente": False},
    "17": {"nombre": "OP Arias Ariel", "altura": 1.67, "presente": False},
    "18": {"nombre": "OP Pereyra Herrera Micaela", "altura": 1.56, "presente": False},
    "19": {"nombre": "OP Iglesias Exequiel", "altura": 1.80, "presente": False},
    "20": {"nombre": "OP Mars Ivana", "altura": 1.70, "presente": False},
    "21": {"nombre": "OP Escalante Maria Celeste", "altura": 1.67, "presente": False},
    "22": {"nombre": "OP Michaluk Martina", "altura": 1.65, "presente": False},
    "23": {"nombre": "OP Gonzalez Agustina", "altura": 1.62, "presente": False},
    "24": {"nombre": "OP Otero Verónica", "altura": 1.57, "presente": False},
    "25": {"nombre": "OP Fernández Ruben", "altura": 1.75, "presente": False},
    "26": {"nombre": "OP Signorio Belen", "altura": 1.60, "presente": False},
    "27": {"nombre": "OP Pereira Paola", "altura": 1.68, "presente": False},
    "28": {"nombre": "OP Luft Melina", "altura": 1.60, "presente": False},
    "29": {"nombre": "OP Peloso Santiago", "altura": 1.80, "presente": False},
    "30": {"nombre": "OP Meli Carolina", "altura": 1.60, "presente": False},
    "31": {"nombre": "OP Brizuela Karen", "altura": 1.57, "presente": False},
    "32": {"nombre": "OP Acuña Diego", "altura": 1.76, "presente": False},
    "33": {"nombre": "OP Flores Federico", "altura": 1.60, "presente": False},
    "34": {"nombre": "OP Cubi Benjamin", "altura": 1.70, "presente": False},
    "35": {"nombre": "OP Capella Tomas", "altura": 1.68, "presente": False},
    "36": {"nombre": "OP Soto Lucia", "altura": 1.66, "presente": False}
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

# --- PANEL DE CONTROL ---
st.subheader("Mi Estado")
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
        if st.button("Actualizar Altura"):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"altura": nueva_alt})
            st.success("Altura guardada.")
            st.rerun()

st.divider()

# --- VISTA EN GRILLA ---
st.subheader("Formación de Presentes")
frente = st.slider("Frente (Columnas):", min_value=1, max_value=12, value=6)

if st.button("🔄 Actualizar Formación"):
    st.rerun()

presentes = [
    (pid, p["nombre"], p["altura"])
    for pid, p in personas_db.items()
    if p.get("presente", False)
]

# Orden descendente (más alto primero)
presentes.sort(key=lambda x: x[2], reverse=True)

if not presentes:
    st.info("No hay personas marcadas como presentes aún.")
else:
    num_columnas = frente
    total_p = len(presentes)
    num_filas = (total_p + num_columnas - 1) // num_columnas

    # Matriz para simular la formación desde la derecha a la izquierda
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