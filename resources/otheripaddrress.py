from flask_restful import Resource
# netaddr is a fast easy python library to make IP address related operations, but we can get rid of it and make it
# from scratch like: sum(bin(int(x)).count('1') for x in ,mask.split('.'))
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask import request, jsonify
import requests, logging, json
from logbase import call_logger, setup_logger
from database.country import country_data as cdata
from database.country import get_country_code


logger_visits = logging.getLogger("logger_visits")
logger_uses = logging.getLogger("logger_uses")

class RemoteAddressSchema(Schema):
    ip = fields.String(required=True, default="0.0.0.0")
    country = fields.String(required=True, default="NA")
    languages = fields.String(required=False, default="NA")
    currency = fields.String(required=False, default="NA")
    



class RemoteAddress(MethodResource, Resource):
    @doc(description='Remomte address', tags=['IP Addreess'])
    @marshal_with(RemoteAddressSchema)  # marshalling
    def get(self, ipaddr):
        result = {}        
        result['ip'] = ipaddr
        country_code = get_country_code(ipaddr)
        country_data = cdata(country_code)
        result['country'] = country_data['Name']
        result['languages'] = country_data['Languages']
        result['currency'] = country_data['Currency']
        logger_visits.info("Remote IP address: {}, Country: {}".format(ipaddr, country_data['Name']))
        return result