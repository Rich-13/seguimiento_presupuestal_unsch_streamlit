import pandas as pd
import numpy as np
import streamlit as st
import grafico_lineas as grafln
import grafico_pizza as grafpz
import grafico_barras as grafbrr
import streamlit.components.v1 as com
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
st.set_page_config(layout='wide')
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title('Seguimiento Presupuestal 2025 :bar_chart: ')
df_seguimiento = pd.read_excel('https://raw.githubusercontent.com/Rich-13/seguimiento_presupuestal_unsch_streamlit/main/data/cn_mes_2025.xlsx')
df_ejecucion = pd.read_excel('https://raw.githubusercontent.com/Rich-13/seguimiento_presupuestal_unsch_streamlit/main/data/ep_mes_2025.xlsx')
tab_titles = [
    "EJECUCIÓN PRESUPUESTAL 2025",
    "CUADRO DE NECESIDADES 2025",
    "REGISTRO DE SEGUIMIENTO 2025"
]
tabs = st.tabs(tab_titles)

#Configurando Filtros
st.sidebar.image('assets/logoUNSCH.png')
st.sidebar.title('Filtros')
lista_cc = sorted(list(df_seguimiento['NOMBRE_DEPEND'].unique()))
lista_tb = sorted(list(df_ejecucion['TIPO_BIEN'].unique()))
lista_ff = sorted(list(df_ejecucion['nombre_ff'].unique()))

#Diccionario para B y S
diccionario_tb = {'S': 'Servicio', 'B': 'Bien','P': 'Planilla(2.2.)', 'V': 'Pasajes y Viáticos','C':'Caja Chica'}

#selectbox
nombres_cc = st.sidebar.selectbox('Centro de Costo',lista_cc,index=None,placeholder="Ingrese el Centro de Costo")
nombres_tb = st.sidebar.selectbox('Tipo de Bien',lista_tb,format_func=lambda x: diccionario_tb.get(x, x),index=None,placeholder="Ingrese el Bien")
nombres_ff = st.sidebar.selectbox('Fuente de Financiamiento',lista_ff,index=None,placeholder="Ingrese la Fuente de Financiamiento")

