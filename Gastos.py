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


# In[ ]:




