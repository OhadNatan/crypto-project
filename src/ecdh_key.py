# Uses python3
import math
import random
import argparse


# Run program with the parameters of the curve as follows:
# python ECDH.py -a 2 -b 2 -p 17 -x 5 -y 1
# a,b - parameters of the curve y^2 = x^3 + ax + b
# p - modulo prime for the curve (Ensure it is a prime number!)
# x,y - Generator coordinates (Ensure it is a point on the curve specified by a and b)


class EllipticCurve():
    def __init__(self, a, b, p, xGen, yGen):
        # Initialize a curve with parameters and generator point
        self.a = a
        self.b = b
        self.p = p
        self.xGen = xGen
        self.yGen = yGen
        self.__E = None
    def computeY(self,x):
        # Returns the y value of the curve given the x value
        return math.sqrt(x ** 3 + self.a * x + self.b) % self.p
    def ellipticGradientE(self, x, y):
        # Returns gradient at point (x,y). This is for the case when you perform point doubling.
        return (((3 * (x ** 2) + self.a) % self.p) * (((2 * y) ** (self.p - 2)) % self.p)) % self.p
    def ellipticGradientNE(self, x1, y1, x2, y2):
        # Returns gradient of the line passing through (x1,y1) and (x2,y2). For Point Addition.
        return (((y2 - y1) % self.p) * (((x2 - x1) ** (self.p - 2)) % self.p)) % self.p
    def PointDoubleGen(self):
        # Returns the point obtained after point doubling on generator P(x,y)
        m = self.ellipticGradientE(self.xGen,self.yGen)
        x3 = (m ** 2 - self.xGen - self.xGen) % self.p
        y3 = (m * (self.xGen - x3) - self.yGen) % self.p
        return (x3,y3)
    def PointDouble(self, x1, y1):
        # Returns the point obtained after point doubling on (x1,y1)
        m = self.ellipticGradientE(x1, y1)
        x3 = (m ** 2 - x1 - x1) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return (x3,y3)
    def PointAdd(self, x1, y1, x2, y2):
        # Returns the point obtained after performing point addition of (x1,y1) and (x2,y2)
        if x2 == x1:
            return (math.inf, math.inf)
        m = self.ellipticGradientNE(x1, y1, x2, y2)
        x3 = (m ** 2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return (x3,y3)
    def numOfPoints(self):
        # Computes the number of points on the curve. Stores #E.
        count = 2
        x2, y2 = self.PointDoubleGen()
        while x2 != math.inf:
            x3, y3 = self.PointAdd(self.xGen,self.yGen,x2,y2)
#             print("Point add P + ", count,"P is ", (x3, y3))
            x2 = x3
            y2 = y3
            count += 1
        self.__E = count
    def generatePrivateKey(self):
        # Generates the private key
        return random.randint(1, self.__E - 1)

def generatePublicKey(privKey, curve):
    # Generates a public key from the given private key
    x,y = curve.PointDoubleGen()
    if privKey == 2:
        return (x,y)
    count = 3
    while count <= privKey:
        x1,y1 = curve.PointAdd(curve.xGen, curve.yGen, x, y)
        x = x1
        y = y1
        count += 1
    return (x,y)


def generateSharedKey(pubKey, privKey, curve):
    # Generates the shared key for two users
    x, y = pubKey
    x2, y2 = curve.PointDouble(x,y)
    if privKey == 2:
        return (x2,y2)
    count = 3
    while count <= privKey:
        x3, y3 = curve.PointAdd(x,y,x2,y2)
        if x3 == math.inf:
            x2, y2 = curve.PointDouble(x,y)
            count += 2
        else:
            x2 = x3
            y2 = y3
            count += 1
    return (x2,y2)