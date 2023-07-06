import yfinance as yf
from datetime import datetime, date

def obter_dados_ticker(ticker, dt_inicio, dt_fim):
    # Convertendo a data para o formato desejado
    data_inicio = datetime.strptime(dt_inicio, '%d/%m/%Y')
    data_fim = datetime.strptime(dt_fim, '%d/%m/%Y')

    # Convertendo a data para o formato desejado
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')

    # Obter dados históricos do ticker
    dados = yf.download(ticker, start=data_inicio_str, end=data_fim_str, progress=False)

    valores_dolar = []

    # Processar valores diários
    for index, row in dados.iterrows():
        valor_dolar = row['Close']
        valores_dolar.append(valor_dolar)

    # Calculando o valor médio em dólar
    valor_medio = sum(valores_dolar) / len(valores_dolar)
    
    return valor_medio

def ler_valores_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    valores_ticker = []
    for linha in linhas:
        valores = linha.strip().split(" - ")
        if len(valores) >= 2:
            ticker = valores[0]
            dt_inicio = valores[1]
            dt_fim = valores[2] if len(valores) >= 3 else date.today().strftime('%d/%m/%Y')
            valores_ticker.append((ticker, dt_inicio, dt_fim))

    return valores_ticker

def salvar_valores_arquivo(valores_ticker, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for ticker, valor_medio in valores_ticker:
            linha = f"{ticker} - {valor_medio:.2f}\n"
            arquivo.write(linha)

# Nome do arquivo de entrada
nome_arquivo_entrada = "tickers.txt"

# Nome do arquivo de saída
nome_arquivo_saida = "papeis.txt"

# Ler os valores do arquivo de entrada
valores_ticker = ler_valores_arquivo(nome_arquivo_entrada)

# Processar os valores dos tickers
valores_processados = []
for ticker, dt_inicio, dt_fim in valores_ticker:
    valor_medio = obter_dados_ticker(ticker, dt_inicio, dt_fim)
    valores_processados.append((ticker, valor_medio))

# Salvar os valores processados no arquivo de saída
salvar_valores_arquivo(valores_processados, nome_arquivo_saida)
