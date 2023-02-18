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
import joblib

def join_csv():
    df=pd.DataFrame()
    for i in os.listdir('Extraction_folder\\blessures'):
        a=pd.read_csv('Extraction_folder\\blessures\\{}'.format(i),sep=",")
        a=pd.DataFrame(a)
        df=pd.concat([df,a],axis=0,sort=False)
    return df 
 

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np




def preprocess_(df):
    df=join_csv()
    df=test_new_injury_and_replace(df) #compare les blessures du nouveau dataframe à celui existant et remplace en français
    df=df.drop_duplicates()
    df=supprimer_NA_nb_Jours(df)#67000 à 60000
    nouvelle_blessure(df)
    df.reset_index(drop=True,inplace=True)
    df=convert_en_date(df)
    df=nb_jours(df)
    df['Modul_Jours']=round(df['Jours']/10,0)
    df['Modul_Jours_high']=round(df['Jours']/50,0)
    try:
        df.drop('Unnamed: 0',axis=1,inplace=True)
    except:
        print(' ')
    df=df.drop(index=df[df['Jours']>800].index)
    df=df[df['Jours']>0]  #60000
    df=mois_année_pour_groupby(df)
    df['Mois_Année']=df['Mois_Année'].astype(str)
    df=df.drop_duplicates() #38561 =perte de 22 000 lignesune fois que la date de fin NA soit enlevée
    df=df.drop_duplicates(['ID_Player','Start']) #jusqu'ici tout va bien pour Tamas
    df=drop_duplicates_module(df) #32477 une fois qu'on supprime les blessures à un jour d'intervalle
    df.reset_index(drop=True,inplace=True)
    df=df.drop_duplicates(['Saison','ID_Player','Jours','Type'])
    df=nb_blessures(df)
    df=rang_blessure(df)
    df=nb_blessures_non_grave(df)
    df=nb_blessures_grave(df)
    df=nb_blessures_moyenne(df)
    df=nb_blessures_mog(df)
    df=nbjours_blessé_3cat(df)
    df=date_premiere_blessure(df)
    df=blessure_plus_importante(df)
    df=ecart_jours_premiere_blessure(df) #JUSQUE LA 
    df=tri_valeur_blessures_abberantes(df)
    df=age_blessure(df)
    df.Team = [col.replace("\n,", "") for col in df.Team]
    df=df.drop(['Mois_Année','rang_blessure','Modul_Jours','Nombres_blessures_non_grave',
       'Nombres_blessures_grave', 'Nombres_blessures_moyenne','nbjours_blessé_grave',
       'nbjours_blessé_non_grave', 'nbjours_blessé_moyen','Modul_Jours_high',
       'Date_premiere_blessure', 'date_du_jour','Nombres_blessures_mog','Blessure_plus_importante','écart_première_blessure','Nombres_blessures','End_2','Start_2'],axis=1)
    df=df.reindex(columns=['ID_Player','Name','birth_date','Team','Saison','Type','Start','End'])
    df.reset_index(drop=True,inplace=True)
    return df
    

def nouvelle_blessure(df):
    liste_blessures=pd.read_csv('Extraction_folder\liste_blessures.csv',sep=',')
    if len(df['Type'].unique())<=len(liste_blessures['FR']):
        print('rien à signaler')
    else:
        print('nouvelle blessure recensée:il faut modifier la liste') 

