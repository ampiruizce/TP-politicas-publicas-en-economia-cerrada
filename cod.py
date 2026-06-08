mport streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

st.set_page_config(
    page_title="Políticas Públicas en Economía Cerrada",
    page_icon="📈",
    layout="wide"
)

# ==================================================
# FUNCIONES ECONÓMICAS
# ==================================================

def equilibrio(a, b, c, d):
    pe = (a - c) / (b + d)
    qe = a - b * pe
    return pe, qe


def excedente_consumidor(a, b, precio, cantidad):
    precio_max_demanda = a / b
    ec = ((precio_max_demanda - precio) * cantidad) / 2
    return ec


def excedente_productor(c, d, precio, cantidad):
    precio_min_oferta = -c / d
    ep = ((precio - precio_min_oferta) * cantidad) / 2
    return ep


def equilibrio_con_subsidio(a, b, c, d, s):
    precio_usuario = (a - c - d * s) / (b + d)
    precio_empresa = precio_usuario + s
    cantidad = a - b * precio_usuario
    return precio_usuario, precio_empresa, cantidad


def exportar_excel(df, nombre_archivo):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Descargar Excel",
        data=output.getvalue(),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def grafico_mercado(a, b, c, d, titulo, precio_intervencion=None, subsidio=None):
    pe, qe = equilibrio(a, b, c, d)

    precio_maximo_grafico = max(pe * 2, 100)
    precios = np.linspace(0, precio_maximo_grafico, 300)

    demanda = a - b * precios
    oferta = c + d * precios

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=demanda,
            y=precios,
            name="Demanda",
            mode="lines"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=oferta,
            y=precios,
            name="Oferta",
            mode="lines"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[qe],
            y=[pe],
            name="Equilibrio inicial",
            mode="markers",
            marker=dict(size=10)
        )
    )

    if precio_intervencion is not None:
        fig.add_hline(
            y=precio_intervencion,
            line_dash="dash",
            annotation_text="Precio máximo",
            annotation_position="top left"
        )

    if subsidio is not None:
        oferta_subsidio = c + d * (precios + subsidio)

        fig.add_trace(
            go.Scatter(
                x=oferta_subsidio,
                y=precios,
                name="Oferta con subsidio",
                mode="lines"
            )
        )

    fig.update_layout(
        title=titulo,
        xaxis_title="Cantidad",
        yaxis_title="Precio",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# PORTADA
# ==================================================

st.title("📈 Políticas Públicas en Economía Cerrada")

st.markdown("""
### Economía para Ingenieros - UNSTA

**Trabajo Práctico N° 2**

**Integrantes**
- Amparo Ruiz
- Candelaria López Avila
- Luz María Ponce de León
""")

# ==================================================
# SOLAPAS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🚍 Subsidios",
    "🏠 Precio Máximo",
    "📊 Comparación",
    "ℹ️ Proyecto"
])

# ==================================================
# SOLAPA 1 - SUBSIDIOS
# ==================================================

