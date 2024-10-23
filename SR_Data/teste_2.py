#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import json
import locale

# Configurações de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações locais
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Diretórios e arquivos
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
config_dir = os.path.join(data_dir, 'config')
graphics_dir = os.path.join(script_dir, 'graphics')

config_file = os.path.join(config_dir, 'config.json')

# Imprimir o caminho do arquivo de configuração
print(f"Caminho do arquivo de configuração: {config_file}")

# Certifique-se de que os diretórios existem
os.makedirs(config_dir, exist_ok=True)
os.makedirs(graphics_dir, exist_ok=True)

# Função para carregar configurações
def load_config(config_file_path):
    if not os.path.exists(config_file_path):
        logger.error(f"Arquivo de configuração não encontrado: {config_file_path}")
        sys.exit(1)
    with open(config_file_path, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao ler o arquivo de configuração: {e}")
            sys.exit(1)
    return config

# Função para obter dados da API Sidra do IBGE
def fetch_data(api_url, params=None):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        # print("Dados recebidos da API:")
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        return data
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar a API: {e}")
        sys.exit(1)

# Função para processar os dados retornados pela API Sidra
def process_data(data):
    # Converter a resposta JSON em um DataFrame
    df = pd.DataFrame(data)
    
    # Remover a primeira linha (metadados)
    df = df.iloc[1:]
    
    # Converter colunas necessárias
    df['valor'] = pd.to_numeric(df['V'], errors='coerce')
    df['date'] = pd.to_datetime(df['D3N'], errors='coerce')
    df.sort_values('date', inplace=True)
    return df

# Função para gerar o gráfico
def generate_graph(df, title, subtitle, output_file, bg_transparent=False):
    fig = go.Figure()

    # Exemplo de gráfico (ajuste conforme necessário)
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['valor'],
        mode='lines+markers',
        name=title
    ))

    # Atualizar layout do gráfico
    fig.update_layout(
        title={'text': f"{title}<br><sub>{subtitle}</sub>", 'x': 0.5},
        xaxis_title='Data',
        yaxis_title='Valor',
        template='plotly_white',
        width=800,
        height=600
    )

    # Salvar o gráfico como imagem
    try:
        pio.write_image(fig, output_file, scale=2)
        logger.info(f"Gráfico salvo em: {output_file}")
    except Exception as e:
        logger.error(f"Erro ao salvar o gráfico: {e}")
        sys.exit(1)

# Função principal
def main():
    # Carregar configurações
    config = load_config(config_file)
    print("Conteúdo do arquivo de configuração:")
    print(json.dumps(config, indent=4, ensure_ascii=False))

    # Verificar se 'api_url' está definido
    api_url = config.get('api_url')
    if not api_url:
        logger.error("A URL da API não está definida no arquivo de configuração.")
        print("Chaves disponíveis no arquivo de configuração:", list(config.keys()))
        sys.exit(1)
    else:
        print(f"API URL encontrada: {api_url}")

    # Parâmetros da API (se necessário)
    api_params = config.get('api_params', {})

    # Título e subtítulo do gráfico
    title = config.get('title', 'Título do Gráfico')
    subtitle = config.get('subtitle', 'Subtítulo do Gráfico')

    # Nome do arquivo de saída
    output_file = os.path.join(graphics_dir, 'grafico.png')

    # Obter dados da API
    data = fetch_data(api_url, params=api_params)

    # Processar dados
    df = process_data(data)

    # Verificar se o DataFrame não está vazio
    if df.empty:
        logger.error("Nenhum dado disponível para gerar o gráfico.")
        sys.exit(1)

    # Gerar gráfico
    generate_graph(df, title, subtitle, output_file, bg_transparent=False)

if __name__ == '__main__':
    main()
