# coding=utf-8
import requests


# api-endpoint 
URL = "https://my.business.blockpays.io/client/api/v1/"
APIKEY = '' 
HEADERS = {}
def setApiKey(apikey):
    global APIKEY
    APIKEY = apikey
    global HEADERS
    HEADERS = { 
            'User-Agent' :'Blockpays/v1.0.0', 
            'accountId' : APIKEY, 
            'Content-Type' : 'application/json', 
            'origins' : '*',
            'accept' : '*/*'
        }

def getCurrencies(params):
        
    # sending get request and saving the response as response object 
    r = requests.post(url = URL + 'getCurrencies', json = params,headers = HEADERS) 
    
    # extracting data in json format 
    
    return r.json()

def isValidAddress(params):
       
    # sending get request and saving the response as response object 
    r = requests.post(url = URL + 'isValidAddress', json = params,headers = HEADERS) 
    
    # extracting data in json format 
    
    return r.json()
    