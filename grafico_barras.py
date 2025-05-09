import pandas as pd
import plotly.express as px

def generar_grafico_top10(df):
    top10_cc = df.groupby('NOMBRE_DEPEND')[['monto_nacional']].sum().sort_values('monto_nacional',ascending = True).reset_index()

    fig = px.bar(top10_cc.tail(10),
        x = 'monto_nacional',
        y = 'NOMBRE_DEPEND',
        text = 'monto_nacional',
        title = 'Los 10 Centros de Costos con Mayor Ejecución Presupuestal'
    )
    fig.update_layout(yaxis_title = 'Centro de Costo', xaxis_title='Ejecución Presupuestal',showlegend=False)

    return fig

def generar_grafico_boottom10(df):
    boottom10_cc = df.groupby('NOMBRE_DEPEND')[['monto_nacional']].sum().sort_values('monto_nacional',ascending = True).reset_index()

    fig = px.bar(boottom10_cc.head(10),
        x = 'monto_nacional',
        y = 'NOMBRE_DEPEND',
        text = 'monto_nacional',
        title = 'Los 10 Centros de Costos con Menor Ejecución Presupuestal'
    )
    fig.update_layout(yaxis_title = 'Centro de Costo', xaxis_title='Ejecución Presupuestal',showlegend=False)

    return fig