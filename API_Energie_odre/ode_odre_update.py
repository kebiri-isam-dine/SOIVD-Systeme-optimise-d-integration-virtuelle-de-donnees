import json
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandasql import sqldf
from termcolor import colored

print(colored("""
Examples of queries to the Energy API 1:
Q1:
    select : *
Q2:
    select : *
    where  : region='Normandie'
Q3:
    select : region,date,consommation_brute_electricite_rte
    where  : region='Nouvelle-Aquitaine' and date='2022-03-27'
\n""", 'green'))

print(colored("""
Examples of queries to the Energy API 2:
Q1:
    select : *
Q2:
    select : *
    where  : region='Bretagne'
Q3:
    select : code, region, energie_injectee
    where  : code=44 and horodate='2019-12-31T23:00:00+00:00'
\n""", 'green'))

print(colored("""
Possibles columns in df2: [code_insee_region, date_heure, date, heure, region, consommation_brute_electricite_rte,consommation_brute_totale,consommation_brute_gaz_totale]"""
    , 'blue'))
print(colored("""Possibles columns in df2: [horodate, code, region, energie_injectee,nb_points_injection]"""
    , 'blue'))


def get_data_from_energy(list_of_tables,url):
    lista=list_of_tables
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
    return data

list_api_1=['code_insee_region','date_heure', 'date', 'heure',  'region', 'consommation_brute_electricite_rte', 'consommation_brute_totale', 'consommation_brute_gaz_totale']
url1='https://odre.opendatasoft.com/api/records/1.0/search/?dataset=consommation-quotidienne-brute-regionale&q=&sort=-consommation_brute_gaz_grtgaz&facet=date_heure&facet=code_insee_region&facet=region'

list_api_2=['horodate','code','region','energie_injectee', 'nb_points_injection' ]
url2="""https://opendata.agenceore.fr/api/records/1.0/search/?dataset=production-demi-horaire-agregee-par-region&q=&sort=-horodate&facet=horodate&facet=region&facet=grd""" 

df1=get_data_from_energy(list_api_1,url1)
print(df1.head(3))

df2=get_data_from_energy(list_api_2,url2)
print(df2.head(3))

# Imagine we have this Globale query and we want to send each column to his corresponding api 
# this we have to extract the column name that exist in each API so that is what we are goining to see in the following cells.

Query=""" 
SELECT df1.region,df2.region, df1.consommation_brute_electricite_rte, df2.energie_injectee
FROM df1
INNER JOIN df2 ON df1.region = df2.region
WHERE df2.region='Pays de la Loire'"""#print(Repense)

print(Query)
sqldf(Query)

start = 'SELECT'#print tables_in_query
end = 'FROM'
tables_in_query=Query[Query.find(start)+len(start):Query.rfind(end)].strip().split(',')
print(tables_in_query)

list_api1 = []
list_api2 = []
list_api3 = []
for word in tables_in_query:
    if word.startswith("df1") or word.startswith(" df1"):#print tables_in_query
        list_api1.append(word.split('.')[1])
    elif word.startswith("df2") or word.startswith(" df2"):
        list_api2.append(word.split('.')[1])
    else:
        list_api3.append(word.split('.')[1])

df1=get_data_from_energy(list_api1,url1)
df2=get_data_from_energy(list_api2,url2)

def get_response(df_1=df1,df_2=df2,df_3=df2,region='Pays de la Loire'):
#     join, left, right, inner, outer
#     union, concatenate ...
    matching_cols='region'
#     Final_Data=df_3.join((df_2.join(df_1.set_index(matching_cols),
#                        on=matching_cols)).set_index(matching_cols),
#                        on=matching_cols)
    Final_Data=(df_2.join(df_1.set_index(matching_cols), on=matching_cols))

    return Final_Data[Final_Data['region']==region]

df=get_response(df1,df2)
print(df)