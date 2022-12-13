# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 19:35:45 2022

@author: dcmol
"""
import os
import json
import re
import networkx as nx
import copy
import numpy as np
import matplotlib.pyplot as plt
import tkinter
from tkinter import ttk,Label
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import keyboard

"""
def on_move(event):
    if event.inaxes:
        a=1
def on_click(event):
    if event.button is MouseButton.LEFT:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')             
"""
def homdeg(P):
    V=P.nodes
    E=P.edges
    dictio={}
    for e in E:
        dictio[e]=remove_vars(e[0],e[1])
    return dictio
def samemonomial(unsigned,signed):
    if "-"+unsigned==signed:
        return True,"-"
    if unsigned==signed:
        return True,"+"
    else:
        return False,"Not"
def equal_up_to_sign(unsigned_column,signed_column):
    unsigned_set=set(unsigned_column)
    signed_set=set(signed_column)
    if '0' in signed_set:
        signed_set.remove('0')
    if len(unsigned_set)!=len(signed_set):
        return False
    for a in unsigned_set:
        if a not in signed_set and "-"+a not in signed_set:
            return False
    return True

def contains_vars(t,s):
    res=re.findall("x[0-9]+",t)
    for var in res:
        if var not in s:
            return False
    return True
def remove_vars(t,s):
    u=s
    res=re.findall("x[0-9]+",t)
    for var in res:
        u=u.replace(var,"")
    while re.search("\*\*", u):
        u=u.replace("**","*")
    if u[-1]=="*":
        u=u[:-1]
    if u[0]=="*":
        u=u[1:]
    return u
def get_key(elem,dictio):
    for key, value in dictio.items():
        if elem in value:
            return value.index(elem),key
    return "key doesn't exist"
def graph_from_list(G):
    Q=nx.DiGraph()
    Q.add_nodes_from((vertex(G)))
    Q.add_edges_from(G)
    return Q
def vertex(P):
    V=[]
    for e in P:
        for v in e:
            if v not in V:
                V.append(v)
    return V
def mltdegmon(l):
    s=""
    flat=[i for s in l for i in s]
    flat.sort()
    starting=True
    for i in flat:
        if starting:
            s=s+"x"+str(i)
            starting=False
        else:
            s=s+"*x"+str(i)
    return s
def mltdegtex(t):
    s="$"
    s=s+t
    s=s.replace("x","x_")
    s=s.replace("*","")
    s=s+"$"
    return s
def separate(l):
    l.append(l[len(l)-1]+2)
    sep=[]
    starter=0
    for i in range(len(l)):
        if l[i]>l[i-1]+1:
            m=l[starter:i]
            sep.append(m)
            starter=i
    return sep        
def basis_removal(l):
    q=[]
    for v in l:
        if len(v)%3==1:
            for i in v:
                cont=[]
                w=v.copy()
                if v.index(i)%3==0:
                    w.remove(i)
                    cont=cont+separate(w)
                    for s in l:
                        if s!=v:
                            cont.append(s)
                    q.append(cont)
        if len(v)%3==0:
            for i in v:
                cont=[]
                w=v.copy()
                if v.index(i)%3!=1:
                    w.remove(i)
                    cont=cont+separate(w)
                    for s in l:
                        if s!=v:
                            cont.append(s)
                    q.append(cont)
        if len(v)%3==2 and len(v)>2:
            for i in v:
                cont=[]
                w=v.copy()
                if v.index(i)%3==2:
                    w.remove(i)
                    cont=cont+separate(w)
                    for s in l:
                        if s!=v:
                            cont.append(s)
                    q.append(cont)
            for i in v:
                for j in v:
                    if v.index(j)>v.index(i) and v.index(i)%3==0 and v.index(j)%3==1:
                        cont=[]
                        w=v.copy()
                        w.remove(i)
                        w.remove(j)
                        cont=cont+separate(w)
                        for s in l:
                            if s!=v:
                                cont.append(s)
                        q.append(cont)
        if len(v)==2:
            cont=[]
            for s in l:
                if s!=v:
                    cont.append(s)
            q.append(cont)
    return q
def basis_graph(n):
    pd=n
    basis={}
    if n%3==0:
        pd=2*(n//3)
        basis={pd:[[list(range(1,n+1))]]}
    if n%3==1:
        pd=2*(n//3)+1
        basis={}
    if n%3==2:
            pd=2*(n//3+1)-1
            basis={pd:[[list(range(1,n+1))]]}
    hd=pd-1
    l=[[list(range(1,n+1))]]
    while hd>0:
        m=[]
        for v in l:
            q=basis_removal(v)
            for a in q:
                a.sort()
                if a not in m:
                    m.append(a)
        basis[hd]=m
        l=m.copy()
        hd+=-1
    return basis
def images(dic,V):
    imag={}
    for d in V:
        cod=[]
        deg=[]
        if len(d)>5:
            for e in dic:
                if d==e[1]:
                    cod.append(e[0])
                    deg.append(dic[e])
            imag[d]=[cod,deg]
    return imag
def transpose(list_of_lists):
    array = np.array(list_of_lists)
    transposed_array = array.T
    transposed_list_of_lists = transposed_array.tolist()
    return transposed_list_of_lists
def to_dict_of_lists(dic):
    p=len(dic)
    leng={}
    heig={}
    matdic={}
    for d in dic:
        leng[d]=len(dic[d])
        heig[d]=len(dic[d]['0'])
    for d in dic:
        matd=[]
        for e in dic[d]:
            matde=list(dic[d][e].values())
            matd.append(matde)
        matdic[d]=transpose(matd)
    return matdic
def Macscript(n):
    s1="k=QQ"
    s2="S=k["
    for i in range(1,n):
        s2+="x"+str(i)+","
    s2+="x"+str(n)+"]"
    s3="I=ideal("
    for i in range(1,n-1):
        s3+="x"+str(i)+"*"+"x"+str(i+1)+","
    s3+="x"+str(n-1)+"*"+"x"+str(n)+")"
    s4="d=(res I).dd"
    return s1+"\n"+s2+"\n"+s3+"\n"+s4
n=7
with open("script.m","w") as scr:
    with open("Outputter.txt") as Outputter:
        scr.write(Macscript(n)+"\n")
        s=Outputter.read()
        scr.write(s)
        scr.close()
os.system('cmd /k "wsl M2 script.m')
ubundir=(os.getcwd().replace("\\","/").replace("C:","/mnt/c"))
os.system('cmd /k "cd"')
with open("output.json","r+") as f:
    data=json.load(f)
    f.seek(0)
    json.dump(data,f,indent=4,sort_keys=True)
data={}
with open("output.json","r+") as f:
    data=json.load(f)
G=basis_graph(n)
Md={}
for f in G:
    A=G[f]
    Md[f]=[mltdegmon(a) for a in A]    
Vertex=[]
for f in G:
    for a in Md[f]:
        Vertex.append(a)
Edges=[]
for s in Vertex:
    for t in Vertex:
        if s!=t and contains_vars(t,s) and get_key(t,Md)[1]==get_key(s,Md)[1]-1:
            Edges.append((t,s))
Poset=graph_from_list(Edges)
pos = {}
for m in Vertex:
    ind=get_key(m,Md)
    ind=[ind[0]-len(G[ind[1]])/2,ind[1]]
    pos[m]=ind
labels={}
homd=homdeg(Poset)
signed_matrices=to_dict_of_lists(data)
del signed_matrices['1']
signs={}
Im=images(homd,Poset.nodes)
for m in Im:
    signs[m]={}
for h in signed_matrices:
    for m in Md[int(h)]:
        for col in signed_matrices[h]:
            if equal_up_to_sign(Im[m][1],col):
                for i in range(len(Im[m][1])):
                    if "-"+Im[m][1][i] in col:
                        Poset.remove_edge(Im[m][0][i],m)
                        Poset.add_edge(m,Im[m][0][i])

root = tkinter.Tk()
root.wm_title("Poset")
nx.draw_networkx(Poset,pos,labels={n: n for n in Poset},node_color="#FFFFFF",edge_color="blue",font_size=8)
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)
entry = ttk.Entry()
entry.pack(side=tkinter.LEFT)
entry2 = ttk.Entry()
entry2.pack(side=tkinter.RIGHT)
def changesign(s):
    Q=Poset.copy()
    for e in Q.edges:
        if s in e:
            Poset.remove_edge(e[0],e[1])
            Poset.add_edge(e[1],e[0])

def key_pressed(event):
    w=Label(root,text="Key Pressed:"+event.char)
    w.place(x=70,y=90)
    if event.char=="c":
        print("Changing sign of: ",entry.get())
        changesign(entry.get())
        plt.clf()
        nx.draw_networkx(Poset,pos,labels={n: n for n in Poset},node_color="#FFFFFF",edge_color="blue",font_size=8)
root.bind("<Key>",key_pressed)
if keyboard.is_pressed('b'):
    print('b Key was pressed')
tkinter.mainloop()
if keyboard.is_pressed('b'):
    print('b Key was pressed')
