from flask import Flask, jsonify
from api.v1.views import app_views

"""
This line tells flask to use the module 
as the starting point for resolving resources 
like templates and static files
"""
app = Flask(__name__)

app.register_blueprint(app_views)

@app.route("/")
def home():
    return jsonify("API started successfully"), 200

if __name__ == "__main__":
    app.run(debug=True)