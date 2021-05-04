from flask import Flask, render_template, request
import requests
import csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
fname = "plik.csv"

with open(fname, "w", newline='') as csvfile:
    csv_file = csv.writer(csvfile, delimiter=";")
    csv_file.writerow(["currency", "code", "bid", "ask"])
    for item in data[0]["rates"]:
        csv_file.writerow([item['currency'], item['code'], item['bid'], item['ask']])


app = Flask(__name__)

def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 1

@app.route("/", methods=["GET", "POST"])
def przelicznik():
    with open(fname, "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        kursy = {}
        for row in csv_reader:
            kursy[row[1]] = row[2]
    if request.method == "POST":
        wybor = request.form.get("waluty_do_wyboru", None)
        if wybor and wybor != "bid":
            wybor = to_float(wybor)
            kwota = to_float(request.form.get("from", 1))
            result = wybor * kwota
            return render_template("przelicznik.html", kursy=kursy, result=result, kwota=kwota)

    return render_template("przelicznik.html", kursy=kursy, result="", kwota="")


app.run(debug=True)