import flask
from flask import request, jsonify
import apiParser


app = flask.Flask(__name__)

@app.route("/420", methods=['GET'])
def response420():
    result = []
    data = apiParser.get_data()
    i = 0    
    for match_data in data:
        line = apiParser.create_data_string(data, "t,s,s,s,N1,s,S1,-,S2,s,N2,s", i)
        result.append(line)  
        i = i+1
    return jsonify(result)

