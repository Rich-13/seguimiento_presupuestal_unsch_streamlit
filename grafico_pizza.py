import pandas as pd
import plotly.express as px

def crear_grafico_cn(df):
    df_ff = df.groupby('NOMBRE_FF').agg(
        total_monto = ('MNTO_TOTAL', 'sum')
    ).reset_index()

    colors = ['#0077b6','#1A4D83']
    fig=px.pie(df_ff,
            values='total_monto',
            names = 'NOMBRE_FF',
            title = 'Presupuesto Progrmado por Fuente de Financiamiento',
            color_discrete_sequence=colors
    )

    fig.update_layout(yaxis_title='Fuente de Financiamiento',xaxis_title='Monto', showlegend=False)
    #fig.update_traces(textposition = 'outside', textinfo = 'label + percent',insidetextfont=dict(size = 12))
    fig.update_traces(textposition = 'outside', textinfo = 'none',texttemplate="%{label}<br>%{percent}",insidetextfont=dict(size = 12))
    return fig

def crear_grafico_ep(df):
    ejecucion_fuente_financiamiento = df.groupby('nombre_ff').agg(
        total_ff = ('monto_nacional','sum')
    ).reset_index()

    colors = ['#0077b6', '#1A4D83', '#063970', '#2f567D']
    fig = px.pie(ejecucion_fuente_financiamiento,
        values = 'total_ff',
        names = 'nombre_ff',
        title = 'Ejecución por Fuente de Financiamiento',
        color_discrete_sequence=colors
    )

    fig.update_layout(yaxis_title = 'Fuente de Financiamiento',xaxis_title='Ejecución Presupuestal', showlegend=False)
    #fig.update_traces(textposition = 'outside', textinfo = 'percent+label',insidetextfont=dict(size = 12))
    fig.update_traces(textposition = 'outside', textinfo = 'none',texttemplate="%{label}<br>%{percent}",insidetextfont=dict(size = 12))

    return fig


