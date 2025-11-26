# Skelbiu & Autoplius Car Scraper
A Scrapy-based web scraper for collecting car listings from **skelbiu.lt** and
then scraping detailed car information from **autoplius.lt**.
The scraper runs in two phases:

1. **SkelbiuAutoSpider**
   - Collects listing data (title, price, params, image, etc.)
   - Saves listing URLs to a `.jsonl` file

2. **AutopliusSpider**
   - Reads collected URLs
   - Scrapes detailed ad information (parameters, description, features, etc.)
   - Saves them into a second `.jsonl` file

Both spiders use **Pydantic models** for data validation.

## Output Files
- `skelbiu_output.jsonl`: Output from SkelbiuAutoSpider
    {
        "Item_ID": "81397611",
        "Title": "Audi A4 allroad, 3.0 l., universalas",
        "City": "Kaunas,",
        "Creation_date": "rugsėjo 30 d.",
        "Item_Params": ["2017 m.", "Dyzelinas", "3.0", "Automatinė", "311018 km"],
        "Price": "16290", "Link": "https://www.skelbiu.lt/skelbimai/pirkdami-automobili-is-musu-nemokamai-gausite-garantija-81397611.html",
        "Image_URL": "https://autoplius-img.dgn.lt/ann_25_367417951/audi-a4-allroad-3-0-l-universalas-2017-dyzelinas.jpg"
    }

- `autoplius_output.jsonl`: Output from AutopliusSpider
    {
        "Id": "A29574861",
        "Price": "6800",
        "Phone": "+370 686 56215",
        "Title": "Audi A4 allroad, 2.0 l., universalas 2011-12 m.,  | A29574861",
        "Link": "https://autoplius.lt/skelbimai/audi-a4-allroad-2-0-l-universalas-2011-dyzelinas-29574861.html", "Parameters":
            {"First_Registration": "2011-12", "Mileage": "212 000 km", "Engine": "2000 cm³, 143 AG (105kW)", "Fuel": "Dyzelinas", "Body_Type": "Universalas", "Doors": "4/5", "Drive": "Visi varantys (4х4)", "Gearbox": "Mechaninė", "Climate_Control": "Klimato kontrolė", "Color": "Juoda", "Tech_Inspection": "N/A", "Rim_Size": "R17", "Weight": "N/A", "Seats": "N/A", "Euro_Standard": "N/A", "CO2_Emission": "~ 164 g/km", "Pollution_Tax": "~ 167.28 €", "City_Consumption": "N/A", "Highway_Consumption": "N/A", "Average_Consumption": "N/A"},
        "Description":
            {"Description": ["Tvarkingas, Lietuvoje neeksploatuotas, originali rida. Daugiau info tel."]},
        "Features":
            {"Features": {"Salonas": ["Daugiafunkcinis vairas", "Šildomos sėdynės", "Bagažinės uždangalas"],
            "Elektronika": ["El. reguliuojami veidrodėliai", "Automatiškai įsijungiantys žibintai", "Kritulių        jutiklis", "Šildomi veidrodėliai", "Atstumo jutiklių sistema", "Autopilotas"],
            "Eksterjeras": ["Lengvojo lydinio ratlankiai", "LED dienos žibintai", "Žibintai „Xenon“", "Rūko žibintai", "Priekinių žibintų plovimo įtaisas"],
            "Kiti ypatumai": ["Neeksploatuota Lietuvoje", "Serviso knygelė", "Katalizatorius", "Keli raktų komplektai"],
            "Saugumas": ["ESP", "ISOFIX tvirtinimo taškai"]}
            }
}

## URLs & constants.py
All base URLs for skelbiu.lt searches are stored in: constants.py AUTO_URLS list.
You can modify this list to scrape different car makes/models.

##  Features

### ✔ Scrapes paginated listings from Skelbiu.lt
### ✔ Extracts detailed ad information from Autoplius.lt
### ✔ Runs spiders **sequentially**
### ✔ Validates output using **Pydantic**
### ✔ Saves results to `.jsonl`
### ✔ Custom delays, headers, retries
### ✔ Logs all activity to `logs/crawler.log`


## Installation
## Install dependencies:

```bash
pip install -r requirements.txt
```

- if use uv:
```bash
uv pip install -r pyproject.toml
```
---

## Run  the script:

```bash
python3 main.py
```
