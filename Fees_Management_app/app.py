from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cno = db.Column(db.Integer, nullable=False)
    cname = db.Column(db.String(100), nullable=False)
    tfees = db.Column(db.Integer, nullable=False)
    feespaid = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


    def __repr__(self) -> str:
        return f"{self.lname} - {self.fname}"

@app.route("/")
def homepage():

    return render_template('index.html')


@app.route("/studentlogin", methods = ['GET','POST'])
def studentlogin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()
        if(student.email == email and student.password == password):
            return render_template('Fees_view.html', student = student)
        else:
            return  redirect('StudentLogin.html')
    students = Student.query.all()
    return render_template('StudentLogin.html', students=students)

@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method =='POST':
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        cno = request.form['cno']
        cname = request.form['cname']
        tfees = request.form['tfees']
        feespaid = request.form['feespaid']
        student = Student(fname=fname, lname=lname, password=password, email = email,cno = cno,cname=cname,tfees=tfees,feespaid=feespaid)
        db.session.add(student)
        db.session.commit()
    students = Student.query.all()
    print(students)
    return render_template('Register.html',students=students)
@app.route("/view")
def students_view():
    students = Student.query.all()
    print(students)

@app.route("/studentview/<email>")
def student_view(email):
    student = Student.query.filter_by(email=email)
    print(student)
    return render_template('Fees_view.html',student=student)


@app.route("/delete/<int:sno>")
def delete(sno):
    student = Student.query.filter_by(sno=sno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/register')

@app.route("/update/<int:sno>",methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        cname = request.form['cname']
        tfees = request.form['tfees']
        feespaid = request.form['feespaid']
        feesadd = request.form['feesadd']
        student = Student.query.filter_by(sno=sno).first()

        student.fname = fname
        student.lname = lname
        student.cname = cname
        student.tfees = tfees
        student.feespaid = int(feespaid) +int(feesadd)
        db.session.add(student)
        db.session.commit()
        return redirect('/register')
    student = Student.query.filter_by(sno=sno).first()
    return render_template('Fees_updating.html', student=student)

if __name__=='__main__':
    app.run(debug=True, port=8000)

#To run this application write in the terminal 'python .\app.py'