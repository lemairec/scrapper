from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import json
import requests

def updateNew():
    url = "https://www.maplaine.fr/annonces/api/update_new"
    req = requests.get(url)

def saveOrUpdate(annonces):
    url = "https://www.maplaine.fr/annonces/api"
    #url = "http://localhost:4000/annonces/api";

    for annonce in annonces:
        print(annonce["type"]+" "+annonce["title"]+" "+annonce["category"]);

    my_json_data = {"annonces" : json.dumps(annonces)};
    req = requests.post(url,data=my_json_data)

def scrappe_leboncoin_appartements():
	villes = ["Pignicourt_02190", "Brimont_51220", "Fresne-l%C3%A8s-Reims_51110"
        , "Loivre_51220", "Aum%C3%A9nancourt_51110", "Orainville_02190", "Berm%C3%A9ricourt_51220"
        , "Brienne-sur-Aisne_08190", "Brimont_51220", "Bourgogne_51110"];
	#villes = ["Aum%C3%A9nancourt_51110"];
	for ville in villes:
		scrappe_leboncoin_appartement(ville)


def scrappe_leboncoin_appartement(ville):
    url = "https://www.leboncoin.fr/recherche/?category=9&locations="+ville;
    scrappe_leboncoin(url, "immobilier", ville)


def scrappe_leboncoin(url, category, remark = ""):
    print url
    driver.get(url)
    print "ok"

    response = driver.page_source
    pos = response.find("window.FLUX_STATE = ") + 20
    pos2 = response.find("</script>", pos)
    response = response[pos:pos2]
    response2 = json.loads(response)

    file = open("log.txt", "w")
    file.write(response.encode('utf-8'))
    file.close()

    data = response2["adSearch"]["data"]
    if("ads" in data):
        data = data["ads"]
    else:
        return;
    #print json.dumps(data)

    mydatas = []
    for d in data:
        mydata = {};
        mydata["type"] = "leboncoin"
        mydata["category"] = category
        mydata["title"] = d["subject"]
        mydata["price"] = 0;
        if 'price' in d and (len(d["price"]) > 0):
            mydata["price"] = d["price"][0]
        mydata["image"] = ""
        if 'thumb_url' in d["images"]:
            mydata["image"] = d["images"]["thumb_url"]
        mydata["url"] = d["url"]
        mydata["clientId"] = d["url"]
        mydata["description"] = remark + d["body"];
        if(category == "immobilier"):
            if(mydata["title"].find("Terrain") >= 0):
    			mydata["category"] = "terrain";
        mydatas.append(mydata)

    #print mydatas;
    saveOrUpdate(mydatas);

def save(page):
    f= open("agriaffaires.html","w+")
    f.write(page.encode('utf-8'))
    f.close();

def load():
    f= open("agriaffaires.html","r")
    contents =f.read()
    f.close();
    return contents


def scrappe_agriaffaire(url):
    print url
    driver.get(url)
    page = driver.page_source
    analyse_agriaffaire(page)


    #requete = requests.get("https://zestedesavoir.com/tutoriels/?category=autres-informatique")
    #page = requete.content

    #print page.encode('utf-8')



def stringlify(str):
    str = str.replace("\n", "")
    str = str.replace("    ", " ")
    str = str.replace("    ", " ")
    str = str.replace("    ", " ")
    str = str.replace("   ", " ")
    str = str.replace("  ", " ")
    str = str.replace(" ", " ")
    return str

def analyse_agriaffaire(page):
    soup = BeautifulSoup(page, "html.parser")
    divs = soup.find_all("div", {"class": "listing--element"})

    print len(divs)
    mydatas = []
    for div in divs:
        #print("\n\n######\n")
        #print(div)
        #print("\n\n######\n")



        try:
            type = "agriaffaire"
            category = ""
            title = div.a.div.text
            price = 0;
            div_price = div.find("div", {"class": "price"})
            if(div_price):
                text = div_price.span.text.replace(" ", "");
                price = int(text)

            image = ""
            div_img = div.find("img", {"class": "loaded"})
            if(div_img):
                image = div_img.attrs["data-src"]
            url = "https://www.agriaffaires.com"+div.a.attrs["href"]
            clientId = url

            text = div.find("div", {"class": "listing--galerie--none"}).text;
            description = stringlify(text)

            mydata = {};
            mydata["type"] = type
            mydata["category"] = category
            mydata["title"] = title
            mydata["price"] = price
            mydata["image"] = image
            mydata["url"] = url
            mydata["clientId"] = clientId
            mydata["description"] = description
            mydatas.append(mydata)
        except Exception as e:
            print("toto")
    saveOrUpdate(mydatas);


def scrappe_agriaffaires():
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/tracteur-agricole/1-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/tracteur-agricole/2-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/tracteur-agricole/3-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/tracteur-agricole/1-france_picardie.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/tracteur-agricole/2-france_picardie.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/outil-non-anime/1-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/outil-non-anime/1-france_picardie.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/benne-cerealiere/1-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/benne-cerealiere/1-france_picardie.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/semoir/1-france_champagne-ardennes.html");
    scrappe_agriaffaire("https://www.agriaffaires.com/occasion/semoir/1-france_picardie.html");


driver = None

def main():
    global driver

    print("update new");

    updateNew();

    # create a new Firefox session
    print("create driver");
    driver = webdriver.Safari()
    driver.implicitly_wait(1)
    #print("driver ok");
    #wait = WebDriverWait(driver, 3);

    scrappe_agriaffaires();


    paths = ["https://www.leboncoin.fr/materiel_agricole/offres/champagne_ardenne/", "https://www.leboncoin.fr/materiel_agricole/offres/picardie/"]
    #paths = ["https://www.leboncoin.fr/materiel_agricole/offres/champagne_ardenne/"]
    for path in paths:
        scrappe_leboncoin(path, "")
    	for i in [2,3]:
    		path2 = path + "p-" + str(i) + "/"
    		scrappe_leboncoin(path2, "")

    scrappe_leboncoin_appartements()

    driver.quit()

main();
#page = load()
#analyse_agriaffaire(page)
