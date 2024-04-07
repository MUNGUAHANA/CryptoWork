import math as m

def rsa(plainText,n,e):
    cipherText  = []
    codeChart = "abcdefghijklmnopqrstuvwxyz"

    for key in codeChart:
        for i in plainText:
            if key == i:
                char = codeChart.index(key)
                # print(char)
                c = int(m.pow(char, e) % n)
                # print(c)
                cipherText.append(c)
    return cipherText


def dechRSA(messageChiffre,d,n):
    plainText = ""
    codeChart = "abcdefghijklmnopqrstuvwxyz"
    for i in messageChiffre:
        # plainText += str(m.pow(i,d)%n)
        char = m.pow(i,d)%n
        for key in range(len(codeChart)):
            if key == char:
                plainText += codeChart[key]
    return plainText



message = "hi"

print(rsa(message, 33, 3))
print(" -----------Dechiffrement--------")

cipherText = [13,17]

# print(rsa(message, 33, 3))
print(dechRSA(cipherText,7,33))