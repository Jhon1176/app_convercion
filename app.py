from flask import Flask, render_template, request

app = Flask(__name__)

def convert_length(value, from_unit, to_unit):
    units_in_meters = {
        'm': 1,
        'km': 1000,
        'mi': 1609.34,
        'ft': 0.3048
    }

    if from_unit not in units_in_meters or to_unit not in units_in_meters:
        return None

    value_in_meters = float(value) * units_in_meters[from_unit]
    return value_in_meters / units_in_meters[to_unit]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    value = from_unit = to_unit = None

    if request.method == "POST":
        value = request.form.get("value")
        from_unit = request.form.get("from_unit")
        to_unit = request.form.get("to_unit")
        if value and from_unit and to_unit:
            try:
                result = convert_length(value, from_unit, to_unit)
            except ValueError:
                result = "Entrada inválida"

    return render_template("index.html", result=result, value=value, from_unit=from_unit, to_unit=to_unit)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
