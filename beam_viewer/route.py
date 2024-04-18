from flask import render_template,redirect,url_for,request,abort,current_app,flash,send_file
from beam_viewer.models import Beam_Inform
from beam_viewer.forms import Beamform
from beam_viewer import db
import os
import uuid
import math
import logging
import shutil


def index():
    form=Beamform(meta={'csrf': False})
    if form.validate_on_submit():
        id=str(uuid.uuid4())
        case_id=form.case_id.data
        file = request.files.getlist('filename')
        if(file[0]):
            save_path=os.path.abspath(os.path.join(os.path.split(__file__)[0],'static/data',case_id,id))
            if (not os.path.exists(save_path)):
                os.makedirs(save_path)
            upload_filename=str(file[0].filename)
            revise=upload_filename.split('.')
            revise_filename=revise[0]+"_M."+revise[1]
            file[0].save(os.path.abspath(save_path+'/'+upload_filename))
            mode=[0,0,0,0]
            if request.form.get('0'):
                mode[0]=1
            if request.form.get('1'):
                mode[1]=1
            if request.form.get('2'):
                mode[2]=1
            if request.form.get('3'):
                mode[3]=1
            revise_beams(save_path,mode,request.form,upload_filename,revise_filename)
            b=Beam_Inform(upload_filename=upload_filename,revise_filename=revise_filename,id=id,case_name=case_id,user_id="A0167",save_path=save_path)
            db.session.add(b)
            db.session.commit()
        if case_id:
            case_name_records=Beam_Inform.case_name_records_casename(case_id)
            return render_template('index.html',form=form,case_name_records=case_name_records,redirect_page='index')

    return render_template('index.html',form=form)

def explore():
    case_name_records=Beam_Inform.case_name_records()
    return render_template('explore.html',case_name_records=case_name_records,redirect_page='explore')


def download(case_id,id,filename):
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0],'static/data',case_id,id))
    return send_file(path+"/"+filename, as_attachment=True)

def delete(case_id,id):
    form=Beamform(meta={'csrf': False})
    b=Beam_Inform.case_name_records_id(id)
    db.session.delete(b)
    db.session.commit()
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0],'static/data',case_id,id))
    shutil.rmtree(path)
    next_page=request.args.get('next')
    print(next_page)
    return redirect (url_for(request.values['redirect_url']))
    # return redirect ('index')
    # return render_template('index.html',form=form,case_name_records=case_name_records)

def show(case_id,id,filename):
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0],'static/data',case_id,id))
    sr=open(path+"/"+filename)
    body=sr.readlines()
    return render_template('show.html',body=body)


def revise_beams(path,mode,requestform,upload_filename,revise_filename):
    sr=open(path+"/"+upload_filename)
    sw=open(path+"/"+revise_filename,"w+")
    log=logging.getLogger()
    logging.basicConfig(filemode='w+',level=logging.INFO)
    new_handL=logging.FileHandler(filename=path+"/ReviseLOG.txt")
    log.addHandler(new_handL)
    temp_s = sr.readline()
    while temp_s:
        if temp_s[0:4]=="BEAM":
            #讀取階段
            #紀錄該梁名稱->預計判別懸臂梁c
            s = ["" for x in range(12)]
            s[0] = temp_s
            for i in range(1,12):
                s[i] = sr.readline()
            #建立資料階段
            #修改階段
            s_new = revise_beam(s, mode,requestform)
            for i in range(12):
                sw.write(s_new[i])
        elif temp_s[0:4]=="BNPG":
            sw.write(temp_s)
        temp_s = sr.readline()
    for hdlr in log.handlers[:]:
        log.removeHandler(hdlr)

def revise_beam(s,mode,requestform):
    B=float(s[2][11:16])
    H = float(s[2][16:21])
    if s[0][0:5]=="BEAM ":
        if mode[0]==1:
            s=change_third_row(s,B,H)
        if mode[1]==1:
            s=change_middle_stirrups(s)
        if mode[2]==1:
            s=change_four_bar(s,B)
        if mode[3]==1:
            s=change_cantilever(s,requestform)
    return s

