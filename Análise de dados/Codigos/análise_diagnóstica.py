import pandas as pd
import os

# CONFIGURAÇÃO DE CAMINHOS
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_dados = os.path.join(diretorio_atual, '..', 'Dados', 'ecommerces_filtrados.csv')

print(f"--- Iniciando Diagnóstico Operacional ---")
print(f"Buscando base de dados em: {os.path.abspath(caminho_dados)}")

if os.path.exists(caminho_dados):
    df = pd.read_csv(caminho_dados)
    
    # Filtra apenas reclamações não resolvidas
    df_falhas = df[df['Avaliação Reclamação'] == 'Não Resolvida']
    
    print("DIAGNÓSTICO DE FALHAS POR EMPRESA")
    
    empresas = df['Nome Fantasia'].unique()
    
    for empresa in empresas:
        df_emp = df[df['Nome Fantasia'] == empresa]
        total_rec = len(df_emp)
        
        if total_rec == 0:
            continue
            
        resolvidas = len(df_emp[df_emp['Avaliação Reclamação'] == 'Resolvida'])
        taxa_resolucao = (resolvidas / total_rec) * 100
        
        print(f"\n>>> EMPRESA: {empresa}")
        print(f"Total de Reclamações: {total_rec}")
        print(f"Taxa de Resolução: {taxa_resolucao:.2f}%")
        
        df_nao_resolvidas = df_emp[df_emp['Avaliação Reclamação'] == 'Não Resolvida']
        
        if len(df_nao_resolvidas) > 0:
            falhas_criticas = df_nao_resolvidas['Grupo Problema'].value_counts().head(3)
            print("Principais Gargalos (Não Resolvidos):")
            for prob, count in falhas_criticas.items():
                perc = (count / len(df_nao_resolvidas)) * 100
                print(f" - {prob}: {count} ocorrências ({perc:.1f}% das falhas)")
        else:
            print("Nenhuma reclamação 'Não Resolvida' encontrada.")
            
    print("[OK] Análise finalizada com sucesso! 🚀")
else:
    print(f"\n[ERRO] Arquivo não encontrado!")