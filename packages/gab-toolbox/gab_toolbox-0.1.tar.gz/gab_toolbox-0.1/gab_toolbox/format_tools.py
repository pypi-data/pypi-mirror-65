# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:06:43 2020

@author: gabri
"""


def valid_title(title,char='_'):
    new_title = title.copy()
    banned_chars = ["/","*","<",">",":","?","|",'"','\\']
    
    for j in banned_chars:
        new_title = new_title.replace(j,char)
    
    return new_title

def import_file(file):
    with open(file,'r') as f:
        txt = [n[:-1] for n in f]
    return txt

def write_file(array,file):
    with open(file,'w') as f:
        for i in array:
            f.writelines(f'{i}\n')
    return None

def dic2arr(dictionary, order=0,sort=0,rev=0):
    if order:
        array = [[dictionary[i],i] for i in dictionary]
    else:
        array = [[i,dictionary[i]] for i in dictionary]
    if sort:
        array = sorted(sort,reverse=rev)
        
    return array


def arr2dic(array, sort=0,rev=0,overwrite=0):
    
    if sort:
        sorted_array = sorted(array,reverse=rev)
        
    if overwrite:
        if sort:
            dic= dict(sorted_array) 
        else:
            dic = dict(array)
    else:
        dic = dict()
        
        def loop(a):
            
            for i in a:
                key = i[0]
                value = i[1]
                if key in dic:
                    dic[key].append(value)
                else:
                    dic[key] = [value]
            return dic
            
        if sort:
           dic = loop(sorted_array)
            
        else:
           dic = loop(array)
		   
    return dic