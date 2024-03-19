import time

import requests
from product import Product
from product import Products


class ParserWB:
    def __init__(self):
        self.params = {
            'TestGroup': 'no_test',
            'TestID': 'no_test',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '27',
            'suppressSpellcheck': 'false'
        }

    def parse(self, query="гитхаб", count=5, min_price="0", max_price="1000000", is_sort_price=False, is_sort_up=True):
        parsed_products = []
        page = 1
        while count > 0:
            params = self.params
            params['query'] = query
            if page != 1:
                params['page'] = str(page)

            if count >= 300:
                params['limit'] = '300'
            else:
                params['limit'] = str(count)

            if min_price != "0" or max_price != "1000000":
                params['priceU'] = min_price + "00"+";"+max_price+"00"

            if is_sort_price:
                if is_sort_up:
                    str_sort = "priceup"
                else:
                    str_sort = "pricedown"
                params['sort'] = str_sort



            waits = 0
            while True:
                try:
                    time.sleep(waits)
                    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/search', params=params)

                    if response.status_code == 200:
                        resp_json = response.json()
                        products = resp_json['data']['products']
                        if len(products) == 0:
                            return Products(parsed_products)

                        prev_count = count
                        for i in range(len(products)):
                            is_find, product = self.__parse_product(products[i]['id'], products[i]['name'],
                                                                    int(products[i]['priceU'] / 100),
                                                                    int(products[i]['salePriceU'] / 100),
                                                                    products[i]['reviewRating'],
                                                                    products[i]['feedbacks'])
                            if is_find:
                                parsed_products.append(product)
                                count -= 1

                        if prev_count == count:
                            raise Exception("Ошибка при запросе к сайту WB")

                        page += 1
                        break

                    else:
                        raise Exception("Ошибка при запросе к сайту WB")

                except Exception:
                    if waits < 5:
                        waits += 1
                    continue

        return Products(parsed_products)



    def __create_link(self, id):
        return f"https://www.wildberries.ru/catalog/{id}/detail.aspx"

    def __parse_product(self, id, name, old_price, new_price, rating, feedbacks):
        link = self.__create_link(id)
        part = int(id / 1000)
        vol = int(part / 100)
        basket = self.__get_basket(vol)
        basket_url = self.__get_basket_url(basket, vol, part, id)
        img_s = self.__get_small_img_url(basket_url)
        img_b = self.__get_big_img_url(basket_url)
        card_url = self.__get_info_card_url(basket_url)

        try:
            response = requests.get(card_url)
            if response.status_code == 200:
                resp_json = response.json()
                desc = resp_json['description']
                category = resp_json['subj_root_name']
                product_name = resp_json['subj_name']
            else:
                raise Exception("Ошибка при запросе к сайту WB")

        except Exception:
            return False, Product()

        return True, Product(link=link, name=name, old_price=old_price, new_price=new_price, rating=rating,
                       feedbacks=feedbacks, img_s=img_s, img_b=img_b, desc=desc, category=category, product_name=product_name)

    def __get_basket_url(self, basket, vol, part, id):
        return f"https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{id}/"

    def __get_info_card_url(self, basket_url):
        return basket_url + "info/ru/card.json"

    def __get_big_img_url(self, basket_url):
        return basket_url + "images/big/1.webp"

    def __get_small_img_url(self, basket_url):
        return basket_url + "images/c246x328/1.webp"

    def __get_basket(self, e):
        if e >= 0 and e <= 143:
            return "01"
        elif e >= 144 and e <= 287:
            return "02"
        elif e >= 288 and e <= 431:
            return "03"
        elif e >= 432 and e <= 719:
            return "04"
        elif e >= 720 and e <= 1007:
            return "05"
        elif e >= 1008 and e <= 1061:
            return "06"
        elif e >= 1062 and e <= 1115:
            return "07"
        elif e >= 1116 and e <= 1169:
            return "08"
        elif e >= 1170 and e <= 1313:
            return "09"
        elif e >= 1314 and e <= 1601:
            return "10"
        elif e >= 1602 and e <= 1655:
            return "11"
        elif e >= 1656 and e <= 1919:
            return "12"
        elif e >= 1920 and e <= 2045:
            return "13"
        elif e >= 2046 and e <= 2189:
            return "14"
        elif e >= 2091 and e <= 2405:
            return "15"
        else:
            return "16"
