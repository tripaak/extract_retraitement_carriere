# coding=utf-8
from datetime import datetime
from os import listdir
from os.path import isfile, join
 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import sys
from scrapy.cmdline import execute
from datetime import date
import os


today = date.today()
def join_csv():
    df=pd.DataFrame()
    for i in os.listdir('Extraction_folder\\selections'):
        # print(i)
        a=pd.read_csv('Extraction_folder\\selections\\{}'.format(i),sep=",")
        a=pd.DataFrame(a)
        df=pd.concat([df,a],axis=0)
    # print(df)    
    return df


def gen_argv(s):
    sys.argv = s.split()

dict_of_version={'key':None}

if __name__ == '__main__':
    dict_of_format = {"1":".csv","2":".json","3":".jsonlines","4":".jl","5":".xml","6":".marshal","7":".pickle"}
    print("Module d\'extraction des données qualitatives\n\n")
    print("Estimation du temps : 25 min. \n")
    print("Choix du format du fichier de sortie : \n")
    print(" 1 - .csv  \n")
    print(" 2 - .json  \n")
    print(" 3 - .jsonlines  \n")
    print(" 4 - .jl  \n")
    print(" 5 - .xml  \n")
    print(" 6 - .marshal  \n")
    print(" 7 - .pickle  \n\n")
    format_number = None   
    table_number=None
    while format_number not in ("1","2","3","4","5","6","7"):  #permet de ne pas planter si l'input est différent des valeurs citées
        format_number = input("Entrez le numéro de format et taper sur entrer : ") #format_number récupère l'entrée       
    if os.path.exists("Extraction_folder\\selections")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\selections", exist_ok=False)
    df=pd.DataFrame()
    df=join_csv()
    df.ID_Player=df.ID_Player.astype(str)
    print(df)
    df=df.drop_duplicates() 
    print(df)
                                  
    if os.path.exists("Extraction_folder\\Agrégé_retraité\\selections_agrégés")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\Agrégé_retraité\\selections_agrégés", exist_ok=False)
    df.to_csv("Extraction_folder\\Agrégé_retraité\\selections_agrégés\\"+'selections_'+str(today)+'_agrege'+dict_of_format[format_number],index=False)
    print("Le processus est terminé !!")