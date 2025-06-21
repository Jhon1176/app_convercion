from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange
from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_super_segura_123'  # Cambia por algo más fuerte

# === Diccionario de unidades ===
units_in_meters = {
    'm': 1,
    'km': 1000,
    'mi': 1609.34,
    'ft': 0.3048
}

# === Formulario seguro con CSRF ===
class ConvertForm(FlaskForm):
    value = StringField("Valor", validators=[InputRequired()])
    from_unit = SelectField("Desde", choices=[(u, u) for u in units_in_meters])
    to_unit = SelectField("A", choices=[(u, u) for u in units_in_meters])
    submit = SubmitField("Convertir")

# === Función de conversión ===
def convert_length(value, from_unit, to_unit):
    if from_unit not in units_in_meters or to_unit not in units_in_meters:
        return None
    value_in_meters = float(value) * units_in_meters[from_unit]
    return value_in_meters / units_in_meters[to_unit]

# === Ruta principal ===
@app.route("/", methods=["GET", "POST"])
def index():
    form = ConvertForm()
    result = None

    if form.validate_on_submit():
        try:
            result = convert_length(form.value.data, form.from_unit.data, form.to_unit.data)
        except ValueError:
            result = "Entrada inválida"

    return render_template("index.html", form=form, result=result)

# === Cabeceras de seguridad ===
@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# === Iniciar la app ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

