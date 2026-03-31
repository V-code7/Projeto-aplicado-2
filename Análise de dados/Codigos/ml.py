# ==============================================================================
# PROJETO APLICADO II - CIÊNCIA DE DADOS
# ETAPA 2: ANÁLISE EXPLORATÓRIA (EDA)
# GRUPO: Daniel, David e Vinicius
# ==============================================================================

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# CONFIGURAÇÃO DE CAMINHOS
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_dados = os.path.join(diretorio_atual, '..', 'Dados', 'ecommerces_filtrados.csv')

# CARREGANDO A BASE FILTRADA
print(f"--- Carregando dados para Machine Learning em: {caminho_dados} ---")

if not os.path.exists(caminho_dados):
    print(f"\n[ERRO] Arquivo não encontrado! Rode o script de filtragem primeiro.")
else:
    df = pd.read_csv(caminho_dados)

    # PRÉ-PROCESSAMENTO (TRATAMENTO DE DADOS)
    # Limpeza: vai remover as linhas sem avaliação (assim)
    df = df.dropna(subset=['Avaliação Reclamação', 'Nota do Consumidor', 'Nome Fantasia', 'Região', 'Grupo Problema'])

    # Target (Y): Prever se a reclamação será 'Resolvida' (1) ou não (0)
    df['Target'] = df['Avaliação Reclamação'].apply(lambda x: 1 if x == 'Resolvida' else 0)

    # Features (X): Variáveis que influenciam o desfecho
    features = ['Nome Fantasia', 'Região', 'Sexo', 'Faixa Etária', 'Grupo Problema']
    X = df[features].copy()
    y = df['Target']

    # Codificação: Transforma categorias (texto) em números para o modelo
    le = LabelEncoder()
    for col in X.columns:
        X[col] = le.fit_transform(X[col].astype(str))

    # DIVISÃO DE TREINO E TESTE
    # 70% treina o modelo, 30% para testar a acurácia
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # TREINAMENTO (RANDOM FOREST)
    print("\n--- Treinando o modelo Random Forest... ---")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # AVALIAÇÃO DE DESEMPENHO (ACURÁCIA)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\n" + "="*50)
    print(f">>> ACURÁCIA DO MODELO: {accuracy:.4f}")
    print("="*50)

    print("\n>>> RELATÓRIO DE CLASSIFICAÇÃO:")
    print(classification_report(y_test, y_pred))

    # Pra gente ver o que mais pesa no resultado
    print("\n>>> IMPORTÂNCIA DAS VARIÁVEIS NO MODELO:")
    importances = pd.DataFrame({'Feature': features, 'Importância': model.feature_importances_})
    print(importances.sort_values(by='Importância', ascending=False))

    print("\n[OK] Modelo de Machine Learning finalizado com sucesso! 🚀🤖")
