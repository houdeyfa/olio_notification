import requests
import json

class StoreNameChecker:
    def __init__(self, email, password, exclude='', filter_keyword=''):

        self.session = requests.Session()
        self.username = email
        self.password = password
        self.exclude = exclude
        self.filter_keyword = filter_keyword
        self.login_data = {'email': self.username, 'password': self.password}
        self.re_login()



    def re_login(self):
        self.login_response = self.session.post('https://volunteers.olioex.com/api/v1/sessions', json=self.login_data)

    def look_up_stores(self):

        store_ids = []
        businesses_ids = []
        names = []
        store_id_url_format = ''
        business_id_url_format = ''


        # Get all the collections
        collection_response = self.session.get(
                url='https://volunteers.olioex.com/api/v1/collections?available=true'
        )
        list_of_collects = json.loads(collection_response.text)

        # Get the stores ids from the collections
        for collect in list_of_collects:
            store_ids.append(collect['store_id'])

        # Get the stores objects from the stores ids
        for store_id in set(store_ids):
            store_id_url_format = store_id_url_format + f'ids%5B%5D={store_id}&'
        store_response = self.session.get(f'https://volunteers.olioex.com/api/v1/stores?{store_id_url_format}')
        list_of_stores = json.loads(store_response.text)

        # Get the business ids from the stores objects
        for store in list_of_stores:
            businesses_ids.append(store['business_id'])

        # Get the businesses objects from the businesses ids
        for business_id in set(businesses_ids):
            business_id_url_format = business_id_url_format + f'ids%5B%5D={business_id}&'

        # Get the businesses names from the businesses objects
        business_response = self.session.get(f'https://volunteers.olioex.com/api/v1/businesses?{business_id_url_format}')
        list_of_business = json.loads(business_response.text)
        for business in list_of_business:
            names.append(business['name'])

        return names

    def check(self):
        names = self.look_up_stores()
        if self.exclude != '':
            names_cleaned = [n for n in names if self.exclude not in n]
            names = names_cleaned
        if len(names) == 0:
            return False
        if self.filter_keyword == '':
            return True
        if [n for n in names if self.filter_keyword in n].__len__() > 0:
            return True
        return False
