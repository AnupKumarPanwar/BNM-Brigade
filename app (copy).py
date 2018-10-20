import time
import datetime
import os
from flask import Flask, render_template, request, Response, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/test')
def test():
    response = {"success": True, "data": "Wild fire has been reported successfully. Assistance will reach to spot soon."}
    return Response(json.dumps(response),  mimetype='application/json')


@app.route('/uploads/<path:path>')
def send_js(path):
    return send_from_directory('uploads', path)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    report_text = request.form['report_text']
    lat = request.form['lat']
    lng = request.form['lng']
    report_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    print(report_text)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)



    data=''

    with open('data.json') as json_file:  
        data = json.load(json_file)

    report = {"image_path": f, "report_text": report_text, "lat": lat, "lng": lng, "report_time": report_time}

    data['data'].append(report)


    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)




    response = {"success": True, "data": "Wild fire has been reported successfully. Assistance will reach to spot soon."}

    return Response(json.dumps(response), mimetype='application/json')


@app.route('/getdata')
def getdata():
    with open('data.json') as json_file:  
        data = json.load(json_file)
    return Response(json.dumps(data),  mimetype='application/json')
