from flask import Flask, jsonify, render_template
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
