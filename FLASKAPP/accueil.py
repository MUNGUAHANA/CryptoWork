import math as m
from flask import Flask, render_template, request, redirect
import mysql.connector


host="localhost"
user="root"
password=""
database="inscription"


app=Flask(__name__)
@app.route('/')
def index():
    return render_template('page1.html')

@app.route("/list", methods=["POST"])
def connector(): 
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    mat=request.form["mat"]
    nom=request.form["nom"]
    faculte=request.form["faculte"]
    Age=request.form["Age"]
    adresse=request.form["adresse"]
   
    plainText=mat
    n=33
    e=3
    #cipherText  = []
    codeChart = "abcdefghijklmnopqrstuvwxyz "
    for key in codeChart:
        for i in plainText:
            if key == i:
                char = codeChart.index(key)
                # print(char)
                c = int(m.pow(char, e) % n)
                # print(c)
               # cipherText.append(c)
               # text=cipherText
    sql="""INSERT INTO etudiant (matricule,noms, faculté,date_de_naissance,adresse) VALUES (%s,%s,%s,%s,%s)"""
    vals=(c,nom,faculte,Age,adresse)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
   # tableau=[ 
          #  {'nom':nom, 'faculte':faculte, 'Age':Age,'adresse':adresse},
       # ]
    return render_template('list.html')

 
#message='nom'
#print(connector(message, 33, 3))


 
@app.route("/list")
def list():
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    sql="SELECT * FROM etudiant"
    
    cursor.execute(sql)
    listEt=cursor.fetchall()
    connection.commit()
    cursor.close
    
    return render_template('list.html',data=listEt) 


@app.route('/delete/<mat>/')
def delete(mat):   
    connection=mysql.connector.connect(   
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    #mat=request.form["mat"]
   
    sql="DELETE FROM etudiant WHERE matricule=%s"
    vals=(mat,)
    cursor.execute(sql,vals)
    
    connection.commit()
    return redirect('/list')


@app.route('/data_call/<mat>/')
def lancer(mat):
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    plainText=mat
    n=33
    e=3
    cipherText  = []
    codeChart = "abcdefghijklmnopqrstuvwxyz "
    for key in codeChart:
        for i in plainText:
            if key == i:
                char = codeChart.index(key)
                # print(char)
                c = int(m.pow(char, e) % n)
                # print(c)
                cipherText.append(c)
                # text=cipherText
    messageChiffre=cipherText
    d=7
    n=33
    plainText = ""
    codeChart = "abcdefghijklmnopqrstuvwxyz"
    for i in messageChiffre:
        # plainText += str(m.pow(i,d)%n)
        char = m.pow(i,d)%n
        for key in range(len(codeChart)):
            if key == char:
                plainText += codeChart[key]
    cursor=connection.cursor()
    sql="SELECT * FROM etudiant WHERE matricule=%s"
    cursor.execute(sql,(plainText,))
    data=cursor.fetchall()
    print(data)
    return render_template('updateStud.html',data=data)

@app.route('/update/<mat>/')
def update(mat):   
    connection=mysql.connector.connect(    
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    
    if request.method=='POST':
        mat=request.form["mat"]
        nom=request.form["nom"]
        facultee=request.form["facultee"]
        Agee=request.form["Agee"]
        adressee=request.form["adressee"]
        sql='UPDATE etudiant SET (nom=%s,faculté=%s,date_de_naissance=%s,adresse=%s) WHERE matricule=%s'
        vals=(nom,facultee,Agee,adressee,mat)
        cursor.executse(sql, vals)
        connection.commit()
         
    return redirect('/list')

if __name__=='__main__':
    app.run(debug=True)