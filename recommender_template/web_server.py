#!/usr/bin/python3
import os, argparse
from flask import Flask, request, json, render_template
from recommendation_engine import RecEng
from embeddings.loaders import load_custom_embeddigns, load_starspace_embeddings
from vk_api import VKapi

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html.j2')

@app.route('/get_recommendations/', methods=['GET'])
def status():
    user_id = request.args.get('user_id')
    if '/' in user_id:
        user_id = vk_api.get_user_profile(user_id.split('/')[-1])[0]['id']
    response = rec_engine.get_recommendations_for_user(user_id)
    return json.jsonify(response)

@app.route('/endpoint', methods=['POST'])
def endpoint():
    input_data = json.loads(request.data)

    output_data = dict()
    for fake_user_id, user_subsriptions in input_data.items():
        most_similar_publics_ids, similarity = rec_engine.get_recommendations_from_publics(user_subsriptions, top_limit=10)
        output_data[fake_user_id] = most_similar_publics_ids

    return json.jsonify(output_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--embedding_file', type=str, required=True)
    parser.add_argument('-k', '--vk_api_key', type=str, required=False)
    args, _ = parser.parse_known_args()

    args.vk_api_key = os.environ.get('VK_KEY', args.vk_api_key)
    if args.vk_api_key is None:
        print('VK_KEY is not set')

    loader = load_starspace_embeddings if args.embedding_file.endswith('.tsv') else load_custom_embeddigns
    trained_embeddings_df = loader(args.embedding_file)

    vk_api = VKapi(args.vk_api_key)
    rec_engine = RecEng(vk_api, trained_embeddings_df)

    app.run(host='0.0.0.0', port=6767, debug=True)