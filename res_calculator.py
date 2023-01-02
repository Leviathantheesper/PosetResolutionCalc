# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 01:34:22 2022

@author: dcmol
"""
import numpy as np
import methods as mt
def list_inter(l1,l2):
    inter=set()
    for a in l1:
        if a in l2:
            inter.add(a)
    return inter
class BettiPoset:
    def __init__(self,n):
        G=mt.basis_graph(n)
        Md={}
        for f in G:
            A=G[f]
            Md[f]=[mt.mltdegmon(a) for a in A]
        Vertex=[]
        for f in G:
            for a in Md[f]:
                Vertex.append(a)
        Edges=[]
        for s in Vertex:
            for t in Vertex:
                if s!=t and mt.contains_vars(t,s) and mt.get_key(t,Md)[1]==mt.get_key(s,Md)[1]-1:
                    Edges.append((t,s))
        Poset=mt.graph_from_list(Edges)
        self.poset=Poset
        self.nodes=self.poset.nodes
        self.edges=self.poset.edges
        self.graph=G
        self.n=n
    def levels(self):
        nodes=self.nodes
        edges=self.poset.edges
        leveler={}
        leveler[1]=[]
        for node in nodes:
            starter=True
            for edge in edges:
                if node==edge[1]:
                    starter=False
            if starter:
                leveler[1].append(node)
        level=2
        loop=True
        while True:
            levelcur=[]
            for node in leveler[level-1]:
                preim=self.preimages(node)
                if preim==[]:
                    loop=False
                    break
                levelcur+=preim
            if not loop:
                break
            leveler[level]=list(set(levelcur))
            level+=1
        return leveler
    def images(self,node):
        im=[]
        for edge in self.poset.edges:
            if node==edge[1] and edge[0] not in im:
                im.append(edge[0])
        return im
    def second(self,node):
        sec=[]
        for node2 in self.images(node):
            for node3 in self.images(node2):
                if node3 not in sec:
                    sec.append(node3)
        return sec
    def preimages(self,node):
        preim=[]
        for edge in self.poset.edges:
            if node==edge[0] and edge[1] not in preim:
                preim.append(edge[1])
        return preim
    def diamonds(self):
        diams=[]
        for node in self.poset.nodes:
            bottoms=self.second(node)
            for node2 in bottoms:
                diam={}
                middle=list_inter(self.images(node),self.preimages(node2))
                diam["bottom"]=node2
                diam["middle"]=middle
                diam["top"]=node
                diams.append(diam)
        return diams
    def isdisbalanced(self):
        bdiams=[]
        diams=self.diamonds()
        for diam in diams:
            top=diam["top"]
            middle=diam["middle"]
            bottom=diam["bottom"]
            topsigns=[]
            bottomsigns=[]
            for node in list(middle):
                topsigns.append(self.signs()[top][node])
                bottomsigns.append(self.signs()[node][bottom])
            if np.prod(topsigns)==np.prod(bottomsigns):
                bdiams.append(diam)
            if len(bdiams)==0:
                return True
            if len(bdiams)>0:
                return False,bdiams,topsigns,bottomsigns
    def signs(self):
        signs={}
        types={}
        pst=self.poset
        for node in pst.nodes():
            sign=1
            if len(mt.da_index(node))>2:
                signs[node]={}
                types[node]={}
            for edge in pst.edges():
                if node==edge[1]:
                    signs[node][edge[0]]=""
                    if len(mt.da_index(node))==len(mt.da_index(edge[0]))+1:
                        types[node][edge[0]]=1
                    if len(mt.da_index(node))==len(mt.da_index(edge[0]))+2:
                        types[node][edge[0]]=2
            for i in mt.da_index(node):
                done=False
                var="x"+str(i)
                rem=mt.remove_vars(var, node)
                if rem in self.images(node):
                    signs[node][rem]=sign
                    done=True
                if len(mt.da_index(node))>2 and set(types[node].values())!={1} and not done:
                    for j in mt.da_index(rem):
                        if j>i:
                            var2="x"+str(j)
                            rem2=mt.remove_vars(var2,rem)
                            if rem2 in self.images(node):
                                signs[node][rem2]=sign
                                done=True
                if done:
                    sign=-sign
        return signs
    def resolution(self):
        res=self.poset.copy()
        edges=res.edges
        for edge in self.edges:
            if self.signs()[edge[1]][edge[0]]==-1:
                res.remove_edge(edge[0],edge[1])
                res.add_edge(edge[1],edge[0])
        return res
