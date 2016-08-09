from scrapy.item import Item, Field


class NaukriItem(Item):
    link = Field()
    org = Field()
    desig = Field()
    location = Field()
