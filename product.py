from typing import List


class Product:
    def __init__(self, name="", old_price=0, new_price=0, desc="", img_s="", img_b="", category="", product_name="", link="", rating=0,
                 feedbacks=0):
        self.name = name
        self.old_price = old_price
        self.new_price = new_price
        self.desc = desc
        self.img_s = img_s
        self.img_b = img_b
        self.category = category
        self.product_name = product_name
        self.link = link
        self.rating = rating
        self.feedbacks = feedbacks

    def class_to_dict(self):
        return self.__dict__


class Products:
    def __init__(self, products: List[Product]):
        for i in range(len(products)):
            products[i] = products[i].class_to_dict()

        self.products = products

    def class_to_dict(self):
        return self.__dict__
