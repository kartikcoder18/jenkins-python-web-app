from flask import Flask

app = Flask(__name__)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
@app.route("/")
def home():
    return "Hello from nnew Python Web App via Jenkins & Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
