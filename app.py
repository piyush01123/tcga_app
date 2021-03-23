
import flask
from werkzeug import secure_filename
import os
import classifier
import base64

app = flask.Flask("Image_Captioning", template_folder="templates")

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World"

@app.route('/classify', methods=['POST'])
def classify():
    infile = "uploads/temp.png"
    outfile = "static/outdir/test.png"
    file = flask.request.files['img']
    print("Input File:", file.filename)
    file.save(infile)
    pred = classifier.get_output(infile, outfile)
    pred_dict = {0: "CANCER", 1: "NORMAL"}
    pred = pred_dict[pred]
    gradcam_base64_str = base64.b64encode(open(outfile, 'rb').read()).decode('utf-8')
    f = open("base64.text",'w')
    f.write(gradcam_base64_str)
    f.close()
    print("Output", pred, "len(b64)", len(gradcam_base64_str))
    return {"pred": pred, "gradcam_base64": gradcam_base64_str}

@app.route('/website', methods=['GET'])
def webpage():
    return flask.render_template('index.html')


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
