from django.shortcuts import render , get_object_or_404 , redirect
from .forms import MoveForm
from .models import Character, Equipement
import random
def home(request):
    charas = Character.objects.all()
    lieux = Equipement.objects.all()
    
    return render(request, 'play/home.html', {'charas' : charas,  'lieux': lieux})

def chara_detail(request,nom):
    chara = get_object_or_404(Character, nom = nom)
    ancien_lieu = chara.lieu
    charas_in_lieu = Character.objects.filter(lieu = ancien_lieu)

    if request.method == "POST":
        form = MoveForm(request.POST, instance=chara)
        if form.is_valid():
            form.save(commit="False")
            nouveau_lieu = get_object_or_404(Equipement, id=chara.lieu.id)
            if nouveau_lieu == ancien_lieu and (chara.etat != "affamé" and chara.lieu != "base"):
                message = f"{chara.nom} est déjà dans ce lieu"
                return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
            

            
            print("nouveau_lieu : ", nouveau_lieu)

            if nouveau_lieu.disponibilite == "libre":
                print("Le nouveau lieu est bien libre")
                nbr = Character.objects.filter(lieu=nouveau_lieu).count()
                

                # Si il n'est pas en état d'aller dans le champs
                if nouveau_lieu.id == "champs" and chara.etat != "repu":
                    print(" ne peut pas aller travailler la terre dans cet état de fatigu")
                    message = f"{chara.nom} ne peut pas aller travailler la terre dans cet état "
                    return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
                
                # Si il n'est pas en état d'aller dans la mine
                if nouveau_lieu.id == "mine" and chara.etat != "repu":
                    print(" ne peut pas aller travailler dans la mine dans cet état de fatigu")
                    message = f"{chara.nom} ne peut pas aller travailler dans la mine dans cet état "
                    return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
                
                if nouveau_lieu.id == "foret" and chara.etat == "fatigué":
                    print(" ne peut pas aller se balader en foret")
                    message = f"{chara.nom} ne peut pas se balader en forêt dans cet état de fatigue"
                    return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
                
               
                # Il va  dans le nouveau lieu
                if nbr >= nouveau_lieu.capacite : # On regarde si le lieu est rempli (en comptant le nouveau personnage)
                    print("on est dans le if")
                    nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

                # si il est repu et dans le champs alors il peut travailler la terre et obtenir de quoi manger après avoir travailler
                print("nouveau_lieu : " + nouveau_lieu.id)
                if nouveau_lieu.id == "champs" and chara.etat == "repu":
                        chara.etat = "fatigué"

                        n = random.randint(0,3)
                        controle = 0
                        if n == 0 : # ajout de la patate douce
                            for objet in chara.inventaire :
                                if objet[0] == "patate douce" :
                                    objet[1] += 1
                                    controle = 1
                                    break
                            if controle == 0 :
                                chara.inventaire.append(["patate douce" , 1])
                            message =f"{chara.nom} vient de déterrer une patate douce"
                            
                        controle = 0

                        if n == 1 : # ajout de la carotte
                            for objet in chara.inventaire :
                                if objet[0] == "carotte" :
                                    objet[1] += 1
                                    controle = 1
                                    break
                            if controle == 0 :
                                chara.inventaire.append(["carotte" , 1])
                            message = f"{chara.nom} vient de déterrer une carotte"
                        controle = 0

                        if n == 2 : # ajout du navet
                            for objet in chara.inventaire :
                                if objet[0] == "navet" :
                                    objet[1] += 1
                                    controle = 1
                                    break
                            if controle == 0 :
                                chara.inventaire.append(["navet" , 1])
                            message = f"{chara.nom} vient de déterrer un navet"
                        
                        controle = 0

                        if n == 3 : # ajout de l'igname 
                            for objet in chara.inventaire :
                                if objet[0] == "igname" :
                                    objet[1] += 1
                                    controle = 1
                                    break
                            if controle == 0 :
                                chara.inventaire.append(["igname" , 1])
                            message = f"{chara.nom} vient de déterrer un igname"
                        chara.save()

                #MINE
                #Il ne va dans la mine que s'il est repu et ça a pour effet de l'affamer et il récolte de la pierre et des minerais
                elif nouveau_lieu.id == "mine" and chara.etat == "repu":
                    chara.etat = "fatigué"

                    n = random.randint(0,100)
                    controle = 0
                    if 0 <= n <60 : # ajout de la pierre
                        for objet in chara.inventaire :
                            if objet[0] == "pierre" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["pierre" , 1])
                        message = f"{chara.nom} a miné de la pierre !"
                        
                    controle = 0

                    if 60 <= n <80 : # ajout du charbon
                        for objet in chara.inventaire :
                            if objet[0] == "charbon" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["charbon" , 1])
                        message = f"{chara.nom} a miné de du charbon !"
                    controle = 0

                    if  80 <= n <95 : # ajout de fer
                        for objet in chara.inventaire :
                            if objet[0] == "fer" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["fer" , 1])
                        message = f"{chara.nom} a miné du fer !!"
                    
                    controle = 0

                    if  95 <= n <100 : # ajout d' or
                        for objet in chara.inventaire :
                            if objet[0] == "or" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["or" , 1])
                        message = f"{chara.nom} a miné de l'or !!!!!!!!!"
                    chara.save()
                    
                    #récolte des pierre et des minerais

                #BASE
                    # si il est fatigué et dans la base il dort 
                elif nouveau_lieu.id == "base" and chara.etat == "fatigué":
                    chara.etat = "affamé"
                    message = f"{chara.nom} s'est bien reposé(e) dans la base"
                    chara.save()
                    # s'il est affamé et dans la base il y mange
                elif nouveau_lieu.id == "base" and chara.etat == "affamé":
                    controle1 = 0
                    for objet in chara.inventaire :
                        if objet[0] == "patate douce" or  objet[0] == "pomme" or objet[0] == "navet" or objet[0] == "carotte" or objet[0] == "igname" or  objet[0] == "champignon" or objet[0] == "baie" :
                            objet[1] = objet[1] - 1
                            if objet[1] == 0:
                                chara.inventaire.remove(objet)
                            message = f"{chara.nom} a mangé un(e) " + objet[0] + " dans la base"
                            controle1 = 1
                            chara.etat = "repu"
                        controle1 == 1
                    if controle1 == 0 :
                        message = f"{chara.nom} n'a rien à manger autant aller dans la forêt pour un rammasser un champignon ou deux"
                    chara.save()

                #FORET
                    # repu et dans la foret
                elif nouveau_lieu.id == "foret" and chara.etat == "repu":
                    chara.etat = "fatigué"
                    controle = 0
                    for objet in chara.inventaire :
                        if objet[0] == "bois" :
                            objet[1] += 1
                            controle = 1
                            break
                    if controle == 0 :
                        chara.inventaire.append(["bois" , 1])
                    message = f"{chara.nom} a coupé du bois dans la forêt..."
                    chara.save()
                    
                    #dans la forêt repu il coupe du bois 
                    # s'il est affamé dans la foret
                elif nouveau_lieu.id == "foret" and chara.etat == "affamé":
                    chara.etat = "fatigué"
                    n = random.randint(0,100)
                    controle = 0
                    if 0 <= n <60 : # ajout d'un champignon
                        for objet in chara.inventaire :
                            if objet[0] == "champignon" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["champignon" , 1])
                        message = f"{chara.nom} a ramassé un champignon dans la forêt, espérons qu'il soit comestible..."
                        
                    controle = 0

                    if 60 <= n <80 : # ajout du baie
                        for objet in chara.inventaire :
                            if objet[0] == "baie" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["baie" , 1])
                        message = f"{chara.nom} a ramassé une baie dans la forêt, espérons qu'elle soit comestible..."
                    controle = 0

                    if  80 <= n <95 : # ajout de pomme
                        for objet in chara.inventaire :
                            if objet[0] == "pomme" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["pomme" , 1])
                        message = f"{chara.nom} a ramassé une pomme dans la forêt !"
                    
                    controle = 0

                    if  95 <= n <100 : # ajout de morceaux de étoile 
                        for objet in chara.inventaire :
                            if objet[0] == "morceau d'étoile" :
                                objet[1] += 1
                                controle = 1
                                break
                        if controle == 0 :
                            chara.inventaire.append(["morceau d'étoile" , 1])
                        message = f"{chara.nom} a ramassé un ... morceau d'étoile !? À quoi ça pourrait nous servir ?"
                    chara.save()

            else:
                chara.lieu = ancien_lieu
                chara.save()
                occupants = Character.objects.filter(lieu=nouveau_lieu)
                occupants_names = ", ".join([o.nom for o in occupants])
                print(occupants_names)
                message = f"Le lieu est déjà occupé par {occupants_names}"
                return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
            
            #return redirect('chara_detail', nom=nom)
            return render(request, 'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form, 'message': message, 'charas_in_lieu': charas_in_lieu})
                      
        #ancien_lieu = get_object_or_404(Equipement, id=chara.lieu.id)
        #ancien_lieu.disponibilite = "libre"
        #ancien_lieu.save()
        #form.save()
        #nouveau_lieu = get_object_or_404(Equipement, id=chara.lieu.id)
        #nouveau_lieu.disponibilite = "occupé"
        #nouveau_lieu.save()
        #return redirect('chara_detail', nom=nom)
    else:
        form = MoveForm()
        return render(request,'play/chara_detail.html', {'chara': chara, 'lieu': chara.lieu, 'form': form})