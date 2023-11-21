from flask import Flask, render_template, jsonify, request
import os 
import requests
from openai import OpenAI
from utils import get_data_from_url, generate_response, get_data, get_data, create_ad


app = Flask(__name__)
df = get_data(online=False)
client = OpenAI()


@app.route('/demo')
def index():
    param_value = request.args.get('page', '1')
    param_value = int(param_value)
    total_pages = len(df) // 3
    selected_df = df[param_value*(3-1): param_value*(3-1) + 3]
    print(df[:3])
    return render_template('index.html', 
                           data=selected_df[:3],
                           page=param_value,
                           total_pages=total_pages) 


@app.route('/generate_ad', methods=['POST'])
def generate_ad_route():
        
    data = request.get_json()
    if not data:
        return jsonify({'result': 'Nekaj je šlo narobe'}), 400

    name = int(data.get('name'))
    target_group = data.get('target_group')
    must_use_words = data.get('must_use_words')
    language = data.get('language')
    name = df.loc[name, "additional_name"]

    response = create_ad(client, name, target_group, must_use_words, language)

    return jsonify({'result': response})


@app.route('/')
def index_bye():
    return "Get out of my swamp! "


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)