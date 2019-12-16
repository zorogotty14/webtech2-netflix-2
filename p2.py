from flask import Flask, jsonify,abort,make_response,request,render_template,session,Response
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
    app.run(debug=True)