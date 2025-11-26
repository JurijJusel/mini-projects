import scrapy
import json
from crawler.models.autop_models import (
    AutopliusCarModel,
    AutopliusCarParameters,
    AutopliusCarDescription,
    AutopliusCarFeatures)
from crawler.spiders.constants import AUTOP_OUTPUT_FILE, SKELBIU_AUTO_OUTPUT_FILE
from rich import print


class AutopliusSpider(scrapy.Spider):
    """
    Scrapy spider that loads previously collected Autoplius listing URLs
    from a JSONL file, then visits each ad page and extracts detailed car data.

    Output:
        Yields dictionaries compliant with AutopliusCarModel Pydantic schema.
    """
    custom_settings = {
        "FEEDS": {
            AUTOP_OUTPUT_FILE: {
                "format": "jsonlines",
                "encoding": "utf-8",
                "overwrite": True,
            }
        }
    }

    name = "autoplius_spider"

    def start_requests(self):
        """
        Reads AUTOP_OUTPUT_FILE (JSONL format), extracts the 'Link' field from
        each line, and schedules a scrapy.Request for each URL.

        Yields:
            scrapy.Request: Requests to individual Autoplius car listing pages.
        """
        urls = []

        with open(SKELBIU_AUTO_OUTPUT_FILE, "r", encoding="utf-8") as jsonl_file:
            for line in jsonl_file:
                data = json.loads(line)
                link = data.get("Link")
                if link:
                    urls.append(link)

        print(f"Found {len(urls)} URLs to crawl")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Parses a single Autoplius car listing page and extracts:
            • Title
            • Description
            • Price
            • Phone number
            • Car parameters (engine, mileage, year, fuel, gearbox, etc.)
            • Car features (interior, safety, multimedia, etc.)

        Parameters:
            response (scrapy.http.Response): The page response.

        Yields:
            dict: Serialized AutopliusCarModel using `model_dump()`.
        """
        status = response.status

        if status != 200:
            print(f"error Failed to fetch the page, status code: {status}")
            return
        else:
            title = response.css("title::text").get(default="N/A").strip()
            description = (
                response.css("div.announcement-description")
                .xpath("string(.)")
                .get(default="N/A")
                .strip()
            )
            clean_description = description.replace("\r", "").replace("\n", "")
            phone = response.css("div.js-phone-number::text").get(default="N/A").strip()
            price = (
                response.css("div.price::text")
                .get(default="N/A")
                .strip()
                .replace(" ", "")
            )
            id = (
                response.css("span.announcement-id::text")
                .get(default="N/A")
                .strip(" ID:")
            )
            parse_url = response.url

            parameter_data = {}
            rows = response.css("div.parameter-row")
            for row in rows:
                label = row.css("div.parameter-label::text").get(default="N/A").strip()
                value = row.css("div.parameter-value::text").get(default="N/A").strip()
                if label and value:
                    parameter_data[label] = value

            year = parameter_data.get("Pirma registracija", "N/A")
            mileage = parameter_data.get("Rida", "N/A")
            engine = parameter_data.get("Variklis", "N/A")
            fuel = parameter_data.get("Kuro tipas", "N/A")
            body_type = parameter_data.get("Kėbulo tipas", "N/A")
            doors = parameter_data.get("Durų skaičius", "N/A")
            drive = parameter_data.get("Varantieji ratai", "N/A")
            gearbox = parameter_data.get("Pavarų dėžė", "N/A")
            climate_control = parameter_data.get("Klimato valdymas", "N/A")
            color = parameter_data.get("Spalva", "N/A")
            tech_inspection = parameter_data.get("Tech. apžiūra iki", "N/A")
            rim_size = parameter_data.get("Ratlankių skersmuo", "N/A")
            weight = parameter_data.get("Nuosava masė, kg", "N/A")
            seats = parameter_data.get("Sėdimų vietų skaičius", "N/A")
            euro_standard = parameter_data.get("Euro standartas", "N/A")
            co2_emission = parameter_data.get("CO₂ emisija, g/km", "N/A")
            pollution_tax = parameter_data.get("Taršos mokestis", "N/A")
            city_consumption = parameter_data.get("Mieste", "N/A")
            highway_consumption = parameter_data.get("Užmiestyje", "N/A")
            average_consumption = parameter_data.get("Vidutinės", "N/A")

            features_data = {}
            feature_rows = response.css("div.feature-row")
            for row in feature_rows:
                label = row.css("div.feature-label::text").get(default="").strip()
                items = row.css("div.feature-list span.feature-item::text").getall()
                cleaned_items = [item.strip() for item in items if item.strip()]
                if label and cleaned_items:
                    features_data[label] = cleaned_items

            car_data = AutopliusCarModel(
                Id=id,
                Price=price,
                Phone=phone,
                Link=parse_url,
                Title=title,
                Parameters=AutopliusCarParameters(
                    First_Registration=year,
                    Mileage=mileage,
                    Engine=engine,
                    Fuel=fuel,
                    Body_Type=body_type,
                    Doors=doors,
                    Drive=drive,
                    Gearbox=gearbox,
                    Climate_Control=climate_control,
                    Color=color,
                    Tech_Inspection=tech_inspection,
                    Rim_Size=rim_size,
                    Weight=weight,
                    Seats=seats,
                    Euro_Standard=euro_standard,
                    CO2_Emission=co2_emission,
                    Pollution_Tax=pollution_tax,
                    City_Consumption=city_consumption,
                    Highway_Consumption=highway_consumption,
                    Average_Consumption=average_consumption,
                ),
                Description=AutopliusCarDescription(Description=[clean_description]),
                Features=AutopliusCarFeatures(Features=features_data),
            )

            yield car_data.model_dump()

    def closed(self, reason):
        """
        Called automatically when the spider finishes or is stopped.
        Parameters:
            reason (str): Reason for spider shutdown (finished, shutdown, error).
        """
        print("\n\n--- AutopliusSpider Crawl Finished ---")
        print(f"Reason for closure Autoplius crawler: {reason}")
