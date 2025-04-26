from dash import Dash, html, dcc
from pages.home import home_layout
import callbacks

# Inicializa o aplicativo Dash
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout principal com gerenciamento de URLs
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Registra os callbacks
callbacks.register_callbacks(app)

# Rodando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)