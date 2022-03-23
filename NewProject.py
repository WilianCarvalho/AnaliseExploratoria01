#Verificando a versão do Python
from platform import python_version
from tkinter.ttk import Style
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
from matplotlib import cm
#from sklearn.feature_extration.text import CountVectorizer
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
    print('Esquema da Tabela: ', tabela)
    print(resultado)
    print('-'*100)
    print('\n')

