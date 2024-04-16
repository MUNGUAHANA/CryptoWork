from flask import Flask, render_template, request, redirect
import mysql.connector
from Crypto.Cipher import DES
import base64
from Crypto.Util.Padding import pad


host="localhost"
user="root"
password=""
database="medicality" 



app=Flask(__name__)
@app.route('/')
def index():
    return render_template('login.html')

# Fonction de chiffrement
def prepare_key_and_pad(key, data):
    """
    Converts the key to bytes and ensures it's the correct length for DES.
    Pads the data to the DES block size for secure encryption.
    """

    if len(key) != DES.block_size:
        raise ValueError("Key length must be equal to DES block size (8 bytes)")

    key_bytes = key  # Secure key handling
    padded_data = pad(data.encode('utf-8'), DES.block_size)  # Pad data with PKCS#7
    return key_bytes, padded_data

# Function to encrypt data
def chiffrer(texte):
    """
    Encrypts the provided text using DES in ECB mode.
    Returns the base64-encoded ciphertext.
    """

    key, padded_data = prepare_key_and_pad(b"ma_clees", texte)  # Secure key handling
    cipher = DES.new(key, DES.MODE_ECB)
    texte_chiffre = cipher.encrypt(padded_data)
    return base64.b64encode(texte_chiffre).decode('utf-8')

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
    
    cipher_id=chiffrer(id)
    cipher_date=chiffrer(date)
    cipher_temperature=chiffrer(temperature)
    cipher_antecedent= chiffrer(antecedent)
    cipher_symptoms=chiffrer(symptoms)
    sql="""INSERT INTO patients (id_patient,poid_patient,taille_patient,temperature_patient,genre_patient,antecedent_patient,date_patient,symptoms_patient) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    vals=(cipher_id,poid,taille,cipher_temperature,genre,cipher_antecedent,cipher_date,cipher_symptoms)
    cursor.execute(sql, vals)
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


