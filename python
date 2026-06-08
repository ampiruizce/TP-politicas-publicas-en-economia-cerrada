import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Políticas Públicas en Economía Cerrada",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Políticas Públicas en Economía Cerrada")
st.markdown(
    """
    **Trabajo Práctico N°2 - Economía para Ingenieros**

    Integrantes:
    - Amparo Ruiz
    - Candelaria López
    - Avila
    """
)

# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------

def equilibrio(a, b, c, d):
    pe = (a - c) / (b + d)
    qe = a - b * pe
    return pe, qe


def excedente_consumidor(a, b, pe, qe):
    precio_reserva = a / b
    return ((precio_reserva - pe) * qe) / 2


def excedente_productor(c, d, pe, qe):
    precio_minimo = -c / d
    return ((pe - precio_minimo) * qe) / 2


def bienestar(ec, ep):
    return ec + ep


def equilibrio_subsidio(a, b, c, d, s):
    pd = (a - c - d * s) / (b + d)
    po = pd + s
    q = a - b * pd
    return pd, po, q


def graficar_subsidio(a, b, c, d, s):

    pe, qe = equilibrio(a, b, c, d)
    pd, po, qs = equilibrio_subsidio(a, b, c, d, s)

    pmax = max(pe, po) * 1.5 + 10

    precios = np.linspace(0, pmax, 300)

    demanda = a - b * precios
    oferta = c + d * precios
    oferta_sub = c + d * (precios + s)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(demanda, precios, label="Demanda")
    ax.plot(oferta, precios, label="Oferta")
    ax.plot(oferta_sub, precios, label="Oferta con subsidio")

    ax.scatter(qe, pe)
    ax.scatter(qs, pd)

    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Precio")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


def graficar_precio_maximo(a, b, c, d, pmax):

    pe, qe = equilibrio(a, b, c, d)

    precios = np.linspace(0, max(pe * 1.5, pmax * 1.5) + 10, 300)

    demanda = a - b * precios
    oferta = c + d * precios

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(demanda, precios, label="Demanda")
    ax.plot(oferta, precios, label="Oferta")

    ax.axhline(
        y=pmax,
        linestyle="--",
        label=f"Precio Máximo = {pmax}"
    )

    ax.scatter(qe, pe)

    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Precio")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Menú")

opcion = st.sidebar.radio(
    "Seleccione una política",
    ["Subsidio", "Precio Máximo"]
)

# --------------------------------------------------
# SUBSIDIO
# --------------------------------------------------

if opcion == "Subsidio":

    st.header("🚍 Subsidio al Transporte Público")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input("Parámetro a", value=1500.0)
        b = st.number_input("Parámetro b", value=25.0)

    with col2:
        c = st.number_input("Parámetro c", value=0.0)
        d = st.number_input("Parámetro d", value=15.0)

    s = st.number_input(
        "Subsidio por unidad",
        value=8.0
    )

    pe, qe = equilibrio(a, b, c, d)

    ec0 = excedente_consumidor(a, b, pe, qe)
    ep0 = excedente_productor(c, d, pe, qe)
    bt0 = bienestar(ec0, ep0)

    pd, po, qf = equilibrio_subsidio(a, b, c, d, s)

    ec1 = excedente_consumidor(a, b, pd, qf)
    ep1 = excedente_productor(c, d, po, qf)

    gasto = s * qf

    bt1 = ec1 + ep1 - gasto

    st.subheader("Situación Inicial")

    st.write(f"Precio de equilibrio: {pe:.2f}")
    st.write(f"Cantidad de equilibrio: {qe:.2f}")
    st.write(f"Excedente consumidor: {ec0:.2f}")
    st.write(f"Excedente productor: {ep0:.2f}")
    st.write(f"Bienestar total: {bt0:.2f}")

    st.subheader("Situación con Subsidio")

    st.write(f"Precio pagado por consumidores: {pd:.2f}")
    st.write(f"Precio recibido por productores: {po:.2f}")
    st.write(f"Cantidad: {qf:.2f}")

    st.write(f"Excedente consumidor: {ec1:.2f}")
    st.write(f"Excedente productor: {ep1:.2f}")

    st.write(f"Gasto del gobierno: {gasto:.2f}")
    st.write(f"Bienestar social: {bt1:.2f}")

    variacion = bt1 - bt0

    if variacion > 0:
        st.success(
            f"El bienestar aumenta en {variacion:.2f}"
        )
    else:
        st.error(
            f"El bienestar disminuye en {abs(variacion):.2f}"
        )

    st.subheader("Gráfico")

    graficar_subsidio(a, b, c, d, s)

    st.subheader("Simulación Automática")

    subsidios = [0, 5, 10, 15, 20]

    resultados = []

    for sub in subsidios:

        pd_sim, po_sim, q_sim = equilibrio_subsidio(
            a, b, c, d, sub
        )

        ec_sim = excedente_consumidor(
            a, b, pd_sim, q_sim
        )

        ep_sim = excedente_productor(
            c, d, po_sim, q_sim
        )

        gasto_sim = sub * q_sim

        bt_sim = ec_sim + ep_sim - gasto_sim

        resultados.append(
            [
                sub,
                round(q_sim, 2),
                round(gasto_sim, 2),
                round(bt_sim, 2)
            ]
        )

    df = pd.DataFrame(
        resultados,
        columns=[
            "Subsidio",
            "Cantidad",
            "Gasto Público",
            "Bienestar"
        ]
    )

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar simulación",
        csv,
        "simulacion_subsidios.csv",
        "text/csv"
    )

