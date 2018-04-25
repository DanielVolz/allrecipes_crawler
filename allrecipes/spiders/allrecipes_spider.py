import json
import os
import re
import urllib
from decimal import Decimal
import logging

from allrecipes.items import Category, Ingredient, Nutrition, Recipe, Review
from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import TextResponse


class AllrecipesSpider(CrawlSpider):
    name = 'allrecipes'
    # allowed_domains = ['allrecipes.com']
    download_delay = 1.5

    start_urls = [
        # 'https://www.allrecipes.com/recipes/17562/dinner/',
        # 'https://www.allrecipes.com/recipes/80/main-dish/',
        'https://www.allrecipes.com/recipes/1227/everyday-cooking/vegan/',
        'https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/',
    ]

    rules = (
        # Follow pagination
        # Rule(
        #     LinkExtractor(restrict_xpaths="//link[contains(@href, 'page')]"),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(restrict_xpaths=('//link[@rel="next"]', )),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(
        #         allow=(), restrict_css=('head > link:nth-child(13)', )),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(
        #         allow=(), restrict_css=('head > link:nth-child(13)', )),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(restrict_xpaths="//html/head/link[3]"),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(allow=(r'recipes\/.+\/\?page=2', )),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(allow=(r'recipes/.+/\?page=\d+', )),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(allow=(r'.com/recipes/.+/\?page=\d+')),
        #     follow=True,
        #     callback='parse_recipe'),
        # Rule(
        #     LinkExtractor(
        #         tags=('button'), attrs=('href', )), follow=True),

        # Extract recipes
        Rule(LinkExtractor(allow=(r'recipe/\d+.*', )), callback='parse_recipe'),)

    def parse_recipe(self, response):
        logging.debug('Call parse_recipe: ' + response.url)

        page = TextResponse(response.url, headers=response.headers, body=response.body, encoding='utf-8')

        cooke_id = response.headers.getlist(b'Set-Cookie')[1].split(b";")[0].split(b"=")

        headers = {
            'accept': "*/*",
            'user-agent':
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36"
            + "(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'Authorization': "Bearer " + cooke_id[1].decode('utf-8') + "=="
        }

        recipe_url = page.url
        m = re.search('\/recipe\/(\d+)', recipe_url)
        recipe_id = m.group(1)

        category_html = page.xpath("/html/body/script[7]/text()").extract()[0]
        category_html.strip()

        m2 = re.search('RdpInferredTastePrefs\s=\s+(.*])', category_html)

        string_cat = m2.group(1)
        string_cat = string_cat.replace("]", "")
        string_cat = string_cat.replace("[", "")
        string_cat = string_cat.replace("\"", "")
        cat_list = string_cat.split(",")

        # hxs = Selector(response)

        recipe = Recipe()
        categories = []

        for cat in cat_list:
            category = Category()
            category['name'] = cat
            categories.append(category)

        recipe["categories"] = categories

        # review_count = response.xpath(
        #     '//span[@class="review-count"]/text()').extract()[0].strip().split(
        #         ' ')[0]
        #
        # review_url = "http://allrecipes.com/recipe/getreviews/?recipeid=" + recipe_id +
        # "&pagenumber=1&pagesize=" + review_count + "&recipeType=Recipe&sortBy=MostHelpful"

        url = "https://apps.allrecipes.com/v1/recipes/" + recipe_id + "?isMetric=true&servings=4"
        # test = "https://apps.allrecipes.com/v1/recipes/17092/reviews/?page=1&pagesize=324&sorttype=HelpfulCountDescending"

        return Request(
            url,
            method="GET",
            headers=headers,
            callback=self.parse_json,
            meta={'recipe': recipe})

    def parse_json(self, response):

        jsonresponse = json.loads(response.body_as_unicode())
        logging.debug("Call parse_json: recipe_name: "+ jsonresponse["title"]+ " id: "+str(jsonresponse["recipeID"]))

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

        # for nutrition in jsonresponse["nutrition"]:
        #     print nutrition

        nutrients = []

        for nutrient_type in (
                'fat', 'calories', 'cholesterol', 'sodium', 'carbohydrates',
                'protein', 'folate', 'magnesium', 'vitaminB6', 'niacin',
                'thiamin', 'iron', 'calcium', 'vitaminC', 'vitaminA', 'sugars',
                'potassium', 'saturatedFat', 'caloriesFromFat', 'fiber'):

            nutrient = Nutrition()
            nutrient['name'] = jsonresponse['nutrition'][nutrient_type]["name"]
            nutrient['amount'] = jsonresponse['nutrition'][nutrient_type]["amount"]
            nutrient['unit'] = jsonresponse['nutrition'][nutrient_type]["unit"]
            nutrient['display_value'] = jsonresponse['nutrition'][nutrient_type]["displayValue"]
            nutrient['percent_daily_value'] = jsonresponse['nutrition'][nutrient_type]["percentDailyValue"]
            nutrients.append(nutrient)

        recipe["nutritions"] = nutrients
        recipeID = jsonresponse["recipeID"]
        recipe_review_count = jsonresponse["reviewCount"]

        review_url = "https://www.allrecipes.com/recipe/getreviews/?recipeid=" + str(recipeID) + "&pagenumber=1&pagesize=" + str(recipe_review_count) + "&recipeType=Recipe&sortBy=MostHelpful"
        # print review_url
        #download_delay = 5
        if recipe['review_count'] > 6000 or recipe['review_count'] == 0:
            logging.debug("review count too high or 0")
            return
        else:
            return Request(
                review_url,
                method="GET",
                callback=self.parse_reviews,
                meta={'recipe': recipe})


    def parse_reviews(self, response):

        reviews_html = response.xpath('//div[@class="review-container clearfix"]')
        recipe = response.meta['recipe']

        logging.debug("Call parse_reviews: reciepe_name: "+ recipe['name']+" id: "+str(recipe['id']))

        reviews = []

        for items in reviews_html:
            review = Review()
            review['reviewer_name'] = items.xpath(
                'normalize-space(.//h4[@itemprop="author"])').extract_first()
            # reviewer_name = items.xpath('normalize-space(.//h4[@itemprop="author"])').extract_first()
            review['reviewer_id'] = int("".join(
                re.findall('\d+', items.xpath(
                    './/div[@class="recipe-details-cook-stats-container"]/a/@href').extract_first())))
            # reviewer_id = re.findall('\d+', items.xpath('.//div[@class="recipe-details-cook-stats-container"]/a/@href').extract_first())
            review['reviewer_favs'] = int(
                items.xpath(
                    './/ul[@class="cook-details__favorites favorites-count"]/li/format-large-number/@number').extract_first())
            # reviewer_favs = items.xpath('.//ul[@class="cook-details__favorites favorites-count"]/li/format-large-number/@number').extract_first()
            review['reviewer_recipe_made_count'] = int(
                items.xpath(
                    './/ul[@class="cook-details__recipes-made recipes-made-count"]/li/format-large-number/@number').extract_first())
            # reviewer_recipe_made_count = items.xpath('.//ul[@class="cook-details__recipes-made recipes-made-count"]/li/format-large-number/@number').extract_first()
            review['reviewer_recipe_rating'] = int(
                items.xpath(
                    './/meta[@itemprop="ratingValue"]/@content').extract_first())
            # reviewer_recipe_rating = items.xpath('.//meta[@itemprop="ratingValue"]/@content').extract_first()

            reviews.append(review)
            # print reviewer_name
            # print reviewer_id
            # print reviewer_favs
            # print reviewer_recipe_made_count
            # print reviewer_recipe_rating

        recipe["reviews"] = reviews
        logging.debug("Item returned: reciepe_name: "+ recipe['name']+" id: "+str(recipe['id']))
        return recipe
