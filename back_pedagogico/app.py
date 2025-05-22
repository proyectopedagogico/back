from src.webserver import app

# Hay que mantener el texto tal cual el de arriba
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