with tab1:

    st.header("🚍 Subsidio al Transporte Público")

    st.markdown("""
    En esta sección se analiza cómo un subsidio por unidad afecta el equilibrio del mercado,
    los precios que pagan los usuarios, los precios que reciben las empresas y el bienestar social.
    """)

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "Parámetro a de la demanda",
            value=1500.0,
            key="sub_a"
        )

        b = st.number_input(
            "Parámetro b de la demanda",
            value=25.0,
            min_value=0.01,
            key="sub_b"
        )

    with col2:
        c = st.number_input(
            "Parámetro c de la oferta",
            value=0.0,
            key="sub_c"
        )

        d = st.number_input(
            "Parámetro d de la oferta",
            value=15.0,
            min_value=0.01,
            key="sub_d"
        )

    s = st.slider(
        "Subsidio por unidad",
        min_value=0,
        max_value=50,
        value=8,
        key="sub_s"
    )

    # -----------------------------
    # Equilibrio inicial
    # -----------------------------

    pe, qe = equilibrio(a, b, c, d)

    # -----------------------------
    # Equilibrio con subsidio
    # -----------------------------

    precio_usuario, precio_empresa, cantidad_final = equilibrio_con_subsidio(
        a, b, c, d, s
    )

    # -----------------------------
    # Excedentes y bienestar
    # -----------------------------

    ec_inicial = excedente_consumidor(a, b, pe, qe)
    ep_inicial = excedente_productor(c, d, pe, qe)

    ec_final = excedente_consumidor(a, b, precio_usuario, cantidad_final)
    ep_final = excedente_productor(c, d, precio_empresa, cantidad_final)

    gasto_gobierno = s * cantidad_final

    bienestar_inicial = ec_inicial + ep_inicial
    bienestar_final = ec_final + ep_final - gasto_gobierno

    variacion_bienestar = bienestar_final - bienestar_inicial

    # -----------------------------
    # Resultados principales
    # -----------------------------

    st.subheader("Equilibrio inicial y equilibrio luego del subsidio")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Precio de equilibrio inicial",
        f"{pe:.2f}"
    )

    col2.metric(
        "Cantidad de equilibrio inicial",
        f"{qe:.2f}"
    )

    col3.metric(
        "Precio pagado por usuarios",
        f"{precio_usuario:.2f}"
    )

    col4.metric(
        "Precio recibido por empresas",
        f"{precio_empresa:.2f}"
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "Cantidad luego del subsidio",
        f"{cantidad_final:.2f}"
    )

    col6.metric(
        "Gasto total del Gobierno",
        f"{gasto_gobierno:.2f}"
    )

    # -----------------------------
    # Excedentes
    # -----------------------------

    st.subheader("Excedentes económicos")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Excedente del consumidor inicial",
            f"{ec_inicial:.2f}"
        )

        st.metric(
            "Excedente del productor inicial",
            f"{ep_inicial:.2f}"
        )

    with col2:
        st.metric(
            "Excedente del consumidor final",
            f"{ec_final:.2f}"
        )

        st.metric(
            "Excedente del productor final",
            f"{ep_final:.2f}"
        )

    # -----------------------------
    # Bienestar
    # -----------------------------

    st.subheader("Bienestar social")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Bienestar inicial",
        f"{bienestar_inicial:.2f}"
    )

    col2.metric(
        "Bienestar final",
        f"{bienestar_final:.2f}"
    )

    col3.metric(
        "Variación del bienestar social",
        f"{variacion_bienestar:.2f}",
        delta=f"{variacion_bienestar:.2f}"
    )

    if variacion_bienestar > 0:
        st.success("La política aumenta el bienestar social.")
    elif variacion_bienestar < 0:
        st.warning("La política reduce el bienestar social.")
    else:
        st.info("La política no modifica el bienestar social.")

    # -----------------------------
    # Tabla resumen
    # -----------------------------

    st.subheader("Tabla resumen")

    df_subsidio = pd.DataFrame({
        "Variable": [
            "Precio de equilibrio inicial",
            "Cantidad de equilibrio inicial",
            "Precio pagado por los usuarios",
            "Precio recibido por las empresas",
            "Cantidad de equilibrio luego del subsidio",
            "Excedente del consumidor inicial",
            "Excedente del consumidor final",
            "Excedente del productor inicial",
            "Excedente del productor final",
            "Gasto total del Gobierno",
            "Variación del bienestar social"
        ],
        "Valor": [
            round(pe, 2),
            round(qe, 2),
            round(precio_usuario, 2),
            round(precio_empresa, 2),
            round(cantidad_final, 2),
            round(ec_inicial, 2),
            round(ec_final, 2),
            round(ep_inicial, 2),
            round(ep_final, 2),
            round(gasto_gobierno, 2),
            round(variacion_bienestar, 2)
        ]
    })

    st.dataframe(df_subsidio, use_container_width=True)

    exportar_excel(
        df_subsidio,
        "resultados_subsidio.xlsx"
    )

    # -----------------------------
    # Gráfico
    # -----------------------------

    st.subheader("Gráfico del mercado")

    grafico_mercado(
        a,
        b,
        c,
        d,
        "Mercado con subsidio",
        subsidio=s
    )

# ==================================================
# SOLAPA 2 - PRECIO MÁXIMO
# ==================================================

