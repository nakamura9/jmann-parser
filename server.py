
# $env:FLASK_APP = "server.py"
# $env:FLASK_ENV = "development"
from flask import Flask, render_template, request, jsonify
import json 
from models import Item, Base
from parsr import find_node

from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite3?check_same_thread=False')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


app = Flask(__name__)
mapping = None
with open('trie.json', 'r') as f:
    mapping = json.load(f)

@app.route('/')
def hello_world():
    lines = [child['description'] for child in mapping['children']]
        
    return render_template('index.html', types=lines)

@app.route('/type-filter')
def product_type_filter():
    resp = {}
    
    product_type = request.args.get('product_type')
    
    res = session.query(Item).filter(Item.product_type == product_type).all()
    resp['items'] = [i.name for i in res[:100]]
    rules = set()
    for node in mapping['children']:
        if node['description'] == product_type:
            for subnode in node['children']:
                rules.add(subnode['description'])
                
    resp['rules'] = list(rules) 
    return jsonify(resp)

@app.route('/q-filter') #/<int:q>
def q1_filter():
    resp = {}
    filters = {}
    product_type = request.args.get('product_type')
    filters['product_type'] = product_type
    # 01 for the department group
    qs = "01" + product_type
    
    def process_q(n, f,response, query_string): 
        global request
        q = request.args.get(n)
        if q:
            f[n] = q
            # no rules at this level
            if n == "q6":
                return
            
            query_string += " " + q
            node = find_node(query_string)
            if node:
                response[n + "_rules"] = [i['description'] for \
                    i in node['children']]
    
    for q in ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']:
        process_q(q, filters, resp, qs)
    
    query = session.query(Item).filter_by(**filters).all()
    resp['items'] = [i.name for i in query[:100]]
    
    return jsonify(resp)