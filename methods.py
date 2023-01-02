# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 01:37:16 2022

@author: dcmol
"""


import re
import numpy as np
import networkx as nx
from network2tikz import plot
def montotex(input_monomial):
    """
    Parameters
    ----------
    input_monomial : TYPE
        DESCRIPTION.

    Returns
    -------
    monomial : TYPE
        DESCRIPTION.

    """
    monomial=input_monomial
    located=re.findall(r"x[0-9]+\*",monomial)
    for var in located:
        num=re.search(r"[0-9]+",var).group(0)
        monomial=monomial.replace(var,"x_{"+num+"}")
    located=re.search(r"x[0-9]+",monomial)
    if located:
        var=located.group(0)
        num=re.search(r"[0-9]+",var).group(0)
        monomial=monomial.replace(var,"x_{"+num+"}")
    monomial="$"+monomial+"$"
    return monomial
def homdeg(poset_res):
    """
    Parameters
    ----------
    poset_res : TYPE
        DESCRIPTION.

    Returns
    -------
    dictio : TYPE
        DESCRIPTION.

    """
    edges=poset_res.edges
    dictio={}
    for edge in edges:
        dictio[edge]=remove_vars(edge[0],edge[1])
    return dictio
def samemonomial(unsigned,signed):
    """
    Parameters
    ----------
    unsigned : TYPE
        DESCRIPTION.
    signed : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.
    str
        DESCRIPTION.

    """
    if "-"+unsigned==signed:
        return True,"-"
    if unsigned==signed:
        return True,"+"
    return False,"Not"
def equal_up_to_sign(unsigned_column,signed_column):
    """
    Parameters
    ----------
    unsigned_column : TYPE
        DESCRIPTION.
    signed_column : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
    unsigned_set=set(unsigned_column)
    signed_set=set(signed_column)
    if '0' in signed_set:
        signed_set.remove('0')
    if len(unsigned_set)!=len(signed_set):
        return False
    for stringy in unsigned_set:
        if stringy not in signed_set and "-"+stringy not in signed_set:
            return False
    return True
def da_vars(mon):
    var=[]
    variabs=re.findall(r'x\d+\*', mon)
    for i in variabs:
        i=i.replace("*","")
        var.append(i)
    reg=re.search(r'x\d+$',mon)
    if reg:
        var.append(reg.group(0))
    return var
def da_index(mon):
    ind=[]
    var=da_vars(mon)
    for i in var:
        j=i
        j=j.replace("x","")
        ind.append(int(j))
    return ind
s='x2*x3*x4*x5*x6*x7*x8*x9*x10*x11*x12'
def contains_vars(mon1,mon2):
    """
    Parameters
    ----------
    mon1 : TYPE
        DESCRIPTION.
    mon2 : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
    vars1=da_vars(mon1)
    vars2=da_vars(mon2)
    for var in vars1:
        if var not in vars2:
            return False
    return True

def remove_vars(mon1,mon2):
    """
    Parameters
    ----------
    mon1 : TYPE
        DESCRIPTION.
    mon2 : TYPE
        DESCRIPTION.

    Returns
    -------
    mon2_copy : TYPE
        DESCRIPTION.

    """
    mon2_copy=mon2
    res=re.findall("x[0-9]+",mon1)
    for var in res:
        mon2_copy=mon2_copy.replace(var+"","",1)
    while re.search(r"\*\*", mon2_copy):
        mon2_copy=mon2_copy.replace("**","*")
    if mon2_copy[-1]=="*":
        mon2_copy=mon2_copy[:-1]
    if mon2_copy[0]=="*":
        mon2_copy=mon2_copy[1:]
    return mon2_copy
def get_key(elem,dictio):
    """
    Parameters
    ----------
    elem : TYPE
        DESCRIPTION.
    dictio : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    for key, value in dictio.items():
        if elem in value:
            return value.index(elem),key
    return "key doesn't exist"
