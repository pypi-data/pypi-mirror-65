
import subprocess,os
import imp
def TTSnorm(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[2]
        TEXT+=B


    return TEXT

def TTSrule(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[0]
        TEXT+=B


    return TEXT

def TTSrawUpper(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[1]
        TEXT+=B


    return TEXT










import subprocess,os
import imp
def TTSnorm_punc(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[2]
        TEXT+=B


    return TEXT

def TTSrule_punc(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[0]
        TEXT+=B


    return TEXT

def TTSrawUpper_punc(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[1]
        TEXT+=B


    return TEXT









def TTSnorm_punc_unknown(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc_unknown"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[2]
        TEXT+=B


    return TEXT

def TTSrule_punc_unknown(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc_unknown"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[0]
        TEXT+=B


    return TEXT

def TTSrawUpper_punc_unknown(text):
    A=imp.find_module('vinorm')[1]

    print(A)
    I=A+"/input.txt"
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main_punc_unknown"
    subprocess.check_call([E], env=myenv, cwd=A)
    
    O=A+"/output.txt"
    with open(O,"r") as fr:
        text=fr.read()

    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
           continue
        B=s.split("#@#")[1]
        TEXT+=B


    return TEXT