# ==============================================================================
# PROJETO APLICADO II - CIÊNCIA DE DADOS
# ETAPA 2: ANÁLISE EXPLORATÓRIA (EDA)
# GRUPO: Daniel, David e Vinicius
# ==============================================================================

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# CONFIGURAÇÃO DE CAMINHOS
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_dados = os.path.join(diretorio_atual, '..', 'Dados', 'ecommerces_filtrados.csv')
pasta_graficos = os.path.join(diretorio_atual, '..', 'Graficos')

if not os.path.exists(pasta_graficos):
    os.makedirs(pasta_graficos)

# CARREGANDO A BASE
if not os.path.exists(caminho_dados):
    print(f"[ERRO] Arquivo não encontrado em: {caminho_dados}")
else:
    df = pd.read_csv(caminho_dados)
    sns.set_style("white")
    plt.rcParams['font.family'] = 'sans-serif'

    # GRÁFICO 1: RANKING POR EMPRESA
    plt.figure(figsize=(10, 6))
    order = df['Nome Fantasia'].value_counts().index
    sns.countplot(data=df, y='Nome Fantasia', order=order, palette='Blues_d', hue='Nome Fantasia', legend=False)
    plt.title('1. Volume de Reclamações por Empresa', fontsize=16, fontweight='bold', pad=20)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, 'Ranking_empresas.png'), dpi=300)
    print("[OK] Gráfico 1 salvo!")

    # GRÁFICO 2: DISTRIBUIÇÃO POR REGIÃO (DONUT)
    plt.figure(figsize=(8, 8))
    regiao_counts = df['Região'].value_counts()
    plt.pie(regiao_counts, labels=regiao_counts.index, autopct='%1.1f%%', startangle=140, 
            colors=sns.color_palette('Blues_r', len(regiao_counts)), wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    plt.gcf().gca().add_artist(centre_circle)
    plt.title('2. Distribuição por Região', fontsize=16, fontweight='bold')
    plt.savefig(os.path.join(pasta_graficos, 'Distribuicao_regioes.png'), dpi=300)
    print("[OK] Gráfico 2 salvo!")

    # GRÁFICO 3: EMPRESA X REGIÃO
    ct = pd.crosstab(df['Nome Fantasia'], df['Região'])
    ax3 = ct.plot(kind='bar', stacked=True, figsize=(12, 7), color=sns.color_palette('Blues', 5), edgecolor='white')
    plt.title('3. Reclamações por Empresa e Região', fontsize=16, fontweight='bold', pad=20)
    plt.legend(title='Região', frameon=False, bbox_to_anchor=(1, 1))
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, 'Empresas_regiao.png'), dpi=300)
    print("[OK] Gráfico 3 salvo!")

    # GRÁFICO 4: TOP 5 PROBLEMAS COM NÚMEROS EXATOS
    plt.figure(figsize=(12, 6))
    top_5_problems = df['Problema'].value_counts().head(5)
    ax4 = sns.barplot(x=top_5_problems.values, y=top_5_problems.index, palette='Blues_d', hue=top_5_problems.index, legend=False)
    for i, v in enumerate(top_5_problems.values):
        ax4.text(v + 3, i, str(v), color='black', va='center', fontweight='bold', fontsize=12)
    plt.title('4. Top 5 Problemas Recorrentes (Volume Total)', fontsize=16, fontweight='bold', pad=20)
    plt.xlim(0, max(top_5_problems.values) * 1.1)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, 'Top5_problemas.png'), dpi=300)
    print("[OK] Gráfico 4 salvo!")

    # GRÁFICO 5: TOP 5 PROBLEMAS POR EMPRESA (COMPARATIVO)
    top_5_empresas = df['Nome Fantasia'].value_counts().head(5).index
    top_5_problemas_lista = df['Problema'].value_counts().head(5).index
    df_comp = df[df['Nome Fantasia'].isin(top_5_empresas) & df['Problema'].isin(top_5_problemas_lista)]
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df_comp, y='Nome Fantasia', hue='Problema', palette='Blues_d', order=top_5_empresas)
    plt.title('5. Top 5 Problemas por Empresa (Comparativo)', fontsize=16, fontweight='bold', pad=20)
    plt.legend(title='Tipo de Problema', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_graficos, 'Comparativo_problemas_por_empresa.png'), dpi=300)
    print("[OK] Gráfico 5 salvo!")

    print(f"\n[SUCESSO] Kit completo com 5 gráficos salvo em: {pasta_graficos} 🚀📊")
