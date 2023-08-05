import requests
from bs4 import BeautifulSoup
from requests import Response
from typing import List

from . import exceptions, constants
from .decorators import safe_parsing


class Parser:
    @staticmethod
    def _make_request(uri: str, params: dict = None, catch404=False) -> Response:
        request_url = constants.DEFAULT_URL + uri
        response = requests.get(request_url, params)

        if catch404 and response.status_code == 404:
            raise exceptions.PageNotFound(request_url)

        response.raise_for_status()

        if True in [e in response.text for e in constants.ERROR_STRINGS]:
            raise exceptions.TemporaryUnavailable()
        return response

    @safe_parsing
    def get_catalogs(self) -> List[dict]:
        catalogs, soup = [], BeautifulSoup(self._make_request('/').content, 'html.parser')

        for catalog_element in soup.select('nav li.dropmenu__list--item.hasDrop'):
            catalog_link_element = catalog_element.select_one('.item__link')

            catalogs.append({
                'id': int(catalog_link_element['href'].split('/')[2]),
                'name': catalog_link_element.text.replace('\t', '').strip().capitalize(),
                'catalogs': []
            })

            for child_catalog_link_element in catalog_element.select('.list__item--link'):
                catalogs[-1]['catalogs'].append({
                    'id': int(child_catalog_link_element['href'].split('/')[2]),
                    'name': child_catalog_link_element.text.replace('\t', '').strip().capitalize()
                })

        return catalogs

    @safe_parsing
    def get_catalog(self, catalog_id: int) -> dict:
        try:
            response = self._make_request(f'/catalog/{catalog_id}/', params={'SHOWALL_1': 1}, catch404=True)
        except exceptions.PageNotFound:
            raise exceptions.CatalogNotFound(catalog_id)

        soup = BeautifulSoup(response.content, 'html.parser')

        catalog = {
            'id': catalog_id, 'products': [], 'catalogs': [],
            'name': soup.select_one('.page-header').text.replace('\n', '')
        }

        for product_element in soup.select('.js-product'):
            product = {
                'id': int(product_element.select_one('.item__link')['href'].split('/')[-2]),
                'url': constants.DEFAULT_URL + product_element.select_one('.item__link')['href'],
                'image_url': constants.DEFAULT_URL + product_element.select_one('.item__pic--in img')['src'],
                'name': product_element.select_one('.item__title--wrap').text.strip()
            }

            product_outer_price_element = product_element.select_one('.item__price')
            product_common_price_element = product_outer_price_element.select_one('s')

            if product_common_price_element:
                product['common_price'] = float(product_common_price_element.text.strip().split()[0].replace(',', ''))
                product['discount_price'] = float(product_outer_price_element.text.strip().split()[0])
            else:
                product['common_price'] = float(product_outer_price_element.text.strip().split()[0])
                product['discount_price'] = None

            catalog['products'].append(product)

        for catalog_link_element in soup.select('.as-categories a'):
            catalog['catalogs'].append({
                'id': int(catalog_link_element['href'].split('/')[-2]),
                'url': constants.DEFAULT_URL + catalog_link_element['href'],
                'name': catalog_link_element.text.strip()
            })

        return catalog

    @safe_parsing
    def get_product(self, catalog_id: int, product_id: int) -> dict:
        try:
            response = self._make_request(f'/catalog/{catalog_id}/{product_id}/', catch404=True)
        except exceptions.PageNotFound:
            raise exceptions.ProductNotFound(catalog_id, product_id)

        soup = BeautifulSoup(response.content, 'html.parser')

        product = {
            'id': product_id, 'catalog_id': catalog_id,
            'name': soup.select_one('.card-b__title').text,
            'article': int(soup.select_one('.card-b__article').text[5:]),
            'image_url': None
        }

        if (image_uri := soup.select_one('.fotorama img')['src']) != constants.NOPHOTO_URI:
            product['image_url'] = constants.DEFAULT_URL + image_uri

        product['common_price'], product['discount_price'] = None, None

        if price_input_value := soup.select_one('.js--price-current')['value']:
            product['common_price'] = float(price_input_value)

            if price_element := soup.select_one('.card-b__price-count_old'):
                product['discount_price'] = float(price_element.text.split('\xa0')[0].replace(' ', ''))
                product['discount_price'], product['common_price'] = product['common_price'], product['discount_price']

        availability_type = soup.select_one('.card-b__count').text.strip().lower()
        product['is_available'] = constants.PRODUCT_AVAILABILITY_STATES[availability_type]

        return product
