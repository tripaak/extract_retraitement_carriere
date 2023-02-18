from datetime import datetime
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import sys

from datetime import date
import os

pd.options.mode.chained_assignment = None


def join_csv():
    df=pd.DataFrame()
    for i in os.listdir('Extraction_folder\\transferts'):
        a=pd.DataFrame()
        a=pd.read_csv('Extraction_folder\\transferts\\{}'.format(i),sep=",")
        df=pd.concat([df,a],axis=0,sort=False)
        print('etape ok')
    return df 
 

def convert_prix(val):      #fonction permettant de convertir au format int les valeurs de transferts
    monnaie=['€ £','€ $','€£','€$','£$','€','$','£']
    for i in monnaie:
        if i in val:
            val=val.split('{}'.format(i))[1]
            #print(i)
            if 'K'in val:
                if '.' in val:
                    val=float(val.split('K')[0])/1000
                else:
                    val=int(val.split('K')[0])/1000

            elif 'k'in val:
                if '.' in val:
                    val=float(val.split('k')[0])/1000
                else:
                    val=int(val.split('k')[0])/1000
                   
            elif 'M' in val:
                try:
                    if '.' in val:
                        val=float(val.split('M')[0])
                    else:
                        val=int(val.split('M')[0])
                except:
                    print(' ')
            return val

def comp_date(date_string_1): #fonction permetant de créer la saison correspondante en fonction de la date
        date_object_1=date_string_1
        date_string_2 = ("Jun 30, {}").format(date_object_1.year)
        date_object_2=datetime.strptime(date_string_2,"%b %d, %Y")
        if (date_object_1<date_object_2):
            return ''.join([str(date_object_2.year-1),"/",str(date_object_2.year)])
            
        else:
            return ''.join([str(date_object_2.year),"/",str(date_object_2.year+1)])

def joueurs_par_saison():
    T_saison=[]
    df_priced=df[np.logical_not(df['Prix_Converti'].isna())]
    for i in df_priced['Saison'].unique():
        T_saison.append([i,len(df_priced[df_priced['Saison']=='{}'.format(i)])])
        return T_saison

def joueurs_par_saison():
    T_saison=[]
    df_priced=df[np.logical_not(df['Prix_Converti'].isna())]
    for i in df_priced['Saison'].unique():
        T_saison.append([i,len(df_priced[df_priced['Saison']=='{}'.format(i)])])
    return T_saison

def remplace_erreur(df):
    remplace_=pd.read_csv('Extraction_folder\\remplace.csv',sep=',')
    remplace_['Prix']=remplace_['Prix'].astype(str)
    remplace_['ID']=remplace_['ID'].astype(str)
    remplace_['Nature'][np.logical_not(remplace_['Prix_Converti'].isna())]='transfert payant'
    remplace_['Nature']=remplace_['Nature'].astype(str)
    remplace_['Date_2']=pd.to_datetime(remplace_['Date'],format='%b %d, %Y')
    df=pd.concat([df,remplace_],axis=0,sort=False)
    df.reset_index(drop=True,inplace=True)
    df.drop_duplicates(['ID','Name','From','To','Date','Prix','Saison'],keep='last',inplace=True)
    return df

def ajuster_valeurs(df):
    df['Prix_Converti']=df['Prix_Converti'].astype(str)
    for i in df.index:
        if len(df.loc[i,'Prix_Converti'])>7:
            df.loc[i,'Prix_Converti']=df.loc[i,'Prix_Converti'][0:5]
    return df

def remplace_na(df):
    df['Prix_Converti'][df['Prix_Converti']=='None']='-'
    df['Prix_Converti'][df['Prix_Converti'].str.contains('N/A')]='-'
    df['Prix_Converti'][df['Prix_Converti'].str.contains('n/a')]='-'
    return df 

def supprimer_na_colonnes(df):
    df=df[np.logical_not(df['To'].isna()&df['Prix'].isna())]
    df=df[np.logical_not(df['From'].isna()&df['Prix'].isna())] #152800
    df=df[np.logical_not(df['To'].isna()&df['From'].isna()&df['Prix_Converti'].isna())]
    return df

def nature(df):
    df['Nature']=['transfert libre' if df['Prix'][i]=='free' else 'prêt' if (df['Prix'][i]=='loan') else 'nc' for i in df.index]
    df['Nature'][np.logical_not(df['Prix_Converti'].isna())]='transfert payant'
    df['Nature']=df['Nature'].astype(str)
    df['Prix_Converti']=df['Prix_Converti'].astype(str)
    return df
def retour_pret(df):
    for i in range(len(df.index)-1):
        if (df['From'][i]==df['To'][i+1])&((df['To'][i]==df['From'][i+1]))&(df['Prix'][i]=='loan'):
            df['Nature'][i+1]='retour de prêt'
    return df
def keep_date(df):
    for i in df.index:  
        if (df['Mois_Année'][i][1]>datetime.today().year+1)|(df['Date_2'][i]>datetime.today()):
            df=df.drop(index=i)
    return df

