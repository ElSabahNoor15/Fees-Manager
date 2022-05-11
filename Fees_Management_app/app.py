from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route("/register", methods = ['GET','POST'])
def register():
    return render_template('Register.html')

if __name__=='__main__':
    app.run(debug=True, port=8000)

#To run this application write in the terminal 'python .\app.py'