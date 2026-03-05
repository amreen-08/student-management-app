import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        student_id = request.form["id"]

        # Check if ID already exists
        existing = Student.query.get(student_id)
        if existing:
            return "Error: Student ID already exists!"

        student = Student(
            id=student_id,
            name=request.form["name"],
            age=int(request.form["age"]),
            gender=request.form["gender"],
            dob=request.form["dob"],
            phone=request.form["phone"],
            email=request.form["email"]
        )

        db.session.add(student)
        db.session.commit()

        return "Student Added Successfully!"

    return render_template("index.html")

@app.route("/view", methods=["GET", "POST"])
def view():
    if request.method == "POST":
        student_id = request.form["id"]
        student = Student.query.get(student_id)

        if student:
            return render_template("view.html", student=student)
        else:
            return "Student Not Found!"

    return render_template("view.html", student=None)

if __name__ == "__main__":
    app.run(debug=True)