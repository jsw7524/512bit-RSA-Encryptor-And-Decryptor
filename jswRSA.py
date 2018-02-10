import sympy
import pickle

class jswRSA:
    def Egcd(self,a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, y, x = self.Egcd(b % a, a)
            return (gcd, x - (b // a) * y, y)

    def ModInv(self, a, modulo):
        gcd, x, y = self.Egcd(a, modulo)
        if gcd != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % modulo

    def ModExpNum(self, number, exp, modulo):
        if 1==exp:
            return number % modulo
        if 0==exp%2:
            return (self.ModExpNum(number,exp//2,modulo))**2%modulo
        else:
            return (((self.ModExpNum(number,exp//2,modulo))**2)*number)%modulo

    def Encrypt(self, number):
        EncryptedNumber=self.ModExpNum(number,self.e,self.pq)
        return EncryptedNumber

    def Decrypt(self, cipher):
        d = self.ModInv(self.e,(self.p-1)*(self.q-1))
        DecryptedNumber = self.ModExpNum(cipher, d, self.p*self.q)
        return DecryptedNumber

    def __init__(self,keyLength=512,privateKey=None,publicKey=None):
        if publicKey is not None:
            self.pq, self.e=publicKey
            return
        if privateKey is not None :
            self.p, self.q, self.e = privateKey
        else:
            while True:
                self.p=sympy.randprime(2**(keyLength//2-1), 2**(keyLength//2))
                self.q=sympy.randprime(2**(keyLength//2-1), 2**(keyLength//2))
                if self.p != self.q:
                    break
            self.e = sympy.randprime(5, 2 ** (keyLength//2))
        self.pq = self.p * self.q
        return

    def GetPublicKey(self):
        return (self.pq, self.e)

    def GetPrivateKey(self):
        return (self.p,self.q, self.e)

'''
jswRSA=jswRSA()
pickle.dump(jswRSA.GetPublicKey(),open('PublicKey.rsa', 'wb'))
pickle.dump(jswRSA.GetPrivateKey(),open('PrivateKey.rsa', 'wb'))
'''
'''
plainText=7524
print("original text:", plainText)
private_Key=(85203509857200512501747207220205690483257770000734320636806025784995452664041, 65379221674771633598258940595201926812553997374321948657660867030603679807109, 27477460916541279120875493995683278682798154183010462213482709398311439703599)
public_Key=(5570539158422502282813541718385125087680305781663922513564599491724964604994699706447502656763751940913478156202381163381645655200262298638900411060467469, 27477460916541279120875493995683278682798154183010462213482709398311439703599)

RSA_Sender=jswRSA(publicKey=public_Key)
encryptedText = RSA_Sender.Encrypt(plainText)
print("encrypted:", encryptedText)

RSA_Receiver=jswRSA(privateKey=private_Key)
decryptedText=RSA_Receiver.Decrypt(encryptedText)
print("decrypted:", decryptedText)
print("Does decrypted text equal original text? ", decryptedText==plainText)
'''