def preprocess_(df):
    print('début process')
    df=pd.DataFrame()
    df=join_csv()
    df=df.reset_index(drop=True)
    df.drop(index=df[df['ID']=='ID'].index,inplace=True)
    df=df.drop_duplicates() #363000
    df['ID_From']=[df['ID_From'].loc[i].split("/")[2] if type(df['ID_From'].loc[i])==str else df['ID_From'].loc[i] for i in df.index]
    df['ID_To']=[df['ID_To'].loc[i].split("/")[2] if type(df['ID_To'].loc[i])==str else df['ID_To'].loc[i] for i in df.index]
    df=df.reindex(columns=['ID','BirthDate','Name','From','ID_From','ID_To','To','Date','Prix','Prix_Converti','Nature'])
    df['ID']=df['ID'].astype(str)
    df.drop_duplicates(['ID','From','To','Date','Prix'],inplace=True)#217000 sans Name convert
    df['Date_2']=pd.to_datetime(df['Date'],format='%b %d, %Y')
    df=df.sort_values(by='Date_2',ascending=False)
    df['Saison']=[comp_date(df["Date_2"][i]) for i in df.index]
    df=df[np.logical_not(df['To'].isna()&df['Prix'].isna())]
    df=df[np.logical_not(df['From'].isna()&df['Prix'].isna())] #152800
    df=df[np.logical_not(df['To'].isna()&df['From'].isna()&df['Prix_Converti'].isna())]
    df['Mois_Année']=[(df['Date_2'][i].month,df['Date_2'][i].year) for i in df.index]
    df.drop_duplicates(['From','To','Mois_Année','Prix','ID'],inplace=True)#152200 , 
    df['Prix']=df['Prix'].astype(str)
    df['Prix_Converti']=[convert_prix(df.loc[i,'Prix']) for i in df.index]
    df.reset_index(drop=True,inplace=True)
    for i in df.index:  
        if (df['Mois_Année'][i][1]>datetime.today().year+1)|(df['Date_2'][i]>datetime.today()):
            df=df.drop(index=i)
    df['Nature']=['transfert libre' if df['Prix'][i]=='free' else 'prêt' if (df['Prix'][i]=='loan') else 'nc' for i in df.index]
    df['Nature'][np.logical_not(df['Prix_Converti'].isna())]='transfert payant'
    df['Nature']=df['Nature'].astype(str)
    df['Prix_Converti']=df['Prix_Converti'].astype(str)
    df.sort_values(by=['ID','Date_2'],inplace=True)
    df.reset_index(drop=True,inplace=True)
    #print('moitié')
    df_t=pd.DataFrame()
    df_t['Nature']=['retour de prêt' if (df['From'][i-1]==df['To'][i])&((df['To'][i-1]==df['From'][i]))&(df['Prix'][i-1]=='loan') else df['Nature'][i] for i in range(1,len(df.index)-1)]
    df_t2=pd.DataFrame()
    df_t2['Nature']=0
    df_t2['Nature'].loc[0]=df['Nature'].loc[0]
    df_t=pd.concat([df_t2['Nature'],df_t['Nature']],axis=0,sort=False)
    df_t.loc[len(df.index)-1]=df['Nature'].loc[len(df.index)-1]
    df_t.reset_index(drop=True,inplace=True)
    df['Nature']=df_t
    df=remplace_erreur(df)
    df=df.sort_values(by='Date_2',ascending=False)
    df['Prix_Converti']=df['Prix_Converti'].astype(str)
    for i in df.index:
        if len(df.loc[i,'Prix_Converti'])>7:
            df.loc[i,'Prix_Converti']=df.loc[i,'Prix_Converti'][0:5]
    df=df.reindex(columns=['ID','BirthDate','Name','ID_From','ID_To','From','To','Date','Prix','Saison','Prix_Converti','Nature'])
    df['Prix_Converti'][df['Prix_Converti']=='None']='-'
    df['Prix_Converti'][df['Prix_Converti'].str.contains('N/A')]='-'
    df['Prix_Converti'][df['Prix_Converti'].str.contains('n/a')]='-'
    
    df2=df.reindex(columns=['ID','BirthDate','Name','ID_From','ID_To','From','To','Date','Prix','Saison','Prix_Converti','Nature'])
    df=df.reindex(columns=['ID','BirthDate','Name','From','To','Date','Prix','Saison','Prix_Converti','Nature'])
    return df,df2



today = date.today()


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
    if os.path.exists("Extraction_folder\\transferts")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\transferts", exist_ok=False)
    df=pd.DataFrame()                                
    df,df2=preprocess_(df)
    if os.path.exists("Extraction_folder\\Agrégé_retraité\\transferts_agrégé_retraités")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\Agrégé_retraité\\transferts_agrégé_retraités", exist_ok=False)
    df.to_csv("Extraction_folder\\Agrégé_retraité\\transferts_agrégé_retraités\\"+'transferts_'+str(today)+'_agrege'+dict_of_format[format_number],index=False)
    df2.to_csv("Extraction_folder\\Agrégé_retraité\\transferts_agrégé_retraités\\"+'transferts_avec_ID_'+str(today)+'_agrege'+dict_of_format[format_number],index=False)
    print("Le processus est terminé !!")