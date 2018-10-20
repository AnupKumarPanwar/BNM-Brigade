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



    #!/usr/bin/python
    ## get subprocess module
    import subprocess ## call date command ##
    p = subprocess.Popen("python label_image1.py --image ./"+f+" --graph output_graph1.pb --labels output_labels1.txt", stdout=subprocess.PIPE, shell=True) ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (output, err) = p.communicate() ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    fire_or_not="No"
    fire_type="NA"
    if output[0]=='y':
    	fire_or_not='Yes'
    	p = subprocess.Popen("python label_image2.py --image ./"+f+" --graph output_graph2.pb --labels output_labels2.txt", stdout=subprocess.PIPE, shell=True) ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    	## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. ##
    	## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    	## or None, if no data should be sent to the child.
    	(output, err) = p.communicate() ## Wait for date to terminate. Get return returncode ##
    	p_status = p.wait()
    	fire_type=output


    data=''

    with open('data.json') as json_file:  
        data = json.load(json_file)

    report = {"image_path": f, "report_text": report_text, "lat": lat, "lng": lng, "report_time": report_time, "fire_detected": fire_or_not, "fire_type": fire_type}

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

