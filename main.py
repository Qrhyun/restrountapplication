from flask import Flask
from customer.server.Personal_Query import personal_query_app
from window.server.window import window_app

app = Flask(__name__)

# Register blueprints
app.register_blueprint(personal_query_app, url_prefix='/personal_query')
app.register_blueprint(window_app, url_prefix='/window')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)