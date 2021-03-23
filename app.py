
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
    # file.save(file.filename)
    file.save(infile)
    pred, gradcam_outfile = classifier.get_output(infile, outfile)
    print(pred, gradcam_outfile)
    return {"pred": pred, "gradcam_outfile": gradcam_outfile}

@app.route('/website', methods=['GET'])
def webpage():
    return flask.render_template('index.html')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
