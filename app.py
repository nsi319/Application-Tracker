from flask import Flask, render_template, url_for, flash, redirect, request,session,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import random, json
import os,glob
from datetime import date,datetime
from utils import get_resume_details_from_file, get_resume_details,change_permissions_recursive,remove_number,get_numbers,check_all,check_any,rank_resume,get_summary
from flask_migrate import Migrate
from flask_heroku import Heroku
import shutil
import nltk
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['UPLOAD_FOLDER']='all_resumes/'
app.config['SECRET_KEY']='nokey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ats.db'
db = SQLAlchemy(app)


@app.route("/")
def test():
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    return render_template('login.html')
@app.route("/home")
def home():
    user = session['name']
    user_type = session['type']
    user_id = session["user_logged"]
    if user_type == "candidate":
        rows = [[1,2,3,4,5,6]]
        
        sortby = request.args.get('sortby')
        post = request.args.get('post')
        company = request.args.get('company')
        doamin = request.args.get('domain')


        with sqlite3.connect('ats.db') as conn:
            res = conn.execute('select jd.id,company,title,desc,skill,experience,salary,working_hours from job_description as jd where ? not in (select cand_id from application as app where app.job_id=jd.id)',(user_id,)).fetchall()
            print(res)
            if res==[]:
                return render_template('home.html', user=user)
            else:
                if sortby == 'salary':
                    res = conn.execute('select jd.id,company,title,desc,skill,experience,salary,working_hours from job_description as jd where ? not in (select cand_id from application as app where app.job_id=jd.id) order by salary desc',(user_id,)).fetchall()
                elif sortby == 'hours':
                    res = conn.execute('select jd.id,company,title,desc,skill,experience,salary,working_hours from job_description as jd where ? not in (select cand_id from application as app where app.job_id=jd.id) order by working_hours desc',(user_id,)).fetchall()
                elif sortby == 'exp':
                    res = conn.execute('select jd.id,company,title,desc,skill,experience,salary,working_hours from job_description as jd where ? not in (select cand_id from application as app where app.job_id=jd.id) order by experience desc',(user_id,)).fetchall()
                elif doamin:
                    res = conn.execute('select jd.id,company,title,desc,skill,experience,salary,working_hours from job_description as jd where ? not in (select cand_id from application as app where app.job_id=jd.id) and domain=? and title=?',(user_id,doamin,post)).fetchall()
                return render_template('home.html', user=user, rows=res)
    else:
        rows=[]
        return redirect(url_for('company_home'))



@app.route("/job_apply",methods=['POST'])
def job_apply():
    if request.method =='POST':
        user_id = session['user_logged']
        jobs=request.form.getlist('applyingfor')
        with sqlite3.connect('ats.db') as conn:
            for job in jobs:
                print(job)
                res = conn.execute('select max(id) as mx from application').fetchall()           
                print(res)
                id = 1
                if(res[0][0]!=None):
                    id=res[0][0]+1
                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                print(formatted_date)
                conn.execute("insert into application values(?,?,?,?,?)",(id, job, user_id,formatted_date,"In Process"))

        with sqlite3.connect('ats.db') as conn:
            rows = conn.execute("select * from application where cand_id = ?",(user_id,)).fetchall()
            #rows2 = rows

        return render_template('applications.html',user=session['name'],rows=rows,rows2=rows2)

@app.route("/applications")
def applications():
    user_id = session['user_logged']
    user = session['name']
    applications = []
    rows = []
    rows2 = []
    i=0
    j=0
    with sqlite3.connect('ats.db') as conn:
        res = conn.execute("select * from application where cand_id = ?",(user_id,)).fetchall()
        for k in range(len(res)):
            comp = conn.execute("select company,title from job_description where id = ?",(res[i][1],)).fetchall()[0]
            if res[k][4]=="In Process":
                data=[]
                data.append(res[k][1])
                data.append(comp[0])
                data.append(comp[1])
                data.append(str(res[k][3]).split(" ")[0])
                data.append(res[k][4])
                rows.append(data)
            else:
                data=[]
                data.append(res[k][1])
                data.append(comp[0])
                data.append(comp[1])
                data.append(str(res[k][3]).split(" ")[0])
                data.append(res[k][4])
                rows2.append(data)
            
    return render_template('applications.html',user=user,rows=rows,rows2=rows2)

