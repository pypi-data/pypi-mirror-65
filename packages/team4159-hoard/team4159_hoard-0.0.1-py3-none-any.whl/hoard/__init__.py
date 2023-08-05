import requests

API_URL = 'https://hoard-4159.herokuapp.com/hoard/'


class Hoard:
    def __init__(self, name: str):
        self.name = name

    def add_item(self, name: str, amount: int, category: str, description: str = None, image_url: str = None) -> dict:
        params = {
            'name': name,
            'category': category,
            'amount': amount
        }

        if image_url is not None:
            params['imageUrl'] = image_url
        if description is not None:
            params['description'] = description

        return requests.post(API_URL + self.name, params=params).json()

    def get_all_items(self) -> dict:
        return requests.get(API_URL + self.name).json()

    def get_item_by_name(self, name: str) -> dict:
        return requests.get(API_URL + self.name + '/name/' + name).json()

    def get_item_by_id(self, _id: str) -> dict:
        return requests.get(API_URL + self.name + '/id/' + _id).json()

    def get_items_by_category(self, category: str) -> dict:
        return requests.get(API_URL + self.name + '/category/' + category).json()

    def update_item_by_name(self, name: str, **kwargs) -> dict:
        return requests.put(API_URL + self.name + '/name/' + name, params=kwargs).json()

    def update_item_by_id(self, _id: str, **kwargs) -> dict:
        return requests.put(API_URL + self.name + '/id/' + _id, params=kwargs).json()

    def delete_item_by_name(self, name: str) -> dict:
        return requests.delete(API_URL + self.name + '/name/' + name).json()
    
    def delete_item_by_id(self, _id: str) -> dict:
        return requests.delete(API_URL + self.name + '/id/' + _id).json()
