Synthèse 

Dans le cas ou ce n'est pas le cas la première étape sera d'installer les differents logiciels/packages et environnments 
Dans l'ordre:
1)Installation de Visual Studio 
    Dans VisualStudio installer les extensions : Python
                                                Python Environnement 
                                                
2)Installation d'Anaconda 
3)Installation de Python
Une fois ces installations effectués:
4)Lancer le Prompt d'Anaconda et dans l'ordre effectuer dans le répertoire d'installation du Projet (cd jusqu'au répertoire..)
pip cd...
pip install conda
pip create nom_environnement python=3.7             
(Bien choisir la version 3.7 car avec les versions supérieur il existera des conflits avec la librairie Scrapy)
5)Une fois dans le dossier et l'environnment créer on installe Scrapy:
   pip install scrapy  ou conda install -c conda-forge scrapy
6)Se rendre dans VisualStudio ouvrir le dossier.
7)En bas à droite de la barre bleu sélectionner l'environnement créé précédement
8)Ouvrir le cmd et vérifier qu'on se situe bien dans le dossier et l'environnement correspondant:
Sinon se placer dedans et éventuellement activer l'environnement avec (conda activate nom_environnement)
On vérifie que Scrapy est bien installé avec la commande scrapy
9)On peut désormais créer le projet:
scrapy startproject (nomprojet) 
PS:Bien veiller à ce que l'environnement créé(python 3.7) soit actif à chaque utilisation






Scrapy
La librairie scrapy est utilisée dans le but de récupérer des informations en quantité à partir d'un URL défini 
La première étape consiste donc à installer cette libraire dans l'environnement correspondant
Pour cela on lance le Prompt d'Anaconda et on execute dans le dossier de Scrapping créé : pip install scrappy 
PS: l'environnement d'installation précedent doit être activé pour que tout s'installe correctement 

Une fois scrapy installé et le projet créé il faut définir créer notre spider. 
Le spider est le fichier contenant: -L'URL de la page à parcourir initalement 
                                    - le programme de parcours de la page initial(+ éventuellement des pages suivantes) dans la fonction parse()
C'est ce fichier qui doit être executé pour tester le scrapping (commande: scrapy crawl nom_spider -o nom_fichier.format)(ex : scrapy crawl transferts -o transferts_2022.csv)
Il est possible de créer plusieurs spider différents pour récupérer différents type d'information (commande scrapy ngenspider nom_spider   URL_page )


Types de parcours :
On peut  utiliser deux types de parcours: 
le parcours via le paramètre css ou le xpath. 
Généralement on utilise le chemin css mais si celui ci est compliqué à récupérer on passe par le xpath et inversement
Pour récupérer le chemin correspondant,on utilise Inspecter élément sur la page et on pointe vers l'information cherchée.
Celle-ci est contenue dans des balises imbriquées entre elle. 

Information sur page initiale-Explication de code:

Pour cette partie on se réfère au spider equipes.py car plus clair que les autres :
Dans la fonction parse on  a pour paramètre response qui sert à retourner l'objet requêté.
on détermine une boucle qui parcours toute les lignes du tableau:
Ici boucle for in response.css(//*[@id="body"]/div[1]/div/div[2]/div/table/tbody/tr'):
Généralement le chemin css se finit par /tr lorsque on récupère des lignes. 
En faisant Ctrl+F dans  l'Inspecteur,on peut vérifer que le code correspond bien aux différentes lignes à parcourir.
Ensuite pour chaque colonne,on attribue à notre dictionnaire les valeurs correspondantes avec le lien qui va avec.
On notera que:
.extract() est utilisé pour récupérer du text dans une balise 
.get() est utilisé lorsqu'on récupère un attribut (ex: response.css(....<tr<attr(href).get()) )

Passage à la page suivante: 
En dehors de la boucle,on utilise les lignes de code :

next_page = response.xpath('//span[@class="bp3-button-text" and text()="Next"]/parent::a/@href').get()

        if next_page:
            yield Request(response.urljoin(next_page))

Ainsi si le parcours détecte le bouton suivant,l'Url de la page passe à celui de la page suivant (attribut href)
Le Yield permet de retourner la requête "aller à la page d'URl (next_page)"

Information à récupérer sur un autre lien présent sur la page-Explications:
Si l'on souhaite récupérer une information se trouvant dans un lien,on doit nécessairement effectuer une requête afin 
d'atteindre le lien pour ensuite scraper l'information.
Pour cela on utilise la fonction Request qui a pour paramètres:
Url = lien sur lequel l'information se trouve
callback= fonction dans laquelle on va scraper les nouvelles données
meta= permet de récupérer les objet créé dans la fonction parse initiale dont on a besoin 
Ex: Dans notre spider equipes,on récupère dans notre boucle le lien de l'équipe grâce à son ID,on attribue la fonction parse_pays
dans le callback ,puis on ajoute notre table item(ou dictionnaire) dans meta car on en a besoin pour retourner le pays dans le tableau.


Explication pour les fonctions parse_transferts,parse_blessures et parse_selections:(+ Documentation dans parse_transfert)
Au moment de récupérer ces tableaux,un problème s'est présenté car d'un joueur à l'autre ,la page ne comportait pas le même nombre de tableau.
Il était impossible de récupérer pour toute les pages un même tableau car sa position était différente (ex:joueur ).
Pour régler ce problème :
                        - 1) on stocke les nom des tableau (transferts,blessures,selections ..) dans un dictionnaire
                          2) on compare ces nom avec la valeur souhaité pour récupérer l'indice du tableau
                          3) On effectue le scraping dans le tableau avec l'indice qui correspond dans notre chemin css



création exe :
pip install pyinstaller 
python extract.py  créer le programme à coder pour executable 
pyinstaller --onefile  extract.py   créer l'executable et les logs qui vont avec 



Lancer extract_quali étapes:
1) faire commande :  python extract_historique.py 
2) 1 6 code 
3) Le fichier se retrouve dans dist/Extrion_folder/stats_quali
