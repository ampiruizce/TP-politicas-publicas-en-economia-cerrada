import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Políticas Públicas en Economía Cerrada",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# FUNCIONES ECONÓMICAS
# --------------------------------------------------

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

# --------------------------------------------------
# PORTADA
# --------------------------------------------------

st.title("📈 Políticas Públicas en Economía Cerrada")

st.markdown("""
### Economía para Ingenieros - UNSTA

**Trabajo Práctico Nº 2**

**Integrantes**
- Amparo Ruiz
- Candelaria López Avila
- Luz Maria Ponce de Leon 
""")

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🚍 Subsidios",
    "🏠 Precio Máximo",
    "📊 Comparación",
    "ℹ️ Proyecto"
])

# ==================================================
# TAB 1 SUBSIDIOS
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
        0,
        50,
        8
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

    st.subheader("Resultados")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Precio Inicial",
        f"{pe:.2f}"
    )

    c2.metric(
        "Cantidad Inicial",
        f"{qe:.2f}"
    )

    c3.metric(
        "Precio Consumidor",
        f"{pd_cons:.2f}"
    )

    c4.metric(
        "Cantidad Final",
        f"{qf:.2f}"
    )

    st.subheader("Bienestar")

    df_bienestar = pd.DataFrame({
        "Situación": ["Inicial", "Final"],
        "Bienestar": [bt0, bt1]
    })

    st.bar_chart(
        df_bienestar.set_index("Situación")
    )

    if bt1 > bt0:
        st.success(
            "El bienestar social aumenta."
        )
    else:
        st.warning(
            "El bienestar social disminuye."
        )

    st.subheader("Ganadores y Perdedoras")

    if ec1 > ec0:
        st.write("✅ Consumidores ganan")

    if ep1 > ep0:
        st.write("✅ Productores ganan")

    if gasto > 0:
        st.write("❌ El Estado incurre en gasto fiscal")

    st.subheader("Curvas de Mercado")

    precios = np.linspace(0, po_prod * 1.8, 300)

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
# TAB 2 PRECIO MÁXIMO
# ==================================================

with tab2:

    st.header("Precio Máximo a los Alquileres")

    pmax = st.slider(
        "Precio Máximo",
        10,
        100,
        40
    )

    a2 = 1800
    b2 = 20
    c2 = 0
    d2 = 12

    pe, qe = equilibrio(
        a2,
        b2,
        c2,
        d2
    )

    qd = a2 - b2 * pmax
    qo = c2 + d2 * pmax

    escasez = max(
        qd - qo,
        0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Cantidad Demandada",
        f"{qd:.0f}"
    )

    col2.metric(
        "Cantidad Ofrecida",
        f"{qo:.0f}"
    )

    col3.metric(
        "Escasez",
        f"{escasez:.0f}"
    )

    precios = [70, 60, 50, 40, 30]

    datos = []

    for pm in precios:

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
            "Demandada",
            "Ofrecida",
            "Escasez"
        ]
    )

    st.dataframe(df_pm)

    exportar_excel(
        df_pm,
        "precio_maximo.xlsx"
    )

# ==================================================
# TAB 3 COMPARACIÓN
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
        1500,
        25,
        0,
        15,
        escenario_a
    )

    pdb, pob, qb = subsidio_equilibrio(
        1500,
        25,
        0,
        15,
        escenario_b
    )

    comparacion = pd.DataFrame({
        "Variable": [
            "Cantidad",
            "Precio Consumidor"
        ],
        "Escenario A": [
            qa,
            pda
        ],
        "Escenario B": [
            qb,
            pdb
        ]
    })

    st.table(comparacion)

# ==================================================
# TAB 4
# ==================================================

with tab4:

    st.header("Acerca del Proyecto")

    st.markdown("""
### Objetivo

Analizar cómo las políticas públicas modifican
el funcionamiento de los mercados.

### Funcionalidades

- Cálculo automático de equilibrios.
- Análisis de subsidios.
- Análisis de precios máximos.
- Excedentes económicos.
- Bienestar social.
- Simulación de escenarios.
- Exportación a Excel.

### Herramientas utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
""")
