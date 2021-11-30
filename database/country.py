import pandas as pd 
from flask import jsonify
import os, requests

dir = os.path.dirname(__file__)

def country_data(country_code):
    datafile = pd.read_csv(os.path.join(dir, 'data.csv'), index_col='Code')
    result = datafile.loc[country_code]
    #print(result)
    return result.to_dict()


def get_country_code(ipaddr):
    try:
        url = 'https://stat.ripe.net/data/whois/data.json?resource={}'.format(ipaddr)
        response = requests.get(url).json()['data']['records'][0]
    except:
        country_code = 'private'
        return country_code
    try:
        for dct in response:
            if dct['key'] == 'country':
                country_code = dct['value']
                #print(country_code)
        return country_code
    except:
        country_code = 'private'
        return country_code
