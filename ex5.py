import os
import json



#cessers code



class CaesarCipher:

    #creats a new object of caesar encryption
    def __init__(self,key):
        self.encryptionKey=key
        self.numOfLetters=ord('z')-ord('a')+1

    #recievs a text to encrypt
    #returns the encrypted text
    def encrypt(self,textToEncrypt):
        encryptedText=' '
        for letter in textToEncrypt:
            if letter.isalpha():
                encryptedText=encryptedText+self.encryptDecryptHelper(letter,True)
            else:
                encryptedText=encryptedText+letter
        return encryptedText[1:]

    #recievs a text to decrypt
    #returns the decrypted text
    def decrypt(self,textToDecrypt):
        decryptedText=' '
        for letter in textToDecrypt:
            if letter.isalpha():
                decryptedText=decryptedText+self.encryptDecryptHelper(letter,False)
            else:
                decryptedText=decryptedText+letter
        return decryptedText[1:]

    #recieve a char to encryptes or decryptes
    #if the char is a letter in the English alphabet
    #   will encrypt/decrypt the char
    #if not a letter in the English alphabet
    #   will return the same character
    def encryptDecryptHelper(self,letter,toEncrypt):
        if toEncrypt:
            key=self.encryptionKey
        else:
            key=-1*self.encryptionKey
        tempAscii=ord(letter)
        if (letter.islower()):
            tempAscii=(ord(letter)-ord('a')+key)%self.numOfLetters+ord('a')
        else:
            tempAscii=(ord(letter)-ord('A')+key)%self.numOfLetters+ord('A')
        return chr(tempAscii)


#vijnier code



class VigenereCipher:

    #creats a new object of vijnear encryption
    def __init__(self,numList):
        self.encryptionKey=numList
        self.numOfLetters=ord('z')-ord('a')+1

    #recievs a text to encrypt
    #returns the encrypted text
    def encrypt(self,textToEncrypt):
        encryptedText=' '
        encryptionIndex=0
        for letter in textToEncrypt:
            currentKey=self.encryptionKey[encryptionIndex] #current key
            if letter.isalpha():
                encryptedText=encryptedText+self.encryptOrDecryptChar(letter,currentKey)
                if(encryptionIndex+1==len(self.encryptionKey)):
                    encryptionIndex=0
                else:
                    encryptionIndex=encryptionIndex+1
            else:
                encryptedText=encryptedText+letter
        return encryptedText[1:]

    #recieve a char to encryptes or decryptes
    #if the char is a letter in the English alphabet
    #   will encrypt/decrypt the char and update the index
    #if not a letter in the English alphabet
    #   will return the same character
    def encryptOrDecryptChar(self,character,key):
        tempAscii=ord(character)
        if (character.islower()):
            tempAscii=(ord(character)-ord('a')+key)%self.numOfLetters+ord('a')
        else:
            tempAscii=(ord(character)-ord('A')+key)%self.numOfLetters+ord('A')
        return chr(tempAscii)
    
    #recievs a text to decrypt
    #returns the decrypted text
    def decrypt(self,textToDecrypt):
        decryptedText=' '
        decryptionIndex=0
        for letter in textToDecrypt:
            currentKey=-1*self.encryptionKey[decryptionIndex] #current key
            if letter.isalpha():
                decryptedText=decryptedText+self.encryptOrDecryptChar(letter,currentKey)
                if(decryptionIndex+1==len(self.encryptionKey)):
                    decryptionIndex=0
                else:
                    decryptionIndex=decryptionIndex+1
            else:
                decryptedText=decryptedText+letter
        return decryptedText[1:]

        #note that decrypting with a value of x s the same as encrypting with -x


#part 2

#the function gets a string
#the function creates a vingere encryption object from the string
def getVigenereFromStr(key):
    keyList=[]
    for letter in key:
        if letter.isalpha():
            keyList.append(getIndexOfLetter(letter))
    return VigenereCipher(keyList)

#the function gets a letter and returns its rank
def getIndexOfLetter(letter):
    if letter.islower():
        return ord(letter)-ord('a')
    else:
        return ord(letter)-ord('A')



#encryption system



#gets the path to the folder
#according to the json file, decrypts/encrypts files
def loadEncryptionSystem(dir_path):
    filePath=os.path.join(dir_path,'config.json')
    with open(filePath,'r') as file:
        encryptDictionary=json.load(file)
        if(encryptDictionary['type']=='Caesar'):#ceasar encryption
            caesarEncryptionSystem(dir_path,encryptDictionary['key'],encryptDictionary['encrypt'])
        else: #vingenere encryption
            vingereEncryptSystem(dir_path,encryptDictionary['key'],encryptDictionary['encrypt'])

#decrypts/encrypts the files in the folder according to Caesar encryption
def caesarEncryptionSystem(dir_path,key,encrypt):
    caesar=CaesarCipher(key)
    encryptOrDecrypt(dir_path,encrypt,caesar)

#decrypts/encrypts the files in the folder according to vigenere encryption
def vingereEncryptSystem(dir_path,key,encrypt):
    vingenere=' '
    if(type(key)==str):
        vingenere=getVigenereFromStr(key)
    else:
        vingenere=VigenereCipher(key)
    encryptOrDecrypt(dir_path,encrypt,vingenere)

#encrypts or decrypts the file according to the encryption object
def encryptOrDecrypt(dir_path,encrypt,encryptionObject):
    for file in os.listdir(dir_path): #for each file
        name,typeFile=os.path.splitext(file)
        fileEncName=dir_path+os.sep+name+'.enc'
        fileTxtName=dir_path+os.sep+name+'.txt'
        if(typeFile=='.txt' and encrypt=='True'): #need to encrypt
            with open(fileEncName,'w') as encFile:
                with open(fileTxtName,'r') as txtFile:
                    encFile.write(encryptionObject.encrypt(txtFile.read()))
        if(typeFile=='.enc' and encrypt=='False'): #need to decrypt
            with open(fileTxtName,'w') as txtFile:
                with open(fileEncName,'r') as encFile:
                    txtFile.write(encryptionObject.decrypt(encFile.read()))
