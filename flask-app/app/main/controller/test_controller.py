import logging
from flask import request
from flask_restplus import Resource

from ..util.dto import TestDto

LOG = logging.getLogger('app')
api = TestDto.api
_user = TestDto.user

parser = api.parser()


@api.route('/')
class TestList(Resource):
    @api.doc('list_of_registered_users')
    def get(self):
        """List all registered users"""
        id = request.args.get('id')
        from pymongo import MongoClient
        from bson.objectid import ObjectId 
        client = MongoClient('mongodb://test:test@mongo-db:27017')
        db = client['test']
        posts = db['posts']
        thing = posts.find_one({'_id': ObjectId(id) })
        if thing:
            return {"code":0, "message":"ok", "title":str(thing['title']), "content":thing['content']}
        return {"code":1, "message":"not found"}

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        from pymongo import MongoClient
        """Creates a new User """
        data = request.json
        client = MongoClient('mongodb://test:test@mongo-db:27017')
        db = client['test']
        posts = db['posts']
        # post_data = {
        #     'title': 'Python and MongoDB',
        #     'content': 'PyMongo is fun, you guys',
        #     'author': 'Scott'
        # }
        result = posts.insert_one(data)
        print('One post: {0}'.format(result.inserted_id))
        return {"code":0, "message":"ok", "id":str(result.inserted_id)}
