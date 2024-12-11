from flask import Flask, render_template
from customer.server.Personal_Query import personal_query_app
from window.server.window import window_app

app = Flask(__name__,template_folder='.')

# Register blueprints
app.register_blueprint(personal_query_app, url_prefix='/personal_query')
app.register_blueprint(window_app, url_prefix='/window')

@app.route('/')
def index():
    return render_template('/templates/index.html')

@app.route('/personal_query')
def index_personal_query():
    meal = []
    meal = meal
    return render_template('/customer/ui/recent_meal.html',meal=meal)

@app.route('/window')
def index_window():
    return render_template('/window/ui/window.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)