from flask import Flask, jsonify,abort,make_response,request,session,Response
import time
import os
import requests
import sqlite3
import re
from flask_cors import CORS
import json
import random


app =Flask(__name__)
CORS(app)
app.secret_key = "abc"  



@app.route('/webtech2/r',methods=['POST'])
def register():
    data= request.json
    msg=404
   # print(data)
    username=request.json['username']
    username=str(username)
    pwd=request.json['pwd']
    password=str(pwd)
    phno =int(request.json['phno'])
    email = str(request.json['email'])
    s=""
    try:
        print("conn")
        conn=sqlite3.connect('netflix.db')
        cur=conn.cursor()
        query="INSERT INTO logininfo (username,password,email,phno) VALUES (?,?,?,?)"
        print(query)
        res =cur.execute(query,(username,password,email,phno))
        query1="INSERT INTO mylist (name,list) VALUES (?,?)"
        print(query1)
        res1=cur.execute(query1,(username,""))
        
        conn.commit()
        cur.close()
        msg=200
    except:
        print("failed")
        conn.rollback()
        msg=404


    return make_response(jsonify("error"),msg)
    


@app.route('/webtech2/l',methods=['POST'])
def login():
    data= request.json
    #print(data)
    username=request.json['username']
    username=str(username)
    pwd=request.json['pwd']
    password=str(pwd)
    #print(password,username)
    conn=sqlite3.connect('netflix.db')
    query= " select * from logininfo where username="+'"'+ username+'"and password="'+password+'" ;'
    #print(query)
    res =conn.execute(query)
    conn.commit()
    
    if(len(list(res))==0):
        return make_response(jsonify("incorrect credentials"),404)
    else:
        return make_response(jsonify(usn=username),200)


    
    


@app.route('/webtech2/i1',methods=['GET'])
def imagemovie():
    
    count=request.args['count']
    msg=404
    d=dict()
    #print(count)
    try:
        conn=sqlite3.connect('netflix.db')
        query= "select name,location from movies where id = "+count+";"
        #print(query)
        res =conn.execute(query)
        #print(res)        
        conn.commit()
        for line in res:
            d[line[0]]=line[1]
        msg=200
    except:
        conn.rollback()
        msg=404

    #print(d)
    t=json.dumps(d)
    if(int(count)<20):
        return make_response(t,200)
    else:
        return make_response("done !!",400)




@app.route('/webtech2/i2',methods=['GET'])
def imagetv():
    #print("\n\n")
    #print("check")
    count=request.args['count']
    msg=404
    d=dict()
    #print(count)
    try:
        conn=sqlite3.connect('netflix.db')
        query= "select name,location from tvseries where if = "+count+";"
        #print(query)
        res =conn.execute(query)
        #print(res)        
        conn.commit()
        for line in res:
            d[line[0]]=line[1]
        msg=200
    except:
        conn.rollback()
        msg=404

    #print(d)
    t=json.dumps(d)
    #print(jsonify(username="arpit"))

    if(int(count)<20):
        return make_response(t,200)
    else:
        return make_response("done !!",400)



    


@app.route('/webtech2/sb',methods=['GET'])
def fetch():
    #print("check")
    data=[]
    term=request.args['term']
    #print(term+"%")
    term=term+"%"

    try:
        conn=sqlite3.connect('netflix.db')
        query= "select name from movies where name like "+'"'+term+'"'+";"
        #print(query)
        res =conn.execute(query)
        #print(res)        
        conn.commit()
        for i in res:
            data.append(i)
        msg=200
    except:
        conn.rollback()
        msg=404
    
    return make_response(jsonify(data),200)





@app.route('/webtech2/list',methods=['GET'])
def mylist():
    #print("check")
    data=[]
    md=[]
    movies=[]
    loc=[]
    des=[]
    name=request.args['name']
    try:
        conn=sqlite3.connect('netflix.db')
        query= "select list from mylist where name = "+'"'+name+'"'+";"
        #print(query)
        res =conn.execute(query)
        for i in res:
            s=i[0]
        data=s.split(",")
       # print(data)
        for i in data:
            query="select name,location,description from movies where name="+'"'+i+'"'+";"
            res=conn.execute(query)
            for i in res:
                movies.append(i[0])
                loc.append(i[1])
                des.append(i[2])

            
        conn.commit()
    except:
        conn.rollback()
        msg=404
    #print(md)
    #print(movies,loc,des)
    return make_response(jsonify(name=movies,location=loc,description=des),200)
    

