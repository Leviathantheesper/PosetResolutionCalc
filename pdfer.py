# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 02:45:51 2023

@author: dcmol
"""
import os
import methods as mt
import res_calculator as rc
from network2tikz import plot
def plot_res(bettiposet):
    pos={}
    for m in bettiposet.poset.nodes:
        G=bettiposet.levels()
        ind=mt.get_key(m,G)
        ind=[(ind[0]-len(G[ind[1]])/2),1.5*ind[1]]
        pos[m]=ind
    style = {}
    style['node_label'] = mt.path_notation(bettiposet)
    style['node_style'] = {m: "{draw=none}" for m in bettiposet.graph}
    style['node_opacity'] = 0.0
    style['node_size'] = 1.3
    style['node_pseudo'] = True
    visual_style={}
    visual_style['canvas'] = (30,30)
    visual_style['edge_width']=0.5
    plot(bettiposet.poset,'network1.tex',layout=pos,**style,**visual_style)
    plot(bettiposet.resolution(),'network2.tex',layout=pos,**style,**visual_style)
    os.system("pdflatex network1.tex")
    os.system("pdflatex network2.tex")
plot_res(rc.BettiPoset(8))