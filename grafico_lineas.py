import pandas as pd
import plotly.express as px

def crear_grafico_cn(df):
    
    # Sumar montos por mes
    montos_mensuales = df[[f'MNTO_{str(i).zfill(2)}' for i in range(1, 13)]].sum()

    # Definir etiquetas de los meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
             'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

    # Crear DataFrame para Plotly
    df_plot = pd.DataFrame({'Mes': meses, 'Monto': montos_mensuales})

    # Crear gráfica con Plotly
    fig = px.line(df_plot,
                x='Mes',
                y='Monto',
                markers=True,
                range_y = (0, df_plot.max()),
                title='Grafico 01: Presupuesto Programado por Mensual',
                #labels={'Monto': 'Monto (S/)', 'Mes': 'Meses'}
                )

    # Personalizar la gráfica
    fig.update_layout(xaxis_title="Meses", yaxis_title="Monto (S/)")

    return fig

def crear_grafico_ep(df):
    ejecucion_mensual = df.set_index('FECHA_DEVENGADO').groupby(pd.Grouper(freq = 'ME'))['monto_nacional'].sum().reset_index()
    ejecucion_mensual['Year'] = ejecucion_mensual['FECHA_DEVENGADO'].dt.year
    ejecucion_mensual['Month'] = ejecucion_mensual['FECHA_DEVENGADO'].dt.month_name()
    ejecucion_mensual = ejecucion_mensual[ejecucion_mensual['Year'] > 2024]
  

    fig = px.line(ejecucion_mensual,
        x = 'Month',
        y = 'monto_nacional',
        markers= True,
        range_y = (0,ejecucion_mensual.max()),
        color = 'Year',
        line_dash = 'Year',
        title = 'Ejecución Mensual'
        )
    fig.update_layout(yaxis_title = 'Ingresos (S/ )')

    return fig