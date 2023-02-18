import sys
from scrapy.cmdline import execute
from datetime import date
import os
import joblib

today = date.today()

def gen_argv(s):
    sys.argv = s.split()

dict_of_version={'key':None}

if __name__ == '__main__':
    dict_of_format = {"1":".csv","2":".json","3":".jsonlines","4":".jl","5":".xml","6":".marshal","7":".pickle"}
    dict_of_choice = {"1":"transferts","2":"blessures","3":"selections","4":"equipes","5":"suspensions","6":"stats_quali"}
    #nb_Extract=int(input("Nombre de dates à extraire"))
    #dict_of_version={"1":"","2":"","3":"","4":"","5":""}
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
        print("Choix de la table voulue : \n")
        print(" 1 - transfert  \n")
        print(" 2 - blessures  \n")
        print(" 3 - selection  \n") 
        print(" 4 - equipes  \n") 
        print(" 5 - suspensions \n")
        print(" 6 - stats_quali \n")

        while table_number not in("1","2","3","4","5","6"):  #permet de ne pas planter si l'input est différent des valeurs citées
            table_number = input("Choix de la table voulue : \n")#table_number récupère l'entrée
            while isinstance(dict_of_version["key"],int) is False:
                print('Entrer code date')
                try :
                    dict_of_version['key']=int(input())
                except:
                    print('Saisie invalide')
    joblib.dump(dict_of_version,"fifa20\\spiders\\date.pkl")
    if os.path.exists("Extraction_folder\\{}".format(dict_of_choice[table_number]))==False: #permet de ne pas recréer le dossier s'il existe
        os.makedirs("Extraction_folder\\{}".format(dict_of_choice[table_number]), exist_ok=False)
    #print("scrapy crawl {} -o ".format(dict_of_choice[table_number]) +"Extraction_folder\\{}\\".format(dict_of_choice[table_number])+'{}_'.format(dict_of_choice[table_number])+str(today)+dict_of_format[format_number])
    gen_argv("scrapy crawl {} -o ".format(dict_of_choice[table_number]) +"Extraction_folder\\{}\\".format(dict_of_choice[table_number])+'{}_'.format(dict_of_choice[table_number])+str(today)+'_{}'.format(dict_of_version["key"])+dict_of_format[format_number])
    execute()  #on créer donc le fichier correspondant avec _date et l'emplacement qui va avec --> print en commentaire permet de voir ce qui est généré
                                    
