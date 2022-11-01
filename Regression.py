# -*- coding: utf-8 -*-
"""Regressao_modelos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ODbrkzuH6S8_uWcpHg6QjgzR99yNTS9K

# **Regressão Linear**
"""

! pip install skl2onnx

"""**CHECKLIST DE COISAS PARA FAZER:**

1.   Dividir o dataset em um de treino e um de testes. (isso é para quando tivermos um dataset maior)
2.   Utilizar Multioutput para predizer mais de um target.
3.   Mesclar o meu código com o do Ricardo.

# **Configurações iniciais da regressão**


1.   Importando as bibliotecas que serão utilizadas
1.   Importando o dataset geral
2.   Filtrando os dados mais importantes
3.   Gerando a matriz de confusão do dataset filtrado
4.   Determinando as variáveis dependentes e independentes
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.metrics import r2_score
from plotnine import ggplot, aes, geom_point, geom_line
from plotnine.themes import theme_minimal
from google.colab import files
from skl2onnx import __max_supported_opset__
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# carregando o dataset
data_to_load = files.upload()
test_df = pd.read_csv(io.BytesIO(data_to_load['data-base.csv']))
test_df

sns.heatmap(test_df.corr(), annot=True, vmin=-2, vmax=2)
plt.show()

# Utilizando alguns dados para realizar os testes
df = test_df[['width', 'height', 'Smooth', 'MinRegionSize', 'minEnemyDistance','minItemDistance', 'RandomFillPercent','EnemyDensity', 'ItemDensity', 'MaxEnemies', 'MaxItems', 'totalLifeLost', 'timeSpent', 'steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'fun', 'averageEnemyDistance', 'averageItemDistance', 'interactions', 'playthroughs', 'GeneratedEnemies', 'GeneratedItems', 'mapSize']]
df

# matriz
sns.heatmap(df.corr(), annot=True, vmin=-1, vmax=1)
plt.show()

# y -> target (variavel dependete)
# x -> variaveis independentes
y = test_df[['width', 'height', 'Smooth', 'MinRegionSize', 'minEnemyDistance','minItemDistance', 'MaxEnemies', 'MaxItems', 'RandomFillPercent','EnemyDensity', 'ItemDensity', 'fun']]  
#x = test_df[['totalLifeLost', 'timeSpent', 'steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'averageEnemyDistance', 'averageItemDistance', 'interactions', 'playthroughs']]  
x = test_df[['totalLifeLost','steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'interactions', 'playthroughs','mapSize']]

# matriz
sns.heatmap(x.corr(), annot=False, vmin=-1, vmax=1, cmap='coolwarm')
plt.show()

"""# **Dividindo o dataset em: dataset de treino e dataset de teste**"""

# fazendo split do dataset
x_train, x_test, y_train, y_test = train_test_split(x, y)

x_train

x_test

y_train

y_test

"""# **Treinamento e predição dos valores com o dataset de treinamento**"""

# criando um modelo de regressão linear
reg = LinearRegression()
mult = MultiOutputRegressor(reg)

# treinando o modelo de regressão
mult.fit(x_train,y_train)

# resultados
# um valor negativo do coeficiente indica uma relação inversa. A variável independente
# aumenta e a variável dependente diminui.
mult.estimators_[0].coef_ #revisar isto

# resultados
mult.estimators_[0].intercept_ #revisar isto

# predição
#y_true = df.Notas
#y_pred = reg.predict(df[['Tempo no mapa gerado', 'Tamanho do mapa', 'Passos', 'Porcentagem de inimigos derrotados']])
y_true = y_train
y_pred = mult.predict(x_train) 
y_pred

# separando as predições em vetores separados
prediction_results = np.hsplit(y_pred,12)
prediction_results

"""# **Métricas de erro**"""

# utilizando a métrica de erro mean squared error
model_error_squared = mean_squared_error(y_true, y_pred)
print(f"The mean squared error of the optimal model is {model_error_squared:.2f}")

# utilizando a métrica de erro mean absolute error
model_error_absolute = mean_absolute_error(y_true, y_pred)
print(f"The mean absolute error of the optimal model is {model_error_absolute:.2f}")

# melhor valor esperado é 1, valores menores são piores resultados
model_error_variance = explained_variance_score(y_true, y_pred)
print(f"The mean absolute error of the optimal model is {model_error_variance:.2f}")

# utilizando a métrica de erro mean pinball error
model_error_pinball_loss = mean_pinball_loss(y_true, y_pred, alpha = 0.5)
print(f"The mean absolute error of the optimal model is {model_error_pinball_loss:.2f}")

# variância
# metrica comum para medir a regressão linear, estimando a proporção da variância.
# Os resultados vão de 0 a 1, quanto maior melhor.
model_error_r2 = r2_score(y_true, y_pred)
print(f"The mean r2 of the optimal model is {model_error_r2:.2f}")

"""# **Resultados finais do dataset de treinamento**"""

# Visualização
#df['fitted'] = y_pred
#df
train_result = pd.concat([x_train, y_train], axis="columns")
train_result['width pred'] = prediction_results[0]
train_result['height pred'] = prediction_results[1]
train_result['Smooth pred'] = prediction_results[2]
train_result['MinRegionSize pred'] = prediction_results[3]
train_result['minEnemyDistance pred'] = prediction_results[4]
train_result['minItemDistance pred'] = prediction_results[5]
train_result['MaxEnemies pred'] = prediction_results[6]
train_result['MaxItems pred'] = prediction_results[7]
train_result['RandomFillPercent pred'] = prediction_results[8]
train_result['EnemyDensity pred'] = prediction_results[9]
train_result['ItemDensity pred'] = prediction_results[10]
train_result['fun pred'] = prediction_results[11]
train_result

ggplot(aes('width', 'height', 'Smooth', 'MinRegionSize', 'minEnemyDistance','minItemDistance', 'RandomFillPercent','EnemyDensity', 'ItemDensity', 'totalLifeLost', 'timeSpent', 'steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'fun'), train_result) \
    + geom_point(alpha = 0.5, color = "#2c3e50") \
    + geom_line(aes(y = 'width pred'), color = 'blue') \
    + geom_line(aes(y = 'height pred'), color = 'green') \
    + geom_line(aes(y = 'Smooth pred'), color = 'blue') \
    + geom_line(aes(y = 'MinRegionSize pred'), color = 'green') \
    + geom_line(aes(y = 'minEnemyDistance pred'), color = 'blue') \
    + geom_line(aes(y = 'minItemDistance pred'), color = 'green') \
    + geom_line(aes(y = 'MaxEnemies pred'), color = 'blue') \
    + geom_line(aes(y = 'MaxItems pred'), color = 'green') \
    + geom_line(aes(y = 'RandomFillPercent pred'), color = 'blue') \
    + geom_line(aes(y = 'EnemyDensity pred'), color = 'green') \
    + geom_line(aes(y = 'ItemDensity pred'), color = 'blue') \
    + geom_line(aes(y = 'fun pred'), color = 'blue') \
    + theme_minimal()

"""# **Utilizando o dataset de testes**




"""

# usando o dataset de testes
# aqui não iremos usar o método de fit para realizar o treinamento
y_true_test = y_test
y_pred_test = mult.predict(x_test)
y_pred_test

prediction_results_test = np.hsplit(y_pred_test,12)
prediction_results_test

train_result_test = pd.concat([x_test, y_test], axis="columns")
train_result_test['width pred'] = prediction_results_test[0]
train_result_test['height pred'] = prediction_results_test[1]
train_result_test['Smooth pred'] = prediction_results_test[2]
train_result_test['MinRegionSize pred'] = prediction_results_test[3]
train_result_test['minEnemyDistance pred'] = prediction_results_test[4]
train_result_test['minItemDistance pred'] = prediction_results_test[5]
train_result_test['MaxEnemies pred'] = prediction_results_test[6]
train_result_test['MaxItems pred'] = prediction_results_test[7]
train_result_test['RandomFillPercent pred'] = prediction_results_test[8]
train_result_test['EnemyDensity pred'] = prediction_results_test[9]
train_result_test['ItemDensity pred'] = prediction_results_test[10]
train_result_test['fun pred'] = prediction_results_test[11]
train_result_test

ggplot(aes('width', 'height', 'Smooth', 'MinRegionSize', 'minEnemyDistance','minItemDistance', 'RandomFillPercent','EnemyDensity', 'ItemDensity', 'totalLifeLost', 'timeSpent', 'steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'fun'), train_result_test) \
    + geom_point(alpha = 0.5, color = "#2c3e50") \
    + geom_line(aes(y = 'width pred'), color = 'blue') \
    + geom_line(aes(y = 'height pred'), color = 'green') \
    + geom_line(aes(y = 'Smooth pred'), color = 'blue') \
    + geom_line(aes(y = 'MinRegionSize pred'), color = 'green') \
    + geom_line(aes(y = 'minEnemyDistance pred'), color = 'blue') \
    + geom_line(aes(y = 'minItemDistance pred'), color = 'green') \
    + geom_line(aes(y = 'MaxEnemies pred'), color = 'blue') \
    + geom_line(aes(y = 'MaxItems pred'), color = 'green') \
    + geom_line(aes(y = 'RandomFillPercent pred'), color = 'blue') \
    + geom_line(aes(y = 'EnemyDensity pred'), color = 'green') \
    + geom_line(aes(y = 'ItemDensity pred'), color = 'blue') \
    + geom_line(aes(y = 'fun pred'), color = 'blue') \
    + theme_minimal()

"""# **Exportando o modelo com joblib**"""

# passando o modelo treinado e o nome do arquivo
joblib.dump(mult, "regression_model.joblib")

"""# **Convertendo modelo para Onnx**"""

initial_type = [('float_input', FloatTensorType([None, 9]))]
onx = convert_sklearn(mult, initial_types=initial_type)
with open("regression.onnx", "wb") as f:
    f.write(onx.SerializeToString())

#['totalLifeLost','steps', 'deaths', 'percentKills', 'percentItems', 'complexity', 'difficulty', 'interactions', 'playthroughs','mapSize']
new_sample = [[40,175,0,1.2,1,3,2,1,1,0]] #célula 27
new_pred_test = mult.predict(new_sample)
new_pred_test