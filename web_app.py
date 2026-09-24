import streamlit as st
import requests
from datetime import datetime, timedelta
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

LISTA_CUMPLEANOS = [
    {"nombre": "Diego Nicolas ACUÑA", "fecha_str": "Sin registrar", "dia": None, "mes": None},
    {"nombre": "Luciana Belen AGUERO", "fecha_str": "04 de junio", "dia": 4, "mes": 6},
    {"nombre": "Florencia Jazmin ANDRADE", "fecha_str": "12 de mayo", "dia": 12, "mes": 5},
    {"nombre": "Ariel Joaquin ARIAS UCEDO", "fecha_str": "Sin registrar", "dia": None, "mes": None},
    {"nombre": "Karen Ivonne BRIZUELA", "fecha_str": "25 de mayo", "dia": 25, "mes": 5},
    {"nombre": "Julieta Anabella BRUNEL", "fecha_str": "30 de junio", "dia": 30, "mes": 6},
    {"nombre": "Tomas CAPELLA", "fecha_str": "01 de marzo", "dia": 1, "mes": 3},
    {"nombre": "Santiago CASSOL", "fecha_str": "12 de diciembre", "dia": 12, "mes": 12},
    {"nombre": "Benjamin David CUBI", "fecha_str": "17 de abril", "dia": 17, "mes": 4},
    {"nombre": "Maria DIAZ VARSI", "fecha_str": "27 de junio", "dia": 27, "mes": 6},
    {"nombre": "Maria Celeste ESCALANTE", "fecha_str": "Sin registrar", "dia": None, "mes": None},
    {"nombre": "Rodolfo Octavio FERNANDEZ", "fecha_str": "05 de septiembre", "dia": 5, "mes": 9},
    {"nombre": "Ruben Alfredo FERNANDEZ", "fecha_str": "06 de diciembre", "dia": 6, "mes": 12},
    {"nombre": "Federico Hernan FLORES", "fecha_str": "Sin registrar", "dia": None, "mes": None},
    {"nombre": "Lorena Natividad GIMENEZ BAUTISTA", "fecha_str": "29 de febrero", "dia": 29, "mes": 2},
    {"nombre": "Agustina Gisele GONZALEZ", "fecha_str": "28 de mayo", "dia": 28, "mes": 5},
    {"nombre": "Exequiel IGLESIAS", "fecha_str": "22 de octubre", "dia": 22, "mes": 10},
    {"nombre": "Federico Andres LOPEZ", "fecha_str": "18 de junio", "dia": 18, "mes": 6},
    {"nombre": "Melina Gisel LUFT", "fecha_str": "03 de septiembre", "dia": 3, "mes": 9},
    {"nombre": "Ivana Nazarena MARS", "fecha_str": "23 de abril", "dia": 23, "mes": 4},
    {"nombre": "Maria Isabel MEDINA", "fecha_str": "12 de junio", "dia": 12, "mes": 6},
    {"nombre": "Carolina Abigail MELI", "fecha_str": "20 de agosto", "dia": 20, "mes": 8},
    {"nombre": "Daiana Elizabeth MERINO", "fecha_str": "20 de septiembre", "dia": 20, "mes": 9},
    {"nombre": "Martina Belen MICHALUK", "fecha_str": "Sin registrar", "dia": None, "mes": None},
    {"nombre": "Rocio NEIRA", "fecha_str": "10 de noviembre", "dia": 10, "mes": 11},
    {"nombre": "Claudio Hernan NUÑEZ", "fecha_str": "04 de enero", "dia": 4, "mes": 1},
    {"nombre": "Maria Pia ORIBE", "fecha_str": "18 de octubre", "dia": 18, "mes": 10},
    {"nombre": "Veronica Ayelen OTERO", "fecha_str": "18 de abril", "dia": 18, "mes": 4},
    {"nombre": "Jorge Santiago Ruben PELOSO", "fecha_str": "31 de enero", "dia": 31, "mes": 1},
    {"nombre": "Paola Margarita PEREIRA", "fecha_str": "29 de marzo", "dia": 29, "mes": 3},
    {"nombre": "Micaela Agustina PEREYRA HERRERA", "fecha_str": "14 de diciembre", "dia": 14, "mes": 12},
    {"nombre": "Agñel Soledad RAMOS", "fecha_str": "29 de abril", "dia": 29, "mes": 4},
    {"nombre": "Paula Vanesa SANCHEZ", "fecha_str": "12 de octubre", "dia": 12, "mes": 10},
    {"nombre": "Maria Belen SIGNORIO", "fecha_str": "31 de octubre", "dia": 31, "mes": 10},
    {"nombre": "Lucia Maria Fernanda SOTO BABICKI", "fecha_str": "22 de julio", "dia": 22, "mes": 7},
    {"nombre": "Emilia Alejandra TOLEDO", "fecha_str": "13 de febrero", "dia": 13, "mes": 2}
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
    for item in CRONOGRAMA_ENCARGADOS:
        fecha_dt = datetime.strptime(item["fecha"], "%d/%m/%Y").date()
        if fecha_dt >= hoy:
            return item
    return CRONOGRAMA_ENCARGADOS[-1]

def verificar_cumpleanos_proximos():
    hoy = datetime.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana_entrante = inicio_semana + timedelta(days=13)
    
    cumpleaneros = []
    for persona in LISTA_CUMPLEANOS:
        if persona["dia"] and persona["mes"]:
            try:
                cumple_ano_actual = datetime(hoy.year, persona["mes"], persona["dia"]).date()
            except ValueError:
                # Caso para 29 de febrero en año no bisiesto
                cumple_ano_actual = datetime(hoy.year, 3, 1).date()
                
            if inicio_semana <= cumple_ano_actual <= fin_semana_entrante:
                cumpleaneros.append((persona["nombre"], persona["fecha_str"]))
    return cumpleaneros

personas_db = obtener_datos()

# Estado de navegación en sesión
if "vista_actual" not in st.session_state:
    st.session_state["vista_actual"] = "menu"

def ir_a(vista):
    st.session_state["vista_actual"] = vista

# --- TITULO PRINCIPAL ---
st.title("🔴 Gestor de Alturas - Formación")

# --- ALERTA DE CUMPLEAÑOS SEMANA ACTUAL Y ENTRANTE ---
cumples_proximos = verificar_cumpleanos_proximos()
if cumples_proximos:
    detalles = ", ".join([f"**{nombre}** ({fecha})" for nombre, fecha in cumples_proximos])
    st.info(f"🎉 **¡Atención! Cumpleaños en la semana actual/entrante:** {detalles}")

# --- RESUMEN SUPERIOR ---
total_efectivos = len(personas_db)
presentes_list = [v for v in personas_db.values() if v.get("presente", False)]
ausentes_list = [v for v in personas_db.values() if not v.get("presente", False)]

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Personal", total_efectivos)
col_m2.metric("Presentes", len(presentes_list))
col_m3.metric("Ausentes", len(ausentes_list))

st.divider()

# ==========================================
# 📌 MENÚ PRINCIPAL
# ==========================================
if st.session_state["vista_actual"] == "menu":
    st.subheader("📋 Menú Principal")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⭐ Encargados de Turno", use_container_width=True):
            ir_a("encargados")
            st.rerun()
            
        if st.button("📏 Modificar Altura", use_container_width=True):
            ir_a("modificar_altura")
            st.rerun()
            
        if st.button("✅ Dar Presente / ❌ Dar Ausente", use_container_width=True):
            ir_a("presente_ausente")
            st.rerun()

        if st.button("📐 Formación en Vivo", use_container_width=True):
            ir_a("formacion")
            st.rerun()

    with col2:
        if st.button("🎂 Cumpleaños", use_container_width=True):
            ir_a("cumpleanos")
            st.rerun()

        if st.button("📋 Registro de Ausentes", use_container_width=True):
            ir_a("registro_ausentes")
            st.rerun()

        if st.button("⚠️ Reiniciar: Marcar a TODOS como Ausentes", use_container_width=True):
            ir_a("reiniciar")
            st.rerun()

# ==========================================
# 1. BOTÓN ENCARGADOS
# ==========================================
elif st.session_state["vista_actual"] == "encargados":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()
        
    st.subheader("⭐ Encargados de Turno / Formación")
    encargados_hoy = obtener_encargados_actuales()

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
            📅 Martes: {encargados_hoy['fecha']}<br>
            👩‍✈️ Encargada: <span style="color: #FFEB3B;">{encargados_hoy['encargada']}</span><br>
            👨‍✈️ Encargado: <span style="color: #FFEB3B;">{encargados_hoy['encargado']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📅 Ver Cronograma Completo de Encargados"):
        st.dataframe(CRONOGRAMA_ENCARGADOS, use_container_width=True)

# ==========================================
# 2. BOTÓN MODIFICAR ALTURA
# ==========================================
elif st.session_state["vista_actual"] == "modificar_altura":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("📏 Modificar Altura")
    nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
    mi_nombre = st.selectbox("Seleccioná tu Nombre:", ["-- Seleccionar --"] + nombres)

    if mi_nombre != "-- Seleccionar --":
        pid = [k for k, v in personas_db.items() if v["nombre"] == mi_nombre][0]
        pdata = personas_db[pid]

        nueva_alt = st.number_input("Mi Altura (m):", min_value=1.0, max_value=2.5, value=float(pdata["altura"]), step=0.01)
        if st.button("Guardar Altura"):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"altura": nueva_alt})
            st.success("Altura guardada correctamente en la base de datos.")
            st.rerun()

