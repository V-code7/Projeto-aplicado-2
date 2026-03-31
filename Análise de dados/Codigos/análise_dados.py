# ==============================================================================
# PROJETO APLICADO II - CIÊNCIA DE DADOS
# ETAPA 2: ANÁLISE EXPLORATÓRIA (EDA)
# GRUPO: Daniel, David e Vinicius
# ==============================================================================

import pandas as pd
import os

# CONFIGURAÇÃO DE CAMINHOS DINÂMICOS
# Pega o caminho absoluto da pasta onde este script está (pasta 'Códigos')
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para a base bruta (Sobe um nível da pasta 'Códigos' e entra em 'Dados')
caminho_entrada = os.path.join(diretorio_atual, '..', 'Dados', 'basecompleta2026-02.csv')

# Define o caminho para salvar o filtrado (Sobe um nível e entra em 'Dados')
caminho_saida = os.path.join(diretorio_atual, '..', 'Dados', 'ecommerces_filtrados.csv')

# CARREGANDO A BASE BRUTA
print(f"--- Iniciando leitura da base bruta em: {caminho_entrada} ---")

if not os.path.exists(caminho_entrada):
    print(f"\n[ERRO] Arquivo não encontrado! Verifique se a base bruta está na pasta 'Dados' com o nome 'basecompleta2026-02.csv'.")
else:
    try:
        # Tenta ler com UTF-8
        df_bruto = pd.read_csv(caminho_entrada, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        # Se der erro de encoding, tenta Latin-1
        df_bruto = pd.read_csv(caminho_entrada, sep=';', encoding='latin1')

    # FILTRANDO OS DADOS
    # Mercado Livre, Amazon, Magalu, Shopee, Americanas e etc.
    Nome_Fantasia_alvo = ['Mercado Livre', 'Amazon', 'Magazine Luiza', 'Shopee', 'Americanas']
    pattern = '|'.join(Nome_Fantasia_alvo)

    # Filtra usando a coluna 'Nome Fantasia'
    df_filtrado = df_bruto[df_bruto['Nome Fantasia'].str.contains(pattern, case=False, na=False)].copy()

    # Limpeza rápida: Tirar 'Amazonas Energia' que o filtro pegou por conter "Amazon"
    df_filtrado = df_filtrado[~df_filtrado['Nome Fantasia'].str.contains('Amazonas Energia', case=False)]

    print(f"\n[INFO] Total de reclamações filtradas: {len(df_filtrado)}")

    # EDA - ANALISANDO O QUE ESTÁ ROLANDO COM CADA EMPRESA

    # Ranking de Reclamações por Empresa
    print("\n>>> RANKING DE RECLAMAÇÕES POR MARCA:")
    print(df_filtrado['Nome Fantasia'].value_counts())

    # Onde o pessoal mais reclama? (Região)
    print("\n>>> RECLAMAÇÕES POR REGIÃO (Sudeste deve dominar):")
    print(df_filtrado['Região'].value_counts())

    # Top 5 Problemas (Isso aqui é fundamental pro relatório!)
    print("\n>>> TOP 5 PROBLEMAS MAIS COMUNS:")
    print(df_filtrado['Problema'].value_counts().head(5))

    # Nota média por empresa (Pra gente ver o nível de satisfação)
    print("\n>>> NOTA MÉDIA DO CONSUMIDOR (1 a 5):")
    media_notas = df_filtrado.groupby('Nome Fantasia')['Nota do Consumidor'].mean().sort_values(ascending=False)
    print(media_notas)

    # AQUI SALVA O DATASET FILTRADO NA PASTA DADOS
    # Agora salva o arquivo e vai direto na pasta 'Dados' para o ML usar depois
    df_filtrado.to_csv(caminho_saida, index=False)
    print(f"\n[OK] Arquivo '{caminho_saida}' gerado com sucesso! 🚀")
