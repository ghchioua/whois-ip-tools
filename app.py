from flask import Flask
from flask_restful import Api
import resources.myipaddress as IP # import our defined resources files
import resources.otheripaddrress as RemoteIP
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from logbase import call_logger, setup_logger


call_logger()

app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='What is my IP address',
        version='v1.0',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/api/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/api/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


# our resources to be allowed in the looking glass, ex(BGP, ping, traceroute, etc..)
api.add_resource(IP.MYIP, '/api/myip/')
api.add_resource(RemoteIP.RemoteAddress, '/api/remip/<string:ipaddr>')
docs.register(IP.MYIP)
docs.register(RemoteIP.RemoteAddress)


if __name__ == '__main__':
    # debug mode has to be turned off in production, it's only for testing.
    app.run(host = "0.0.0.0", port = "5500")