@app.route('/webtech2/addlist',methods=['GET'])
def addlist():
    #print("check")
    s=""
    d=[]
    name=request.args['name']
    mname=request.args['mname']
    #print(name,mname)
    try:
        conn=sqlite3.connect('netflix.db')
        query= "select list from mylist where name = "+'"'+name+'"'+";"
        #print(query)
        res =conn.execute(query)
        for i in res:
            s=i[0]
        d=s.split(",")
        #print(d)   
        if(mname not in d):
            #print("nope") 
            if(s==""):
                s=s+mname
            else:
                s=s+","+mname
            query="update mylist set list = "+'"'+s+'"'+" where name = "+'"'+name+'"'+";"
            #print(query)
            res =conn.execute(query)

        conn.commit()
    except:
        conn.rollback()
    #print(s)
    
    return make_response("ok",200)
    

@app.route('/webtech2/removelist',methods=['GET'])
def removelist():
    #print("check")
    s=""
    d=[]
    msg=404
    name=request.args['name']
    mname=request.args['mname']
    #print(name,mname)
    try:
        conn=sqlite3.connect('netflix.db')
        cur=conn.cursor()
        query= "SELECT list FROM mylist WHERE name = ?"
        res =cur.execute(query,(name,))
        #print(list(res)[0])
        for i in res:
            s=i[0]
        print(s)
        d=s.split(",")
        print(d)
        d.remove(mname)
        print(d)
        s=",".join(d)
        print(s)
        query1="UPDATE mylist SET list = ? WHERE name=?"
        res1=cur.execute(query1,(s,name))

        conn.commit()
        cur.close()
        msg=200
    except:
        conn.rollback()
        msg=404
    #print(s)
    if(msg==200):
        return make_response("ok",200)
    else:
        return make_response("error",400)


@app.route('/webtech2/rec',methods=['GET'])
def recom():
    #print("check")
    msg=200
    s=""
    movie=""
    loc=""
    desc=""
    g={"action":0,"adventure":0,"comedy":0,"romance":0,"thriller":0,"drama":0,"horror":0}
    name=request.args['name']
    print(name)
    try:
        conn=sqlite3.connect('netflix.db')
        cur=conn.cursor()
        query="SELECT list FROM mylist WHERE name =?"
        print(query)
        res=cur.execute(query,(name,))
        for i in res:
            s=i[0]

        d=s.split(",")
        print(d)
        if(len(d)!=0 and d[0]!=""):
            for i in d:
                query1="SELECT genre FROM movies WHERE name=?"
                print(query1)
                res1=cur.execute(query1,(i,))
                for i in res1:
                    s=i[0]
                g[s]+=1
            print(g)
            m=max(g.items(), key=lambda k: k[1])
            gen=m[0]
            print(gen)
            query2="SELECT name,location,description FROM movies WHERE genre=?"
            print(query2)
            res2=cur.execute(query2,(gen,))
            
            l=cur.fetchall()
            print(l)
            k=l[random.randint(0,len(l)-1)]
            movie=k[0]
            loc=k[1]
            desc=k[2]
        else:
            n=random.randint(0,38)
            query2="SELECT name,location,description FROM movies WHERE id=?"
            res2=cur.execute(query2,(n,))
            l=cur.fetchall()
            k=l[0]
            movie=k[0]
            loc=k[1]
            desc=k[2]  
        conn.commit()
        cur.close()
        msg=200
    except:
        conn.rollback()
        msg=404
    if(msg==200):
        return make_response(jsonify(mname=movie,location=loc,description=desc),200)
    else:
        return make_response("error",400)




@app.route("/webtech2/recent")
def recent():
    
    def getid():
        l=0
        try:
            conn=sqlite3.connect("netflix.db")
            cur=conn.cursor()
            query= "SELECT max(id) FROM movies"
            res=cur.execute(query)
            k=cur.fetchone()
            l=k[0]
            #print(l)
            conn.commit()
            cur.close()
        except:
            conn.rollback()
        return l
    def getmovie(t):
        movie=""
        loc=""
        desc=""

        try:
            conn=sqlite3.connect("netflix.db")
            cur=conn.cursor()
            query= "SELECT name,location,description FROM movies WHERE id= ?"
            res=cur.execute(query,(t,))
            l=cur.fetchall()
            k=l[0]
            movie=k[0]
            loc=k[1]
            desc=k[2]
            
            conn.commit()
            cur.close()
        except:
            conn.rollback()
        return movie+"|"+loc+"|"+desc

    def eventStream():
        global n

        while True:
            if(getid()>n):
                n=getid()
                st=getmovie(n)
                print(st)
                yield "data: %s\n\n"%st
    return Response(eventStream(), mimetype="text/event-stream")
    

n=0






    


    


    

if __name__=='__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")