with tabs[0]:
    st.header('Ejecución Presupuestal')

    #Filtrando los datos
    if nombres_cc:
        df_ejecucion = df_ejecucion[df_ejecucion['NOMBRE_DEPEND']==nombres_cc]

    if nombres_tb:
        df_ejecucion = df_ejecucion[df_ejecucion['TIPO_BIEN']==nombres_tb]

    if nombres_ff:
        df_ejecucion = df_ejecucion[df_ejecucion['nombre_ff']==nombres_ff]

    #Ejecución por tipo
    df_ejecucion_bien = df_ejecucion[df_ejecucion['TIPO_BIEN'] =='B']
    df_ejecucion_servicio = df_ejecucion[df_ejecucion['TIPO_BIEN'] =='S']
    df_ejecucion_viaticos = df_ejecucion[df_ejecucion['TIPO_BIEN'] =='V']
    df_ejecucion_planillas = df_ejecucion[df_ejecucion['TIPO_BIEN'] =='P']
    df_ejecucion_caja = df_ejecucion[df_ejecucion['TIPO_BIEN'] =='C']

    #Llamar Gráfico
    graf_lineas_ep = grafln.crear_grafico_ep(df_ejecucion)
    graf_pizza_ep = grafpz.crear_grafico_ep(df_ejecucion)
    graf_barras_ep_top = grafbrr.generar_grafico_top10(df_ejecucion)
    graf_barras_ep_bootom = grafbrr.generar_grafico_boottom10(df_ejecucion)
    #Columnas
    col1, col2 = st.columns(2)
    with col1:
        st.metric('**Presupuesto Ejecutado:**', f"S/ {(df_ejecucion['monto_nacional'].sum()):,.2f}")
        st.metric('**Caja Chica:**', f"S/ {(df_ejecucion_caja['monto_nacional'].sum()):,.2f}")
        st.metric('**Planilla y Pensiones (2.2.):**', f"S/ {(df_ejecucion_planillas['monto_nacional'].sum()):,.2f}")
        st.plotly_chart(graf_pizza_ep, use_container_width=True)
        st.plotly_chart(graf_barras_ep_top, use_container_width=True)
        
    with col2:
        
        st.metric('**Bien:**', f"S/ {(df_ejecucion_bien['monto_nacional'].sum()):,.2f}")
        st.metric('**Servicio:**', f"S/ {(df_ejecucion_servicio['monto_nacional'].sum()):,.2f}")
        st.metric('**Pasajes y Viáicos:**', f"S/ {(df_ejecucion_viaticos['monto_nacional'].sum()):,.2f}")
        st.plotly_chart(graf_lineas_ep, use_container_width=True)
        st.plotly_chart(graf_barras_ep_bootom, use_container_width=True)

    month_order_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_translation = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

    df_ejecucion['mes'] = df_ejecucion['FECHA_DEVENGADO'].dt.month_name()
    df_ejecucion = df_ejecucion[['nombre_tarea','nombre_ff','NOMBRE_CLASIF','NOMBRE_ITEM','mes','monto_nacional']]
    df_pivot_ep = df_ejecucion.pivot_table(index=['nombre_tarea','nombre_ff','NOMBRE_CLASIF','NOMBRE_ITEM'],columns='mes',values='monto_nacional',aggfunc='sum').reset_index()
    df_pivot_ep.columns.name = None
    df_pivot_ep = df_pivot_ep.fillna(0)

    #st.dataframe(df_pivot_ep)

    # Identificar automáticamente las columnas de meses presentes en df_pivot_ep
    df_pivot_ep.rename(columns=month_translation, inplace=True)

    #st.dataframe(df_pivot_ep)

    columnas_mes = [month for month in month_order_es if month in df_pivot_ep.columns]
    df_pivot_ep = df_pivot_ep[['nombre_tarea','nombre_ff','NOMBRE_CLASIF','NOMBRE_ITEM'] + columnas_mes]

    #st.dataframe(df_pivot_ep)

    # Crear el diccionario de agregación dinámicamente
    agg_dict = {month: 'sum' for month in columnas_mes}

    #(agg_dict)
    
    #totales_ep = df_pivot_ep.iloc[:, 1:].sum()
    #fila_totales_ep = pd.DataFrame([["TOTAL"] + totales_ep.tolist()], columns=df_pivot_ep.columns)
    #df_pivot_ep = pd.concat([fila_totales_ep, df_pivot_ep], ignore_index=True)
    df_datos_grupos_ep = []
    if agg_dict:
        df_datos_grupos_ep = df_pivot_ep.groupby(['nombre_tarea','nombre_ff','NOMBRE_CLASIF','NOMBRE_ITEM']).agg(agg_dict).reset_index()

        #df_datos_grupos_ep = df_datos_grupos_ep.sort_values('MNTO_TOTAL',ascending=False)
        gob1 = GridOptionsBuilder.from_dataframe(df_datos_grupos_ep)
        

        gob1.configure_default_column(group= True,
                                    value=True,
                                    enableRowGroup=True,
                                    aggFunc='sum',
                                    wrapText=True,
                                    autoHeight=True,

                                    valueFormatter="parseFloat(value.toLocaleString()).toFixed(2)'",                      
        )

        gob1.configure_column(
            field="nombre_tarea",
            hide=True,
            header_name="Nombre Tarea",
            width=150,
            #pinned='left',
            rowGroup=True,
            
        )
        gob1.configure_column(
            field="nombre_ff",
            hide=True,
            header_name="Nombre Tarea",
            width=150,
            #pinned='left',
            rowGroup=True,
            
        )

        gob1.configure_column(
            field="NOMBRE_CLASIF",
            hide=True,
            header_name="Clasificador",
            width=150,
            #pinned='left',
            rowGroup=True,
            
        )
        gob1.configure_column(
            field="NOMBRE_ITEM",
            hide=True,
            header_name="Item",
            width=150,
            #pinned='left',
            rowGroup=True,
            
        )
        for month in columnas_mes:
            gob1.configure_column(
                field=month,
                header_name=month,
                minWidth=100,
                width=100,  # Ancho ajustado
                valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
            )

        gob1.configure_grid_options(
            suppressAggFuncInHeader = True,
            #pinnedBottomRowData=[totales_row],
            autoGroupColumnDef = {
                "headerName": "Actividad Operativa",
                "minWidth": 500,  # Ancho mínimo de la columna "Group"
                "width": 500,     # Ajusta el ancho a tu gusto
                "pinned": "left",
                "cellRendererParams":{"suppressCount": True},

                },
        )

        gridOptions1 = gob1.build()
        st.markdown("**TABLA 01: EJECUCIÓN PRESUPUESTAL POR MES, 2025**")

        AgGrid(
            df_datos_grupos_ep,
            gridOptions=gridOptions1,
            height=500,
            width='100%',
            theme='streamlit',
            fit_columns_on_grid_load=True,
        )

        #st.dataframe(df_pivot_ep)
        #st.image('assets/trabajando.gif')
        #st.dataframe(df_ejecucion)
        #df_ejecucion = df_ejecucion[df_ejecucion['NOMBRE_DEPEND']==nombres_cc]
        #st.dataframe(df_ejecucion)

