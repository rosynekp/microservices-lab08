from flask import Flask, render_template, jsonify, request
from database import AnimalCrossingDatabase
from services import UserService, ItemService
import requests
import json

app = Flask(__name__)
# @app.after_request
# def add_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = "*"
#     response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
#     response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
#     return response

@app.route('/')
def index():
    return render_template('index.html')

# ------------ ITEM ENDPOINTS ------------
@app.route('/fish/all', methods=["GET"])
def all_fish():
    """Returns all fish"""
    table_name = 'fish'
    return jsonify(ItemService(table=table_name).get_all())


@app.route('/fish/id/<fishID>', methods=["GET"])
def get_fish_by_id(fishID):
    """Returns all fish"""
    table_name = 'fish'
    return jsonify(ItemService(table=table_name).get_by_id(fishID))


@app.route('/fish/name', methods=["POST"])
def get_fish_by_name():
    """Returns fish by name"""
    table_name = 'fish'
    return jsonify(ItemService(table=table_name).get_by_name(request.get_json()))


@app.route('/filter/fish/sell', methods=["POST"])
def fish_filter_by_sell():
    """Returns fish filtered by sell price"""
    table_name = 'fish'
    return jsonify(ItemService(table=table_name).filter_by_sell_price(request.get_json()))


@app.route('/insects/all', methods=["GET"])
def all_insects():
    """Returns all insects"""
    table_name = 'insect'
    return jsonify(ItemService(table=table_name).get_all())


@app.route('/insects/id/<insectID>', methods=["GET"])
def get_insect_by_id(insectID):
    """Returns insect with given id"""
    table_name = 'insect'
    return jsonify(ItemService(table=table_name).get_by_id(insectID))


@app.route('/insects/name', methods=["POST"])
def get_insect_by_name():
    """Returns insect by name"""
    table_name = 'insect'
    return jsonify(ItemService(table=table_name).get_by_name(request.get_json()))


@app.route('/filter/insects/sell', methods=["POST"])
def insect_filter_by_sell():
    """Returns insect filtered by sell price"""
    table_name = 'insect'
    return jsonify(ItemService(table=table_name).filter_by_sell_price(request.get_json()))


@app.route('/tools/all', methods=["GET"])
def all_tools():
    """Returns all tools"""
    table_name = 'tool'
    return jsonify(ItemService(table=table_name).get_all())


@app.route('/tools/id/<toolID>', methods=["GET"])
def get_tool_by_id(toolID):
    """Returns tool with given id"""
    table_name = 'tool'
    return jsonify(ItemService(table=table_name).get_by_id(toolID))


@app.route('/tools/name', methods=["POST"])
def get_tool_by_name():
    """Returns tool by name"""
    table_name = 'tool'
    return jsonify(ItemService(table=table_name).get_by_name(request.get_json()))


@app.route('/filter/tools/sell', methods=["POST"])
def tools_filter_by_sell():
    """Returns tools filtered by sell price"""
    table_name = 'tool'
    return jsonify(ItemService(table=table_name).filter_by_sell_price(request.get_json()))

# ------------ USER ENDPOINTS ------------
@app.route('/users/all', methods=["GET"])
def all_users():
    """Returns all users"""
    return jsonify(UserService().get_all_users())

@app.route("/users/create", methods=["POST"])
def add_user():
    """Add a user to the database"""
    return jsonify(UserService().create(request.get_json()))

@app.route("/users/<userID>", methods=["DELETE"])
def delete_user(userID):
    """Remove a user from the database"""
    return jsonify(UserService().delete_user(userID))

@app.route("/users/<userID>", methods=["GET"])
def get_user(userID):
    """Get user data by userID"""
    return jsonify(UserService().get_by_id(userID))

@app.route("/users/<userID>", methods=["PUT"])
def update_user(userID):
    return jsonify(UserService().update_username(userID, request.get_json()))



if __name__ == "__main__":
    AnimalCrossingDatabase()
    app.run(debug=True, host='127.0.0.1', port=5000)
