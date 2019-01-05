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
    url = "https://www.leboncoin.fr/recherche/?category=9&region=8&region_near=1&cities="+ville;
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



print("update new");
updateNew();

# create a new Firefox session
print("create driver");
driver = webdriver.Safari()
driver.implicitly_wait(1)
print("driver ok");
#wait = WebDriverWait(driver, 3);

paths = ["https://www.leboncoin.fr/materiel_agricole/offres/champagne_ardenne/", "https://www.leboncoin.fr/materiel_agricole/offres/picardie/"]
#paths = ["https://www.leboncoin.fr/materiel_agricole/offres/champagne_ardenne/"]
for path in paths:
	scrappe_leboncoin(path, "")
for path in paths:
	for i in [2,3]:
		path2 = path + "p-" + str(i) + "/"
		scrappe_leboncoin(path2, "")

scrappe_leboncoin_appartements()

driver.quit()
