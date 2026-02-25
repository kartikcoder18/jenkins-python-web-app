from flask import Flask

app = Flask(_name_)

@app.route("/")
def home():
    return "Hello from NEW Python Web App via Jenkins & Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
