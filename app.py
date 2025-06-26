from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Flask App is Working!</h1><p>If you see this, your Flask app is running correctly.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5001) 