import streamlit as st
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Configuración de página
st.set_page_config(page_title="Gestor de Alturas - Formación", layout="wide")

# Auto-recarga automática cada 3 segundos
st_autorefresh(interval=3000, limit=None, key="formacion_autorefresh")

FIREBASE_URL = "https://formacion-cupro-alfa-default-rtdb.firebaseio.com/personas.json"
HISTORIAL_URL = "https://formacion-cupro-alfa-default-rtdb.firebaseio.com/historial_cambios.json"
NOVEDADES_URL = "https://formacion-cupro-alfa-default-rtdb.firebaseio.com/novedades_generales.json"

# Contraseña para acceder a la sección de Actualizaciones
ADMIN_PASSWORD = "1234"

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

LISTA_CUMPLEANOS_RAW = [
    ("Diego Nicolas ACUÑA", 7, 11),
    ("Luciana Belen AGUERO", 4, 6),
    ("Florencia Jazmin ANDRADE", 12, 5),
    ("Ariel Joaquin ARIAS UCEDO", None, None),
    ("Karen Ivonne BRIZUELA", 25, 5),
    ("Julieta Anabella BRUNEL", 30, 6),
    ("Tomas CAPELLA", 1, 3),
    ("Santiago CASSOL", 12, 12),
    ("Benjamin David CUBI", 17, 4),
    ("Maria DIAZ VARSI", 27, 6),
    ("Maria Celeste ESCALANTE", None, None),
    ("Rodolfo Octavio FERNANDEZ", 5, 9),
    ("Ruben Alfredo FERNANDEZ", 6, 12),
    ("Federico Hernan FLORES", None, None),
    ("Lorena Natividad GIMENEZ BAUTISTA", 29, 2),
    ("Agustina Gisele GONZALEZ", 28, 5),
    ("Exequiel IGLESIAS", 22, 10),
    ("Federico Andres LOPEZ", 18, 6),
    ("Melina Gisel LUFT", 3, 9),
    ("Ivana Nazarena MARS", 23, 4),
    ("Maria Isabel MEDINA", 12, 6),
    ("Carolina Abigail MELI", 20, 8),
    ("Daiana Elizabeth MERINO", 20, 9),
    ("Martina Belen MICHALUK", None, None),
    ("Rocio NEIRA", 10, 11),
    ("Claudio Hernan NUÑEZ", 4, 1),
    ("Maria Pia ORIBE", 18, 10),
    ("Veronica Ayelen OTERO", 18, 4),
    ("Jorge Santiago Ruben PELOSO", 31, 1),
    ("Paola Margarita PEREIRA", 29, 3),
    ("Micaela Agustina PEREYRA HERRERA", 14, 12),
    ("Agñel Soledad RAMOS", 29, 4),
    ("Paula Vanesa SANCHEZ", 12, 10),
    ("Maria Belen SIGNORIO", 31, 10),
    ("Lucia Maria Fernanda SOTO BABICKI", 22, 7),
    ("Emilia Alejandra TOLEDO", 13, 2)
]

MESES_NOMBRES = {
    0: "Todos los Meses",
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def registrar_cambio_altura(detalle):
    try:
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nuevo_registro = {"fecha_hora": ahora, "detalle": detalle}
        requests.post(HISTORIAL_URL, json=nuevo_registro, timeout=3)
    except Exception:
        pass

def obtener_historial():
    try:
        res = requests.get(HISTORIAL_URL, timeout=3)
        data = res.json()
        if data:
            lista = list(data.values())
            lista.reverse()
            return lista
        return []
    except Exception:
        return []

def publicar_novedad_general(autor, titulo, mensaje):
    try:
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        registro = {
            "fecha_hora": ahora,
            "autor": autor,
            "titulo": titulo,
            "mensaje": mensaje
        }
        requests.post(NOVEDADES_URL, json=registro, timeout=3)
    except Exception:
        pass

def obtener_novedades_generales():
    try:
        res = requests.get(NOVEDADES_URL, timeout=3)
        data = res.json()
        if data:
            return data
        return {}
    except Exception:
        return {}

def eliminar_novedad_general(key_node):
    try:
        url_node = NOVEDADES_URL.replace(".json", f"/{key_node}.json")
        requests.delete(url_node, timeout=3)
    except Exception:
        pass

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
    for nombre, dia, mes in LISTA_CUMPLEANOS_RAW:
        if dia and mes:
            try:
                cumple_ano_actual = datetime(hoy.year, mes, dia).date()
            except ValueError:
                cumple_ano_actual = datetime(hoy.year, 3, 1).date()
                
            if inicio_semana <= cumple_ano_actual <= fin_semana_entrante:
                cumpleaneros.append((nombre, f"{dia:02d}/{mes:02d}"))
    return cumpleaneros

personas_db = obtener_datos()

# Estado de navegación en sesión
if "vista_actual" not in st.session_state:
    st.session_state["vista_actual"] = "menu"

def ir_a(vista):
    st.session_state["vista_actual"] = vista

# --- TÍTULO PRINCIPAL ---
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

        if st.button("✅ Dar Presente", use_container_width=True):
            ir_a("dar_presente")
            st.rerun()
            
        if st.button("❌ Registrar Ausente", use_container_width=True):
            ir_a("dar_ausente")
            st.rerun()

        if st.button("📢 Novedades y Avisos", use_container_width=True):
            ir_a("novedades_generales")
            st.rerun()

        if st.button("📏 Modificar Altura", use_container_width=True):
            ir_a("modificar_altura")
            st.rerun()

    with col2:
        if st.button("📐 Formación en Vivo", use_container_width=True):
            ir_a("formacion")
            st.rerun()

        if st.button("🎂 Cumpleaños", use_container_width=True):
            ir_a("cumpleanos")
            st.rerun()

        if st.button("📋 Registro de Ausentes", use_container_width=True):
            ir_a("registro_ausentes")
            st.rerun()

        if st.button("🔐 Actualizaciones (Historial)", use_container_width=True):
            ir_a("actualizaciones")
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
# 2. BOTÓN DAR PRESENTE
# ==========================================
elif st.session_state["vista_actual"] == "dar_presente":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("✅ Dar Presente")
    nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
    mi_nombre = st.selectbox("Seleccioná tu Nombre:", ["-- Seleccionar --"] + nombres)

    if mi_nombre != "-- Seleccionar --":
        pid = [k for k, v in personas_db.items() if v["nombre"] == mi_nombre][0]
        pdata = personas_db[pid]
        
        estado_actual = "Presente" if pdata.get("presente", False) else "Ausente"
        st.write(f"Estado actual: **{estado_actual}**")

        if st.button("Confirmar PRESENTE", type="primary", use_container_width=True):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"presente": True, "novedad": ""})
            st.success("✅ Marcado como PRESENTE.")
            st.rerun()

