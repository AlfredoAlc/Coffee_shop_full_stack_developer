import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES

# @TODO implement endpoint
# GET /drinks
# it should be a public endpoint
# it should contain only the drink.short() data representation
# returns status code 200 and json {"success": True, "drinks": drinks}
# where drinks is the list of drinks or appropriate status
# code indicating reason for failure


@app.route('/drinks', methods=['GET'])
def show_drinks():

    try:
        selection = Drink.query.all()
        drinks = [Drink.short(drink) for drink in selection]
        return jsonify({
           'success': True,
           'drinks': drinks
        })
    except Exception:
        abort(404)


# @TODO implement endpoint
# GET /drinks-detail
# it should require the 'get:drinks-detail' permission
# it should contain the drink.long() data representation
# returns status code 200 and json {"success": True, "drinks": drinks}
# where drinks is the list of drinks or appropriate status code
# indicating reason for failure

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drink-detail')
def show_drink_detail(token):

    try:
        selection = Drink.query.all()
        drink = [Drink.long(drink) for drink in selection]
        return jsonify({
            'success': True,
            'drink_detail': drink
        })
    except Exception:
        abort(404)

# @TODO implement endpoint
# POST /drinks
# it should create a new row in the drinks table
# it should require the 'post:drinks' permission
# it should contain the drink.long() data representation
# returns status code 200 and json {"success": True, "drinks": drink}
# where drink an array containing only the newly created drink
# or appropriate status code indicating reason for failure


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(token):

    try:
        body = request.get_json()
        new_title = body.get('title')
        new_recipe = json.dumps(body['recipe'])

        drink = Drink(title=new_title, recipe=new_recipe)
        Drink.insert(drink)
        drink_array = Drink.long(drink)
        return jsonify({
            'success': True,
            'drink_id': drink_array
        })

    except Exception:
        abort(422)

# @TODO implement endpoint
# PATCH /drinks/<id>
# where <id> is the existing model id
# it should respond with a 404 error if <id> is not found
# it should update the corresponding row for <id>
# it should require the 'patch:drinks' permission
# it should contain the drink.long() data representation
# returns status code 200 and json {"success": True, "drinks": drink}
# where drink an array containing only the updated drink
# or appropriate status code indicating reason for failure


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(token, drink_id):

    try:
        drink = Drink.query.get(drink_id)
    except Exception:
        abort(404)

    body = request.get_json()
    if 'title' in body:
        new_title = body.get('title')
        setattr(drink, 'title', new_title)
    if 'recipe' in body:
        new_recipe = json.dumps(body['recipe'])
        setattr(drink, 'recipe', new_recipe)

    Drink.update(drink)

    drink_update = Drink.query.get(drink_id)
    return jsonify({
        'success': True,
        'drink_id': Drink.long(drink_update)
    })

# @TODO implement endpoint
# DELETE /drinks/<id>
# where <id> is the existing model id
# it should respond with a 404 error if <id> is not found
# it should delete the corresponding row for <id>
# it should require the 'delete:drinks' permission
# returns status code 200 and json {"success": True, "delete": id}
# where id is the id of the deleted record
# or appropriate status code indicating reason for failure


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):

    try:
        drink = Drink.query.get(drink_id).delete()
    except Exception:
        abort(404)

    return jsonify({
        'success': True,
        'drink_deleted': drink_id
    })

# Error Handling
# Example error handling for unprocessable entity


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

# @TODO implement error handlers using the @app.errorhandler(error)
# decorator each error handler should return (with approprate messages):
# jsonify({
#   "success": False,
#   "error": 404,
#   "message": "resource not found"
#   }), 404


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404

# @TODO implement error handler for 404
# error handler should conform to general task above

# @TODO implement error handler for AuthError
# error handler should conform to general task above

# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
