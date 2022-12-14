# Logica de programação
# Passo 0 - Entender o desafio que você quer resolver
# Passo 1 - Percorrer todos os arquivos da pasta base de dados (Vendas)
# Passo 2 - Importar as bases de dados de vendas
# Passo 3 - Tratar / Compilar as bases de dados
# Passo 4 - Calcular o produto mais vendido (em quantidade)
# Passo 5 - Calcular o produto que mais faturou (em faturamento)
# Passo 6 - Calcular a loja/cidade que mais vendeu (em faturamento) - criar um gráfico / dashboard

import os
import pandas as pd
import plotly.express as px

lista_arquivo = os.listdir("/content/drive/MyDrive/Curso Básico de Python/Vendas") # Passo 1

tabela_total = pd.DataFrame()

for arquivo in lista_arquivo:
  if "Vendas" in arquivo:
    tabela = pd.read_csv(f"/content/drive/MyDrive/Curso Básico de Python/Vendas/{arquivo}") # Passo 2
    tabela_total = tabela_total.append(tabela) # Passo 3

tabela_produtos = tabela_total.groupby("Produto").sum()[["Quantidade Vendida", "Preco Unitario"]].sort_values(by="Preco Unitario", ascending=False) # Passo 4
display(tabela_produtos)
print('# ------------------------------------------------------------------------------------------------------------------- # \n# ------------------------------------------------------------------------------------------------------------------- #')
# -------------------------------------------------------------------------------------------------------------------
# tabela_faturamento = tabela_produtos
# tabela_faturamento["Faturamento"] = tabela_faturamento["Quantidade Vendida"] * tabela_faturamento["Preco Unitario"]
# display(tabela_faturamento[["Faturamento"]].sort_values(by="Faturamento", ascending=False))
# Ideia errada, falhou :/
# -------------------------------------------------------------------------------------------------------------------

tabela_total["Faturamento"] = tabela_total["Quantidade Vendida"] * tabela_total["Preco Unitario"] # Passo 5
tabela_faturamento = tabela_total.groupby("Produto").sum()[["Faturamento"]].sort_values(by="Faturamento", ascending=False) # Passo 5
display(tabela_faturamento)
print('# ------------------------------------------------------------------------------------------------------------------- # \n# ------------------------------------------------------------------------------------------------------------------- #')

tabela_lojas = tabela_total.groupby("Loja").sum()[["Faturamento"]].sort_values(by='Faturamento', ascending=False)
display(tabela_lojas)

grafico = px.bar(tabela_lojas, x=tabela_lojas.index, y='Faturamento')
grafico.show()