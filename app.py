from flask import Flask, render_template, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import logging
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_super_segura_123'

# ✅ Para desarrollo local en HTTP, comentar Secure
# En producción, cámbialo a True si usas HTTPS
# app.config['SESSION_COOKIE_SECURE'] = True

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Inicializar CSRF
csrf = CSRFProtect(app)

# Configurar logging para errores
logging.basicConfig(level=logging.INFO)

# === Diccionario de unidades ===
units_in_meters = {
    'm': 1,
    'km': 1000,
    'mi': 1609.34,
    'ft': 0.3048
}

# === Formulario seguro con validación numérica ===
class ConvertForm(FlaskForm):
    value = DecimalField("Valor", validators=[InputRequired(), NumberRange(min=0)])
    from_unit = SelectField("Desde", choices=[(u, u) for u in units_in_meters])
    to_unit = SelectField("A", choices=[(u, u) for u in units_in_meters])
    submit = SubmitField("Convertir")

# === Función de conversión ===
def convert_length(value, from_unit, to_unit):
    if from_unit not in units_in_meters or to_unit not in units_in_meters:
        return None
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None
    value_in_meters = numeric_value * units_in_meters[from_unit]
    return value_in_meters / units_in_meters[to_unit]


# === Ruta para favicon (opcional) ===
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# === Ruta principal ===
@app.route("/", methods=["GET", "POST"])
def index():
    form = ConvertForm()
    result = None
    error_message = None

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                result = convert_length(form.value.data, form.from_unit.data, form.to_unit.data)
            except Exception as e:
                app.logger.error(f"Error de conversión: {e}")
                error_message = "Error al procesar la conversión."
        else:
            error_message = "Por favor, ingrese un número válido."

    return render_template("index.html", form=form, result=result, error_message=error_message)

# === Cabeceras de seguridad ===
@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    return response

# === Manejo de errores personalizados ===
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Error interno del servidor: {e}")
    return render_template("500.html"), 500

@app.errorhandler(Exception)
def all_exception_handler(e):
    if isinstance(e, HTTPException):
        return e
    app.logger.error(f"Excepción no controlada: {e}")
    return render_template("500.html"), 500

# === Iniciar la app ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