def graph_from_list(edge_list):
    """
    Parameters
    ----------
    edge_list : TYPE
        DESCRIPTION.

    Returns
    -------
    digraph : TYPE
        DESCRIPTION.

    """
    digraph=nx.DiGraph()
    digraph.add_nodes_from((vertex(edge_list)))
    digraph.add_edges_from(edge_list)
    return digraph
def vertex(edge_list):
    """


    Parameters
    ----------
    edge_list : TYPE
        DESCRIPTION.

    Returns
    -------
    vertex_list : TYPE
        DESCRIPTION.

    """
    vertex_list=[]
    for edge in edge_list:
        for vert in edge:
            if vert not in vertex_list:
                vertex_list.append(vert)
    return vertex_list
def mltdegmon(vector):
    """
    Transforms a list of lists into a monomial string readable by Macaulay2.
    Parameters
    ----------
    vector : list
        list of lists of integers.

    Returns
    -------
    mon : string
        monomial associated to the list.

    """
    mon=""
    flat=[var for comp in vector for var in comp]
    flat.sort()
    starting=True
    for var in flat:
        if starting:
            mon=mon+"x"+str(var)
            starting=False
        else:
            mon=mon+"*x"+str(var)
    return mon
def separate(vector):
    """
    Separates a list of integers in all the consecutive components, i.e.
    computes the connected components of a path.
    Parameters
    ----------
    vector : list
        vector of integers.

    Returns
    -------
    sep : list
        list of vectors.

    """
    vector.append(vector[len(vector)-1]+2)
    sep=[]
    starter=0
    for i in range(len(vector)):
        if vector[i]>vector[i-1]+1:
            sep_vec=vector[starter:i]
            sep.append(sep_vec)
            starter=i
    return sep
def basis_removal(list_of_vectors):
    """
    removes vertices according to the rules to reduce pd in 1.
    Parameters
    ----------
    list_of_vectors : list
        list of basis graphs of a given pd.
    Returns
    -------
    removed : list
        list of basis graphs with pd minus one.

    """
    removed=[]
    for vect in list_of_vectors:
        if len(vect)%3==1:
            for i in vect:
                cont=[]
                vect_copy=vect.copy()
                if vect.index(i)%3==0:
                    vect_copy.remove(i)
                    cont=cont+separate(vect_copy)
                    for vect2 in list_of_vectors:
                        if vect2!=vect:
                            cont.append(vect2)
                    removed.append(cont)
        if len(vect)%3==0:
            for i in vect:
                cont=[]
                vect_copy=vect.copy()
                if vect.index(i)%3!=1:
                    vect_copy.remove(i)
                    cont=cont+separate(vect_copy)
                    for vect2 in list_of_vectors:
                        if vect2!=vect:
                            cont.append(vect2)
                    removed.append(cont)
        if len(vect)%3==2 and len(vect)>2:
            for i in vect:
                cont=[]
                vect_copy=vect.copy()
                if vect.index(i)%3==2:
                    vect_copy.remove(i)
                    cont=cont+separate(vect_copy)
                    for vect2 in list_of_vectors:
                        if vect2!=vect:
                            cont.append(vect2)
                    removed.append(cont)
            for i in vect:
                for j in vect:
                    if vect.index(j)>vect.index(i) and vect.index(i)%3==0 and vect.index(j)%3==1:
                        cont=[]
                        vect_copy=vect.copy()
                        vect_copy.remove(i)
                        vect_copy.remove(j)
                        cont=cont+separate(vect_copy)
                        for vect2 in list_of_vectors:
                            if vect2!=vect:
                                cont.append(vect2)
                        removed.append(cont)
        if len(vect)==2:
            cont=[]
            for vect2 in list_of_vectors:
                if vect2!=vect:
                    cont.append(vect2)
            removed.append(cont)
    return removed
