import os
import re
import urlparse
import urllib
import json
import scrapy


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request

from allrecipes.items import Recipe, Ingredient, Category, Nutrition


class AllrecipesSpider2(scrapy.Spider):
    name = 'allrecipes2'
    allowed_domains = ['allrecipes.com']
    download_delay = 1


    start_urls = [
        'http://allrecipes.com/recipes/722/world-cuisine/european/german/page=1',
        'http://allrecipes.com/recipes/80/main-dish/'
    ]


    def parse(self, response):

        cook1 = response.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")

        headers = {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'Authorization': "Bearer " + cook1[1] + "=="
        }

        url2 = response.url
        m = re.search('\/recipe\/(\d+)', url2)

        cattext = response.xpath("/html/body/script[7]/text()").extract()[0]
        cattext.strip()

        m2 = re.search('RdpInferredTastePrefs\s=\s+(.*])', cattext)

        string_cat = m2.group(1)
        string_cat = string_cat.replace("]", "")
        string_cat = string_cat.replace("[", "")
        string_cat = string_cat.replace("\"", "")
        cat_list = string_cat.split(",")

        url = "https://apps.allrecipes.com/v1/recipes/" + m.group(1) + "?isMetric=true&servings=4"

        hxs = Selector(response)
        recipe = Recipe()


        categories = []

        for cat in cat_list:
            category = Category()
            category['name'] = cat
            categories.append(category)

        recipe["categories"] = categories

        print {"page": response.url}
        yield Request(url, method="GET", headers=headers, callback=self.parse_json, meta={'recipe': recipe})


    def parse_json(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        recipe = response.meta['recipe']
        recipe["name"] = jsonresponse["title"]
        recipe['id'] = jsonresponse["recipeID"]
        recipe["authorId"] = jsonresponse["submitter"]["userID"]
        recipe["author"] = jsonresponse["submitter"]["name"]
        recipe["description"] = jsonresponse["description"]
        recipe["prep_time"] = jsonresponse["prepMinutes"]
        recipe["cook_time"] = jsonresponse["cookMinutes"]
        recipe["ready_in_time"] = jsonresponse["readyInMinutes"]
        recipe["servings"] = jsonresponse["servings"]
        recipe["rating"] = jsonresponse["ratingAverage"]
        recipe["rating_count"] = jsonresponse["ratingCount"]
        recipe["review_count"] = jsonresponse["reviewCount"]
        recipe["made_it_count"] = jsonresponse["madeItCount"]
        recipe["api_url"] = jsonresponse["links"]["self"]["href"]
        recipe["url"] = jsonresponse["links"]["recipeUrl"]["href"]

        ingredients = []

        for ing in jsonresponse["ingredients"]:
            ingredient = Ingredient()
            ingredient['id'] = ing["ingredientID"]
            ingredient['name'] = ing["displayValue"]
            ingredient['grams'] = ing["grams"]
            ingredient['type'] = ing["displayType"]
            ingredients.append(ingredient)
        recipe['ingredients'] = ingredients

        for nutrition in jsonresponse["nutrition"]:
            print nutrition

        nutrients = []

        for nutrient_type in ('fat', 'calories', 'cholesterol', 'sodium',
                              'carbohydrates', 'protein', 'folate', 'magnesium', 'vitaminB6', 'niacin',
                               'thiamin', 'iron', 'calcium', 'vitaminC', 'vitaminA', 'sugars', 'potassium',
                               'saturatedFat', 'caloriesFromFat', 'fiber' ):

            nutrient = Nutrition()
            nutrient['name'] = jsonresponse['nutrition'][nutrient_type]["name"]
            nutrient['amount'] = jsonresponse['nutrition'][nutrient_type]["amount"]
            nutrient['unit'] = jsonresponse['nutrition'][nutrient_type]["unit"]
            nutrient['display_value'] = jsonresponse['nutrition'][nutrient_type]["displayValue"]
            nutrient['percent_daily_value'] = jsonresponse['nutrition'][nutrient_type]["percentDailyValue"]
            nutrients.append(nutrient)


        recipe["nutritions"] = nutrients

        return recipe

        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
