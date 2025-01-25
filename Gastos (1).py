#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st


# In[7]:


#pip install --upgrade streamlit


# In[3]:


# Título de la app
st.title("Gestión de gastos personales")

# Sección de ingreso de datos
st.header("Registrar ingreso o gasto")
tipo = st.radio("Tipo de movimiento:", ["Ingreso", "Gasto"])
monto = st.number_input("Monto (€):", min_value=0.0, step=0.01)
categoria = st.selectbox("Categoría:", ["Comida", "Transporte", "Compras", "Ocio", "Otros"])
comentario = st.text_input("Comentario (opcional):")

# Botón para registrar
if st.button("Registrar"):
    with open("gastos.csv", "a") as file:
        file.write(f"{tipo},{monto},{categoria},{comentario}\n")
    st.success("Movimiento registrado con éxito.")

# Mostrar historial de gastos
st.header("Historial de movimientos")
try:
    with open("gastos.csv", "r") as file:
        datos = file.readlines()
        for linea in datos:
            st.text(linea.strip())
except FileNotFoundError:
    st.warning("No hay movimientos registrados aún.")

# Mostrar balance
st.header("Balance actual")
try:
    ingresos = 0
    gastos = 0
    with open("gastos.csv", "r") as file:
        for linea in file:
            tipo, monto, _, _ = linea.strip().split(",")
            if tipo == "Ingreso":
                ingresos += float(monto)
            elif tipo == "Gasto":
                gastos += float(monto)
    st.metric("Total ingresos (€):", f"{ingresos:.2f}")
    st.metric("Total gastos (€):", f"{gastos:.2f}")
    st.metric("Balance (€):", f"{ingresos - gastos:.2f}")
except FileNotFoundError:
    st.warning("No hay datos para calcular el balance.")


# In[9]:


import pandas as pd
import plotly.express as px

# Mostrar gráficos
st.header("Gráficos de balance y gastos")

# Cargar datos del CSV
try:
    data = pd.read_csv("gastos.csv", names=["Tipo", "Monto", "Categoría", "Comentario"])
    data["Monto"] = data["Monto"].astype(float)

    # Gráfico de barras por categoría
    gastos_por_categoria = data[data["Tipo"] == "Gasto"].groupby("Categoría")["Monto"].sum().reset_index()
    fig_gastos = px.bar(gastos_por_categoria, x="Categoría", y="Monto", title="Gastos por categoría", text="Monto")
    st.plotly_chart(fig_gastos)

    # Gráfico de pastel para balance general
    balance = data.groupby("Tipo")["Monto"].sum().reset_index()
    fig_balance = px.pie(balance, names="Tipo", values="Monto", title="Distribución de ingresos y gastos")
    st.plotly_chart(fig_balance)
except FileNotFoundError:
    st.warning("No hay datos suficientes para generar gráficos.")


# In[13]:


#pip install streamlit-calendar pandas


# In[18]:


import pandas as pd
import os

# Intentar cargar el archivo gastos.csv
if os.path.exists("gastos.csv"):
    data = pd.read_csv("gastos.csv", names=["Tipo", "Monto", "Categoría", "Comentario"])
    data["Monto"] = data["Monto"].astype(float)
else:
    st.warning("No se encontró el archivo 'gastos.csv'. Por favor, registra algún gasto o ingreso primero.")
    data = pd.DataFrame(columns=["Tipo", "Monto", "Categoría", "Comentario"])


# In[20]:


from datetime import datetime

st.header("Gestión mensual de ingresos y gastos")

# Selección de mes y año
year = st.selectbox("Año:", [2023, 2024, 2025], index=1)
month = st.selectbox("Mes:", range(1, 13), format_func=lambda x: datetime(2022, x, 1).strftime("%B"))

# Filtrar datos por mes
try:
    data["Fecha"] = pd.to_datetime(data["Comentario"], errors="coerce")  # Asume que hay fechas en comentarios
    data_mes = data[(data["Fecha"].dt.year == year) & (data["Fecha"].dt.month == month)]

    # Mostrar balance del mes seleccionado
    st.subheader(f"Movimientos de {datetime(2022, month, 1).strftime('%B')} {year}")
    st.table(data_mes)

    # Balance mensual
    ingresos_mes = data_mes[data_mes["Tipo"] == "Ingreso"]["Monto"].sum()
    gastos_mes = data_mes[data_mes["Tipo"] == "Gasto"]["Monto"].sum()
    st.metric("Ingresos mensuales (€):", f"{ingresos_mes:.2f}")
    st.metric("Gastos mensuales (€):", f"{gastos_mes:.2f}")
    st.metric("Balance mensual (€):", f"{ingresos_mes - gastos_mes:.2f}")
except KeyError:
    st.warning("No hay datos para este mes.")


# In[22]:


if not data.empty:  # Verifica si hay datos cargados
    # Filtrar por mes y año
    data["Fecha"] = pd.to_datetime(data["Comentario"], errors="coerce")  # Fecha desde los comentarios
    data_mes = data[(data["Fecha"].dt.year == year) & (data["Fecha"].dt.month == month)]

    if not data_mes.empty:
        # Mostrar movimientos del mes
        st.subheader(f"Movimientos de {datetime(2022, month, 1).strftime('%B')} {year}")
        st.table(data_mes)

        # Balance mensual
        ingresos_mes = data_mes[data_mes["Tipo"] == "Ingreso"]["Monto"].sum()
        gastos_mes = data_mes[data_mes["Tipo"] == "Gasto"]["Monto"].sum()
        st.metric("Ingresos mensuales (€):", f"{ingresos_mes:.2f}")
        st.metric("Gastos mensuales (€):", f"{gastos_mes:.2f}")
        st.metric("Balance mensual (€):", f"{ingresos_mes - gastos_mes:.2f}")
    else:
        st.warning(f"No hay datos para {datetime(2022, month, 1).strftime('%B')} {year}.")
else:
    st.warning("Aún no se han registrado movimientos.")


# In[ ]:




