
import os, glob,collections,shutil
organs = ['BRCA', 'COAD', 'KICH', 'KIRC', 'KIRP', 'LIHC', 'LUAD', 'LUSC', 'PRAD', 'READ', 'STAD']

del_data = collections.defaultdict(dict)
# del_data['BRCA']['cancer'] = [0,1,2,5,8]
del_data['BRCA']['cancer'] = []
del_data['BRCA']['normal'] = []
# del_data['COAD']['cancer'] = [0,3,4,5,6]
del_data['COAD']['cancer'] = []
del_data['COAD']['normal'] = []
del_data['KICH']['cancer'] = []
del_data['KICH']['normal'] = []
del_data['KIRC']['cancer'] = []
del_data['KIRC']['normal'] = []
del_data['KIRP']['cancer'] = []
del_data['KIRP']['normal'] = []
del_data['LIHC']['cancer'] = []
del_data['LIHC']['normal'] = []
del_data['LUAD']['cancer'] = []
del_data['LUAD']['normal'] = []
del_data['LUSC']['cancer'] = []
del_data['LUSC']['normal'] = []
del_data['PRAD']['cancer'] = []
del_data['PRAD']['normal'] = []
del_data['READ']['cancer'] = []
del_data['READ']['normal'] = []
del_data['STAD']['cancer'] = []
del_data['STAD']['normal'] = []

bools = []

for organ in organs:
    for cls in ["cancer","normal"]:
        filenames = os.listdir(os.path.join("static/TINY",organ,cls,"original"))
        files = [os.path.join("static/TINY",organ,cls,"original",fn) for fn in filenames]
        bools.extend([os.path.isfile(f) for f in files])


        os.makedirs(os.path.join("RECYCLE_BIN",organ,cls,"original"), exist_ok=True)
        for i in del_data[organ][cls]:
            shutil.move(files[i],os.path.join("RECYCLE_BIN",organ,cls,"original"))
        for organ2 in organs:
            for type in "gradcam", "gc_simp", "gc_th", "gc_bb_box":
                files = [os.path.join("static/TINY",organ,cls,type,organ2,fn) for fn in filenames]
                bools.extend([os.path.isfile(f) for f in files])
                os.makedirs(os.path.join("RECYCLE_BIN",organ,cls,type,organ2), exist_ok=True)
                for i in del_data[organ][cls]:
                    shutil.move(files[i],os.path.join("RECYCLE_BIN",organ,cls,type,organ2))

print(all(bools))
