import numpy as np
from sympy import *


def sphereMetric():
    inputsym = ['r', 'theta', 'phi']
    ginput = {}
    for i in inputsym:
        tmp = {}
        for j in inputsym:
            tmp[j] = '0';
        ginput[i] = tmp
    ginput['r']['r'] = '1';
    ginput['theta']['theta'] = 'r*r'
    ginput['phi']['phi'] = 'r*r*sin(theta)*sin(theta)'
    return ginput,inputsym
def orthMetric(n):
    inputsym = ['x'+str(i) for i in range(n)]
    ginput = {}
    for i in inputsym:
        tmp = {}
        for j in inputsym:
            tmp[j] = '0';
        ginput[i] = tmp
    for i in range(n):
        ginput[inputsym[i]][inputsym[i]]='1'
    return ginput, inputsym
def coord2MetricFromOrth(n,coordList,varlist):
    #i.e.   n=3;   coordList=['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)']
    #              varlist=['r','theta','phi']
    assert(n==len(coordList))
    assert(n==len(varlist))
    x = [0] * n
    sym={}
    for i in range(n):
        sym[varlist[i]] = i
        x[i] = Symbol(varlist[i])
    for i in range(n):
        coordList[i]=eval(changeVarName(coordList[i],varlist,x))
    g = {}
    for i in varlist:
        tmp = {}
        for j in varlist:
            tmp[j] = str(simplify(sum([diff(coordList[coord],x[sym[i]])*diff(coordList[coord],x[sym[j]]) for coord in range(n)])));
        g[i] = tmp


    return g,varlist


def ischar(ch):
    return ord(ch) >= 97 and ord(ch) <= 122
def changeVarName(s,varlist,x):
    cnt=0
    try:
        m=len(s)
    except TypeError:
        print('need to write metric in string')
    tmp=''
    flag=[True]*m
    for i in range(m):
        if flag[i]==False:
            continue
        breakj=False
        for j in range(i+1,m+1):
            for k in range(len(varlist)):
                if s[i:j] ==varlist[k]:
                    if (i==0 or (not ischar(s[i-1]))) and (j==m or (not ischar(s[j]))):
                        tmp=tmp+'x['+str(k)+']'
                        flag[i:j]= [False]*(j-i)
                        breakj=True
                        break
            if breakj==True:# or (j==m or (not ischar(s[j]))):
                break
        if breakj==False:
            tmp=tmp+s[i]
    # print(tmp)
    return tmp
def getChristSymb(ginput,coordinateName):

# coordinateName is the given axis name i.e. ['r', 'theta','phi']
# ginput is metric field i.e. ginput={'r': {'r': '1', 'theta': '0', 'phi': '0'},
#                           'theta': {'r': '0', 'theta': 'r*r', 'phi': '0'},
#                           'phi': {'r': '0', 'theta': '0', 'phi': 'r*r*sin(theta)*sin(theta)'}}
    n=len(coordinateName)
    x = [0] * n
    sym={};
    for i in range(n):
        sym[coordinateName[i]] = i
        x[i] = Symbol(coordinateName[i])
    g = Matrix([[eval(changeVarName(ginput[coordinateName[i]][coordinateName[j]], coordinateName,x)) for j in range(n)] for i in range(n)])
    g_inv = (g ** -1)
    g_deriv = np.array([[[diff(g[i, j], x[k]) for k in range(n)] for j in range(n)] for i in range(n)])
    # T=(g_deriv+np.transpose(g_deriv,(0,2,1))-np.transpose(g_deriv,(1,2,0)))
    # T=(np.dot(g_inv,np.transpose(T,(1,0,2))))/2
    T = ([[[0 for i in range(n)] for j in range(n)] for k in range(n)])
    for i in range(n):
        for j in range(n):
            for k in range(n):
                tmp = g_inv[i, :] * Matrix((g_deriv[:, j, k] + g_deriv[:, k, j] - g_deriv[j, k, :]) / 2)
                T[i][j][k] = tmp[0]

    return T
def getRiemannCurvature(T,symb):# T - christSymb n*n*n            symb   -    r, theta, phi
    n=len(symb)
    x = [0] * n
    for i in range(n):
        x[i] = Symbol(symb[i])
    R = ([[[[0 for m in range(n)] for i in range(n)] for j in range(n)] for k in range(n)])
    for u in range(n):
        for v in range(n):
            for d in range(n):
                for p in range(n):
                    tmp=sum([T[lam][d][u]*T[p][v][lam]-T[lam][d][v]*T[p][u][lam] for lam in range(n)])
                    R[u][v][d][p]=diff(T[p][u][d],x[v])-diff(T[p][v][d],x[u])+tmp
    print(1)
    return R
def getRici(T,symb):
    n = len(symb)
    x = [0] * n
    for i in range(n):
        x[i] = Symbol(symb[i])
    Rici=[[0 for i in range(n)] for j in range(n)]
    for u in range(n):
        for d in range(n):
            tmp=sum([diff(T[v][u][d],x[v])-diff(T[v][v][d],x[u]) for v in range(n)])
            Rici[u][d]=tmp+sum([sum([T[lam][u][d]*T[v][lam][v]-T[lam][v][d]*T[v][lam][u] for lam in range(n)]) for v in range(n)])
    return Rici
def listDepth(list):
    depth=0
    if type(list)!=type([]):
        return depth
    tmp=list[0]
    depth=depth+1
    while type(tmp)==type([]):
        tmp=tmp[0]
        depth=depth+1
    return depth
def list2Dict(list,symb,depth):
    # depth=listDepth(list)
    n=len(symb)
    if depth==1:
        return dict(zip(symb,list))
    else:
        return dict(zip(symb,[list2Dict(list[i],symb,depth-1) for i in range(n)]))
    return
# g,v=coord2MetricFromOrth(3,['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)'],['r','theta','phi'])
print('import util success')
print('''use   [g,symbol] = sphereMetric() to create a example metric
        ##symbol=['r','theta','phi']##
use T=getChristSymb(g,symbol) to get the christ tensor
use R=getRiemannCurvature(T,symbol) to get riemann curvature tensor
The input metric g should be given in dictionary form
''')

