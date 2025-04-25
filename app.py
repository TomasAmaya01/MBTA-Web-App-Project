import os
from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form.get("place", "")
    if not place.strip():
        return render_template("error.html", message="Please enter a valid place or address.")

    try:
        geocode_url = mbta_helper.build_geocode_url(place)
        stop_info = mbta_helper.find_stop_near(place)
        return render_template(
            "mbta_station.html",
            place=place,
            geocode_url=geocode_url,
            stop_info=stop_info
        )
    except Exception as e:
        return render_template("error.html", message=str(e))

if __name__ == "__main__":
    app.run(debug=True)
