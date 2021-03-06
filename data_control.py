# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
#!!!!                                                                         #
#                                                                             #
#please note the code is not up to date. It may not work actually due to      #
#change on the web site host from where data is extracted.                    #
#                                                                             #
#!!!!                                                                         #
#-----------------------------------------------------------------------------#

from tool_kit import path_log, create_path, dispatch, curl, oldnew_ipadress
from bs4 import BeautifulSoup
import time
import pandas as pd

#-----------------------------------------------------------------------------#
#               get urls from real estate announces                           #
#-----------------------------------------------------------------------------#
def function_2(path_log, file_name="backup_file1.txt") :
    create_path() 
    url = ["http://www.seloger.com/immobilier/tout/immo-paris-%seme-75/" % (str(i)) for i in range(1,21)]          
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    backup_file2 = open(path_log + "backup_file2.txt", "w")
    for url in url_liste :
        pool = curl(url)
#        oldnew_ipadress(path_log)
        for c in pool :
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            s1 = soup1.findAll('div', {'class' : 'content_infos othergroupsite'})
            s1 = s1[0].findAll('li')
            print "len(s1) : ", len(s1)        
            print "\n"
            som_nbr_annonce = 0
            som_list = []
            for i in range(len(s1)) : 
                url = s1[i].findAll('a')[0]['href']
                len_url = len(url.split("/"))
                len_departement = len(url.split("/")[len_url-4].split("-"))
                departement = url.split("/")[len_url-4].split("-")[len_departement-1]
                type_bien1 = url.split("/")[len_url-3].replace("bien-", "")
                nbr_annonce = s1[i].findAll('b')[0].string
                if nbr_annonce != None :
                    pass
                else :
                    nbr_annonce = 0                
                som_nbr_annonce = float(som_nbr_annonce) + float(nbr_annonce)
                som_list.append(float(som_nbr_annonce))
                nbr_piece = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[2]
                if nbr_piece == "studio" :
                    nbr_piece = '1'
                else :
                    pass
                type_transaction = s1[i].findAll('a')[0]['title'].replace("Immobilier ", "").replace(type_bien1, "").strip().split(" ")[0]
                print i, str(som_nbr_annonce), departement, str(nbr_annonce), type_transaction, type_bien1, nbr_piece, url
                backup_file2.write(departement + ";" + str(nbr_annonce)+ ";" + type_transaction + ";" + type_bien1 + ";" + nbr_piece + ";" + url + ";")
                backup_file2.write("\n")
    backup_file2.close()
    print "\n"
    
#-----------------------------------------------------------------------------#
#               Get number of page and urls to get through                    #
#-----------------------------------------------------------------------------#
def function_3(path_log) :
    backup_file = open(path_log + "backup_file2.txt", "r").readlines()
    print "len(backup_file) : ", len(backup_file)
    print "\n"
    urls_parcours = open(path_log + "urls_parcours.txt", "w")
    urls_list = []
    for i in range(len(backup_file)) :
        url = backup_file[i].split(";")[5]
        nbr = float(backup_file[i].split(";")[1])
        nbr_page_init = nbr/10
        partie_entiere = int(str(nbr_page_init).split(".")[0])
        apres_dec = int(str(nbr_page_init).split(".")[1])
        if apres_dec == 0 :
            nbr_page = partie_entiere
        elif apres_dec > 0 :
            nbr_page = partie_entiere + 1
        else :
            print "Probleme nbr_page"                
        print "nbr : ", nbr
        print "url : ", url
        print nbr, nbr_page_init, "nous donne :", nbr_page, "page(s)", "\n"
        if nbr_page == 1 or nbr_page == 0 :
            if nbr_page == 0 :
                print "Attention prise en charge du cas '0' page releve : ", "\n"
            else :
                b = url
                urls_list.append(b)
                urls_parcours.write(b + ";" + "\n")
                print b
        elif nbr_page == 2 :
            b = url
            c = url + "?ANNONCEpg=2"               
            urls_list.append(b)
            urls_list.append(c)
            urls_parcours.write(b + ";" + "\n")
            urls_parcours.write(c + ";" + "\n")
            print c
            print b
        elif nbr_page > 2 :
            for j in range(2, nbr_page) :                    
                b =  url + "?ANNONCEpg=%s" %(str(j))
                urls_list.append(b)
                urls_parcours.write(b + ";" + "\n")
                print b
        else :
            print "Problem nbr_page re construction"
    print "len(urls_list) : ", len(urls_list)
            
