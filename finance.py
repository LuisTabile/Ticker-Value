import yfinance as yf
from forex_python.converter import CurrencyRates
from datetime import datetime
import numpy as np

def obter_dados_ticker(ticker, data_inicio, data_fim):
    # Convertendo a data para o formato desejado
    data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
    data_fim = datetime.strptime(data_fim, '%d/%m/%Y')

    if data_inicio > datetime.now() or data_fim > datetime.now():
        raise ValueError("A data de início ou fim não pode ser maior do que a data de hoje.")

    # Convertendo a data para o formato desejado
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')

    # Obter dados históricos do ticker
    dados = yf.download(ticker, start=data_inicio_str, end=data_fim_str)

    # Converter o valor da moeda
    cr = CurrencyRates()
    dolar_atual = cr.get_rate('USD', 'BRL')

    valor_maximo = 0
    valor_minimo = np.inf
    data_max = None
    data_min = None
    valores_dolar = []

    # Processar valores diários
    for index, row in dados.iterrows():
        valor_dolar = row['Close']
        valores_dolar.append(valor_dolar)

        # Atualizando valor máximo e mínimo
        if valor_dolar > valor_maximo:
            valor_maximo = valor_dolar
            data_max = index.date()
        if valor_dolar < valor_minimo:
            valor_minimo = valor_dolar
            data_min = index.date()

    # Imprimindo valores diários em dólar
    for i, valor in enumerate(valores_dolar):
        print(f"Data: {dados.index[i].date().strftime('%d/%m/%Y')}, Valor: {valor:.4f}")

    # Calculando o valor médio em dólar
    valor_medio = sum(valores_dolar) / len(valores_dolar)
    print("\n-----------------------------------------------------------------------------------------")
    print("Maior Valor:")
    print(f"{valor_maximo:.4f} Dólares.")
    print(f"{valor_maximo * dolar_atual:.4f} Reais.")
    print(f"Data: {data_max.strftime('%d/%m/%Y')}")
    print("\n-----------------------------------------------------------------------------------------")
    print("Menor Valor:")
    print(f"{valor_minimo:.4f} Dólares.")
    print(f"{valor_minimo * dolar_atual:.4f} Reais.")
    print(f"Data: {data_min.strftime('%d/%m/%Y')}")
    print("\n-----------------------------------------------------------------------------------------")
    print("Valor Médio:")
    print(f"{valor_medio:.4f} Dólares.")
    print(f"{valor_medio * dolar_atual:.4f} Reais.")
    print("\n-----------------------------------------------------------------------------------------")

# Solicitar entrada do usuário
ticker = input("Digite o nome do ticker: ")
data_inicio = input("Digite a data de início (DD/MM/AAAA): ")
data_fim = input("Digite a data final (DD/MM/AAAA): ")

# Obter e imprimir dados do ticker
obter_dados_ticker(ticker, data_inicio, data_fim)
