from PIL import Image
from IPython.display import display
import requests as rs
import datetime as dt
import csv
from urllib.parse import quote

# USANDO API DO COVID-19
url = 'https://api.covid19api.com/dayone/country/brazil'
resp = rs.get(url)
raw_data = resp.json()
# Passando os dados do json para uma lista
final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])

final_data.insert(0, ['Confrimados', 'Óbitos', 'Recuperados', 'Ativos', 'Data']) # Inserção do cabeçalho na lista
CONFIRMADOS = 0
OBIDOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4
# MANIPULANDO A COLUNA "DATA" DA LISTA 
for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]

# PASSANDO A LISTA PARA UM ARQUIVO CSV
with open('brasil-covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(final_data)
# ALTERAÇÃO DA COLUNA "DATA" USANDO A LIB datetime
for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d')

# Usando API para geração de gráficos
# DEFINIÇAO DE DADOS
def get_datasets (y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [{
            'label': labels[0],
            'data': y
        }]
# DEFINIÇÃO DE TITULO
def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title': title,
        'display': display
    }

# CRIAÇÃO DO DICIONÁRIO
def create_chart(x, y, labels, kind='bar', title=''):

    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    return chart

def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = rs.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)

y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data_1, y_data_2], labels, title='Gráfico confirmados vs recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeiro-gráfico.png', chart_content)
display_image('meu-primeiro-gráfico.png')

def get_api_qrcode(link):
    text = quote(link) # parsing do link para url
    url_base = 'https://quickchart.io/qr'
    resp = rs.get(f'{url_base}?text={text}')
    return resp.content

url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')