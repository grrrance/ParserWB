from parser import ParserWB
from flask import Flask, request, abort
from flask_restful import Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api()


class QuerySchema(Schema):
    count = fields.Int(required=True)
    query = fields.Str(required=True)


schema = QuerySchema()
parser = ParserWB()


class Main(Resource):
    def get(self):
        args = request.args
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))
        return parser.parse(args['query'], int(args['count']))


api.add_resource(Main, "/products")
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=1488, host="0.0.0.0")