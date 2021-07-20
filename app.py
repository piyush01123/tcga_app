
import flask
from werkzeug import secure_filename
import os
import visualizer
import visualizer_v2
import base64
import random

app = flask.Flask("TCGA Website", template_folder="templates")
organs = ['BRCA', 'COAD', 'KICH', 'KIRC', 'KIRP', 'LIHC', 'LUAD', 'LUSC', 'PRAD', 'READ', 'STAD']


@app.route('/test', methods=['GET'])
def hello_world():
    return {"msg_type": "test message", "msg": "Hello World"}


@app.route('/predict', methods=['POST'])
def prediction():
    file = flask.request.files['img']
    print("Input File:", file.filename)
    rnd_num = random.randint(0,100000)
    infile = "uploads/{}.png".format(rnd_num)
    file.save(infile)
    file.close()
    response = {}
    for organ in organs:
        outfile = "static/outdir/{}_{}.png".format(rnd_num, organ)
        pred = visualizer.get_output(infile, outfile, organ)
        pred_dict = {0: "CANCER", 1: "NORMAL"}
        pred = pred_dict[pred]
        gradcam_base64_str = base64.b64encode(open(outfile, 'rb').read()).decode('utf-8')
        response[organ] = {"pred": pred, "gradcam_base64": gradcam_base64_str}
    return response


@app.route('/predict_v2', methods=['POST'])
def prediction_v2():
    file = flask.request.files['img']
    print("Input File:", file.filename)
    rnd_num = random.randint(0,100000)
    infile = "uploads/{}.png".format(rnd_num)
    file.save(infile)
    file.close()
    response = {}
    for organ in organs:
        outfile_a = "static/outdir/{}_{}_a.png".format(rnd_num, organ)
        outfile_b = "static/outdir/{}_{}_b.png".format(rnd_num, organ)
        pred = visualizer_v2.get_output(infile, outfile_a, outfile_b, organ)
        pred_dict = {0: "CANCER", 1: "NORMAL"}
        pred = pred_dict[pred]
        gradcam_base64_str_a = base64.b64encode(open(outfile_a, 'rb').read()).decode('utf-8')
        gradcam_base64_str_b = base64.b64encode(open(outfile_b, 'rb').read()).decode('utf-8')
        response[organ] = {"pred": pred, "gradcam_base64": [gradcam_base64_str_a, gradcam_base64_str_b]}
    return response


@app.route('/v1', methods=['GET'])
def webpage_v1():
    return flask.render_template('index_v1.html')


@app.route('/', methods=['GET'])
def webpage():
    return flask.render_template('index_v2.html', organs=organs)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
