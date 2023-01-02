# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 03:14:43 2023

@author: dcmol
"""
import res_calculator as rc
KIRA=5
while(True):
    a=rc.BettiPoset(KIRA)
    print("Verificado para n=",KIRA,": ",a.isdisbalanced())
    KIRA+=1