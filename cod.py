import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Políticas Públicas en Economía Cerrada",
    page_icon="📈",
    layout="wide"
)

# ==================================================
# FUNCIONES
# ==================================================

def equilibrio(a, b, c, d):
    pe = (a - c) / (b + d)
    qe = a - b * pe
    return pe, qe

def excedente_consumidor(a, b, p, q):
    precio_reserva = a / b
    return ((precio_reserva - p) * q) / 2

def excedente_productor(c, d, p, q):
    precio_min = -c / d if d != 0 else 0
    return ((p - precio_min) * q) / 2

def subsidio_equilibrio(a, b, c, d, s):
    pd = (a - c - d * s) / (b + d)
    po = pd + s
    q = a - b * pd
    return pd, po, q

def exportar_excel(df, nombre):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        "📥 Descargar Excel",
        output.getvalue(),
        file_name=nombre,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==================================================
# PORTADA
# ==================================================

st.title("📈 Políticas Públicas en Economía Cerrada")

st.markdown("""
### Economía para Ingenieros - UNSTA

**Trabajo Práctico N° 2**

### Integrantes
- Amparo Ruiz
- Candelaria López Avila
- Luz María Ponce de León
""")

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🚍 Subsidios",
    "🏠 Precio Máximo",
    "📊 Comparación",
    "ℹ️ Proyecto"
])

# ==================================================
# TAB 1 - SUBSIDIOS
# ==================================================

with tab1:

    st.header("Subsidio al Transporte Público")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input("Parámetro a", value=1500.0)
        b = st.number_input("Parámetro b", value=25.0)

    with col2:
        c = st.number_input("Parámetro c", value=0.0)
        d = st.number_input("Parámetro d", value=15.0)

    s = st.slider(
        "Subsidio por viaje",
        min_value=0,
        max_value=50,
        value=8
    )

    pe, qe = equilibrio(a, b, c, d)

    ec0 = excedente_consumidor(a, b, pe, qe)
    ep0 = excedente_productor(c, d, pe, qe)
    bt0 = ec0 + ep0

    pd_cons, po_prod, qf = subsidio_equilibrio(
        a, b, c, d, s
    )

    ec1 = excedente_consumidor(
        a, b, pd_cons, qf
    )

    ep1 = excedente_productor(
        c, d, po_prod, qf
    )

    gasto = s * qf

    bt1 = ec1 + ep1 - gasto

    variacion = bt1 - bt0

    st.subheader("Resultados")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Precio Inicial", f"{pe:.2f}")
    c2.metric("Cantidad Inicial", f"{qe:.2f}")
    c3.metric("Precio Consumidor", f"{pd_cons:.2f}")
    c4.metric("Cantidad Final", f"{qf:.2f}")

    st.subheader("Bienestar Social")

    b1, b2, b3 = st.columns(3)

    b1.metric(
        "Bienestar Inicial",
        f"{bt0:.2f}"
    )

    b2.metric(
        "Bienestar Final",
        f"{bt1:.2f}"
    )

    b3.metric(
        "Variación",
        f"{variacion:.2f}",
        delta=f"{variacion:.2f}"
    )

    df_bienestar = pd.DataFrame({
        "Situación": ["Inicial", "Final"],
        "Bienestar": [bt0, bt1]
    })

    st.bar_chart(
        df_bienestar.set_index("Situación")
    )

    st.subheader("Interpretación Económica")

    if bt1 > bt0:
        st.success(
            "El subsidio incrementa el bienestar social."
        )
    else:
        st.warning(
            "El costo fiscal supera los beneficios obtenidos."
        )

    st.subheader("Ganadores y Perdedores")

    if ec1 > ec0:
        st.write("✅ Los consumidores ganan.")

    if ep1 > ep0:
        st.write("✅ Los productores ganan.")

    if gasto > 0:
        st.write("❌ El Estado incurre en gasto fiscal.")

    st.subheader("Curvas de Mercado")

    precios = np.linspace(
        0,
        max(po_prod * 1.8, pe * 2),
        300
    )

    demanda = a - b * precios
    oferta = c + d * precios
    oferta_sub = c + d * (precios + s)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=demanda,
            y=precios,
            name="Demanda"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=oferta,
            y=precios,
            name="Oferta"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=oferta_sub,
            y=precios,
            name="Oferta con Subsidio"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Simulación Automática")

    resultados = []

    for sub in [0, 5, 10, 15, 20]:

        pdx, pox, qx = subsidio_equilibrio(
            a, b, c, d, sub
        )

        ecx = excedente_consumidor(
            a, b, pdx, qx
        )

        epx = excedente_productor(
            c, d, pox, qx
        )

        gastox = sub * qx

        bienestarx = ecx + epx - gastox

        resultados.append([
            sub,
            round(qx, 2),
            round(gastox, 2),
            round(bienestarx, 2)
        ])

    df_sub = pd.DataFrame(
        resultados,
        columns=[
            "Subsidio",
            "Cantidad",
            "Gasto Público",
            "Bienestar"
        ]
    )

    st.dataframe(df_sub)

    exportar_excel(
        df_sub,
        "subsidios.xlsx"
    )

