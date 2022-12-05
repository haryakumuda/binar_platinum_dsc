import pandas as pd
from flask import Flask, request, jsonify, make_response, Response, render_template
from flask_swagger_ui import get_swaggerui_blueprint
from sentimentprediction import sentiment_text, sentiment_file

# Init app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  #Agar Return JSON dalam urutan yang benar

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Tworst!"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


# Homepage
@app.route('/', methods=['GET'])
def get():
    return "WELCOME TO TWORST!" 


@app.route('/nn/text', methods=["POST"])
def nn_text():
    if request.method == "POST":
        input_text = str(request.form["text"])
        sentiment = sentiment_text(input_text,'nn')
        output = dict(input=input_text, sentiment=sentiment)
        return jsonify(output)

@app.route('/nn/file', methods=["POST"])
def nn_file():
    if request.method == "POST":
        file = request.files['file']

        try:
            file = pd.read_csv(file, encoding='iso-8859-1')
        except:
            try:
                file = pd.read_csv(file, encoding='utf-8')
            except:
                try:
                    file = pd.read_csv(file, sep='\t')
                except:
                    pass
        print("======== read data csv to pandas =========")
        print(type(file))
        if(isinstance(file, pd.DataFrame)):
            file = sentiment_file(file,'nn')
            if(isinstance(file, pd.DataFrame)):
                response = Response(file.to_json(orient="records"), mimetype='application/json')
            else:
                response = "Error"
        else:
            response = "Error"
        return response

@app.route('/lstm/text', methods=["POST"])
def lstm_text():
    if request.method == "POST":
        input_text = str(request.form["text"])
        sentiment = sentiment_text(input_text,'lstm')
        output = dict(input=input_text, sentiment=sentiment)
        return jsonify(output)

@app.route('/lstm/file', methods=["POST"])
def lstm_file():
    if request.method == "POST":
        file = request.files['file']

        try:
            file = pd.read_csv(file, encoding='iso-8859-1')
        except:
            try:
                file = pd.read_csv(file, encoding='utf-8')
            except:
                try:
                    file = pd.read_csv(file, sep='\t')
                except:
                    pass
        print("======== read data csv to pandas =========")
        print(type(file))
        if(isinstance(file, pd.DataFrame)):
            file = sentiment_file(file,'lstm')
            if(isinstance(file, pd.DataFrame)):
                response = Response(file.to_json(orient="records"), mimetype='application/json')
            else:
                response = "Error"
        else:
            response = "Error"
        return response



# error handling
@app.errorhandler(400)
def handle_400_error(_error):
    "Return a http 400 error to client"
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    "Return a http 401 error to client"
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    "Return a http 404 error to client"
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)


#Run Server
if __name__ == '__main__':
    app.run(debug=True)
# Default IP 127.0.0.1 Port 5000








