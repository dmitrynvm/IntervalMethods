# -*- coding: cp1251

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from interval import interval, inf, imath
from PairList import *
from numpy import *


def f1(x):
    return x ** 2 -  31 * x


def f1_grad(x):
    return 2*x - 31


def f1_hess(x):
    return interval[2]


def f2(x1, x2):
    return 100*(x2 - x1**2)**2 + (1 - x1)**2


def f2_grad(x1, x2):
    return [-200*(x2-x1)**2 - 2*(1-x1), 200*(x2-x1)] 


def f2_hess(x1, x2):
    return [-400*(x2-3*x1)+2, interval[200]]


def f3(x1, x2):
    return x1**4 + 4*x1**3 + 4*x1**2 + x2**2


def f3_grad(x1, x2):
    return [3*x1**3+12*x1**2+8*x1, 2*x2] 


def f3_hess(x1, x2):
    return [9*x1**2+24*x1+8, interval[2]]


def Bisect(iv):
    return interval[iv[0][0], iv.midpoint], interval[iv.midpoint, iv[0][1]]

def w1d(iv):
    return iv[0][1] - iv[0][0]

def w2d(iv):
    return max(iv[0][0][0] - iv[0][0][1], iv[1][0][1] - iv[1][0][0])

def ArgMaxDiam(self):
        maxWidth = self[0][0][1] - self[0][0][0]
        argMaxWidth = 0
        for i in range(len(self)):
            w = self[i][0][1] - self[i][0][0]
            if maxWidth < w:
                maxWidth = w
                argMaxWidth = i
        return argMaxWidth
        


class IntervalOptimizer():

    def __init__(self):
        pass
    
    
    def SaveIntegralInfoToFile(self, filename, integralInfo):
        file = QFile(filename)  
        file.open(QFile.WriteOnly | QFile.Text)
        outf = QTextStream(file)
        self.SaveOptionsToStream(outf)
        for i in range(len(integralInfo)):
            outf << str(integralInfo[i])
    
    def Optimize1d(self, f, f1, f2, boxStart, epsilon):
    
        L = PairList()
        Lres = PairList()
        p = boxStart
        f_wave = f(p)[0][1]
#        print f(p)
        integralInfo = []
        
        i = 0;
        while True:
            I = 0
            boxesPair = Bisect(p)
            integralInfo.append([str(i) + ')', p, '=>', boxesPair])
            for b in boxesPair:
                f_inc = f(b)
                if (f_inc[0][0] > f_wave):
                    continue
                if (0 not in f1(b)):
                    continue
                if(f2(b)[0][0] < 0):
                    continue
                
                f_inf = f_inc[0][0]
                L.Append([b, f_inf])
            doBisection = False
            while (len(L)>0 and not doBisection):
                p, f_inf = L.PopHead()
                m = p.midpoint
                fm = f(m)[0][0]
                f_wave = min(f_wave, fm)
                L.MultiDelete(f_wave)
                
                f_star = [interval[f_inf, f_wave]]
                w = f_wave - f_inf
                if (w<epsilon and p[0][1]-p[0][0]<epsilon):
                    Lres.Append([p, f_inf])
                else:
                    doBisection = True
            if not doBisection:
                break
              
            i = i + 1
            
        integralInfo.append(['Lres', Lres])
        return Lres, integralInfo


    def Optimize2d(self, f, f1, f2, box1, box2, epsilon):
    
        L = PairList()
        Lres = PairList()
        p = [box1, box2]
        f_wave = f(p[0], p[1])[0][1]
        integralInfo = []
        
        i = 0;
        while True:
            I = 0
            if w1d(p[1]) > w1d(p[0]):
                I = 1
            bisectedIv = Bisect(p[I])
            
            if I == 0:
                boxesPair = [[bisectedIv[0], p[1]], [bisectedIv[1], p[1]]]
            if I == 1:
                boxesPair = [[p[0], bisectedIv[0]], [p[0], bisectedIv[1]]]
            
            integralInfo.append([str(i) + ')', p, '=>', boxesPair])
            for b in boxesPair:
                f_inc = f(b[0], b[1])
                if (f_inc[0][0] > f_wave):
                    integralInfo.append(['Low bound test: -'])
                    continue
                else:
                    integralInfo.append(['Low bound test: +'])
                
                if (0 not in f1(b[0], b[1])[0] and 0 not in f1(b[0], b[1])[1]):
                    integralInfo.append(['Monotonity test: -'])
                    continue
                else:
                    integralInfo.append(['Monotonity test: +'])

                if(f2(b[0], b[1])[0][0] < 0 and f2(b[0], b[1])[0][1] < 0):
                    integralInfo.append(['Concavity test: -'])
                    continue
                else:
                    integralInfo.append(['Concavity test: +'])
                
                f_inf = f_inc[0][0]
                L.Append([b, f_inf])
            doBisection = False
            while (len(L)>0 and not doBisection):
                p, f_inf = L.PopHead()
                m0 = p[0].midpoint
                m1 = p[1].midpoint
                fm = f(m0, m1)[0][0]
                f_wave = min(f_wave, fm)
                L.MultiDelete(f_wave)
                
                f_star = interval[f_inf, f_wave]
