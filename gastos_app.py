#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Título de la app
st.title("Gestión de gastos personales")

# 1. **Registrar ingreso o gasto**
st.header("Registrar ingreso o gasto")
tipo = st.radio("Tipo de movimiento:", ["Ingreso", "Gasto"])
monto = st.number_input("Monto (€):", min_value=0.0, step=0.01)
categoria = st.selectbox("Categoría:", ["Comida", "Transporte", "Compras", "Ocio", "Otros"])
comentario = st.text_input("Comentario (opcional):")

# Guardar los datos en un archivo CSV
if st.button("Registrar"):
    with open("gastos.csv", "a") as file:
        file.write(f"{tipo},{monto},{categoria},{comentario}\n")
    st.success("Movimiento registrado con éxito.")

# 2. **Cargar los datos del archivo CSV**
if os.path.exists("gastos.csv"):
    data = pd.read_csv("gastos.csv", names=["Tipo", "Monto", "Categoría", "Comentario"])
    data["Monto"] = data["Monto"].astype(float)
else:
    data = pd.DataFrame(columns=["Tipo", "Monto", "Categoría", "Comentario"])
    st.warning("No se encontró el archivo 'gastos.csv'. Por favor, registra algún movimiento primero.")

# 3. **Historial de movimientos**
st.header("Historial de movimientos")
if not data.empty:
    st.dataframe(data)
else:
    st.warning("No hay movimientos registrados aún.")

# 4. **Balance general**
st.header("Balance actual")
if not data.empty:
    ingresos = data[data["Tipo"] == "Ingreso"]["Monto"].sum()
    gastos = data[data["Tipo"] == "Gasto"]["Monto"].sum()
    st.metric("Total ingresos (€):", f"{ingresos:.2f}")
    st.metric("Total gastos (€):", f"{gastos:.2f}")
    st.metric("Balance (€):", f"{ingresos - gastos:.2f}")
else:
    st.warning("No hay datos para calcular el balance.")

# 5. **Gráficos**
st.header("Gráficos de balance y gastos")
if not data.empty:
    # Gráfico de barras por categoría
    gastos_por_categoria = data[data["Tipo"] == "Gasto"].groupby("Categoría")["Monto"].sum().reset_index()
    fig_gastos = px.bar(gastos_por_categoria, x="Categoría", y="Monto", title="Gastos por categoría", text="Monto")
    st.plotly_chart(fig_gastos)

    # Gráfico de pastel para balance general
    balance = data.groupby("Tipo")["Monto"].sum().reset_index()
    fig_balance = px.pie(balance, names="Tipo", values="Monto", title="Distribución de ingresos y gastos")
    st.plotly_chart(fig_balance)
else:
    st.warning("No hay datos suficientes para generar gráficos.")

# 6. **Gestión mensual**
st.header("Gestión mensual de ingresos y gastos")
year = st.selectbox("Año:", [2023, 2024, 2025], index=1)
month = st.selectbox("Mes:", range(1, 13), format_func=lambda x: datetime(2022, x, 1).strftime("%B"))

if not data.empty:
    # Crear columna de fecha desde el comentario (asumimos que el comentario tiene formato de fecha)
    data["Fecha"] = pd.to_datetime(data["Comentario"], errors="coerce")
    data_mes = data[(data["Fecha"].dt.year == year) & (data["Fecha"].dt.month == month)]

    if not data_mes.empty:
        st.subheader(f"Movimientos de {datetime(2022, month, 1).strftime('%B')} {year}")
        st.table(data_mes)

        # Mostrar balance mensual
        ingresos_mes = data_mes[data_mes["Tipo"] == "Ingreso"]["Monto"].sum()
        gastos_mes = data_mes[data_mes["Tipo"] == "Gasto"]["Monto"].sum()
        st.metric("Ingresos mensuales (€):", f"{ingresos_mes:.2f}")
        st.metric("Gastos mensuales (€):", f"{gastos_mes:.2f}")
        st.metric("Balance mensual (€):", f"{ingresos_mes - gastos_mes:.2f}")
    else:
        st.warning(f"No hay datos para {datetime(2022, month, 1).strftime('%B')} {year}.")
else:
    st.warning("No hay movimientos registrados para mostrar datos mensuales.")


# In[5]:





# In[ ]:




