import pandas as pd
import matplotlib.pyplot as plt
import re
import matplotlib.patches as mpatches

# ----------------------------------------------------------------------------------------------------------------------
# Primero leemos el csv y modificamos algunos datos en el dataframe para su posterior uso.
# ----------------------------------------------------------------------------------------------------------------------

df = pd.read_csv('CSVAcumulativo.csv', index_col=0)

# Primero cambiamos los valores nulos por 0, necesario para después calcular la media del retraso.
df.replace('--', 0, inplace=True)

# Después, eliminamos los asteriscos de los tipos de trenes, ya que la distinción a la que hace referencia no nos hace
# falta.
df['Tren'] = df['Tren'].apply(lambda x: re.sub('\s\*', '', x))

# Además, convertimos el tipo de tren, 'TORRE ORO' en Intercity ya que pese a que aparece como un tipo de tren a parte,
# pertenece a dicha clase. Lo mismo ocurre con 'EUROMED', que es del tipo 'ALVIA'.
df.replace('TORRE ORO', 'Intercity', inplace=True)
df.replace('EUROMED', 'ALVIA', inplace=True)

# Convertimos además los datos de la columna 'Retraso' en enteros, para poder operar con ellos.
df['Retraso'] = df['Retraso'].astype('int64')

# ----------------------------------------------------------------------------------------------------------------------
# Ahora, agrupamos los datos según el tipo de tren al que pertenecen.
# ----------------------------------------------------------------------------------------------------------------------

grouped_df = df.groupby('Tren')

# ----------------------------------------------------------------------------------------------------------------------
# Sacamos dos dataframes, según su carácter de larga o media distancia, analizando el tipo de tren.
# ----------------------------------------------------------------------------------------------------------------------

# Larga distancia:
df_AVE = grouped_df.get_group('AVE')
df_Avlo = grouped_df.get_group('AVLO')
df_Alvia = grouped_df.get_group('ALVIA')
df_Intercity = grouped_df.get_group('Intercity')

# Media distancia:
df_MD = grouped_df.get_group('MD')
df_REGIONAL = grouped_df.get_group('REGIONAL')
df_REGEXP = grouped_df.get_group('REG.EXP.')
df_AVANT = grouped_df.get_group('AVANT')

# Unimos los distintos dataframes:
df_LDist = pd.concat([df_AVE, df_Avlo, df_Alvia, df_Intercity])
df_MDist = pd.concat([df_MD, df_REGEXP, df_REGIONAL, df_AVANT])
tipos_LD = df_LDist['Tren'].unique()
tipos_MD = df_MDist['Tren'].unique()

# ----------------------------------------------------------------------------------------------------------------------
# GRÁFICA 1: Tiempo medio de demora acorde el tipo de tren.
# ----------------------------------------------------------------------------------------------------------------------

# Calculamos la media de los datos agrupados y le indicamos que solo opere las columnas con valores numéricos, en
# nuestro caso, la columna donde se indican los retrasos.
er_distribution = grouped_df.mean(numeric_only=True)['Retraso']
# Esto nos devuelve una serie.
# Mostramos los datos obtenidos en un histograma:
plt.style.use('ggplot')
plt.title('TIEMPO MEDIO DE DEMORA ACORDE EL TIPO DE TREN', fontdict={'fontsize': 10})
plt.ylabel('Tiempo Medio de Demora (Minutos)')

colors = []
for count in er_distribution.keys():
    if count in tipos_LD:
        colors.append('purple')
    else:
        colors.append('violet')

er_distribution.plot(kind='bar', color=colors, alpha=0.8, width=0.25)

First_patch = mpatches.Patch(color='purple', label='Larga Distancia')
Second_patch = mpatches.Patch(color='violet', label='Media Distancia')
plt.legend(handles=[First_patch, Second_patch])

plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# GRÁFICA 2: Frecuencia de actividad acorde el tipo de tren.
# ----------------------------------------------------------------------------------------------------------------------

# Contamos las apariciones de cada tipo de tren en la columna que lo indica, para saber en forma de porcentaje, la
# cantidad de trenes que hay activos según su tipo correspondiente.
er_distribution2 = grouped_df['Tren'].count()
# Mostramos los datos obtenidos en un diagrama de tarta:
plt.style.use('ggplot')
plt.title('FRECUENCIA DE ACTIVIDAD ACORDE EL TIPO DE TREN', fontdict={'fontsize': 10})
plt.ylabel('Porcentaje')
colores = ['mediumslateblue', 'mediumpurple', 'blueviolet', 'darkorchid', 'mediumorchid', 'violet', 'plum', 'thistle']
er_distribution2.plot(kind='pie', autopct='%1.1f%%', colors=colores)
tipos = df['Tren'].unique()
plt.legend(tipos, bbox_to_anchor=(0, 1))

plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# GRÁFICA 3: Frecuencia de actividad acorde el tipo de tren [TRENES DE LARGA DISTANCIA]
# ----------------------------------------------------------------------------------------------------------------------

# Contamos las apariciones de cada tipo de tren en la columna que lo indica, para saber en forma de porcentaje, la
# cantidad de trenes que hay activos según su tipo correspondiente.
grouped_df_LDist = df_LDist.groupby('Tren')
er_distribution_LD = grouped_df_LDist['Tren'].count()
# Mostramos los datos obtenidos en un diagrama de tarta:
plt.style.use('ggplot')
plt.title('FRECUENCIA DE ACTIVIDAD ACORDE EL TIPO DE TREN [TRENES DE LARGA DISTANCIA]', fontdict={'fontsize': 10})
plt.ylabel('Porcentaje')
colores = ['mediumslateblue', 'mediumpurple', 'blueviolet', 'darkorchid']
er_distribution_LD.plot(kind='pie', autopct='%1.1f%%', colors=colores)
plt.legend(tipos_LD, bbox_to_anchor=(0, 1))

plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# GRÁFICA 4: Frecuencia de actividad acorde el tipo de tren [TRENES DE MEDIA DISTANCIA]
# ----------------------------------------------------------------------------------------------------------------------

# Contamos las apariciones de cada tipo de tren en la columna que lo indica, para saber en forma de porcentaje, la
# cantidad de trenes que hay activos según su tipo correspondiente.
grouped_df_MDist = df_MDist.groupby('Tren')
er_distribution_MD = grouped_df_MDist['Tren'].count()
# Mostramos los datos obtenidos en un diagrama de tarta:
plt.style.use('ggplot')
plt.title('FRECUENCIA DE ACTIVIDAD ACORDE EL TIPO DE TREN [TRENES DE MEDIA DISTANCIA]', fontdict={'fontsize': 10})
plt.ylabel('Porcentaje')
colores = ['mediumorchid', 'violet', 'plum', 'thistle']
er_distribution_MD.plot(kind='pie', autopct='%1.1f%%', colors=colores)
plt.legend(tipos_MD, bbox_to_anchor=(0, 1))

plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Imprimimos los dataframes:
# ----------------------------------------------------------------------------------------------------------------------
print(df)
print()
print(er_distribution)