from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

url = "https://www.themoviedb.org/tv"
artiste_url = "https://www.themoviedb.org/person"
site_web_url = "https://www.themoviedb.org"

data = []
header_emissions = ['Titre', 'Date de sortie, Sous titre', 'Description', 'Acteurs' ]

header_artistes = ['Nom', 'Participer dans Films']

# recupérer les détails de chaque film
def get_detail_by_id(url_id, tableau):
    req = Request(url_id, headers={'User-Agent': 'Mozilla/5.0'})
    site_web = urlopen(req).read()
    bsoup_site_web = soup(site_web, "html.parser")

    containers = bsoup_site_web.find_all("div", class_="header_poster_wrapper false")
    for emission in containers:
        parent_content = emission.find("div", class_="header_info")
        sous_titre = parent_content.find("h3", class_="tagline")
        parent_description = parent_content.find("div", class_="overview")
        description = parent_description.find("p")

        if sous_titre and sous_titre.text:
            #print("sous_titre : ", sous_titre.text)
            tableau.append(str(sous_titre.text).strip(""))
        #print("description : ", description.text)
        tableau.append(str(description.text).strip(""))

        parent_createur_1 = parent_content.find("ol", class_="people no_image")
        if parent_createur_1 and parent_createur_1.find_all("li", class_="profile"):
            parent_createur_2 = parent_createur_1.find_all("li", class_="profile")
            liste_createurs = ""
            for createur_content in parent_createur_2:
                createur = createur_content.find("a")
                liste_createurs += createur.text+", "
            tableau.append(str(liste_createurs).strip(""))
        #print("Auteur : ", liste_createurs)



def get_all_films_or_tv_with_details():
    print("\n----------")
    print("\tEMISSIONS / FILMS : ")
    print("-----------\n")
    tableau = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    site_web = urlopen(req).read()
    bsoup_site_web = soup(site_web, "html.parser")

    containers = bsoup_site_web.find_all("div", class_="card style_1")
    for emission in containers:
        parent_titre = emission.find("div", class_="content")
        sec_parent_titre = parent_titre.find("h2")
        titre = sec_parent_titre.find("a")
        lien = sec_parent_titre.find("a", href=True)
        date_sortie = parent_titre.find("p")
        #print("\n----------------------------------------------")
        tableau.append(str(titre.text).strip(""))
        #print("Titre : ", titre.text)
        tableau.append(str(date_sortie.text).strip(""))
        #print("Date : ", date_sortie.text)
        #print("Lien : ", lien['href'])
        get_detail_by_id(site_web_url+""+str(lien['href']), tableau)
        #print("--------------------------------------------------\n")
        data.append(tableau)
        
        #print(tableau)
        #print('\n')
        tableau = []
        #print(emission)
    return data


def get_liste_artistes():
    print("\n----------")
    print("\tARTISTES : ")
    print("-----------\n")
    data_artistes = []
    tableau = []
    req = Request(artiste_url, headers={'User-Agent': 'Mozilla/5.0'})
    site_web = urlopen(req).read()
    bsoup_site_web = soup(site_web, "html.parser")

    listes_artistes = bsoup_site_web.find_all("div", class_="fifty_square")

    for artiste_data in listes_artistes:
        parent_data = artiste_data.find("div", class_="meta")
        nom_artiste = parent_data.find("p", class_="name")
        film_jouer = parent_data.find("p", class_="sub")
        #print("\n----------------------------------------------")
        tableau.append(str(nom_artiste.text).strip(""))
        tableau.append(str(film_jouer.text).strip(""))
        #print("Nom : ", nom_artiste.text)
        #print("Film : ", film_jouer.text)
        data_artistes.append(tableau)
        tableau = []
        #print("--------------------------------------------------\n")
    return data_artistes


def set_csv_files(name_of_file, header, data):
    with open(name_of_file+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("--------------------------------------------------\n")
    print("\tMENU\t\n")
    print("1- Liste des émissions/films\n")
    print("2- Liste des artistes\n")
    print("Tapez une autre touche pour quitter\n")
    print("--------------------------------------------------\n")

    x = input("Tapez quelque chose ici : ")
    if x == "1":
        data = get_all_films_or_tv_with_details()
        set_csv_files('emissions', header_emissions, data)
    elif x == "2":
        data_artistes = get_liste_artistes()
        set_csv_files('artistes', header_artistes, data_artistes)
    else:
        print("AU REVOIR")
