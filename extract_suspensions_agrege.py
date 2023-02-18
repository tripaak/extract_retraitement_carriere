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
    for i in os.listdir('Extraction_folder\\suspensions'):
        a=pd.read_csv('Extraction_folder\\suspensions\\{}'.format(i),sep=",")
        a=pd.DataFrame(a)
        df=pd.concat([df,a],axis=0)
    return df

def preprocess_(df):
    df=join_csv() 
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True,drop=True) 
    df['Nb_Suspensions']=[len(df[df['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    df['Start_2']=df['Start'].astype('datetime64[ns]')
    df['End_2']=df['End'].astype('datetime64[ns]')
    df['Jour_2']=[(df['End_2'][i]-df['Start_2'][i]).days+1 for i in df.index]
    df['Modul_Date']=[(int(df['Start_2'][i].day/10),df['Start_2'][i].month,df['Start_2'][i].year) for i in df.index]
    df.drop_duplicates(['ID_Player','Start','End'],inplace=True)
    df.drop_duplicates(['ID_Player','Jours','Modul_Date'],inplace=True)
    df['Jours']=df['Jour_2']
    #df.drop(['Nb_Suspensions','Start_2','Modul_Date','Jour_2','End_2'],axis=1,inplace= True)
    df.sort_values(by='Start',ascending=False,inplace=True) 
    for i in df[df['End'].isna()].index:
        df.drop(index=i,inplace=True)
    df.Jours=df.Jours.astype(int)
    df.sort_values(by='Start_2',ascending=False,inplace=True) 
    df=df.reindex(columns=['ID_Player','Name','birth_date','Team','Saison','Type','Start','End','Jours'])
    df.reset_index(drop=True,inplace=True)
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
    if os.path.exists("Extraction_folder\\suspensions")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\suspensions", exist_ok=False)
    df=pd.DataFrame()                                
    df=preprocess_(df)
    if os.path.exists("Extraction_folder\\Agrégé_retraité\\suspensions_agrégés")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\Agrégé_retraité\\suspensions_agrégés", exist_ok=False)
    df.to_csv("Extraction_folder\\Agrégé_retraité\\suspensions_agrégés\\"+'suspensions_'+str(today)+'_agrege'+dict_of_format[format_number],index=False)
    print("Le processus est terminé !!")