with tabs[1]:

    st.header('Cuadro de Necesidades')

    #Crear unidades por mes
    for mes in range(1, 13):
        mnto_col = f'MNTO_{mes:02}'
        cant_col = f'CANT_{mes:02}'
        uni_col = f'UNI_{mes:02}'
        
        # Añadir condición para cuando tanto el numerador como el denominador sean cero
        df_seguimiento[uni_col] = np.where(
            (df_seguimiento[mnto_col] == 0) & (df_seguimiento[cant_col] == 0), 
            0,  # Resultado cuando ambos son 0
            np.where(
                df_seguimiento['TIPO_BIEN'] == 'S', 
                df_seguimiento[mnto_col] / df_seguimiento[cant_col], 
                df_seguimiento[cant_col]
            )
        )

    #Filtrando los datos
    if nombres_cc:
        df_seguimiento = df_seguimiento[df_seguimiento['NOMBRE_DEPEND']==nombres_cc]

    if nombres_tb:
        df_seguimiento = df_seguimiento[df_seguimiento['TIPO_BIEN']==nombres_tb]

    if nombres_ff:
        df_seguimiento = df_seguimiento[df_seguimiento['NOMBRE_FF']==nombres_ff]

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

    df_datos_grupos = df_seguimiento.groupby(['nombre_tarea','NOMBRE_CLASI','NOMBRE_ITEM']).agg({'MNTO_01':'sum','UNI_01':'sum','MNTO_02':'sum','UNI_02':'sum','MNTO_03':'sum','UNI_03':'sum','MNTO_04':'sum','UNI_04':'sum','MNTO_05':'sum','UNI_05':'sum','MNTO_06':'sum','UNI_06':'sum','MNTO_07':'sum','UNI_07':'sum','MNTO_08':'sum','UNI_08':'sum','MNTO_09':'sum','UNI_09':'sum','MNTO_10':'sum','UNI_10':'sum','MNTO_11':'sum','UNI_11':'sum','MNTO_12':'sum','UNI_12':'sum','MNTO_TOTAL':'sum'}).reset_index()
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
        field="UNI_01",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
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
        field="UNI_02",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_03",
        header_name="Marzo",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_03",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_04",
        header_name="Abril",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_04",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_05",
        header_name="Mayo",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_05",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_06",
        header_name="Junio",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_06",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_07",
        header_name="Julio",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_07",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_08",
        header_name="Agosto",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_08",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_09",
        header_name="Setiembre",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_09",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_10",
        header_name="Octubre",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_10",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_11",
        header_name="Noviembre",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_11",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )

    gob2.configure_column(
        field="MNTO_12",
        header_name="Diciembre",
        minWidth=100,
        width=100,  # Ancho ajustado
        valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
    )
    gob2.configure_column(
        field="UNI_12",
        header_name="Un",
        minWidth=60,
        width=60,  # Ancho ajustado
        filter=False,
        #cellStyle={"backgroundColor": "#ffeb3b", "color": "black"},
        #valueFormatter="value.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })",
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
    st.markdown("**TABLA 02: CUADRO DE NECESIDADES POR MES, 2025**")
    AgGrid(
        df_datos_grupos,
        gridOptions=gridOptions,
        height=500,
        width='100%',
        theme='streamlit',
        fit_columns_on_grid_load=True,
    )

with tabs[2]:
    
    st.header('Guía para Registro de seguimiento')

    st.subheader("Ingreso al aplicativo", divider=True)
    st.link_button("IR AL APLICATIVO CEPLAN", "http://app.ceplan.gob.pe/POI2025/ingresar.aspx")
    
    st.subheader("Video Tutorial", divider=True)
    guidde_guia_ep= st.video("https://storage.app.guidde.com/v0/b/guidde-production.appspot.com/o/uploads%2FJQs1ODfyRDNRy4bYXv5KOds2pEg1%2Fg7GEx5YzXjTJbtxLYQQKuc.mp4?alt=media&token=debb47a4-2480-46da-b610-0b56bf08361f")

    st.subheader("Material de Apoyo", divider=True)
    canva_guia_ep="""
    <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
    <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;" src="https://www.canva.com/design/DAGiZfYEPro/kqDPenFePEKAi50WK3AQpw/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
    </iframe>
    </div>
    <a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGiZfYEPro&#x2F;kqDPenFePEKAi50WK3AQpw&#x2F;view?utm_content=DAGiZfYEPro&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">Blue Modern Travel Guide Presentation</a> de Richard Yancce Tineo
    """
    st.markdown(canva_guia_ep, unsafe_allow_html=True)