# ==========================================
# 3. BOTÓN REGISTRAR AUSENTE
# ==========================================
elif st.session_state["vista_actual"] == "dar_ausente":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("❌ Registrar Causa de Ausencia")
    nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
    mi_nombre = st.selectbox("Seleccioná tu Nombre:", ["-- Seleccionar --"] + nombres)

    if mi_nombre != "-- Seleccionar --":
        pid = [k for k, v in personas_db.items() if v["nombre"] == mi_nombre][0]
        pdata = personas_db[pid]
        
        motivo = st.text_input(
            "Causa / Motivo de ausencia:", 
            value=pdata.get("novedad", ""), 
            placeholder="Ej: Licencia médica, Franco, Comisión de servicio..."
        )
        
        if st.button("Confirmar AUSENCIA", type="primary", use_container_width=True):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"presente": False, "novedad": motivo})
            st.warning("❌ Registrado como AUSENTE con la novedad ingresada.")
            st.rerun()

# ==========================================
# 4. BOTÓN NOVEDADES Y AVISOS (NUEVO)
# ==========================================
elif st.session_state["vista_actual"] == "novedades_generales":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("📢 Novedades y Avisos Generales")

    with st.expander("✏️ Publicar una nueva Novedad / Aviso", expanded=True):
        nombres = [v["nombre"] for k, v in sorted(personas_db.items())] if personas_db else []
        autor_nov = st.selectbox("Publicado por:", ["-- Seleccionar --"] + nombres, key="autor_nov")
        titulo_nov = st.text_input("Asunto / Título:", placeholder="Ej: Examen del martes / Apuntes disponiles / Guardia...")
        msg_nov = st.text_area("Detalle del aviso:", placeholder="Escribí el contenido de la novedad aquí...")

        if st.button("Publish Novedad / Aviso", type="primary"):
            if autor_nov != "-- Seleccionar --" and titulo_nov.strip() and msg_nov.strip():
                publicar_novedad_general(autor_nov, titulo_nov, msg_nov)
                st.success("¡Novedad publicada correctamente!")
                st.rerun()
            else:
                st.error("Por favor completa tu nombre, asunto y detalle antes de publicar.")

    st.divider()
    st.markdown("### 📌 Avisos Publicados:")
    dict_novs = obtener_novedades_generales()

    if dict_novs:
        # Ordenar más recientes primero
        items_novs = list(dict_novs.items())
        items_novs.reverse()

        for key_id, info in items_novs:
            with st.container():
                st.markdown(f"#### 🔹 {info.get('titulo', 'Sin Título')}")
                st.write(f"{info.get('mensaje', '')}")
                st.caption(f"👤 **Publicado por:** {info.get('autor', 'Anónimo')} | 🕒 **Fecha:** {info.get('fecha_hora', '')}")
                
                # Opción de borrado individual por el autor/usuario
                col_b1, col_b2 = st.columns([1, 3])
                with col_b1:
                    if st.button("🗑️ Borrar mi aviso", key=f"del_{key_id}"):
                        eliminar_novedad_general(key_id)
                        st.success("Aviso eliminado.")
                        st.rerun()
                st.divider()
    else:
        st.info("No hay avisos o novedades publicados por el momento.")

