import pandas as pd

# Função para carregar os dados de homicídios
def load_homicide_data():
    df = pd.read_csv('data/homicidios_brasil.csv')
    return df

# Função para obter tendências de homicídios por ano
def get_homicide_trends():
    df = load_homicide_data()
    trends = df.groupby('ano')['homicidios'].sum().reset_index()
    return trends

# Função para obter homicídios por estado
def get_homicide_by_state(estado):
    df = load_homicide_data()
    state_data = df[df['estado'] == estado]
    return state_data