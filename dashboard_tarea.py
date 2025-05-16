import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar datos
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.set_page_config(page_title="Dashboard Supermarket Sales", layout="wide")
st.title("🏨 Dashboard de Ventas - Supermercado")

st.markdown("""
Este dashboard permite analizar el comportamiento de ventas y clientes en una cadena de tiendas de conveniencia. Usa visualizaciones interactivas para facilitar la toma de decisiones.
""")

# Sidebar
st.sidebar.header("Filtros")
branch = st.sidebar.multiselect("Selecciona Sucursal:", options=df['Branch'].unique(), default=df['Branch'].unique())
product_line = st.sidebar.multiselect("Selecciona Línea de Producto:", options=df['Product line'].unique(), default=df['Product line'].unique())
df_filtered = df[(df['Branch'].isin(branch)) & (df['Product line'].isin(product_line))]

# 1. Evolución de ventas totales
df_by_date = df_filtered.groupby('Date')['Total'].sum().reset_index()
st.subheader("1. Evolución de las Ventas Totales")
fig1 = px.line(df_by_date, x='Date', y='Total', title='Ventas Totales a lo largo del tiempo')
st.plotly_chart(fig1, use_container_width=True)

# 2. Ingresos por línea de producto
st.subheader("2. Ingresos por Línea de Producto")
df_product = df_filtered.groupby('Product line')['Total'].sum().reset_index().sort_values(by='Total', ascending=False)
fig2 = px.bar(df_product, x='Product line', y='Total', color='Product line', title='Ingresos por Línea de Producto')
st.plotly_chart(fig2, use_container_width=True)

# 3. Distribución de la calificación de clientes
st.subheader("3. Distribución de la Calificación de Clientes")
fig3, ax3 = plt.subplots()
sns.histplot(df_filtered['Rating'], kde=True, ax=ax3, color='skyblue')
ax3.set_title('Distribución de Calificación')
st.pyplot(fig3)

# 4. Comparación del gasto por tipo de cliente
st.subheader("4. Gasto Total por Tipo de Cliente")
fig4 = px.box(df_filtered, x='Customer type', y='Total', color='Customer type', title='Distribución del Gasto por Tipo de Cliente')
st.plotly_chart(fig4, use_container_width=True)

# 5. Relación entre COGS y Ganancia Bruta
st.subheader("5. Relación entre Costo de Bienes Vendidos y Ganancia Bruta")
fig5 = px.scatter(df_filtered, x='cogs', y='gross income', trendline="ols", title='COGS vs Ganancia Bruta')
st.plotly_chart(fig5, use_container_width=True)

# 6. Métodos de pago preferidos
st.subheader("6. Métodos de Pago Preferidos")
df_payment = df_filtered['Payment'].value_counts().reset_index()
df_payment.columns = ['Payment Method', 'Count']
fig6 = px.pie(df_payment, names='Payment Method', values='Count', title='Distribución de Métodos de Pago')
st.plotly_chart(fig6, use_container_width=True)

# 7. Análisis de correlación numérica
st.subheader("7. Correlación entre Variables Numéricas")
numeric_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.heatmap(df_filtered[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax7)
ax7.set_title('Matriz de Correlación')
st.pyplot(fig7)

# 8. Ingreso Bruto por Sucursal y Línea de Producto
st.subheader("8. Ingreso Bruto por Sucursal y Línea de Producto")
df_branch_income = df_filtered.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
fig8 = px.bar(df_branch_income, x='Branch', y='gross income', color='Product line', barmode='stack', title='Ingreso Bruto por Sucursal y Línea de Producto')
st.plotly_chart(fig8, use_container_width=True)

# Reflexión final
st.markdown("""
### 📊 Reflexiones
- Las ventas fluctúan según la fecha, lo que permite ajustar campañas de marketing estacionales.
- Hay diferencias marcadas en el ingreso por línea de producto, lo cual puede guiar decisiones de inventario.
- La correlación entre variables como `cogs`, `gross income` y `Total` respalda la consistencia del modelo de ingresos.
- La interactividad del dashboard permite explorar hipótesis y patrones sin necesidad de escribir código.
""")
