from .parser import Parser

__all__ = [
    'get_catalogs', 'get_catalog', 'get_product'
]

parser = Parser()

get_catalogs = parser.get_catalogs
get_catalog = parser.get_catalog
get_product = parser.get_product
