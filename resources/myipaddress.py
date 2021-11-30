from flask_restful import Resource
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

class MyIpAddressSchema(Schema):
    ip = fields.String(required=True, default="0.0.0.0")
    country = fields.String(required=True, default="NA")
    languages = fields.String(required=False, default="NA")
    currency = fields.String(required=False, default="NA")


class MYIP(MethodResource, Resource):
    @doc(description='My IP address', tags=['IP Addreess'])
    @marshal_with(MyIpAddressSchema)  # marshalling
    def get(self):
        result = {}
        ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        result['ip'] = ipaddr
        country_code = get_country_code(ipaddr)
        country_data = cdata(country_code)
        result['languages'] = country_data['Languages']
        result['currency'] = country_data['Currency']
        result['country'] = country_data['Name']
        logger_visits.info("IP address: {}, Country: {}".format(ipaddr, country_data['Name']))
        return result
