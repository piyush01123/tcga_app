
import flask
# from werkzeug import secure_filename
import os
import glob
import visualizer
import visualizer_v2
import base64
import random
import pandas as pd
from PIL import Image
import numpy as np
from collections import defaultdict

app = flask.Flask("TCGA Website", template_folder="templates")
organs = ['BRCA', 'COAD', 'KICH', 'KIRC', 'KIRP', 'LIHC', 'LUAD', 'LUSC', 'PRAD', 'READ', 'STAD']
sample_dir = "static/TINY"

@app.route('/test', methods=['GET'])
def hello_world():
    return {"msg_type": "test message", "msg": "Hello World"}


# @app.route('/predict', methods=['POST'])
# def prediction():
#     file = flask.request.files['img']
#     print("Input File:", file.filename)
#     rnd_num = random.randint(0,100000)
#     infile = "uploads/{}.png".format(rnd_num)
#     file.save(infile)
#     file.close()
#     response = {}
#     for organ in organs:
#         outfile = "static/outdir/{}_{}.png".format(rnd_num, organ)
#         pred = visualizer.get_output(infile, outfile, organ)
#         pred_dict = {0: "CANCER", 1: "NORMAL"}
#         pred = pred_dict[pred]
#         gradcam_base64_str = base64.b64encode(open(outfile, 'rb').read()).decode('utf-8')
#         response[organ] = {"pred": pred, "gradcam_base64": gradcam_base64_str}
#     return response


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


# @app.route('/v1', methods=['GET'])
# def webpage_v1():
#     return flask.render_template('index_v1.html', organs=organs)
#
#
# @app.route('/v2', methods=['GET'])
# def webpage_v2():
#     return flask.render_template('index_v2.html', organs=organs)
def jacidx(a,b):
    A = np.array(Image.open(a))
    B = np.array(Image.open(b))
    A_white, = np.where(A.flatten()>0)
    B_white, = np.where(B.flatten()>0)
    A_white = set(A_white.tolist())
    B_white = set(B_white.tolist())
    return len(A_white.intersection(B_white))/ len(A_white.union(B_white))

def get_sample_results():
    data = defaultdict(dict)
    for organ in organs:
        orig_files = sorted(glob.glob(os.path.join(sample_dir,\
                                        organ,'original','*.png')))
        data[organ]['original'] = orig_files
        for type in "gradcam", "gc_simp", "gc_th", "gc_bb_box":
            data[organ][type] = {}
            for organ2 in organs:
                data[organ][type][organ2] = sorted(glob.glob(os.path.join(sample_dir,organ,type,organ2,'*.png')))
        data[organ]["preds"] = {}
        for organ2 in organs:
            csv = os.path.join(sample_dir,organ,"final_predictions_csv",organ2,"final_pred.csv")
            df = pd.read_csv(csv)
            df['files'] = df.paths.apply(lambda item: item.split('/')[-1])
            preds = df.pred_class[df.files.isin([item.split('/')[-1] for item in orig_files])]
            data[organ]["preds"][organ2] = preds.tolist()
    return data


@app.route('/', methods=['GET'])
def webpage_v3():
    data = get_sample_results()
    n_samples = len(data["BRCA"]["original"])
    return flask.render_template('index_v3.html', organs=organs, \
    results=data, sample_ids=list(range(n_samples)), s="original", t="preds", \
    arr=["gradcam", "gc_simp", "gc_th", "gc_bb_box"])


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