@app.route("/login",methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login_form",methods=['POST'])
def login_form():
    if request.method=='POST':
        with sqlite3.connect('ats.db') as conn:
            username = request.form.get("username")
            password = request.form.get("pwd")
            print(username,password)
            res = conn.execute('select password from user where username = ?',(username,)).fetchall()
            print(res)
            if res==[] or res[0][0]!=password:
                print('error')
                return render_template('login.html',error='wrong username or password')
            else:
                data = conn.execute('select name,usertype,id from user where username = ?',(username,)).fetchall()
                session['type'] = data[0][1]
                session['name'] = data[0][0]
                session['user_logged'] = data[0][2]
                return redirect(url_for('home'))

@app.route("/register",methods=['GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')

@app.route("/upload_resume", methods=['GET','POST'])
def upload_resume():
    error= ""
    if request.method == 'POST':
        session['resumes']=[]
        files = request.files.getlist('file')
        print(len(files))
        print("heyoo")
        if files:
            if len(files)==1:
                if files[0].filename=='':
                    return render_template('register.html',total="No files selected")
            dire = 'assets'
            if os.path.exists(os.path.abspath(dire)):
                shutil.rmtree(dire)
            os.makedirs(os.path.abspath(dire))
            for file in files:
                file.save(os.path.join(os.path.abspath(dire), file.filename))

            total=0
            dict_res = {'dict1':None,'dict2':None,'total':None,'filename':None}
            data = get_resume_details(os.path.abspath(dire))
            print(data)
            # remove files in assets and move to assets_all

            dire = 'assets'
            if os.path.exists(os.path.abspath(dire)):
                shutil.rmtree(dire)
            os.makedirs(os.path.abspath(dire))
            print("files removed")

            if data==-1:
                return render_template('register.html',total="Error parsing resume data..") 
            else:
                dict_res=data
                total = int(dict_res['total'])
                filenames = dict_res['filename']
                complete=dict_res['complete']
                from models import Candidate
                duplicate=0
                for i in range(total):
                    k=0
                    first=[]
                    second=[]
                    for text in ['email','linkedin','phone','exp_years','duration']:
                        first.append(dict_res['dict1'][text][i])
                    for text in ['summary','skills','experience','education','extra','awards']:
                        second.append("\n".join(dict_res['dict2'][text][i].splitlines()))
                    timestamp = datetime.now().timestamp()
                    uniq =  "./all_resumes/" + str(timestamp) +  files[i].filename
                    files[i].save(uniq)

                    # insert into candidate table
                    with sqlite3.connect('ats.db') as conn:
                        res = conn.execute('select max(id) as mx from candidate').fetchall()           
                        print(res)
                        id = 1
                        if(res[0][0]!=None):
                            id=res[0][0]+1
                        conn.execute("insert into candidate values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,first[2][0],str(first[0]),first[1],first[3],"\n".join(first[4]),second[0],second[1],second[2],second[3],second[4],second[5],uniq,filenames[i],complete[i]))
                        return render_template('register.html', total="Resume uploaded successfully", path=uniq)
        else:
            return render_template('register.html', total="This field is required")


            


        
@app.route("/register_form",methods=['POST'])
def register_form():
    if request.method=='POST':
        with sqlite3.connect('ats.db') as conn:
            username = request.form.get("username")
            pwd = request.form.get("pwd")
            name = request.form.get("name")
            age = request.form.get("age")
            sex = request.form.get("sex")
            domain = request.form.get("domain")
            pref = request.form.get("pref")
            exp = request.form.get("exp")
            edu = request.form.get("edu")   #assume edu = exp
            resume_path = request.form.get("path")

            print("resume path: " + resume_path)
            res = conn.execute('select max(id) as mx from user').fetchall()           
            print(res)
            id = 1
            if(res[0][0]!=None):
                id=res[0][0]+1

            conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(id,username,age,name,sex,domain,pref,exp,resume_path,pwd,'candidate'))
            return redirect(url_for('login'))

@app.route("/company_home",methods=['GET','POST'])
def company_home():
    # company_name = session['company_name']
    company_name = session["name"]
    company_id = session["user_logged"]
    sortby = request.args.get("sortby")
    domain = request.args.get("domain")

    with sqlite3.connect('ats.db') as conn:
        res = conn.execute('select id,domain,title,experience,post_date from job_description where company = ?',(company_id,)).fetchall()
        print(res)
        
        if sortby == 'exp':
            res = conn.execute('select id,domain,title,experience,post_date from job_description where company = ? order by experience desc',(company_id,)).fetchall()
        elif sortby == 'domain':
            res = conn.execute('select id,domain,title,experience,post_date from job_description where company = ? order by domain desc',(company_id,)).fetchall()
        elif sortby == 'title':
            res = conn.execute('select id,domain,title,experience,post_date from job_description where company = ? order by title desc',(company_id,)).fetchall()
        elif domain:
            res = conn.execute('select id,domain,title,experience,post_date from job_description where company = ? and domain = ?',(company_id,domain,)).fetchall()

        for i in range(len(res)):
            applicants = conn.execute('select count(*) from application where job_id = ?',(res[i][0],)).fetchall()[0][0]
            print(applicants)
            list_res = list(res[i])
            list_res[4] = str(list_res[4]).split(" ")[0]
            list_res.append(applicants)
            res[i] = tuple(list_res)
        
        return render_template('company_home.html', name=company_name, rows=res)



@app.route("/applicant/<job>", methods=['GET','POST'])
def applicant(job):
    with sqlite3.connect('ats.db') as conn:
        res = conn.execute('select * from application where job_id = ?',(job,)).fetchall()
        print(res)
        row=[]
        for i in range(len(res)):
            applicant_id = conn.execute('select id from user where id = ?',(res[i][2],)).fetchall()[0][0]
            candidate = conn.execute('select * from candidate where id = ?',(applicant_id)).fetchall()[0]
            row.append(candidate)
        
        result_list = rank_resume(row,[],all_key_list,any_key_list)
        return render_template('result.html',result=result_list,skills="[ ]",exp = ",",key = " ".join(keywords_matched) ,items=len(filter_list),count=str(total) + "/" + str(total_final),url=filter_link,all="",any="")    

@app.route("/add_job",methods=['GET','POST'])
def add_job():
    if request.method=='POST':
        with sqlite3.connect('ats.db') as conn:
            title = request.form.get("jtitle")
            desc = request.form.get("jdesc")
            exp = request.form.get("jexp")
            working = request.form.get("jwork")
            salary = request.form.get("jsalary")
            skills = request.form.get("jskills")
            domain = request.form.get("jdomain")
            jedu = request.form.getlist("jedu")
            print(jedu)
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            print(formatted_date)
            res = conn.execute('select max(id) as mx from job_description').fetchall()           
            print(res)
            id = 1
            if(res[0][0]!=None):
                id=res[0][0]+1
            conn.execute('insert into job_description values (?,?,?,?,?,?,?,?,?,?,?)',(id,domain,title,desc,salary,working,exp,",".join(jedu),formatted_date,session['user_logged'], skills))
            return redirect(url_for('home'))
    else:
        return render_template('add_job.html')

@app.route('/filter_job/',methods=['GET','POST'])
def filter_job():
    con = sql.connect('database.db')
    cur=con.cursor()
    cid=session['comp_id']
    cur.execute("select name from company where company_id=(?)",(cid,))
    name=cur.fetchone()
    if request.method == 'POST':
        domain = request.form['domain']
        pref=request.form['preferences']
        exp=request.form['experience']
        country=request.form['country']
    if country=="True":
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company, has_permit_for where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and has_permit_for.candidate_id=candidate.candidate_id and has_permit_for.country_id=company.country_id and company.company_id=(?)",(cid,))
    else:
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) and resume.domain=(?) and resume.experience>=(?) and resume.preferences=(?) ",(cid,domain,exp,pref))
    rows=cur.fetchall()
    return render_template('company_home.html',name=name,rows=rows)

@app.route('/sort_job/',methods=['POST','GET'])
def sort_job():
    con = sql.connect('database.db')
    cur=con.cursor()
    if request.method == 'POST':
        pref = request.form['pref']
    print(pref)
    cid=session['comp_id']
    cur.execute("select name from company where company_id=(?)",(cid,))
    name=cur.fetchone()
    if pref=='Age':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.age",(cid,))
    elif pref=='Gen':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.sex",(cid,))
    elif pref=='Domain':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.domain",(cid,))
    elif pref=='Preferences':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.preferences",(cid,))
    elif pref=='Experience':
        cur.execute("Select applied_for.job_id,applied_for.cand_id as candidate_id, resume.name, resume.age, resume.sex, resume.domain, resume.preferences, resume.experience from applied_for, resume, candidate, job_description, company where applied_for.cand_id=candidate.candidate_id and resume.resume_id=candidate.resume_id and applied_for.job_id=job_description.job_id and job_description.comp_id=company.company_id and company.company_id=(?) order by resume.experience",(cid,))
    rows=cur.fetchall()
    for row in rows:
        print(row)
    return render_template('company_home.html',name=name,rows=rows)


@app.route('/schedule/',methods=['GET','POST'])
def schedule():
    con = sql.connect('database.db')
    cur=con.cursor()
    cid=session['comp_id']
    aajkitareek=(datetime.now().date())+timedelta(2)
    print(aajkitareek)
    if request.method=='POST':
        jids=request.form.getlist('pref1')
        cids=request.form.getlist('pref2')
        print(jids)
        print(cids)
        l=len(jids)
        status="pending"
        for i in range(0,l):
            cur.execute("insert into interviewed_by values(?,?,?,?,?)",(cids[i],jids[i],aajkitareek,"11:00:00",status,))
        con.commit()
        cur.execute("select interviewed_by.cand_id as candidate_id,interviewed_by.jo_id as job_id, resume.name as name,interviewed_by.int_date as date, interviewed_by.int_time as time, interviewed_by.status as status from interviewed_by, resume, candidate, job_description, company where resume.resume_id=candidate.resume_id and candidate.candidate_id=interviewed_by.cand_id and job_description.comp_id=company.company_id and interviewed_by.jo_id=job_description.job_id and company.company_id=(?)",(cid,))
        rows2=cur.fetchall()
    return render_template("inter.html",rows2=rows2)


@app.route("/search",methods=['GET','POST'])
def search():
    error= ""
    if request.method == 'POST':
        session['resumes']=[]
        files = request.files.getlist('file')
        print(len(files))
        if files:
            if len(files)==1:
                if files[0].filename=='':
                    return render_template('search.html',total="No files selected")
            dire = 'assets'
            if os.path.exists(os.path.abspath(dire)):
                shutil.rmtree(dire)
            os.makedirs(os.path.abspath(dire))
            for file in files:
                file.save(os.path.join(os.path.abspath(dire), file.filename))

            total=0
            dict_res = {'dict1':None,'dict2':None,'total':None,'filename':None}
            data = get_resume_details(os.path.abspath(dire))
            if data==-1:
                return render_template('search.html',total="Error parsing data..") 
            else:
                dict_res=data
                total = int(dict_res['total'])
                filenames = dict_res['filename']
                complete=dict_res['complete']

                from models import Candidate
                duplicate=0
                for i in range(total):
                    k=0
                    first=[]
                    second=[]
                    for text in ['email','linkedin','phone','exp_years','duration']:
                        first.append(dict_res['dict1'][text][i])
                    for text in ['summary','skills','experience','education','extra','awards']:
                        second.append("\n".join(dict_res['dict2'][text][i].splitlines()))
                    timestamp = datetime.now().timestamp()
                    all_res = "all_resumes"
                    path_res = os.path.abspath(all_res)
                    uniq = path_res + "/" + str(timestamp) +  filenames[i].split("/")[-1].split(".")[0] + "." + filenames[i].split(".")[-1]
                    #print("filename and unique",(filenames[i],uniq))
                    new_cand = Candidate(email=str(first[0]),linkedin=first[1],phone=first[2][0],exp_years=first[3],duration="\n".join(first[4]),summary=second[0],skills=second[1],experience=second[2],education=second[3],extra=second[4],awards=second[5],resume=uniq,filename=filenames[i],complete_resume=complete[i])
                    if new_cand.email=='NA' and new_cand.phone=='NA':
                        #print("inside both na",filenames[i])
                        #print(new_cand.email + " " + new_cand.phone)
                        shutil.copy(filenames[i],uniq)
                        db.session.add(new_cand)
                        db.session.commit()

                    else:

                        for cand in Candidate.query.all():
                            if new_cand.phone=='NA' and new_cand.email!='NA':
                                #print("inside na notna",filenames[i])
                                #print(new_cand.email + " " + new_cand.phone)

                                if new_cand.email == cand.email:
                                    duplicate=duplicate+1
                                    k=1
                                    break
                            elif new_cand.phone!='NA' and new_cand.email=='NA':
                                #print("inside not na na",filenames[i])
                                #print(new_cand.email + " " + new_cand.phone)
                                if new_cand.phone == cand.phone:
                                    duplicate=duplicate+1
                                    k=1
                                    break
                            else:
                                #print("inside both not na",filenames[i])
                                #print(new_cand.email + " " + new_cand.phone)
                                if new_cand.phone==cand.phone or new_cand.email==cand.email:
                                    duplicate=duplicate+1
                                    k=1
                                    break
                        if k==0:
                            shutil.copy(filenames[i],uniq)
                            db.session.add(new_cand)
                            db.session.commit()
                        k=0
                
                #remove files in assets and move to assets_all
                files = glob.glob(os.path.join(r'assets'))
                #change_permissions_recursive(os.path.abspath(r'assets'),0o777)
                '''
                for file in files:
                    shutil.move(file,os.path.abspath('assets_all'))
                print("files moved and removed")
                '''
                dire = 'assets'

                if os.path.exists(os.path.abspath(dire)):
                    shutil.rmtree(dire)
                os.makedirs(os.path.abspath(dire))

                #print("files moved and removed")
                if total==0:
                    return render_template('search.html',total="No resumes of the format pdf,doc,docx were found") 
                else:
                    if duplicate==0:
                        return render_template('search.html',total="Found and uploaded " + str(total) + " resumes")
                    else:
                        return render_template('search.html',total= "Found " + str(total) + " resumes.. Found " + str(duplicate) + "/" + str(total) + " duplicate resumes")
        else:
            return render_template('search.html')
    else:
        return render_template('search.html')
    


@app.route("/result",methods=['GET', 'POST'])
def result():
    if request.method=='POST':
        if request.form.get('post')=="search_results":
            #search on results
            any_key = request.form['rany_key']
            all_key = request.form['rall_key']
            print("resumes found before and after: ")
            print(session["resumes"])
            if session['resumes']==[]:
                resumes = request.form.getlist('found_resumes')
                session['resumes']=resumes
            else:
                resumes = session['resumes']

            print(session["resumes"])
            any_key_list = any_key.split(",")
            all_key_list = all_key.split(",")
            found_candidates=[]
            filter_list =[]
            filter_link =[]
            total = 0
            total_final=0
            keywords_matched=[]
            from models import Candidate
            for res in resumes:
                cand = Candidate.query.filter_by(resume=res).first()
                found_candidates.append(cand)

            for cand in found_candidates:
                total_final = total_final + 1
                if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                    filter_list.append(cand)
                    total=total+1
                    
            keywords_matched.append("| ".join(any_key_list))
            if all_key_list:
                keywords_matched.append("| ")
            keywords_matched.append("| ".join(all_key_list))
            session["total"] = total
            session["total_final"] = total_final
            if len(filter_list)==0:
                empty="NO MATCHES FOUND"
                filter_link=[]
                return render_template('result.html',result=filter_list,skills="[ ]",exp = ",",key = " ".join(keywords_matched) ,items=len(filter_list),count=str(total) + "/" + str(total_final),empty=empty,url=filter_link,all=all_key,any=any_key)
            else:
                filter_link=[]
                for cand in filter_list:
                    url_link = cand.resume
                    filter_link.append(url_link.split("/")[-1])
                result_list = rank_resume(filter_list,[],all_key_list,any_key_list)
                return render_template('result.html',result=result_list,skills="[ ]",exp = ",",key = " ".join(keywords_matched) ,items=len(filter_list),count=str(total) + "/" + str(total_final),url=filter_link,all=all_key,any=any_key)

        else:

            session['resumes']=[]

            skill = request.form.getlist('skill')
            skill_exp = request.form.getlist('skill_exp')
            skill_cond = request.form['skill_condition']
            skill_iter = request.form.get('skill_full')
            any_key = request.form['any_key']
            all_key = request.form['all_key']
            min_expyear = request.form['min_expyear']
            max_expyear = request.form['max_expyear']

            
            #search for skill and exp

            filter_list =[]
            filter_link =[]
            total = 0
            total_final=0
            keys_matched = []
            exp_matched = ""
            keywords_matched=[]
            mini=min_expyear
            maxi=max_expyear
            if str(min_expyear)=='':
                min_expyear="0"
            if str(max_expyear)=='':
                max_expyear="10000"
            

            any_key_list = any_key.split(",")
            all_key_list = all_key.split(",")

            from models import Candidate
            for cand in Candidate.query.all():
                total_final=total_final+1
                res = get_numbers(str(cand.exp_years))
                if res:
                    sort_res = sorted(res)
                    years = float(sort_res[-1])
                else:
                    years = 0
                #print(cand.filename + " " + str(years))

                if int(min_expyear)<=years and years<=int(max_expyear):
                    t=0
                    for sk in skill:
                        if sk=='':
                            t=t+1
                    if t==len(skill):
                        if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                            filter_list.append(cand)
                            total=total+1
                    else:
                        if str(skill_cond)=="0" and str(skill_iter)=="None":
                            k=0
                            if cand.skills:
                                text = str(cand.complete_resume)
                            else:
                                text=str(cand.skills)
                            freqdist = nltk.FreqDist(text.lower().split())
                            for sk in skill:
                                if sk!='':
                                    for v in freqdist.keys():
                                        if remove_number(v).find(sk.lower().strip())>=0:
                                            if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                                                filter_list.append(cand)
                                                total=total+1
                                            keys_matched.append(sk + ", ")
                                            k=1
                                            break
                                if k==1:
                                    break

                        elif str(skill_cond)=="1" and str(skill_iter)=="None":
                            if cand.skills:
                                text = str(cand.complete_resume)
                            else:
                                text=str(cand.skills)

                            freqdist = nltk.FreqDist(text.lower().split())
                            p=0
                            for sk in skill:
                                if sk!='':
                                    p=p+1
                            k=0
                            for sk in skill:
                                if sk!='':
                                    for v in freqdist.keys():
                                        if remove_number(v).find(sk.lower().strip())>=0:
                                            if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                                                keys_matched.append(sk + ", ")
                                                k=k+1
                            if k==p:
                                filter_list.append(cand)
                                total=total+1
                        

                        elif str(skill_cond)=="0" and str(skill_iter)=="1":
                            text=str(cand.complete_resume)
                            freqdist = nltk.FreqDist(text.lower().split())
                            k=0
                            for sk in skill:
                                if sk!='':
                                    for v in freqdist.keys():
                                        if remove_number(v).find(sk.lower().strip())>=0:
                                            if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                                                filter_list.append(cand)
                                                total=total+1
                                                keys_matched.append(sk + ", ")
                                                k=1
                                                break
                                if k==1:
                                    break
                            
                        elif str(skill_cond)=="1" and str(skill_iter)=="1":
                            text=str(cand.complete_resume)
                            freqdist = nltk.FreqDist(text.lower().split())
                            p=0
                            for sk in skill:
                                if sk!='':
                                    p=p+1
                            k=0
                            for sk in skill:
                                if sk!='':
                                    for v in freqdist.keys():
                                        if remove_number(v).find(sk.lower().strip())>=0:
                                            if check_any(cand,any_key_list)==1 and check_all(cand,all_key_list)==1:
                                                k=k+1
                                                keys_matched.append(sk + ", ")
                            if k==p:
                                filter_list.append(cand)
                                total=total+1
            
            set_keys = set(keys_matched)

            exp_matched = str(mini) + " , " + str(maxi)
            list_set_keys = list(set_keys)
            keywords_list=[]
            if any_key_list!=['']:
                keywords_list=any_key_list
            if all_key_list!=['']:
                [keywords_list.append(val) for val in all_key_list]
            print(keywords_list)
            keywords_matched.append(" | ".join(list(set(keywords_list))))
            p=0
            for sk in skill:
                if sk=='':
                    p=p+1
            if p==len(skill):
                val = " [ ] "
            else:
                val=""
            
            to_session = []
            for res in filter_list:
                to_session.append(res.resume)
                
            session["resumes"] = to_session

            print("resume session")
            print(session["resumes"])
            session["total"] = total
            session["total_final"] = total_final
            if len(filter_list)==0:
                empty="NO MATCHES FOUND"
                filter_link=[]
                return render_template('result.html',result=filter_list,skills= val + " ".join(list_set_keys),exp = " " + exp_matched + " " ,key = " ".join(keywords_matched) ,items=len(filter_list),count=str(total) + "/" + str(total_final),empty=empty,url=filter_link,all="",any="",from_search=1)
            else:
                filter_link=[]
                for cand in filter_list:
                    url_link = cand.resume
                    filter_link.append(url_link.split("/")[-1])
                result_list = rank_resume(filter_list,skill,all_key_list,any_key_list)
                return render_template('result.html',result=result_list,skills= val + " ".join(list_set_keys),exp = " " + exp_matched + " " ,key = " ".join(keywords_matched) ,items=len(filter_list),count=str(total) + "/" + str(total_final),url=filter_link,all="",any="",from_search=1)
    else:
        from models import Candidate
        print("resume session")
        print(session["resumes"])
        filter_list=[]
        for res in session['resumes']:
            cand = Candidate.query.filter_by(resume=res).first()
            filter_list.append(cand)
        filter_link=[]
        for cand in filter_list:
            url_link = cand.resume
            filter_link.append(url_link.split("/")[-1])
        total = session["total"] 
        total_final = session["total_final"] 
        return render_template('result.html',result=filter_list,skills= " ",exp = " " ,key = " " ,items=len(filter_list),count=str(total) + "/" + str(total_final),url=filter_link,all="",any="",from_search=1)


@app.route("/view/<link>", methods=['GET','POST'])

def view(link):
    from models import Candidate
    all_res = "all_resumes"
    path_res = os.path.abspath(all_res)
    cand = Candidate.query.filter_by(resume=path_res + "/" + link).first()
    print(link)
    if cand.skills:
        skill = str(cand.skills).replace('\n','<br>')
    else:
        skill='NA'
    if cand.experience:
        exp = str(cand.experience).replace('\n','<br>')
    else:
        exp='NA'
    
    dur = str(cand.duration).replace('\n','<br>')

    return render_template('candidate.html',cand=cand,download=link,name=remove_number(link),skill=skill,exp=exp,dur=dur)



@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename,as_attachment=True,attachment_filename=remove_number(filename))

@app.route("/upload_resumes",methods=['POST'])
def upload_resumes():
    files = request.files.getlist('file')
    print(files)
    if files:
        for file in files:
                file.save(os.path.join('assets', file.filename))
    return render_template('search.html')
            
@app.route("/cardview",methods=['GET'])
def cardview():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run(debug=True)
