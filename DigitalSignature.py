import jswRSA
import pickle
import hashlib

class DigitalSignaturer:
    def __init__(self,privateKey=None,publicKey=None):
        if (publicKey is not None):
            publicKeyFile = open(publicKey, 'rb')
            resotredPublicKey = pickle.load(publicKeyFile)
            self.rsa = jswRSA.jswRSA(publicKey=resotredPublicKey)
            publicKeyFile.close()
        if (privateKey is not None):
            privateKeyFile = open(privateKey, 'rb')
            resotredprivateKey = pickle.load(privateKeyFile)
            self.rsa = jswRSA.jswRSA(privateKey=resotredprivateKey)
            privateKeyFile.close()

    def AddDigitalSignature(self,srcFileNmae,destFileNmae):
        MessageFile = open(srcFileNmae, 'rb')
        SalesMessage = MessageFile.read()
        SalesMessageMD5 = int(hashlib.md5(SalesMessage).hexdigest(), 16)
        Tag = self.rsa.Encrypt(SalesMessageMD5)
        pickle.dump((SalesMessage, Tag), open(destFileNmae, 'wb'))
        MessageFile.close()

    def ReadFileWithDigitalSignature(self,srcFileNmae,writeContenToFile=None):
        DigitalSignatureFile = open(srcFileNmae, 'rb')
        DigitalSignature = pickle.load(DigitalSignatureFile)
        ResotredMessage, ResotredTag = DigitalSignature


        if  (int(hashlib.md5(ResotredMessage).hexdigest(),16) == self.rsa.Decrypt(ResotredTag)):
            print("Generating File......")
            if writeContenToFile is not None:
                destFile = open(writeContenToFile, 'wb')
                destFile.write(ResotredMessage)
                destFile.close()
        else:
            print("MD5 is not matched!")
            if writeContenToFile is not None:
                destFile = open(writeContenToFile, 'w')
                destFile.write("MD5 is not matched!")
                destFile.close()
        DigitalSignatureFile.close()


myDigitalSignaturer= DigitalSignaturer(publicKey='PublicKey.rsa')
myDigitalSignaturer.AddDigitalSignature(srcFileNmae="MessageForYou.txt",destFileNmae="MessageForYouWith.DigitalSignature")
''''''

myDeDigitalSignaturer= DigitalSignaturer(privateKey='PrivateKey.rsa')
myDeDigitalSignaturer.ReadFileWithDigitalSignature("MessageForYouWith.DigitalSignature",writeContenToFile="Undo_MessageForYou.txt")