# --------------------------------------------------
# PRECIO MÁXIMO
# --------------------------------------------------

else:

    st.header("🏠 Precio Máximo a los Alquileres")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "Parámetro a",
            value=1800.0
        )
        b = st.number_input(
            "Parámetro b",
            value=20.0
        )

    with col2:
        c = st.number_input(
            "Parámetro c",
            value=0.0
        )
        d = st.number_input(
            "Parámetro d",
            value=12.0
        )

    pmax = st.number_input(
        "Precio Máximo",
        value=40.0
    )

    pe, qe = equilibrio(a, b, c, d)

    ec0 = excedente_consumidor(a, b, pe, qe)
    ep0 = excedente_productor(c, d, pe, qe)
    bt0 = bienestar(ec0, ep0)

    qd = a - b * pmax
    qo = c + d * pmax

    escasez = max(qd - qo, 0)

    cantidad_transada = min(qd, qo)

    ec1 = ((a / b) - pmax) * cantidad_transada / 2

    ep1 = (
        (pmax - (-c / d))
        * cantidad_transada
        / 2
    )

    bt1 = ec1 + ep1

    st.subheader("Equilibrio Inicial")

    st.write(f"Precio equilibrio: {pe:.2f}")
    st.write(f"Cantidad equilibrio: {qe:.2f}")

    st.subheader("Con Precio Máximo")

    st.write(f"Cantidad demandada: {qd:.2f}")
    st.write(f"Cantidad ofrecida: {qo:.2f}")
    st.write(f"Escasez: {escasez:.2f}")

    st.write(f"Excedente consumidor: {ec1:.2f}")
    st.write(f"Excedente productor: {ep1:.2f}")
    st.write(f"Bienestar social: {bt1:.2f}")

    variacion = bt1 - bt0

    if variacion > 0:
        st.success(
            f"El bienestar aumenta en {variacion:.2f}"
        )
    else:
        st.error(
            f"El bienestar disminuye en {abs(variacion):.2f}"
        )

    st.subheader("Gráfico")

    graficar_precio_maximo(
        a,
        b,
        c,
        d,
        pmax
    )

    st.subheader("Simulación Automática")

    precios = [70, 60, 50, 40, 30]

    resultados = []

    for pm in precios:

        qd_pm = a - b * pm
        qo_pm = c + d * pm

        resultados.append(
            [
                pm,
                round(qd_pm, 2),
                round(qo_pm, 2),
                round(max(qd_pm - qo_pm, 0), 2)
            ]
        )

    df = pd.DataFrame(
        resultados,
        columns=[
            "Precio Máximo",
            "Cantidad Demandada",
            "Cantidad Ofrecida",
            "Escasez"
        ]
    )

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar simulación",
        csv,
        "simulacion_precios_maximos.csv",
        "text/csv"
    )

st.markdown("---")
st.caption(
    "Economía para Ingenieros - UNSTA | TP N°2"
)