#-----------------------------------------------------------------------------#
#        get urls from real estate announces for each link                    #
#-----------------------------------------------------------------------------#
def function_4(path_log, file_name="urls_parcours.txt") :
#    d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
    d2 = str(time.strftime('%d/%m/%y %H:%M:%S',time.localtime()))    
    d3 = str(time.strftime('%d-%m-%y',time.localtime()))
    backup_file1 = open(path_log + file_name, "r").readlines()
    url = [] 
    for i in range(len(backup_file1)) :
        a = backup_file1[i].split(";")[0].strip()
        url.append(a)
    url_liste = dispatch(path_log + "dispatch1.txt", url)
    url_done = open(path_log + "url_done.txt", "w")
    path_logout = "log/"
    compteur = 0
    for url in url_liste :
        compteur += 1
        print compteur, "/", len(url_liste)        
        for i in range(len(url)) :
            url_done.write(url[i] + "\n")
        pool = curl(url)
#        oldnew_ipadress(path_log)
        compteur1 = 0
        for c in pool :
            compteur1 += 1
            print compteur1, "/", len(pool)
            data = c.body.getvalue()
            soup1 = BeautifulSoup(data)
            d = str(time.strftime('%d-%m-%y_%Hh%Mmin%Ssec',time.localtime()))
            l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
            dico = {'TYPE_TRANSACTION' : l0, 'NOMBRE_PHOTOS' : l1 , 
                    'NOMBRE_PIECE' : l2, 'NOMBRE_M2' : l3, 'ETAGE' : l4, 
                    'BALCON' : l5, 'CUISINE' : l6, 'AUTRE' : l7,
                    'CHAMBRE(S)' : l8, 'MEUBLE' : l9, 'TYPE_CHAUFFAGE' : l10, 
                    'LOCALISATION' : l11, 'PROXIMITE' : l12, 'PRIX' : l13, 
                    'CHARGE' : l14, 'NOM_AGENCE' : l15, 'URL' : l16, 
                    'EXTRACTION_DATE' : l17}
            #-----------------------------------------------------------------#
            #HERE LOOKING FOR WORDS LOCATIONS / VENTES / INVESTISSEMENT / VIAGER :
            s0 = soup1.findAll('div', {'class' : 'main'})
            for i in range(len(s0)) :
                if s0[i].findAll('span', {'class' : 'title_recherche'}) == [] :
                    transaction_type = "NA"
                else :
                    transaction_type = s0[i].findAll('span', {'class' : 'title_recherche'})
                    transaction_type = transaction_type[0].text
                    if "locations" in transaction_type :                        
                        transaction_type = "LOCATION"
                    elif "ventes" in transaction_type :
                        transaction_type = "ACHAT"
                    elif "investissement" in transaction_type :
                        transaction_type = "INVESTISSEMENT"
                    elif "viager" in transaction_type :
                        transaction_type = "VIAGER"
                    else :
                        pass
            #-----------------------------------------------------------------#
            #We are looking for the photo number in html page then add var TRANSACTION_TYPE
            s1 = soup1.findAll('div', {'class' : 'annonce__visuel__pictogrammes'})
            for i in range(len(s1)) :
                if s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'}) == [] :
                    nbr_photo = 0
                else :
                    nbr_photo = s1[i].findAll('a', {'class' : 'annonce__visuel__picto picto__photo'})
                    nbr_photo = nbr_photo[0]['title']
                    nbr_photo = nbr_photo.replace(" photos", "")
                    nbr_photo = int(nbr_photo)
                l1.append(nbr_photo)
                l0.append(transaction_type)
            #-----------------------------------------------------------------#
            s2 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s2)) :
                details1 = s2[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details1 = details1.replace("\xe8", "e")
                details1 = details1.replace("m\xb2", "m2")
                details1 = details1.replace("\xe9", "e")
                details1 = details1.split(",")
                nbr_piece = "NA"
                nbr_m2 = "NA"
                etage = "NA"
                balcon = "NA"
                cuisine = "NA"
                autre = "NA"
                chambre = "NA"
                meuble = "NA"
                chauffage = "NA"
                for j in details1 :
                    if "Piece" in j :
                        if nbr_piece == "NA" :
                            nbr_piece = j.replace(" Piece", "").replace("s", "").strip()
                        else : 
                            pass
                    if "m2" in j :
                        if nbr_m2 == "NA" :
                            nbr_m2 = j.replace(" m2", "").strip()
                        else : 
                            pass
                    if "Etage" in j :
                        if etage == "NA" :
                            etage = j.replace(" Etage", "").strip()
                        else : 
                            pass
                    if "Balcon" in j :
                        if balcon == "NA" :
                            balcon = j.replace(" Balcon", "").strip()
                            balcon = j.replace("s", "").strip()
                        else : 
                            pass
                    if "cuisine" in j :
                        if cuisine == "NA" :
                            cuisine = j.replace(" cuisine", "").strip()
                        else : 
                            pass
                    if "Chambre" in j :
                        if chambre == "NA" :
                            chambre = j.replace(" Chambre", "")
                            chambre = chambre.replace("s", "").strip()
                        else :
                            pass
                    if "Meuble" in j :
                        if meuble == "NA" :
                            meuble = "YES"
                        else :
                            pass
                    if "chauffage" in j :
                        if chauffage == "NA" :
                            chauffage = j.replace("chauffage ", "")
                            chauffage = j.replace(" radiateur", "")
                        else :
                            pass
                    if "Piece" not in j and "m2" not in j and "Etage" not in j \
                    and "Balcon" not in j and "cuisine" not in j and "Chambre" not in j \
                    and "Meuble" not in j and "chauffage" not in j :
                        autre = j.strip()
                    else : 
                        pass
                l2.append(nbr_piece)
                l3.append(nbr_m2)
                l4.append(etage)
                l5.append(balcon)
                l6.append(cuisine)
                l7.append(autre)
                l8.append(chambre)
                l9.append(meuble)
                l10.append(chauffage)   
            #-----------------------------------------------------------------#
            #LOCATION : 
            s3 = soup1.findAll('span', {'class' : 'annone__detail__localisation'})
            for i in range(len(s3)) :
                details2 = s3[i].findAll('span', {'class' : 'annone__detail__param'})[0].text
                details2 = details2.replace(" (Paris)", "")
                details2 = details2.replace(" ()", "")
                l11.append(details2)    
            #-----------------------------------------------------------------#
            #NEAR LOCATION : 
            s4 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s4)) :
                details3 = s4[i].findAll('span', {'class' : 'annone__detail__proximite'})
                if details3 != [] :
                    details3 = details3[0].text
                    details3 = details3.replace("&#201;", "E")
                    details3 = details3.replace("&#233;", "e")
                    details3 = details3.replace("&#234;", "e")
                    details3 = details3.replace("&#235;", "e")
                    details3 = details3.replace("&#226;", "a")
                    details3 = details3.replace("&#244;", "o")
                    details3 = details3.replace("&quot", "")
                    details3 = details3.replace("&#206;", "")
                    details3 = details3.replace("&#231;", "c")
                    details3 = details3.replace("M&#176;", "Metro ")
                    details3 = details3.replace("Metro ", "")
                    details3 = details3.replace("Metro", "")
                    details3 = details3.replace("&#39;", "'")
                    details3 = details3.replace("&amp;", "et")
                    details3 = details3.replace("&#232;", "e")
                    details3 = details3.replace("/", ",")
                    details3 = details3.replace(": ", "")
                    details3 = details3.replace("metro", "") 
                    details3 = details3.replace("&#224;", "a")
                    details3 = details3.replace("&#238;", "i")
                    details3 = details3.replace("&#239;", "i")                    
                    details3 = details3.replace("Centre ville,", "")
                    details3 = details3.replace("ecole,", "")
                    details3 = details3.replace("commerces,", "")
                    details3 = details3.replace("bus,", "")
                    details3 = details3.replace("*", "")
                else :
                    details3 = "NA"
                proximite = details3
                l12.append(proximite)
            #-----------------------------------------------------------------#
            #PRICE AND DETAILS OF ADDITIVE PRICE CHARGES : 
            s5 = soup1.findAll('div', {'class' : 'annonce__agence'})
            for i in range(len(s5)) :
                details4 = s5[i].findAll('span', {'class' : 'annonce__agence__prix annonce__nologo'})
                details5 = s5[i].findAll('span', {'class' : 'annonce__agence__prix '})
                if details4 != [] :
                    details4 = details4[0].text
                    details4 = details4.replace("\xa0", "")
                    details4 = details4.replace("\x80", "")
                    details4 = details4.split(" ")
                else :
                    details4 = 0
                if details5 != [] :
                    details5 = details5[0].text
                    details5 = details5.replace("\xa0", "")
                    details5 = details5.replace("\x80", "")                   
                    details5 = details5.split(" ")
                else :
                    details5 = 0
                if details4 == 0 :
                    detailsx = details5 
                elif details5 == 0 :
                    detailsx = details4
                try :
                    l13.append(float(detailsx[0].replace(",", ".").replace("Â", "")))
                except :
                    l13.append(str(detailsx[0]))
                if "FAI" in detailsx[1] :
                    new = detailsx[1].replace("FAI", "")
                    try :
                        l14.append(float(new))
                    except :
                        l14.append(new)
                elif "+" in detailsx[1] :
                    new = detailsx[1].replace("+", "")
                    l14.append(new)
                else :
                    l14.append(detailsx[1].strip())
            #-----------------------------------------------------------------#
            #REAL ESTATE AGENCY NAMES : 
            s6 = soup1.findAll('div', {'class' : 'annonce__agence'})
            for i in range(len(s6)) :
                details6 = s6[i].findAll('span', {'class' : 'annone__detail__nom'})
                if details6 != [] :
                    details6 = details6[0].text
                else :
                    details6 = "NA"
                l15.append(details6)                    
            #-----------------------------------------------------------------#
            #GET THE URL VALUE : 
            s7 = soup1.findAll('div', {'class' : 'annonce__detail'})
            for i in range(len(s7)) :
                url_cible = s7[i].findAll('a', {'class' : 'annone__detail__title annonce__link'})
                url_cible = url_cible[0]['href']
                url_cible = url_cible.split("?")[0]
                l16.append(url_cible)                    
                #-----------------------------------#
                #DATE : 
                l17.append(d2)
            #-----------------------------------------------------------------# 
            #WRITE DATA IN FILE :
            if dico['CUISINE'] == [] : 
                pass
            else : 
                try :
                    df = pd.DataFrame(dico) 
                    df.to_csv(path_logout + 'seloger_%s.txt' %(d3), mode="a", header=False)                
                    print compteur, df
                    print "\n"
                except :
                    print "ValueError : ", ValueError
                    print "dico : ", dico
                    log_dico = open(path_log + "log_dico.txt", "a")
                    for i in dico : 
                        print "len(dico[i])  : ", str(len(dico[i])), str(i), str(dico[i]) 
                        log_dico.write(str(len(dico[i])) + ";" + str(i) + ";" + str(dico[i]))
                    log_dico.close()
        print "\n"
            

