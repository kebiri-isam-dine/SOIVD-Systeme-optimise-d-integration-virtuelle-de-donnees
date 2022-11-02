import json
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandasql import sqldf
def get_data_query():
    url='https://odre.opendatasoft.com/api/records/1.0/search/?dataset=consommation-quotidienne-brute-regionale&q=&sort=-consommation_brute_gaz_grtgaz&facet=date_heure&facet=code_insee_region&facet=region'
    lista=['code_insee_region','date_heure', 'date', 'heure',  'region', 'consommation_brute_electricite_rte', 'consommation_brute_totale', 'consommation_brute_gaz_totale']
    response= rq.get(url)
    Repense = response.content
    parse_json = json.loads(Repense)
    n=parse_json['records'].__len__()
    list_data=[x for x in parse_json['records']]
    list_dic,df={},{}
    for i in range(n):
        list_dic[i]={key: list_data[i]["fields"][key] for key in lista}
    data=pd.DataFrame.from_dict(list_dic[0], orient='index').T
    for i in range(1,n):
        df[i]=pd.DataFrame.from_dict(list_dic[i], orient='index').T
        data=pd.concat([data,df[i]], axis=0)
    print(data)
    print(f'select columns from {lista}')
    cols = str(input('\n SELECT (columns):'))
    where_condition =  str(input("\n FROM : (Data) \n\n WHERE (column = 'condition') : "))
    if cols and where_condition:
        query = f""" 
            SELECT {cols} 
            FROM data
            WHERE {where_condition}
            """
    elif cols:
        query = f""" 
            SELECT {cols} 
            FROM data
            """
    else:
        print('you did not select any column to query !!')
#     TO USE : TRY .....
    return sqldf(query)
get_data_query()

# Examples:
# Q1: 
#     select : *
# Q2:
#     select : *
#     where  : region='Normandie'
# Q3:
#     select : region,date,consommation_brute_electricite_rte
#     where  : region='Nouvelle-Aquitaine' and date='2022-03-27'
