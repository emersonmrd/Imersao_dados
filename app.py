import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Especificar o símbolo da ação e o período de tempo desejado
Simbolo = 'BTC-USD'
Periodo = '6mo'

# Coletando os dados
Dados = yf.download(Simbolo, period=Periodo)
Dados.columns = [f'{col[0]}' for col in Dados.columns]
Dados['Media_Movel'] = Dados['Close'].rolling(window=5).mean()

# Função para atualizar os dados com base no período selecionado
def atualizar_dados(periodo_selecionado):
    global Periodo, Dados
    valores_validos = ['max', 'ytd', '10y', '5y', '1y', '6mo', '3mo', '1mo', '5d', '1d']
    if periodo_selecionado in valores_validos:
        Periodo = periodo_selecionado

    Dados = yf.download(Simbolo, period=Periodo)
    Dados.columns = [f'{col[0]}' for col in Dados.columns]
    Dados['Media_Movel'] = Dados['Close'].rolling(window=5).mean()

# Layout do aplicativo
app = dash.Dash(
    __name__,
    title='Evento Dashboard',
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
        'https://fonts.googleapis.com/css2?family=Joan&family=Roboto:ital,wght@0,100;1,300&family=Source+Sans+Pro:ital,wght@0,400;1,300&display=swap'
    ]
)

# Gráfico Candlestick
Grafico_Candlestick = go.Figure(
    data=[
        go.Candlestick(
            x=Dados.index,
            open=Dados['Open'],
            high=Dados['High'],
            low=Dados['Low'],
            close=Dados['Close'],
            increasing_line_color='red',
            decreasing_line_color='green'
        )
    ]
)

Grafico_Candlestick.update_layout(
    xaxis_rangeslider_visible=False,
    title='Análise Fechamento',
    xaxis_title='Período',
    yaxis_title='Preço de Fechamento'
)

Grafico_Candlestick.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
)

# Gráfico de Linhas
Grafico_Linhas = go.Figure()

Grafico_Linhas.add_trace(go.Scatter(
    x=Dados.index,
    y=Dados['Media_Movel'],
    mode='lines',
    name='Média Móvel',
    line=dict(color='blue')
))

Grafico_Linhas.add_trace(go.Scatter(
    x=Dados.index,
    y=Dados['Close'],
    mode='lines',
    name='Fechamento',
    line=dict(color='green')
))

Grafico_Linhas.update_layout(
    title='Análise Média Móvel e Fechamento',
    xaxis_title='Período',
    yaxis_title='Preço',
    template='plotly_dark',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=9)
    )
)

# Layout do aplicativo
app.layout = html.Div(
    children=[
        html.Div(
            className='navbar navbar-expand-lg bg-primary',
            style={
                'height': 'fit-content',
                #'background': '#111111',
                'display': 'flex',
                'flex-direction': 'row',
                'align-items': 'center',
                'justify-content': 'space-between',
                'border-bottom': '1px solid #4b5460',
                'padding': '1rem 5rem',
                'width': '100%',
            },
            children=[
                html.Div(
                    className='banner-title',
                    children=[
                        html.H5(
                            ['Dashboard'],
                            style={
                                'font-family': 'open sans semi bold, sans-serif',
                                'font-weight': '500'
                            }
                        ),
                        html.H6('Análise BITCOIN')
                    ]
                ),
                html.Div(
                    className='banner-logo',
                    children=[
                        html.Img(src=app.get_asset_url('icone_bitcoin.png'), height='60px', alt='logo')
                    ]
                )
            ]
        ),
        html.Div(
            className="container",
            children=[
                html.Div(
                    [
                        html.Label("Selecione o período", style={'color': 'white'}),
                        dcc.Dropdown(
                            id='periodo-dropdown',
                            options=[
                                        {'label': '1 Dia', 'value': '1d'},
                                        {'label': '5 Dias', 'value': '5d'},
                                        {'label': '1 Mês', 'value': '1mo'},
                                        {'label': '3 Meses', 'value': '3mo'},
                                        {'label': '6 Meses', 'value': '6mo'},
                                        {'label': '1 Ano', 'value': '1y'},
                                        {'label': '5 Anos', 'value': '5y'},
                                        {'label': '10 Anos', 'value': '10y'},
                                        {'label': 'YTD (Ano até a data atual)', 'value': 'ytd'},
                                        {'label': 'Máximo (Desde o início dos dados)', 'value': 'max'}
                            ],
                            value='6mo',
                            clearable=False,
                            style={ 'color': 'black'},
                            className='custom-dropdown'
                        ),
                    
                    ],
                    className="my-4"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='candlestick-chart',
                            figure=Grafico_Candlestick
                        )
                    ],
                    className="my-4"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='graph2',
                            figure=Grafico_Linhas
                        )
                    ],
                    className="my-4"
                ),
            ]
        )
    ]
)


@app.callback(
    Output('candlestick-chart', 'figure'),
    Output('graph2', 'figure'),
    Input('periodo-dropdown', 'value')
)


def atualizar_graficos(periodo_selecionado):
    atualizar_dados(periodo_selecionado)

    Grafico_Candlestick = go.Figure(
        data=[
            go.Candlestick(
                x=Dados.index,
                open=Dados['Open'],
                high=Dados['High'],
                low=Dados['Low'],
                close=Dados['Close'],
                increasing_line_color='red',
                decreasing_line_color='green'
            )
        ]
    )

    Grafico_Candlestick.update_layout(
        xaxis_rangeslider_visible=False,
        title='Análise Fechamento',
        xaxis_title='Período',
        yaxis_title='Preço de Fechamento'
    )

    Grafico_Candlestick.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )

    Grafico_Linhas = go.Figure()
    Grafico_Linhas.add_trace(go.Scatter(
        x=Dados.index,
        y=Dados['Media_Movel'],
        mode='lines',
        name='Média Móvel',
        line=dict(color='blue')
    ))

    Grafico_Linhas.add_trace(go.Scatter(
        x=Dados.index,
        y=Dados['Close'],
        mode='lines',
        name='Fechamento',
        line=dict(color='green')
    ))

    Grafico_Linhas.update_layout(
        title='Análise Média Móvel e Fechamento',
        xaxis_title='Período',
        yaxis_title='Preço',
        template='plotly_dark',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=9)
        )
    )

    return Grafico_Candlestick, Grafico_Linhas


if __name__ == '__main__':
    app.run_server(debug=True)