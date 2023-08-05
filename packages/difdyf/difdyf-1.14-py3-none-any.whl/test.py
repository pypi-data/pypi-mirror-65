from sympy import *
from difdyf.util_func import *
import numpy as np

########### r theta phi      3-d sphere axis
n=3
# inputsym=['r','theta','phi']
# ginput={}
# for i in inputsym:
#     tmp={}
#     for j in inputsym:
#         tmp[j]='0';
#     ginput[i]=tmp
# ginput['r']['r']='1';
# # ginput['r']['theta']=0
# ginput['theta']['theta']='r*r'
# ginput['phi']['phi']='r*r*sin(theta)*sin(theta)'
[ginput, inputsym]=sphereMetric()
####################################################### init the metric field  ginput

T=getChristSymb(ginput,inputsym)
print(T)          #############################################get the christ symbol
T_dict=list2Dict(T,inputsym,listDepth(T))
R=getRiemannCurvature(T,inputsym) #####################################get the riemann curvature tensor
R_dict=list2Dict(R,inputsym,listDepth(R))
print(R_dict)
# sym={};
# x=[0]*n
# for i in range(n):
#     sym[inputsym[i]]=i
#     x[i]=Symbol(inputsym[i])
#
# g=Matrix([[eval(changeVarName(ginput[inputsym[i]][inputsym[j]],inputsym)) for j in range(n)] for i in range(n)])
# g_inv=(g**-1)
# g_deriv=np.array([[[diff(g[i,j],x[k]) for k in range(n)] for j in range(n)] for i in range(n)])
# # T=(g_deriv+np.transpose(g_deriv,(0,2,1))-np.transpose(g_deriv,(1,2,0)))
# # T=(np.dot(g_inv,np.transpose(T,(1,0,2))))/2
# T=([[[0 for i in range(n)] for j in range(n)] for k in range(n)])
# for i in range(n):
#     for j in range(n):
#         for k in range(n):
#             tmp=g_inv[i,:]*Matrix((g_deriv[:,j,k]+g_deriv[:,k,j]-g_deriv[j,k,:])/2)
#             T[i][j][k]=tmp[0]

# print(changeVarName('r*r*sin(theta)',['r','theta']))