# ==========================================
# 5. BOTÓN MODIFICAR ALTURA
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
        alt_anterior = float(pdata["altura"])

        nueva_alt = st.number_input("Mi Altura (m):", min_value=1.0, max_value=2.5, value=alt_anterior, step=0.01)
        if st.button("Guardar Altura"):
            url_node = FIREBASE_URL.replace(".json", f"/{pid}.json")
            requests.patch(url_node, json={"altura": nueva_alt})
            registrar_cambio_altura(f"📏 {mi_nombre} cambió su altura de {alt_anterior:.2f}m a {nueva_alt:.2f}m.")
            st.success("Altura guardada correctamente en la base de datos.")
            st.rerun()

# ==========================================
# 6. BOTÓN FORMACIÓN EN VIVO
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
# 7. BOTÓN CUMPLEAÑOS
# ==========================================
elif st.session_state["vista_actual"] == "cumpleanos":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("🎂 Listado de Cumpleaños")

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        mes_seleccionado = st.selectbox(
            "📅 Filtrar por Mes:", 
            options=list(MESES_NOMBRES.keys()), 
            format_func=lambda x: MESES_NOMBRES[x]
        )

    with col_f2:
        busqueda = st.text_input("🔍 Buscar por Nombre:", placeholder="Escribí un nombre o apellido...")

    tabla_cumples = []
    for nombre, dia, mes in LISTA_CUMPLEANOS_RAW:
        if mes_seleccionado != 0 and mes != mes_seleccionado:
            continue
            
        if busqueda and busqueda.lower() not in nombre.lower():
            continue

        fecha_fmt = f"{dia:02d}/{mes:02d}" if (dia and mes) else "Sin registrar"
        tabla_cumples.append({"Nombre Completo": nombre, "Cumpleaños": fecha_fmt})

    if tabla_cumples:
        st.dataframe(tabla_cumples, use_container_width=True)
    else:
        st.info("No se encontraron cumpleaños con los filtros seleccionados.")

# ==========================================
# 8. BOTÓN REGISTRO DE AUSENTES
# ==========================================
elif st.session_state["vista_actual"] == "registro_ausentes":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("📋 Registro de Novedades (Ausentes)")

    ausencias = [
        {"Nombre": v["nombre"], "Causa / Novedad": v.get("novedad") if v.get("novedad") else "Sin especificar"}
        for v in personas_db.values() if not v.get("presente", False)
    ]
    
    if ausencias:
        st.dataframe(ausencias, use_container_width=True)
    else:
        st.success("¡Personal completo! No hay ausentes registrados.")

# ==========================================
# 9. BOTÓN ACTUALIZACIONES (CON CONTRASEÑA)
# ==========================================
elif st.session_state["vista_actual"] == "actualizaciones":
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a("menu")
        st.rerun()

    st.subheader("🔐 Registro de Cambios y Panel de Control")

    if "admin_autenticado" not in st.session_state:
        st.session_state["admin_autenticado"] = False

    if not st.session_state["admin_autenticado"]:
        pwd_input = st.text_input("Ingresá la contraseña para acceder:", type="password")
        if st.button("Ingresar"):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state["admin_autenticado"] = True
                st.success("Acceso concedido.")
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    else:
        st.success("🔓 Sesión autorizada como Administrador")
        
        # Opciones de administración masiva
        st.markdown("### ⚙️ Acciones de Administrador")
        if st.button("✅ Marcar a TODOS como Presentes", type="primary", use_container_width=True):
            datos_actualizados = {k: {**v, "presente": True, "novedad": ""} for k, v in personas_db.items()}
            requests.put(FIREBASE_URL, json=datos_actualizados)
            st.success("Se marcaron todos los efectivos como PRESENTES.")
            st.rerun()

        st.divider()

        # SECCIÓN NOVEDADES GENERALES (ADMIN)
        st.markdown("### 📢 Gestión de Novedades y Avisos Generales")
        dict_novs_admin = obtener_novedades_generales()
        if dict_novs_admin:
            lista_admin_novs = [
                {
                    "ID": k,
                    "Fecha": v.get("fecha_hora"),
                    "Autor": v.get("autor"),
                    "Título": v.get("titulo"),
                    "Mensaje": v.get("mensaje")
                }
                for k, v in dict_novs_admin.items()
            ]
            st.dataframe(lista_admin_novs, use_container_width=True)
            if st.button("🗑️ Borrar TODAS las Novedades y Avisos Generales"):
                requests.delete(NOVEDADES_URL)
                st.success("Todas las novedades generales fueron eliminadas.")
                st.rerun()
        else:
            st.info("No hay novedades o avisos generales activos.")

        st.divider()

        # SECCIÓN HISTORIAL DE ALTURAS
        historial = obtener_historial()
        if historial:
            st.markdown("### 📝 Historial de Modificaciones de Altura:")
            st.dataframe(historial, use_container_width=True)

            if st.button("🗑️ Borrar Historial de Cambios de Altura"):
                requests.delete(HISTORIAL_URL)
                st.success("Historial eliminado.")
                st.rerun()
        else:
            st.info("No hay modificaciones de altura registradas todavía.")

        st.divider()

        if st.button("🔒 Cerrar Sesión de Administrador"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

# ==========================================
# 10. BOTÓN REINICIAR (TODOS AUSENTES)
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
