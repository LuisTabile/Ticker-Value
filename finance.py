import yfinance as yf
from datetime import datetime, date

def obter_dados_ticker(ticker, dt_inicio, dt_fim):
    data_inicio = datetime.strptime(dt_inicio, '%d/%m/%Y')
    data_fim = datetime.strptime(dt_fim, '%d/%m/%Y')

    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')

    try:
        dados = yf.download(ticker, start=data_inicio_str, end=data_fim_str, progress=False)
    except Exception as e:
        print(f"Erro ao obter dados do ticker: {ticker}. Erro: {str(e)}")
        return 0.0

    valores_dolar = []
    for index, row in dados.iterrows():
        valor_dolar = row['Close']
        valores_dolar.append(valor_dolar)

    valor_medio = sum(valores_dolar) / len(valores_dolar) if valores_dolar else 0.0
    
    return valor_medio

def obter_valor_atual(ticker):
    try:
        ticker_yf = yf.Ticker(ticker)
        ticker_history = ticker_yf.history(period='1d')
        if not ticker_history.empty:
            regular_market_price = ticker_history['Close'][0]
        else:
            regular_market_price = 0.0
    except Exception as e:
        print(f"Erro ao obter valor atual do ticker: {ticker}. Erro: {str(e)}")
        return 0.0

    return regular_market_price

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
        for ticker, valor_medio, valor_atual in valores_ticker:
            linha = f"{ticker} - {valor_medio:.2f} - {valor_atual:.2f}\n"
            arquivo.write(linha)

nome_arquivo_entrada = "tickers.txt"
nome_arquivo_saida = "papeis.txt"

valores_ticker = ler_valores_arquivo(nome_arquivo_entrada)

valores_processados = []
for ticker, dt_inicio, dt_fim in valores_ticker:
    valor_medio = obter_dados_ticker(ticker, dt_inicio, dt_fim)
    valor_atual = obter_valor_atual(ticker)
    valores_processados.append((ticker, valor_medio, valor_atual))

salvar_valores_arquivo(valores_processados, nome_arquivo_saida)
