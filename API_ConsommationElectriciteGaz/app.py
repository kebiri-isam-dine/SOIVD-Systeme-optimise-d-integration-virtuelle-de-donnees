# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:44:17 2022

@author: Mesrs
"""

from flask import Flask , render_template
import requests 
import json


#Instantiation de flask
app = Flask(__name__)

#Create endpoint 

@app.route('/',methods=['GET'])
def index():
    
    #make request to the url
    req = requests.get('https://tinyurl.com/4f95debc')
    #check if there is an error
    #print(req.content)s
    #Convert the data into python dictionnary  using the json model 
    #parsing data to index 
    data = json.loads(req.content)
    #convert the data into python object
    #json_data = json.loads(data) #loads : convert the data into python object
    
    return render_template('index.html',data=data)

@app.route('/meteo',methods=['GET'])
def meteo():
    
    #make request to the url
    req = requests.get('https://tinyurl.com/4btap4f6')
   
    data = json.loads(req.content)
    
    
  
    
    return render_template('meteo.html',data=data)