# ==================================================
# TAB 2 - PRECIO MÁXIMO
# ==================================================

with tab2:

    st.header("Precio Máximo a los Alquileres")

    a2 = 1800
    b2 = 20
    c2 = 0
    d2 = 12

    pmax = st.slider(
        "Precio Máximo",
        min_value=10,
        max_value=100,
        value=40
    )

    pe, qe = equilibrio(
        a2,
        b2,
        c2,
        d2
    )

    ec0 = excedente_consumidor(
        a2,
        b2,
        pe,
        qe
    )

    ep0 = excedente_productor(
        c2,
        d2,
        pe,
        qe
    )

    bt0 = ec0 + ep0

    qd = a2 - b2 * pmax
    qo = c2 + d2 * pmax

    escasez = max(
        qd - qo,
        0
    )

    cantidad_transada = min(
        qd,
        qo
    )

    ec1 = (
        ((a2 / b2) - pmax)
        * cantidad_transada
        / 2
    )

    ep1 = (
        (pmax - (-c2 / d2))
        * cantidad_transada
        / 2
    )

    bt1 = ec1 + ep1

    variacion = bt1 - bt0

    c1, c2_, c3 = st.columns(3)

    c1.metric(
        "Cantidad Demandada",
        f"{qd:.0f}"
    )

    c2_.metric(
        "Cantidad Ofrecida",
        f"{qo:.0f}"
    )

    c3.metric(
        "Escasez",
        f"{escasez:.0f}"
    )

    st.subheader("Excedentes")

    e1, e2 = st.columns(2)

    with e1:
        st.metric(
            "EC Inicial",
            f"{ec0:.2f}"
        )

        st.metric(
            "EP Inicial",
            f"{ep0:.2f}"
        )

    with e2:
        st.metric(
            "EC Final",
            f"{ec1:.2f}"
        )

        st.metric(
            "EP Final",
            f"{ep1:.2f}"
        )

    st.subheader("Bienestar Social")

    w1, w2, w3 = st.columns(3)

    w1.metric(
        "Bienestar Inicial",
        f"{bt0:.2f}"
    )

    w2.metric(
        "Bienestar Final",
        f"{bt1:.2f}"
    )

    w3.metric(
        "Variación",
        f"{variacion:.2f}",
        delta=f"{variacion:.2f}"
    )

    if escasez > 0:
        st.warning(
            "El precio máximo genera escasez."
        )
    else:
        st.success(
            "El precio máximo no genera escasez."
        )

    datos = []

    for pm in [70, 60, 50, 40, 30]:

        qd_pm = a2 - b2 * pm
        qo_pm = c2 + d2 * pm

        datos.append([
            pm,
            qd_pm,
            qo_pm,
            max(qd_pm - qo_pm, 0)
        ])

    df_pm = pd.DataFrame(
        datos,
        columns=[
            "Precio Máximo",
            "Cantidad Demandada",
            "Cantidad Ofrecida",
            "Escasez"
        ]
    )

    st.subheader("Simulación Automática")

    st.dataframe(df_pm)

    exportar_excel(
        df_pm,
        "precio_maximo.xlsx"
    )

# ==================================================
# TAB 3 - COMPARACIÓN
# ==================================================

with tab3:

    st.header("Comparación de Escenarios")

    escenario_a = st.slider(
        "Subsidio Escenario A",
        0,
        20,
        5
    )

    escenario_b = st.slider(
        "Subsidio Escenario B",
        0,
        20,
        15
    )

    pda, poa, qa = subsidio_equilibrio(
        1500, 25, 0, 15, escenario_a
    )

    pdb, pob, qb = subsidio_equilibrio(
        1500, 25, 0, 15, escenario_b
    )

    comparacion = pd.DataFrame({
        "Variable": [
            "Cantidad",
            "Precio Consumidor"
        ],
        "Escenario A": [
            round(qa, 2),
            round(pda, 2)
        ],
        "Escenario B": [
            round(qb, 2),
            round(pdb, 2)
        ]
    })

    st.table(comparacion)

# ==================================================
# TAB 4 - ACERCA DEL PROYECTO
# ==================================================

with tab4:

    st.header("Acerca del Proyecto")

    st.markdown("""
### Objetivo

Analizar cómo las políticas públicas afectan
a consumidores, productores y al bienestar social.

### Funcionalidades

- Equilibrio de mercado.
- Subsidios.
- Precio máximo.
- Excedentes económicos.
- Bienestar social.
- Simulación de escenarios.
- Exportación a Excel.

### Tecnologías

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL
""")
