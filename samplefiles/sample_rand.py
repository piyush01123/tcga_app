
# Run on ECDP server
import os, glob, random, shutil
organs = ['BRCA','COAD','KICH','KIRC','KIRP','LIHC','LUAD','LUSC','PRAD','READ','STAD']
N=50

for organ in organs:
    for cls in "cancer", "normal":
        files = glob.glob("TCGA_PATCHES/{}/test/{}/*/*.png".format(organ,cls))
        samples  = random.sample(files, N)
        os.makedirs("samplefiles/{}/{}/original".format(organ,cls), exist_ok=True)
        os.makedirs("samplefiles/{}/{}/gradcam".format(organ,cls), exist_ok=True)
        os.makedirs("samplefiles/{}/{}/gc_simp".format(organ,cls), exist_ok=True)
        for file in samples:
            shutil.copy(file, "samplefiles/{}/{}/original".format(organ,cls))
        print("{} {} Done".format(organ,cls))
