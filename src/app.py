import redis
from flask import Flask, request
from flask_restful import Resource, Api
from src.routes.SimpleTestRoute import SimpleRoute

app = Flask(__name__)
api = Api(app)
connection = 'zookeeper://guest:guest@localhost:4041//'
r = redis.StrictRedis(host='localhost', port=6379, db=0)


class HelloWorld(Resource):

    def get(self):
        tmp = r.get(request.remote_addr + request.url)
        if tmp:
            return tmp
        route = SimpleRoute()
        route.build()
        route.input("hello world")
        result = route.output()
        r.set(request.remote_addr + request.url, result, ex=10)
        return result


api.add_resource(HelloWorld, '/')
