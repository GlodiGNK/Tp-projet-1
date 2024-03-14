'''
TRAVAIL FAIT PAR : 
NTUMBA KABONGO GLODI ET 
PENDJI SAIDI
'''

from datetime import datetime
#CLASS CLIENT
class Client:
    def __init__(self, nom, date_naissance, numero_telephone):
        self.nom                = nom
        self.date_naissance     = date_naissance
        self.numero_telephone   = numero_telephone
        self.facture            = 0
    def get_nom(self):
        return self.nom
    def getdate_naissance(self):
        return self.date_naissance
    def getnumero_telephone(self):
        return self.numero_telephone
    def get_facture(self):
        return self.facture
    
#LA CLASS QUI S'OCCUPE DE LA GESTION DES CLIENTS 
class GererClients(Client):
    def __init__(self):
        self.clients                       = []
    def setNom(self, Nom_nouveau):
        self.nom                           = Nom_nouveau
    def setDateNaissance(self, Nouvelle_date):
        self.date_naissance                = Nouvelle_date
    def setNumeroTelephone(self, Nouveau_numero_de_telephone):
        self.numero_telephone              = Nouveau_numero_de_telephone
    def setfacture(self, Nouvelle_facture):
        self.facture                       = Nouvelle_facture
    def ajouter_client(self, client):
        self.clients.append(client)

#IMPORTATION DU FICHIER CDR
class ImportCDR:
    def __init__(self, file_path):
        self.cdr_champ = []
        with open(file_path, 'r') as file:
            for line in file:
                champ = line.strip().split('|')
                cdr_dict = {
                    "Identifiant de l'appel":                       int(champ[0]),
                    'Type call'             :                       int(champ[1]),
                    'Date et heure'         :                       datetime.strptime(champ[2], '%Y%m%d%H%M%S'),
                    'Appelant'              :                       champ[3],
                    'Appelé'                :                       champ[4],
                    'Durée'                 :                       int(champ[5]),
                    'Taxe'                  :                       int(champ[6]),
                    'TotalVolume'           :                       int(champ[7])
                }
                self.cdr_champ.append(cdr_dict)

class GenererFacture:
    def __init__(self, client, cdr_champ):
        self.client = client
        self.cdr_champ = cdr_champ

    def generer_facture_client(self):
        for cdr in self.cdr_champ:

            # CAS DE L'APPEL
            if cdr['Type call'] == 0:

                # CAS MEME RESEAU  
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:  
                    facture_client = cdr['Durée'] * 0.025

                    # EN APPLIQUANT AUCUNE TAXE, ON A : 
                    if cdr['Taxe']== 0: 
                        self.client.facture += facture_client    

                    #EN APPLIQUANT l'ACCISE 10%                    
                    elif cdr['Taxe'] == 1: 
                        self.client.facture += (facture_client + (facture_client * 0.1))

                    #APPLIQUANT LA TVA 16%
                    elif cdr['Taxe'] == 2: 
                        self.client.facture += (facture_client + (facture_client * 0.16))                        
                else:
                    facture_client += cdr['Durée'] * 0.05

                    #AUCUNE TAXE EST APPLIQUEE
                    if cdr['Taxe']== 0:  
                        self.client.facture += facture_client

                    #APPLIQUANT l'ACCISE 10%                        
                    elif cdr['Taxe'] == 1: 
                        self.client.facture += (facture_client + (facture_client * 0.1))

                    #APPLIQUANT LA TVA 16%
                    elif cdr['Taxe'] == 2: 
                        self.client.facture += (facture_client + (facture_client * 0.16))

            # CAS D'SMS
            elif cdr['Type call'] == 1:  
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:

                    # MEME RESEAU
                    facture_client = 0.001

                    #AUCUNE TAXE EST APPLIQUEE
                    if cdr['Taxe']== 0: 
                        self.client.facture += facture_client   

                    #APPLICATION DE l'ACCISE 10%                     
                    elif cdr['Taxe'] == 1: 
                        self.client.facture += (facture_client + (facture_client * 0.1))
                    
                    #APPLICATION DE LA TVA 16%
                    elif cdr['Taxe'] == 2: 
                        self.client.facture += (facture_client + (facture_client * 0.16))
                else:
                    facture_client = 0.002

                    # AUCUNE TAXE
                    if cdr['Taxe']== 0: 
                        self.client.facture += facture_client

                    #APPLICATION DE l'ACCISE 10%                        
                    elif cdr['Taxe'] == 1: 
                        self.client.facture += (facture_client + (facture_client * 0.1))
                    
                    #APPLICATION DE LA TVA 16%
                    elif cdr['Taxe'] == 2: 
                        self.client.facture += (facture_client + (facture_client * 0.16))                    
            
            # CAS DE L'INTERNET
            elif cdr['Type call'] == 2:  
                facture_client = cdr['TotalVolume'] * 0.03

                #AUCUNE TAXE
                if cdr['Taxe']== 0:
                    self.client.facture += facture_client   

                #APPLICATION DE l'ACCISE 10%                     
                elif cdr['Taxe'] == 1: 
                    self.client.facture += (facture_client + (facture_client * 0.1))
                
                #APPLICATION DE LA TVA 16%
                elif cdr['Taxe'] == 2: 
                    self.client.facture += (facture_client + (facture_client * 0.16))