# ==========================================
# 3. BOTÓN PRESENTE / AUSENTE
# ==========================================
elif st.session_state["vista_actual"] == "presente_ausente":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("👤 Marcar Estado Individual (Presente / Ausente)")
    nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
    mi_nombre = st.selectbox("Seleccioná tu Nombre:", ["-- Seleccionar --"] + nombres)

    if mi_nombre != "-- Seleccionar --":
        pid = [k for k, v in personas_db.items() if v["nombre"] == mi_nombre][0]
        pdata = personas_db[pid]
        
        estado_actual = "Presente" if pdata.get("presente", False) else "Ausente"
        st.write(f"Estado actual: **{estado_actual}**")

        col_pres, col_aus = st.columns(2)
        
        with col_pres:
            if st.button("✅ Dar Presente", use_container_width=True, type="primary"):
                url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
                requests.patch(url_node, json={"presente": True, "novedad": ""})
                st.success("Marcado como PRESENTE.")
                st.rerun()

        with col_aus:
            st.markdown("#### ❌ Marcar Ausente")
            motivo = st.text_input("Motivo de ausencia / Novedad:", value=pdata.get("novedad", ""), placeholder="Ej: Licencia médica, Servicio...")
            if st.button("Confirmar Ausencia", use_container_width=True):
                url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
                requests.patch(url_node, json={"presente": False, "novedad": motivo})
                st.warning("Marcado como AUSENTE.")
                st.rerun()

