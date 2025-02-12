import pandas as pd
import streamlit as st
import grafico_lineas as grafln
import grafico_pizza as grafpz
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


st.set_page_config(layout='wide')
st.title('Seguimiento Presupuestal 2025 :bar_chart: ')
st.header('1. Cuadro de Necesidades')

df_seguimiento = pd.read_excel('https://raw.githubusercontent.com/Rich-13/seguimiento_presupuestal_unsch/main/cn_mes_2025.xlsx')


#Configurando Filtros
st.sidebar.title('Filtros')
lista_cc = sorted(list(df_seguimiento['NOMBRE_DEPEND'].unique()))
nombres_cc = st.sidebar.selectbox('Centro de Costo',lista_cc,index=None,placeholder="Ingrese el Centro de Costo")

#Filtrando los datos
if nombres_cc:
    df_seguimiento = df_seguimiento[df_seguimiento['NOMBRE_DEPEND']==nombres_cc]

#Ejecución por tipo
df_asignacion_bien = df_seguimiento[df_seguimiento['TIPO_BIEN'] =='B']
df_asignacion_servicio = df_seguimiento[df_seguimiento['TIPO_BIEN'] =='S']

#Llamar Gráfico
graf_lineas = grafln.crear_grafico_cn(df_seguimiento)
graf_pizza = grafpz.crear_grafico_cn(df_seguimiento)

#Columnas
col1, col2 = st.columns(2)
with col1:
    st.metric('**Presupuesto Programado:**', f"S/ {(df_seguimiento['MNTO_TOTAL'].sum()):,.2f}")
    st.metric('**Bienes Programado:**', f"{(df_asignacion_bien['CANT_TOTAL'].sum()):,.0f}")
    st.plotly_chart(graf_pizza, use_container_width=True)

with col2:
    st.metric('**Bien:**', f"S/ {(df_asignacion_bien['MNTO_TOTAL'].sum()):,.2f}")
    st.metric('**Servicio:**', f"S/ {(df_asignacion_servicio['MNTO_TOTAL'].sum()):,.2f}")
    
    st.plotly_chart(graf_lineas, use_container_width=True)

df_datos_grupos = df_seguimiento.groupby(['nombre_tarea','NOMBRE_CLASI','NOMBRE_ITEM']).agg({'MNTO_01':'sum','CANT_01':'sum','MNTO_02':'sum','MNTO_03':'sum','MNTO_04':'sum','MNTO_05':'sum','MNTO_06':'sum','MNTO_07':'sum','MNTO_08':'sum','MNTO_09':'sum','MNTO_10':'sum','MNTO_11':'sum','MNTO_12':'sum','MNTO_TOTAL':'sum'}).reset_index()
df_datos_grupos = df_datos_grupos.sort_values('MNTO_TOTAL',ascending=False)
gob2 = GridOptionsBuilder.from_dataframe(df_datos_grupos)

gob2.configure_default_column(group= True,
                              value=True,
                              enableRowGroup=True,
                              aggFunc='sum',
                              wrapText=True,
                              autoHeight=True,

                              valueFormatter="parseFloat(value.toLocaleString()).toFixed(2)'",                      
)


gob2.configure_column(
    field="nombre_tarea",
    hide=True,
    header_name="Nombre Tarea",
    width=150,
    #pinned='left',
    rowGroup=True,
    
)

gob2.configure_column(
    field="NOMBRE_CLASI",
    hide=True,
    header_name="Clasificador",
    width=150,
    #pinned='left',
    rowGroup=True,
    
)
gob2.configure_column(
    field="NOMBRE_ITEM",
    hide=True,
    header_name="Item",
    width=150,
    #pinned='left',
    rowGroup=True,
    
)

gob2.configure_column(
    field="MNTO_01",
    header_name="Enero",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)
gob2.configure_column(
    field="CANT_01",
    header_name="Ca",
    minWidth=60,
    width=60,  # Ancho ajustado
    filter=False,
    cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
    #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_02",
    header_name="Febrero",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_03",
    header_name="Marzo",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_04",
    header_name="Abril",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_05",
    header_name="Mayo",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_06",
    header_name="Junio",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_07",
    header_name="Julio",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_08",
    header_name="Agosto",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_09",
    header_name="Setiembre",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_10",
    header_name="Octubre",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_11",
    header_name="Noviembre",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_12",
    header_name="Diciembre",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

gob2.configure_column(
    field="MNTO_TOTAL",
    header_name="MNTO TOTAL",
    minWidth=100,
    width=100,  # Ancho ajustado
    valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
)

# Calcular los totales para cada columna
totales = df_datos_grupos[['MNTO_01', 'MNTO_02', 'MNTO_03', 'MNTO_04', 'MNTO_05', 'MNTO_06', 'MNTO_07', 'MNTO_08', 'MNTO_09', 'MNTO_10', 'MNTO_11', 'MNTO_12', 'MNTO_TOTAL']].sum()

# Crear una fila con las sumas
totales_row = {'nombre_tarea': 'Totales', 'NOMBRE_CLASI': '', 'NOMBRE_ITEM': '', **totales.to_dict()}

# Usar pd.concat() para agregar la fila de totales al DataFrame
df_datos_grupos = pd.concat([df_datos_grupos, pd.DataFrame([totales_row])], ignore_index=True)

gob2.configure_grid_options(
    suppressAggFuncInHeader = True,
    pinnedBottomRowData=[totales_row],
    autoGroupColumnDef = {
        "headerName": "Actividad Operativa",
        "minWidth": 500,  # Ancho mínimo de la columna "Group"
        "width": 500,     # Ajusta el ancho a tu gusto
        "pinned": "left",
        "cellRendererParams":{"suppressCount": True},

        },
)

gridOptions = gob2.build()
st.markdown("**TABLA 01: CUADRO DE NECESIDADES MENSUALIZADO 2025**")
AgGrid(
    df_datos_grupos,
    gridOptions=gridOptions,
    height=500,
    width='100%',
    theme='streamlit',
    fit_columns_on_grid_load=True,
)

st.header('2. Ejecución Presupuestal')


st.dataframe(df_seguimiento)