with tab2:

    st.header("🏠 Precio Máximo a los Alquileres")

    st.markdown("""
    En esta sección se analiza el efecto de un precio máximo sobre el mercado,
    observando la cantidad demandada, la cantidad ofrecida, la escasez y la variación del bienestar social.
    """)

    col1, col2 = st.columns(2)

    with col1:
        a_pm = st.number_input(
            "Parámetro a de la demanda",
            value=1800.0,
            key="pm_a"
        )

        b_pm = st.number_input(
            "Parámetro b de la demanda",
            value=20.0,
            min_value=0.01,
            key="pm_b"
        )

    with col2:
        c_pm = st.number_input(
            "Parámetro c de la oferta",
            value=0.0,
            key="pm_c"
        )

        d_pm = st.number_input(
            "Parámetro d de la oferta",
            value=12.0,
            min_value=0.01,
            key="pm_d"
        )

    precio_maximo = st.slider(
        "Precio máximo",
        min_value=10,
        max_value=100,
        value=40,
        key="pm_precio"
    )

    # -----------------------------
    # Equilibrio inicial
    # -----------------------------

    pe_pm, qe_pm = equilibrio(a_pm, b_pm, c_pm, d_pm)

    # -----------------------------
    # Situación con precio máximo
    # -----------------------------

    cantidad_demandada = a_pm - b_pm * precio_maximo
    cantidad_ofrecida = c_pm + d_pm * precio_maximo

    escasez = max(cantidad_demandada - cantidad_ofrecida, 0)

    cantidad_transada = min(cantidad_demandada, cantidad_ofrecida)

    # -----------------------------
    # Excedentes y bienestar
    # -----------------------------

    ec_inicial_pm = excedente_consumidor(a_pm, b_pm, pe_pm, qe_pm)
    ep_inicial_pm = excedente_productor(c_pm, d_pm, pe_pm, qe_pm)

    ec_final_pm = excedente_consumidor(
        a_pm,
        b_pm,
        precio_maximo,
        cantidad_transada
    )

    ep_final_pm = excedente_productor(
        c_pm,
        d_pm,
        precio_maximo,
        cantidad_transada
    )

    bienestar_inicial_pm = ec_inicial_pm + ep_inicial_pm
    bienestar_final_pm = ec_final_pm + ep_final_pm

    variacion_bienestar_pm = bienestar_final_pm - bienestar_inicial_pm

    # -----------------------------
    # Equilibrio inicial
    # -----------------------------

    st.subheader("Equilibrio inicial")

    col1, col2 = st.columns(2)

    col1.metric(
        "Precio de equilibrio",
        f"{pe_pm:.2f}"
    )

    col2.metric(
        "Cantidad de equilibrio",
        f"{qe_pm:.2f}"
    )

    # -----------------------------
    # Precio máximo
    # -----------------------------

    st.subheader("Situación al precio máximo")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Cantidad demandada",
        f"{cantidad_demandada:.2f}"
    )

    col2.metric(
        "Cantidad ofrecida",
        f"{cantidad_ofrecida:.2f}"
    )

    col3.metric(
        "Escasez generada",
        f"{escasez:.2f}"
    )

    if precio_maximo < pe_pm:
        st.warning("El precio máximo es efectivo porque se encuentra por debajo del precio de equilibrio.")
    else:
        st.info("El precio máximo no es efectivo porque no se encuentra por debajo del precio de equilibrio.")

    # -----------------------------
    # Excedentes
    # -----------------------------

    st.subheader("Excedentes económicos")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Excedente del consumidor antes",
            f"{ec_inicial_pm:.2f}"
        )

        st.metric(
            "Excedente del productor antes",
            f"{ep_inicial_pm:.2f}"
        )

    with col2:
        st.metric(
            "Excedente del consumidor después",
            f"{ec_final_pm:.2f}"
        )

        st.metric(
            "Excedente del productor después",
            f"{ep_final_pm:.2f}"
        )

    # -----------------------------
    # Bienestar
    # -----------------------------

    st.subheader("Bienestar social")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Bienestar inicial",
        f"{bienestar_inicial_pm:.2f}"
    )

    col2.metric(
        "Bienestar final",
        f"{bienestar_final_pm:.2f}"
    )

    col3.metric(
        "Variación del bienestar social",
        f"{variacion_bienestar_pm:.2f}",
        delta=f"{variacion_bienestar_pm:.2f}"
    )

    if variacion_bienestar_pm > 0:
        st.success("La política aumenta el bienestar social.")
    elif variacion_bienestar_pm < 0:
        st.warning("La política reduce el bienestar social.")
    else:
        st.info("La política no modifica el bienestar social.")

    # -----------------------------
    # Tabla resumen
    # -----------------------------

    st.subheader("Tabla resumen")

    df_precio_maximo = pd.DataFrame({
        "Variable": [
            "Precio de equilibrio",
            "Cantidad de equilibrio",
            "Cantidad demandada al precio máximo",
            "Cantidad ofrecida al precio máximo",
            "Escasez generada",
            "Excedente del consumidor antes",
            "Excedente del consumidor después",
            "Excedente del productor antes",
            "Excedente del productor después",
            "Variación del bienestar social"
        ],
        "Valor": [
            round(pe_pm, 2),
            round(qe_pm, 2),
            round(cantidad_demandada, 2),
            round(cantidad_ofrecida, 2),
            round(escasez, 2),
            round(ec_inicial_pm, 2),
            round(ec_final_pm, 2),
            round(ep_inicial_pm, 2),
            round(ep_final_pm, 2),
            round(variacion_bienestar_pm, 2)
        ]
    })

    st.dataframe(df_precio_maximo, use_container_width=True)

    exportar_excel(
        df_precio_maximo,
        "resultados_precio_maximo.xlsx"
    )

    # -----------------------------
    # Gráfico
    # -----------------------------

    st.subheader("Gráfico del mercado")

    grafico_mercado(
        a_pm,
        b_pm,
        c_pm,
        d_pm,
        "Mercado con precio máximo",
        precio_intervencion=precio_maximo
    )

