from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return render_template('formulaire.html')

    @app.route('/post_submit',methods=['get','post'])
    def post_submit():
        res = None
        if request.method == 'POST':
            city = request.form["city"]
            meteo = request.form['meteo']
            nrg1 = request.form["energie"]
            print("City : ", city, "\nmeteo : ", meteo , "\nenergie : ", nrg1)
            res = "Success"
        else:
            res =  'Error'
        
        return res


    return app