def basis_graph(number):
    """
    Computes all the basis graphs of a path.
    Parameters
    ----------
    number : int
        Number of vertices.

    Returns
    -------
    basis : list
        list of basis graphs.

    """
    proj_dim=number
    basis={}
    if number%3==0:
        proj_dim=2*(number//3)
        basis={proj_dim:[[list(range(1,number+1))]]}
    if number%3==1:
        proj_dim=2*(number//3)+1
        basis={}
    if number%3==2:
        proj_dim=2*(number//3+1)-1
        basis={proj_dim:[[list(range(1,number+1))]]}
    homol_deg=proj_dim-1
    rang=[[list(range(1,number+1))]]
    while homol_deg>0:
        list_of_vectors=[]
        for lst in rang:
            removed=basis_removal(lst)
            for comps in removed:
                comps.sort()
                if comps not in list_of_vectors:
                    list_of_vectors.append(comps)
        basis[homol_deg]=list_of_vectors
        rang=list_of_vectors.copy()
        homol_deg+=-1
    return basis
def images(dic,free_mod_gens):
    """
    Computes the arrows of a list of monomials in the minfree resolution of a path.
    Parameters
    ----------
    dic : dict
        dictionary of the free resolution.
    free_mod_gens : list
        list of monomials.
    Returns
    -------
    imag : list
        list of monomials.
    """
    imag={}
    for mon in free_mod_gens:
        cod=[]
        deg=[]
        if len(mon)>5:
            for edge in dic:
                if mon==edge[1]:
                    cod.append(edge[0])
                    deg.append(dic[edge])
            imag[mon]=[cod,deg]
    return imag
def transpose(list_of_lists):
    """
    Transposes a matrix.
    Parameters
    ----------
    list_of_lists : list
        Matrix

    Returns
    -------
    transposed_list_of_lists : list
        Transpose matrix.
    """
    array = np.array(list_of_lists)
    transposed_array = array.T
    transposed_list_of_lists = transposed_array.tolist()
    return transposed_list_of_lists
def to_dict_of_lists(dic):
    """
    Transforms the json of the resolution to a dictionary of matrices
    transposing them so that each list in the matrix is a column.
    Parameters
    ----------
    dic : dict
        dictionary containing the differentials as dictionaries.
    Returns
    -------
    matdic : dict
        dictionary containing the matrices as lists of lists.
    """
    leng={}
    heig={}
    matdic={}
    for entry in dic:
        leng[entry]=len(dic[entry])
        heig[entry]=len(dic[entry]['0'])
    for entry in dic:
        matd=[]
        for edge in dic[entry]:
            matde=list(dic[entry][edge].values())
            matd.append(matde)
        matdic[entry]=transpose(matd)
    return matdic
def mac2script(number):
    """
    Generates the Macaulay2 script that computes a free resolution of the edge ideal of a path.
    Parameters
    ----------
    number : int
        the number of vertices.

    Returns
    -------
    string
        Macaulay2 code.

    """
    line1="k=QQ"
    line2="S=k["
    for i in range(1,number):
        line2+="x"+str(i)+","
    line2+="x"+str(number)+"]"
    line3="I=ideal("
    for i in range(1,number-1):
        line3+="x"+str(i)+"*"+"x"+str(i+1)+","
    line3+="x"+str(number-1)+"*"+"x"+str(number)+")"
    line4="d=(res I).dd"
    return line1+"\n"+line2+"\n"+line3+"\n"+line4
def convert_to_path_notation(mon,n):
    notation=""
    ind=da_index(mon)
    sep=separate(ind)
    for r in range(len(sep)):
        c=sep[r]
        if r==0:
            a=c[0]-1
            notation+="."*a
        notation+="P"+str(len(c))
        if r<len(sep)-1:
            last=c[-1]
            i=ind.index(last)
            first=ind[i+1]
            number=first-last-1
            notation+="."*number
        if r==len(sep)-1:
            a=n-c[-1]
            notation+="."*a
    return notation
def path_notation(bettiposet):
    n=bettiposet.n
    nodes=bettiposet.poset.nodes
    dic={}
    for node in nodes:
        dic[node]=convert_to_path_notation(node,n)
    return dic