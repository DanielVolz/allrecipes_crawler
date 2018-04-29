# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Review(Item):
    reviewer_name = Field()
    reviewer_id = Field()
    recipe_id = Field()
    reviewer_favs = Field()
    reviewer_recipe_made_count = Field()
    reviewer_recipe_rating = Field()


class Nutrition(Item):
    name = Field()
    amount = Field()
    unit = Field()
    display_value = Field()
    percent_daily_value = Field()


class Category(Item):
    name = Field()


class Ingredient(Item):
    name = Field()
    grams = Field()
    id = Field()
    type = Field()


class Recipe(Item):
    id = Field()
    name = Field()
    author = Field()
    authorId = Field()
    description = Field()
    ingredients = Field()
    nutritions = Field()
    reviews = Field()
    instructions = Field()
    published_date = Field()
    updated_date = Field()
    categories = Field()
    prep_time = Field()
    cook_time = Field()
    ready_in_time = Field()
    servings = Field()
    rating = Field()
    rating_count = Field()
    review_count = Field()
    made_it_count = Field()
    nutrients = Field()
    api_url = Field()
    url = Field()
