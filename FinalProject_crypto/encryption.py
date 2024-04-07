from flask import Flask, render_template, request, redirect
import mysql.connector
from Crypto.Cipher import DES

host="localhost"
user="root"
password=""
database="medicality" 

#Clé DES (8 caractères)
key = b"correct_"

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('login.html')

# Fonction de chiffrement
def chiffrer(texte):
    if texte==" ":
        codeChart = "abcdefghijklmnopqrstuvwxyz"

        for key in codeChart:
            for i in texte:
                if key == i:
                    char = codeChart.index(key)        
        msgByte=b''.join(char)
    else:
        msgByte=b''.join(texte)
        
              
    cipher = DES.new(key, DES.MODE_ECB)
    texte_chiffre = cipher.encrypt(msgByte)   
    return texte_chiffre

@app.route("/symptoms", methods=["POST"])
def connector(): 
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    id=request.form["password"]
    nom_pat=request.form["name"]
   
   
    sql="""INSERT INTO login (pass_word,username) VALUES (%s,%s)"""
    vals=(id,nom_pat)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
   
    return render_template('symptoms.html')
   

@app.route("/list", methods=["POST"])
def connector1(): 
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    id=request.form["id"]
    poid=request.form["80"]
    taille=request.form["2.4"]
    temperature=request.form["temperature"]
    genre=request.form["gender"]
    antecedent=request.form["antecedents"]
    date=request.form["date"]
    symptoms=request.form["symptoms"]
   
   
    sql="""INSERT INTO patients (id_patient,poid_patient,taille_patient,temperature_patient,genre_patient,antecedent_patient,date_patient,symptoms_patient) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    vals=(id,poid,taille,temperature,genre,antecedent,date,symptoms)
    texte_chiffre = chiffrer(vals)
    cursor.execute(sql, texte_chiffre)
    connection.commit()
    cursor.close()
   
    return render_template('patients.html')

@app.route("/list")
def list():
    connection=mysql.connector.connect(  
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    sql="SELECT * FROM patients"
    
    cursor.execute(sql)
    listPat=cursor.fetchall()
    connection.commit()
    cursor.close
    
    return render_template('patients.html',data=listPat) 

@app.route('/delete/<id>/')
def delete(id):   
    connection=mysql.connector.connect(   
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=connection.cursor()
    #mat=request.form["mat"]
   
    sql="DELETE FROM patients WHERE id_patient=%s"
    vals=(id,)
    cursor.execute(sql,vals)
    
    connection.commit()
    return redirect('/list')


if __name__=='__main__':
        app.run(debug=True)


