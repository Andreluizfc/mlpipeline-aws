# python imports
import json

# third imports
from flask import Flask, request, jsonify, make_response

# local imports
from server import utils

app = Flask(__name__)


@ app.route('/healthcheck', methods=('GET',))
def healthcheck():
    resp = make_response(jsonify({"Status": "ok"}), 200,)
    resp.headers["Content-Type"] = "application/json"
    return resp


@ app.route('/predict', methods=('GET',))
def predict():
    request_data = request.get_json()
    image = request_data['image']
    prediction = utils.predict(image.encode())
    resp = make_response(
        jsonify({
            "Status": "ok",
            "Prediction": prediction
        }), 200,)

    resp.headers["Content-Type"] = "application/json"
    return resp


@ app.route('/query', methods=('GET',))
def query():
    request_data = request.get_json()
    query = request_data['query']
    display = request_data['display']
    n_images = request_data['n_images']
    bucket = request_data['bucket_name']
    augment = request_data['augment']

    images = {}
    dict_df = {}
    dict_sample_df = {}
    status = "bad request"
    status_code = 400

    if query:
        df = utils.query(query)
        dict_df = df.to_dict()
        if not df.empty:
            status_code = 200
            status = "ok"
            if display:
                sample_df = df.sample(n=n_images)
                dict_sample_df = sample_df.to_dict()
                images = json.dumps(utils.load_images(
                    sample_df, bucket, augment))

    resp = make_response(
        jsonify({
            "Status": status,
            "Results": dict_df,
            "Samples": images,
            "Samples_Results": dict_sample_df,
        }), status_code,)

    resp.headers["Content-Type"] = "application/json"
    return resp


def start():
    app.run(threaded=True, host="0.0.0.0", port=5050)


def stop():
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    except Exception as e:
        print(f"Server not running - {e}")