class Statistiques:
    def __init__(self, cdr_champ):
        self.cdr_champ = cdr_champ

    def calculer_statistiques(self):
        nb_appels = sum(1 for cdr in self.cdr_champ if cdr['Type call'] == 0)
        duree_appels = sum(cdr['Durée'] for cdr in self.cdr_champ if cdr['Type call'] == 0)
        nb_sms = sum(1 for cdr in self.cdr_champ if cdr['Type call'] == 1)
        volume_internet = sum(cdr['TotalVolume'] for cdr in self.cdr_champ if cdr['Type call'] == 2)
        return nb_appels, duree_appels, nb_sms, volume_internet

# TEST UNITAIRE
print()

#TEST 1 AVEC LE FICHIER (cdr.txt) AVEC LES DEUX NUMEROS DU CLIENT
test_client_1           = Client("POLYTECHNIQUE", "2023-01-11", "243818140560, 243818140120")
fichier_cdr_import      = ImportCDR("C:/Users/MUSINDONDO/Desktop/PROJET ALGO/cdr.txt")
generer_facture         = GenererFacture(test_client_1, fichier_cdr_import.cdr_champ)
generer_facture.generer_facture_client()
statistiques            = Statistiques(fichier_cdr_import.cdr_champ)
nb_appels, duree_appels, nb_sms, volume_internet = statistiques.calculer_statistiques()

#TEST 2 AVEC LE FICHIER (tp_algo-1.txt) AVEC LES DEUX NUMEROS DU CLIENT
test_client_2 = Client("POLYTECHNIQUE", "2023-01-11", "243818140560, 243818140120,")
fichier_tp_algo_import = ImportCDR("C:/Users/MUSINDONDO/Desktop/PROJET ALGO/tp_algo-1.txt")
generer_facture = GenererFacture(test_client_2, fichier_tp_algo_import.cdr_champ)
generer_facture.generer_facture_client()
statistiques = Statistiques(fichier_tp_algo_import.cdr_champ)
nb_appels1, duree_appels1, nb_sms1, volume_internet1 = statistiques.calculer_statistiques()
print ("FACTURE 00001/14-03-2024")
print()
print(f"Le montant à payer du client {test_client_2.nom} est estimé à : ",test_client_2.facture + test_client_1.facture, "$")
print()
print(f"1. Il a passé un nombre d'appels total d'une durée de :", nb_appels + nb_appels1, "et en secondes, on a une valeur de :", duree_appels + duree_appels1 ," secondes")
print()
print(f"2. Nombre de SMS: ", nb_sms + nb_sms1)
print()
print(f"3. Il a utulisé un volume internet de : ", volume_internet + volume_internet1 ,"Mo")
print()


'''Ce projet nous a permis  à developper un système de facturation pour les clients de l'opérateur téléphonique Vodacom. 
Notre travail est capable de : 
1. impoter les fichiers CDR (call Detail Record) qui contiennent les details de chaque appel, sms et utilisation d'internet des clients.
2. Générer la facture de chaque client en fonction de sa consommation.
3. Calculer les statistiques d'utilisation des clients (nombre d'appels, durée des appels, nombre de SMS, volume internet)

Ce projet nous a permis de comprendre comment fonctionne les entreprise téléphonique. comment il procède pour l'automatisation de leur
facturation des ses clients et leur fournir des statistiques sur leur utilisation des services de vodacom.


NOTE : Pour le fichier cdr.txt, nous avons remarqué quand nous étions entrain de l'importer, le code le considerait comme une erreur
       donc pour palier à ce problème; nous avons ajouté le chiffre 0 qui est synonyme de vide en programmation'''