# ==========================================
# 4. BOTÓN FORMACIÓN EN VIVO
# ==========================================
elif st.session_state["vista_actual"] == "formacion":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

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

        # --- CONSULTA DE POSICIÓN ---
        st.divider()
        st.markdown("#### 🔍 Consultar mi Ubicación Exacta")
        nombres_presentes = [p[1] for p in presentes]
        nombre_buscado = st.selectbox("Seleccioná tu nombre para ver tu ubicación:", ["-- Seleccionar --"] + nombres_presentes)

        if nombre_buscado != "-- Seleccionar --":
            idx_persona = next(i for i, p in enumerate(presentes) if p[1] == nombre_buscado)
            numero_orden = idx_persona + 1
            num_fila = (idx_persona // num_columnas) + 1
            num_columna_der = (idx_persona % num_columnas) + 1
            
            st.info(
                f"📍 **{nombre_buscado}**:\n\n"
                f"- **Número de Orden:** ({numero_orden})\n"
                f"- **Fila:** {num_fila} (contando desde adelante)\n"
                f"- **Columna:** {num_columna_der} (contando desde la derecha)"
            )

# ==========================================
# 5. BOTÓN CUMPLEAÑOS
# ==========================================
elif st.session_state["vista_actual"] == "cumpleanos":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("🎂 Listado de Cumpleaños")
    st.dataframe(LISTA_CUMPLEANOS, use_container_width=True)

# ==========================================
# 6. BOTÓN REGISTRO DE AUSENTES
# ==========================================
elif st.session_state["vista_actual"] == "registro_ausentes":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("📋 Registro de Novedades (Ausentes)")

    ausencias_con_motivo = [
        {"Nombre": v["nombre"], "Motivo / Novedad": v.get("novedad", "Sin registrar")}
        for v in personas_db.values() if not v.get("presente", False)
    ]
    
    if ausencias_con_motivo:
        st.dataframe(ausencias_con_motivo, use_container_width=True)
    else:
        st.success("¡Personal completo! No hay ausentes registrados.")

# ==========================================
# 7. BOTÓN REINICIAR (TODOS AUSENTES)
# ==========================================
elif st.session_state["vista_actual"] == "reiniciar":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("⚠️ Reiniciar Formación")
    st.warning("⚠️ **Atención:** Esta acción marcará a TODO el personal como AUSENTE y borrará las novedades guardadas.")
    
    confirmar = st.checkbox("Entiendo la acción y deseo continuar")
    
    if confirmar:
        if st.button("❌ REINICIAR: Marcar a TODOS como Ausentes", type="primary"):
            datos_actualizados = {k: {**v, "presente": False, "novedad": ""} for k, v in personas_db.items()}
            requests.put(FIREBASE_URL, json=datos_actualizados)
            st.success("Se reinició la formación. Todo el personal figura ausente.")
            ir_a("menu")
            st.rerun()
