import csv
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def exchange():
    rates = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = rates.json()
    
    waluta = ""
    wybor = ""
    info = ""
    if request.method == "POST":
        dane = request.form
        waluta = dane.get("waluta")
        ilosc = float(dane.get('ilosc'))
        wybor = waluta.strip()

        for item in data[0]['rates']:
            if item["currency"] == wybor:
                wynik=item["bid"]*ilosc
        return render_template("exchange.html", tablica=data[0]['table'], data=data[0]["rates"], wynik=round(wynik,2), wybor=dane.get('waluta'), ilosc=ilosc, opis=f'Wybrana ilość: {str(ilosc)}{wybor} .Całkowity koszt to: {str(round(wynik,2))}')
    if request.method == "GET":
        return render_template("exchange.html", tablica=data[0]['table'],data= data[0]["rates"],wynik=0.00, wybor=' ', ilosc=0)
    