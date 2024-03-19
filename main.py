import json
import product
from parser import ParserWB
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api()


class QuerySchema(Schema):
    count = fields.Int(required=False)
    query = fields.Str(required=False)
    min_price = fields.Int(required=False)
    max_price = fields.Int(required=False)
    sort_price = fields.Bool(required=False)
    sort_up = fields.Bool(required=False)


schema = QuerySchema()
parser = ParserWB()


class Main(Resource):
    def get(self):
        args = request.args
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))

        query = "гитхаб"
        count = 5
        min_price = "0"
        max_price = "1000000"
        is_sort_price = False
        is_sort_up = True

        if "query" in args:
            query = args["query"]

        if "count" in args:
            count = int(args["count"])

        if "min_price" in args:
            min_price = args["min_price"]

        if "max_price" in args:
            max_price = args["max_price"]

        if "sort_price" in args:
            is_sort_price = args["sort_price"]

        if "sort_up" in args:
            is_sort_up = args["sort_up"]

        return jsonify(parser.parse(query, count, min_price, max_price, is_sort_price, is_sort_up).class_to_dict())


api.add_resource(Main, "/products")
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=1488, host="0.0.0.0")