#                w = f_wave - f_inf
#                print w1d(f_star), w2d(p)
                if (w1d(f_star)<epsilon and w2d(p)<epsilon):
                    Lres.Append([p, f_inf])
                else:
                    doBisection = True
            if not doBisection:
                break
              
            i = i + 1
        integralInfo.append(['Lres'])
        for res in Lres:
            integralInfo.append(res)
#        print Lres
        return Lres, integralInfo



    def SaveIntegralInfoToFile(self, filename, integralInfo):
        file = QFile(filename)  
        file.open(QFile.WriteOnly | QFile.Text)
        outf = QTextStream(file)
#        //self.SaveOptionsToStream(outf)
        for i in range(len(integralInfo)):
            outf << str(integralInfo[i]) << '\n'
            
 
def VecMinus(iv1, iv2):
#        print box1[0][0]
        return (iv2[0][0] - iv1[0][0]), (iv2[0][1] - iv1[0][1])
    
def BoxMinux(box1, box2):
        return Box()
    
def Rho1d(iv1, iv2):
        '''
        Eвклидовой норма.
        '''
        return sqrt(VecMinus(iv1, iv2)[0]**2 + VecMinus(iv1, iv2)[1]**2)
         
def FormClusters(Lres, minPho):
    
    n = len(Lres)
    source = []
    for i in range(n):
        source.append(Lres[i])
    
    adjMatrix = mat(zeros([n,n]), dtype=float)
    for i in range(n):
        for j in range(i+1, n):
            r1 = Rho1d(Lres[i][0][0], Lres[j][0][0])
            r2 = Rho1d(Lres[i][0][1], Lres[j][0][1])
            pho = r1**2 + r2**2
            adjMatrix[i,j] = r1**2 + r2**2
#    //opt.SaveIntegralInfoToFile('info1.txt', adjMatrix)  
    
    
    listMatrix = []
    for i in range(n):
        setElement = set()
        for j in range(i+1, n):
            if adjMatrix[i,j] < minPho:
                setElement.add(j)
        listMatrix.append(setElement)
        
    
    
    copiedMatrix = [l for l in listMatrix]
    n = len(listMatrix)
    clasters = []
    for i in range(n):
        doClustering = True
        clasterSource = [l for l in copiedMatrix[i]]
#        print clasterSource
        for j in range(n):
            claster = set()
            claster = claster.union(clasterSource)
            elemsToDel = set()
            for elem in clasterSource:
                claster = claster.union(copiedMatrix[elem])
                elemsToDel.add(elem)
            copiedMatrix[j] = copiedMatrix[j] - elemsToDel
            clasterSource = claster.copy()
            
        clasters.append(claster)    
     
    finalClasters = []
    for elem in clasters:
        if elem != set([]):
            finalClasters.append(elem)
    
#    print finalClasters[0]
#    print len(finalClasters)
#    print set(finalClasters[1]).intersection(set(finalClasters[2]))
    ivClasters = []
    for i in range(len(finalClasters)):
        ivClaster = []
        for j in finalClasters[i]:
            ivClaster.append(Lres[j][0])
        ivClasters.append(ivClaster)
#    print ivClasters[2]
    return GetCenters(ivClasters)
    
            
def GetCenters(ivClasters):
#    for ivClaster in ivClasters:
    ivCenters = []
    for ivClaster in ivClasters:
#        ivClaster = ivClasters[2]
        s00 = 0
        s01 = 0
        s10 = 0
        s11 = 0
        for i in range(len(ivClaster)):
            s00 += ivClaster[i][0][0][0] 
            s01 += ivClaster[i][0][0][1] 
            s10 += ivClaster[i][1][0][0] 
            s11 += ivClaster[i][1][0][1] 
        
        midIvs0 = interval[s00/len(ivClaster), interval[s01/len(ivClaster)]]
        midIvs1 = interval[s10/len(ivClaster), interval[s11/len(ivClaster)]]
#        print [midIvs0, midIvs1]
        ivCenters.append([midIvs0, midIvs1])
        return ivCenters