def change_cantilever(s,requestform):
    if s[0][5:25] in requestform:
        if requestform[s[0][5:25]]=="right":
            s[3] = s[3][0:35] + " -20. - 0" + s[3][44:81]
            logging.info(s[0][0:24]+"右端改為懸挑")
        elif requestform[s[0][5:25]]=="left":
            s[2] = s[2][0:35] + " -20. - 0" + s[2][44:81]
            logging.info(s[0][0:24]+"左端改為懸挑")
    return s




def change_four_bar(s,B):
    if(B>=65):
        if(s[10][1:2]=="2" and ((int(s[2][35:39])>0)|(int(s[2][40:44])>0))):
            if int(s[4][0:2])<4 and s[4][10:12]==" 0":
                s[4]=" 4"+s[4][2:81]
                logging.info(s[0][0:24]+"左上改為4#"+s[4][3:5])
            if int(s[5][0:2])<4 and s[5][10:12]==" 0":
                s[5]=" 4"+s[5][2:81]
                logging.info(s[0][0:24]+"左下改為4#"+s[5][3:5])
        if(s[10][21:22]=="2" and ((int(s[3][35:39])>0)|(int(s[3][40:44])>0))):
            if int(s[8][0:2])<4 and s[8][10:12]==" 0":
                s[8]=" 4"+s[8][2:81]
                logging.info(s[0][0:24]+"右上改為4#"+s[8][3:5])
            if int(s[9][0:2])<4 and s[9][10:12]==" 0":
                s[9]=" 4"+s[9][2:81]
                logging.info(s[0][0:24]+"右下改為4#"+s[9][3:5])

    return s
    

def change_middle_stirrups(s):
    stirup=int(s[10][11:12])
    space=int(s[10][16:18])
    if space/2>=10 and stirup==2:
        logging.info(s[0][0:24])
        logging.info("中間原箍筋為：" + s[10][11:20])
        space=int(space/2)
        stirup=int(stirup-1)
        s[10]=s[10][0:11]+str(stirup)+s[10][12:16]+str(space)+s[10][18:81]
        logging.info("調整中間箍筋為：" + s[10][11:20])
    return s

def change_third_row(s,B,H):
    for i in range(4,10):
        if not float(s[i][20:22])==0:
            logging.info(s[0][0:24])
            logging.info("原鋼筋排列"+s[i][0:2]+" "+s[i][10:12]+" "+s[i][20:22])
            total_bar = int(s[i][0:2]) +int(s[i][10:12])+ int(s[i][20:22])
            max_bar = max_num(B, int(s[i][3:5]))
            bar_new = change_bar(total_bar, max_bar)
            s[i] = bar_new[0] + s[i][2:10]+ bar_new[1] + s[i][12:20] + bar_new[2] + s[i][22:81]
            logging.info("總鋼筋根數" + str(total_bar)+"調整後鋼筋排列"+s[i][0:2]+" "+s[i][10:12]+" "+s[i][20:22])
    return s

def max_num(B,size):
    coc = 4.0
    rib = 1.6
    size_dia = 3.22
    size_dia_code = 2.5
    match size:
        case 7:
            size_dia = 2.22
            size_dia_code = 2.5
        case 8:
            size_dia = 2.54
            size_dia_code = 2.54
        case 10:
            size_dia = 3.22
            size_dia_code = 3.22
    n=math.floor((B - coc * 2 - 2 * rib - size_dia) / (size_dia + size_dia_code))+1
    return n

def change_bar(total_bar, max_bar):
    bar = [ 0, 0, 0 ]
    if 2*max_bar<total_bar:
        logging.info("Can't change all rebars to 1st and 2nd row")
        bar=[max_bar,max_bar,total_bar-2*max_bar]
    else:
        bar[0]=math.ceil(total_bar/2)
        bar[1]=total_bar-bar[0]
    bar_str=["" for x in range(3)]
    for i in range(3):
        bar_str[i]=str(bar[i]).rjust(2)
    return bar_str