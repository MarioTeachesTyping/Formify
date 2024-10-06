from flask import Flask, render_template, jsonify, request
# from flask import Flask, 

# import request
from testCamera import *
# import jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/elbow')
def elbow():
    return render_template('elbow.html')

@app.route('/elbowDemo')
def elbow_demo():
    return render_template('elbowDemo.html')

@app.route('/elbowStretch')
def elbow_stretch():
    return render_template('elbowStretch.html')

@app.route('/knee')
def knee():
    return render_template('knee.html')

@app.route('/kneeDemo')
def knee_demo():
    return render_template('kneeDemo.html')

@app.route('/kneeStretch')
def knee_stretch():
    return render_template('kneeStretch.html')

@app.route('/wrist')
def wrist():
    return render_template('wrist.html')

@app.route('/wristDemo')
def wrist_demo():
    return render_template('wristDemo.html')

@app.route('/wristStretch')
def wrist_stretch():
    return render_template('wristStretch.html')

@app.route('/process', methods=['POST'])
def process():
    # Get data from the request (e.g., from frontend)
    m = request.json.get('m')
    n = request.json.get('n')
    x = request.json.get('x')
    
    # Call your Python function
    result = process_camera(m, n, x)
    
    # Return the result as JSON
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)