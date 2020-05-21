import os

from flask import Flask, render_template, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

dburl = 'postgresql://natasha:natasha@localhost:5432/mydb'
engine = create_engine(dburl)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def add():
  day = request.form.get("day")
  month = request.form.get("month")
  goal = request.form.get("goal")
  total = float(request.form.get("total"))
  easy_total = float(request.form.get("easy_total"))
  medium_total = float(request.form.get("medium_total"))
  hard_total = float(request.form.get("hard_total"))
  percent_easy = float((easy_total*100) /total)
  percent_medium = float((medium_total*100) /total)
  percent_hard = float((hard_total*100) /total)
  db.execute("INSERT INTO productivity (day, month, goal, total, easy_total, medium_total, hard_total, percent_easy, percent_medium, percent_hard) VALUES (:day, :month, :goal, :total, :easy_total, :medium_total, :hard_total, :percent_easy, :percent_medium, :percent_hard)", {"day": day, "month": month, "goal": goal, "total": total, "easy_total": easy_total, "medium_total": medium_total, "hard_total": hard_total, "percent_easy": percent_easy, "percent_medium": percent_medium, "percent_hard": percent_hard})
  db.commit()
  works = db.execute("SELECT * FROM productivity").fetchall()
  return render_template("logbook.html", works=works)

#run with:
#export FLASK_APP=application1.py
#flask run
