#Verificando a versão do Python
from operator import index
from platform import python_version
from sys import displayhook
from tkinter.ttk import Style
from turtle import color
print(python_version())


#importação de pacotes
import re
import time
import sqlite3
import pycountry 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm, colors
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style = "whitegrid")

#Carregar dados IMDB-SQL (Instalações.txt)

#Conectar ao banco de dados
conn = sqlite3.connect('imdb.db')

# Extrair lista de tabelas
tabelas = pd.read_sql_query('SELECT name as TableName FROM sqlite_master WHERE type = "table"',conn)
print(type(tabelas))
#print(tabelas)

#Converter tabela em Lista
tabelas = tabelas['TableName'].values.tolist()

#Percorer lista da tabela no banco e extrair o squema de cada uma

for tabela in tabelas:
    consulta = "PRAGMA TABLE_INFO({})".format(tabela)
    resultado = pd.read_sql_query(consulta,conn)
    #print('Esquema da Tabela: ', tabela)
    #print(resultado)
    #print('-'*100)
    #print('\n')


#-----------------------------------------------------------------------#
# 1- Quais são as categorias mais comuns de Filmes?                     #
#-----------------------------------------------------------------------#

# CRIA CONSULTA SQL
consulta1 = '''SELECT type, count(*) as count FROM titles GROUP BY type'''

#EXTAI O RESULTADO
resultado1 = pd.read_sql_query(consulta1,conn)
#print(resultado1)
#CALCULAR PERCENTUAL PARA CADAS TIPO

resultado1['percentual'] = (resultado1['count'] / resultado1['count'].sum()) * 100
#print(resultado1)

#Criar gráficos com apenas 4 categorias:
# As as 3 categorias com mais titulos e 1 categoria com todo o restante

#Criar um dicionário vazio
others = {}

#Filtra percentual em 5% e soma o total
others ['count'] = resultado1[resultado1['percentual']<5]['count'].sum()

#Grava o percentual
others['percentual'] = resultado1[resultado1['percentual']< 5]['percentual'].sum()

#ajusta o nome
others['type'] = 'others'
#print(others)

#filtra o dataframe de resultado 
resultado1 = resultado1[resultado1['percentual'] > 5]

#APPEND com o dataframe de outras categorias
resultado1 = resultado1.append(others, ignore_index = True)

#Ordena o resultado
resultado1 = resultado1.sort_values(by = 'count', ascending=False)

#mostra o resultado
#print(resultado1)

#Ajustar o Labes - List Comprehension
labels = [str(resultado1['type'][i])+' '+'['+str(round(resultado1['percentual'][i],2))+'%'+']' for i in resultado1.index]

#PLOT
#mapa de cores
cs = cm.Set3(np.arange(100))
#Cria a figura
f = plt.figure()
#Pie PLOT
plt.pie(resultado1['count'],labeldistance = 1, radius=1,colors = cs, wedgeprops=dict(width = 0.2))
plt.legend(labels,loc = 'center', prop = {'size':12})
plt.title("Distribuição de Título", loc = 'center', fontdict={'fontsize':20,'fontweight':20})
#plt.show()

#--------------------------------------------------------------------#
#   2 - Numero de titulos por Genero?                                #
#--------------------------------------------------------------------#

# Definir Instrução SQL
consulta2 = ''' SELECT genres, COUNT(*) FROM titles WHERE type = "movie" GROUP BY genres'''

#Resultado 
resultado2 = pd.read_sql_query(consulta2,conn)

#Visualizar Dados
#print(resultado2)

#Converte as String para minusculo
resultado2['genres'] = resultado2['genres'].str.lower().values

#Remove os valores NA (ausentes)
temp = resultado2['genres'].dropna()

#Criar um vetor usando expressão regular para filtrar as string
padrao = '(?u)\\b[\\w-]+\\b'
vetor = CountVectorizer(token_pattern = padrao, analyzer='word').fit(temp)
#print(type(vetor))

#Aplica a vetorização ao dataset sem valores NA
bag_generos = vetor.transform(temp)
#print(type(bag_generos))

#retorna Generos Univos 
generos_unicos = vetor.get_feature_names()

#Cria o DataFrame de Generos
generos = pd.DataFrame(bag_generos.todense(), columns= generos_unicos, index = temp.index)

#Drop na coluna N
generos = generos.drop(columns='n',axis = 0)

#Calcula o Percentual
generos_percentual = 100 * pd.Series(generos.sum()).sort_values(ascending=False) / generos.shape[0]
print(generos_percentual.head(10))

#PLOT 

plt_gen = plt.figure(figsize=(10,4))
plt_gen = sns.barplot(x = generos_percentual.values, y = generos_percentual.index, orient="h", palette="terrain")
plt_gen = plt.ylabel('Gênero')
plt_gen = plt.xlabel("\nPercentual de Filmes (%)")
plt_gen = plt.title('\n Número (Percentual) de Títulos por Gênero\n')
plt_gen = plt.show()