def blessure_plus_importante(df):
    df['Blessure_plus_importante']=[max(df['Jours'][df['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    return df

def date_premiere_blessure(df):
    df['Date_premiere_blessure']=[min(df['Start_2'][df['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    return df

def nb_blessures(df):
    df['Nombres_blessures']=0
    df['Nombres_blessures']=[len(df[df['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    return df

def nb_blessures_non_grave(df):
    df_ng=df[df['Jours']<20]
    df['Nombres_blessures_non_grave']=[len(df_ng[df_ng['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    return df

def nb_blessures_grave(df):
    #df['Nombres_blessures_non_grave']=0
    df_bis=df[df['Jours']>100]
    df['Nombres_blessures_grave']=[len(df_bis[df_bis['ID_Player']==df['ID_Player'][i]]) for i in df.index]
    return df
 

def nb_blessures_moyenne(df):
    df['Nombres_blessures_moyenne']=[df['Nombres_blessures'][i]-df['Nombres_blessures_grave'][i]-df['Nombres_blessures_non_grave'][i] for i in df.index]
    return df

def nb_blessures_mog(df):
    df['Nombres_blessures_mog']=df['Nombres_blessures']-df['Nombres_blessures_non_grave']
    return df

def supprimer_NA_nb_Jours(df):
    #Supprimer les NA sur End pour pouvoir calculer nb_Jours
    df=df[np.logical_not(df['End'].isna())]
    return df

def ecart_jours_premiere_blessure(df):
    df['date_du_jour']=datetime.now()
    for i in df.index:
        df.loc[i,'écart_première_blessure']=(df.loc[i,'date_du_jour']-df.loc[i,'Date_premiere_blessure']).days
    return df

def convert_en_date(df):
    df['End_2']=df['End'].astype('datetime64[ns]')
    df['Start_2']=df['Start'].astype('datetime64[ns]')
    df['birth_date_2']=df['birth_date'].astype('datetime64[ns]')
    return df

def age_blessure(df):
    df['Age_Blessure']=0
    df['Age_Blessure']=[int(((df['Start_2'][i]-df['birth_date_2'][i]).days)/365) for i in df.index]
    return df

def nb_jours(df):
    df['Jours']=(df['End_2']-df['Start_2'])
    df['Jours']=[df['Jours'][i].days for i in df.index]
    return df

def mois_année_pour_groupby(df):
    df['Mois_Année']=[[int(df['Start_2'][1].day/10),df['Start_2'][i].month, df['Start_2'][i].year]  for i in df.index]
    return df

def liste_blessures_graves(df):
#Regrouper les blessures graves:
    df_bg=df.groupby(['Type']).Jours.agg("mean").sort_values()
    df_bg=df_bg[df_bg>90]
    df_bg=pd.DataFrame(df_bg)
    liste_bg=df_bg.iloc[0:,:0]#récupère les noms seulementage_s après groupby
    return (liste_bg.index)

def liste_blessures_non_graves(df):
#Regrouper les blessures non graves
    df_bng=df.groupby(['Type']).Jours.agg("mean").sort_values()
    df_bng=df_bng[df_bng<20]
    df_bng=pd.DataFrame(df_bng)
    liste_bng=df_bng.iloc[0:,:0]#récupère les noms seulements après groupb
    return(liste_bng.index)

def drop_duplicates_module(df):
    df_sup=df[df['Jours']>200]
    df_moins=df[df['Jours']<=200]
    df_sup=df_sup.drop_duplicates(['ID_Player','Type','Modul_Jours_high','Mois_Année'])
    df_moins=df_moins.drop_duplicates(['ID_Player','Type','Mois_Année'])
    df=pd.concat([df_moins,df_sup],axis=0)
    return df

def tri_valeur_blessures_abberantes(df):
    df_tb=df
    #print('Taille initiale ',len(df_tb))
    cpt=0
    liste_bg=liste_blessures_graves(df)
    for i in df_tb.index:
        if df_tb['Type'][i] in liste_bg and df_tb['Jours'][i]<50:
            df_tb=df_tb.drop(index=i)
            cpt=cpt+1
    print(cpt)
    liste_bng=liste_blessures_non_graves(df)
    for i in df_tb.index:
        if df_tb['Type'][i] in liste_bng and df_tb['Jours'][i]>30:
            df_tb=df_tb.drop(index=i)
            cpt=cpt+1
    #print(cpt)
    #print("taille finale",len(df_tb))
    return df_tb

def rang_blessure(df):
    df['rang_blessure']=0
    df['rang_blessure']=[0 if df.loc[i,'Jours']<=7 else 1 if (df.loc[i,'Jours']<=21)&(df.loc[i,'Jours']>7) else 2 if (df.loc[i,'Jours']>21) else 0 for i in df.index]
    return df

def nbjours_blessé_3cat(df):
    df['nbjours_blessé_grave']=0
    df['nbjours_blessé_non_grave']=0
    df['nbjours_blessé_moyen']=0
    df['nbjours_blessé_grave']= [sum(df['Jours'][(df['rang_blessure']==2)&(df['ID_Player']==df.loc[i,'ID_Player'])]) for i in df.index]
    df['nbjours_blessé_non_grave']=[ sum(df['Jours'][(df['rang_blessure']==0)&(df['ID_Player']==df.loc[i,'ID_Player'])]) for i in df.index]
    df['nbjours_blessé_moyen']= [sum(df['Jours'][(df['rang_blessure']==1)&(df['ID_Player']==df.loc[i,'ID_Player'])]) for i in df.index]
    return df

def test_new_injury_and_replace(df):
    liste_bl=pd.read_csv('Extraction_folder\\liste_blessures.csv',sep=',')
    liste_bl_comp=np.array(liste_bl['A'])
    print(liste_bl_comp)
    print(df)
    liste_base=df['Type'].unique()
    list_difference = []
    for i in liste_base:
        if i not in liste_bl_comp:
            list_difference.append(i)
    if len(list_difference)>0:
        print('éléments nouveaux:',list_difference,len(list_difference))
    else:
        print('Pas de nouvelle blessure trouvée')
    for i,j in zip(liste_bl['A'],liste_bl['FR']):
        df['Type']=df['Type'].replace(i,j)
    return df

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
    if os.path.exists("Extraction_folder\\blessures")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\blessures", exist_ok=False)
    df=pd.DataFrame()                                
    df=preprocess_(df)
    if os.path.exists("Extraction_folder\\Agrégé_retraité\\blessures_agrégés")==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\Agrégé_retraité\\blessures_agrégés", exist_ok=False)
    df.to_csv("Extraction_folder\\Agrégé_retraité\\blessures_agrégés\\"+'blessures_'+str(today)+'_agrege'+dict_of_format[format_number],index=False)
    print("Le processus est terminé !!")