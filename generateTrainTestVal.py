import numpy as np
import os
from sklearn.model_selection import train_test_split
import shutil

classIndfile_path = "./otherFiles/classInd.txt"
dataset_path = "./datasets/UCF101/Raw/" # path to the dataset
tmpfiles_path1 = "./tmp_files/tmp1/" # A tmp folder
tmpfiles_path2 = "./tmp_files/split_videos/" # Another tmp folder


#Create tmp_files folder if it does not exist
if not os.path.exists(tmpfiles_path1):
    os.makedirs(tmpfiles_path1)

if not os.path.exists(tmpfiles_path2):
    os.makedirs(tmpfiles_path2)

class_labels = np.loadtxt(classIndfile_path,dtype=np.str)
dict1 = {}

for i in range(class_labels.shape[0]):
    dict1[class_labels[i][1] ] = class_labels[i][0]

folders = os.listdir(dataset_path)

# To change class names to corresponding class index
for directory in folders:
    # To check if folders are already renamed
    if directory in dict1:
        os.rename(dataset_path+directory,dataset_path+dict1[directory])

folders = os.listdir(dataset_path)

for name in folders:
    cur_dir = dataset_path + name
    l = [] # list of video clip in current folder
    for path, subdirs, files in os.walk(cur_dir):
        for name1 in files:            
            l.append(os.path.join(path,name1))    
    l = np.array(l)
    np.savetxt(tmpfiles_path1 + name ,l,fmt='%s',delimiter='\n')


x_train_global = np.empty(shape=[0,2])
x_val_global = np.empty(shape=[0,2])
x_test_global = np.empty(shape=[0,2])

files = os.listdir(tmpfiles_path1)
for file in files:
    x = np.loadtxt(tmpfiles_path1+file,dtype=np.str)
    x_train, x_test = train_test_split(x,test_size=0.1,random_state=1)
    x_train, x_val = train_test_split(x_train,test_size=0.1,random_state=1)
    label = int(file)
    x_train = np.c_[x_train,label*np.ones(x_train.shape[0],dtype=int)]
    x_val = np.c_[x_val,label*np.ones(x_val.shape[0],dtype=int)]
    x_test = np.c_[x_test,label*np.ones(x_test.shape[0],dtype=int)]
    x_train_global = np.r_[x_train_global,x_train]
    x_val_global = np.r_[x_val_global,x_val]
    x_test_global = np.r_[x_test_global,x_test]
    
print(x_train_global.shape)
print(x_val_global.shape)
print(x_test_global.shape)

np.savetxt(tmpfiles_path1 + 'train_set.txt',x_train_global,fmt='%s',delimiter=' ')
np.savetxt(tmpfiles_path1 + 'val_set.txt',x_val_global,fmt='%s',delimiter=' ')
np.savetxt(tmpfiles_path1 + 'test_set.txt',x_test_global,fmt='%s',delimiter=' ')

#Copy files
path = tmpfiles_path1 + "train_set.txt"
savepath = tmpfiles_path2 + "train/"
paths = np.loadtxt(path,dtype=np.str)
paths = paths[:,0]
print(paths.shape[0])

for i in range(paths.shape[0]):
    parts = paths[i].split('/')
    newpath = '/'.join(parts[-2:])
    newpath = savepath + newpath
    print(paths[i])
    print(newpath)
    #os.makedirs(os.path.dirname(newpath), exist_ok=True) # doesn't work on python2
    if not os.path.exists(os.path.dirname(newpath)):
        os.makedirs(os.path.dirname(newpath))
    shutil.copy2(paths[i],newpath)

path = tmpfiles_path1 +  "val_set.txt"
savepath = tmpfiles_path2  + "val/"
paths = np.loadtxt(path,dtype=np.str)
paths = paths[:,0]
print(paths.shape[0])

for i in range(paths.shape[0]):
    parts = paths[i].split('/')
    newpath = '/'.join(parts[-2:])
    newpath = savepath + newpath
    print(paths[i])
    print(newpath)
    if not os.path.exists(os.path.dirname(newpath)):
        os.makedirs(os.path.dirname(newpath))
    shutil.copy2(paths[i],newpath)

path = tmpfiles_path1 + "test_set.txt"
savepath = tmpfiles_path2 + "test/"
paths = np.loadtxt(path,dtype=np.str)
paths = paths[:,0]
print(paths.shape[0])

for i in range(paths.shape[0]):
    parts = paths[i].split('/')
    newpath = '/'.join(parts[-2:])
    newpath = savepath + newpath
    print(paths[i])
    print(newpath)
    if not os.path.exists(os.path.dirname(newpath)):
        os.makedirs(os.path.dirname(newpath))
    shutil.copy2(paths[i],newpath)

print('Train Test Validation split is done.')