# ==================================================
# SOLAPA 3 - COMPARACIÓN
# ==================================================

with tab3:

    st.header("📊 Comparación de escenarios")

    st.markdown("""
    Esta sección permite comparar automáticamente distintos niveles de subsidio
    y distintos precios máximos.
    """)

    st.subheader("Comparación de subsidios")

    subsidios = [0, 5, 10, 15, 20]

    datos_subsidios = []

    for sub in subsidios:
        pu, pe_emp, q_sub = equilibrio_con_subsidio(
            1500,
            25,
            0,
            15,
            sub
        )

        pe_base, qe_base = equilibrio(
            1500,
            25,
            0,
            15
        )

        ec0 = excedente_consumidor(1500, 25, pe_base, qe_base)
        ep0 = excedente_productor(0, 15, pe_base, qe_base)

        ec1 = excedente_consumidor(1500, 25, pu, q_sub)
        ep1 = excedente_productor(0, 15, pe_emp, q_sub)

        gasto = sub * q_sub

        bt0 = ec0 + ep0
        bt1 = ec1 + ep1 - gasto

        datos_subsidios.append([
            sub,
            round(pu, 2),
            round(pe_emp, 2),
            round(q_sub, 2),
            round(gasto, 2),
            round(bt1 - bt0, 2)
        ])

    df_comp_subsidios = pd.DataFrame(
        datos_subsidios,
        columns=[
            "Subsidio",
            "Precio usuarios",
            "Precio empresas",
            "Cantidad",
            "Gasto Gobierno",
            "Variación bienestar"
        ]
    )

    st.dataframe(df_comp_subsidios, use_container_width=True)

    st.subheader("Comparación de precios máximos")

    precios_maximos = [70, 60, 50, 40, 30]

    datos_pm = []

    pe_base_pm, qe_base_pm = equilibrio(
        1800,
        20,
        0,
        12
    )

    ec0_pm = excedente_consumidor(1800, 20, pe_base_pm, qe_base_pm)
    ep0_pm = excedente_productor(0, 12, pe_base_pm, qe_base_pm)
    bt0_pm = ec0_pm + ep0_pm

    for pm in precios_maximos:
        qd = 1800 - 20 * pm
        qo = 0 + 12 * pm
        esc = max(qd - qo, 0)
        qt = min(qd, qo)

        ec1_pm = excedente_consumidor(1800, 20, pm, qt)
        ep1_pm = excedente_productor(0, 12, pm, qt)
        bt1_pm = ec1_pm + ep1_pm

        datos_pm.append([
            pm,
            round(qd, 2),
            round(qo, 2),
            round(esc, 2),
            round(bt1_pm - bt0_pm, 2)
        ])

    df_comp_pm = pd.DataFrame(
        datos_pm,
        columns=[
            "Precio máximo",
            "Cantidad demandada",
            "Cantidad ofrecida",
            "Escasez",
            "Variación bienestar"
        ]
    )

    st.dataframe(df_comp_pm, use_container_width=True)

# ==================================================
# SOLAPA 4 - PROYECTO
# ==================================================

with tab4:

    st.header("ℹ️ Acerca del proyecto")

    st.markdown("""
    ### Objetivo

    La aplicación tiene como objetivo analizar el impacto de políticas públicas
    en una economía cerrada, considerando dos casos principales:

    1. Subsidio al transporte público.
    2. Precio máximo aplicado al mercado de alquileres.

    ### Funcionalidades incluidas

    - Cálculo del equilibrio inicial.
    - Cálculo de precios y cantidades luego de la intervención.
    - Excedente del consumidor antes y después.
    - Excedente del productor antes y después.
    - Gasto total del Gobierno en el caso del subsidio.
    - Escasez generada en el caso del precio máximo.
    - Variación del bienestar social.
    - Tablas resumen.
    - Gráficos del mercado.
    - Comparación de escenarios.
    - Exportación de resultados a Excel.

    ### Herramientas utilizadas

    - Python.
    - Streamlit.
    - Pandas.
    - NumPy.
    - Plotly.
    - OpenPyXL.
    """)
