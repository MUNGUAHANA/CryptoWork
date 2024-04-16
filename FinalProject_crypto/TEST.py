import base64
from flask import Flask, request, jsonify
from Crypto.Cipher import DES

app = Flask(__name__)

# Clé DES (8 caractères)
key = b"ma_cle_secrete"

# Fonction de chiffrement
def chiffrer(texte):
    cipher = DES.new(key, DES.MODE_ECB)
    texte_chiffre = cipher.encrypt(texte.encode())
    return base64.b64encode(texte_chiffre).decode()

# Fonction de déchiffrement
def dechiffrer(texte_chiffre):
    cipher = DES.new(key, DES.MODE_ECB)
    texte_dechiffre = cipher.decrypt(base64.b64decode(texte_chiffre))
    return texte_dechiffre.decode()

# Route pour chiffrer un texte
@app.route("/chiffrer", methods=["POST"])
def api_chiffrer():
    texte = request.json["texte"]
    texte_chiffre = chiffrer(texte)
    return jsonify({"texte_chiffre": texte_chiffre})

# Route pour déchiffrer un texte
@app.route("/dechiffrer", methods=["POST"])
def api_dechiffrer():
    texte_chiffre = request.json["texte_chiffre"]
    texte_dechiffre = dechiffrer(texte_chiffre)
    return jsonify({"texte_dechiffre": texte_dechiffre})

if __name__ == "__main__":
    app.run(debug=True)
