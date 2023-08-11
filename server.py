from flask import Flask, render_template, jsonify, request
import pandas as pd
from aero import cal_prob


app = Flask(__name__)
#### This take input from the html form 
@app.route("/", methods =["GET", "POST"])
def home():
    if request.method == "POST":
        f_date= request.form.get("date")
        airplane=request.form.get("streamlistselect")
        dept_airport=request.form.get("streamlistselectdept")
        arr_airport=request.form.get("streamlistselectarr")
        dept_time=request.form.get("depttime")
        arr_time=request.form.get("arrtime")
    
        Day=f_date.split('-')
        DayofMonth=int(Day[2])
        passe = cal_prob(DayofMonth,dept_time,arr_time,airplane,arr_airport,dept_airport) # variables are passed to the prediction function
        print(passe)

        return render_template("home.html",passe=passe,pname=airplane, fromairport=dept_airport, toairport=arr_airport,ad=dept_time,aa=arr_time) # the prediction along with some of teh useful variables ,
                                                                                                                                                    #the variables are send to html page to be displayed
    return render_template("home.html")

@app.route("/carrier")# this is the api, which gets called in frontend to provide vales of airplanes to dropdown box
def ho():
    my_file = open("clean_carr.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    return data_into_list

@app.route("/dept")# this is the api, which gets called in frontend to provide vales of departure airports to dropdown box
def hodept():
    my_file = open("dept.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    return data_into_list

@app.route("/arr")# this is the api, which gets called in frontend to provide vales of arrival airports to dropdown box
def hoarr():
    my_file = open("arr.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    return data_into_list
    
if __name__ == "__main__":
    app.run(debug=True)