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