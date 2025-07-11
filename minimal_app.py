# minimal_app.py
# Esta es la aplicación de Flask más simple posible.
# SOLO importamos Flask. No hay ollama, requests, etc.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/testvoz')
def test_voz_route():
    """
    Esta ruta sirve exactamente el mismo archivo de prueba de antes,
    pero desde una app completamente limpia.
    """
    print("Sirviendo /testvoz desde la APP MÍNIMA.")
    return render_template('test_voz.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)