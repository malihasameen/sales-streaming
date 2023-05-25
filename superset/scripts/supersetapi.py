import requests

class SupersetAPIClient:
    
    def __init__(self, host):
        self.base_url = host + "/api/v1"
        self.access_token = ""

    def login(self, username, password):
        payload = {
            "username": username,
            "password": password,
            "provider": "db"
        }

        r = requests.post(url=self.base_url + "/security/login", json=payload)
        r.raise_for_status()

        self.access_token = r.json()["access_token"]
    
    def create_database(self, database_name, driver, engine, sqlalchemy_uri):
        payload = {
            "configuration_method": "sqlalchemy_form",
            "database_name": database_name,
            "driver": driver,
            "engine": engine,
            "sqlalchemy_uri": sqlalchemy_uri
        }

        headers_auth = {
            'Authorization': 'Bearer ' + self.access_token
        }

        r = requests.post(url=self.base_url + "/database", json=payload, headers=headers_auth)
        r.raise_for_status()

        database_id = r.json()['id']
        return database_id

    def create_dataset(self, database_id, schema, table):
        payload = {
            "database": database_id,
            "schema": schema,
            "table_name": table
        }

        headers_auth = {
            'Authorization': 'Bearer ' + self.access_token
        }

        r = requests.post(url=self.base_url + "/dataset", json=payload, headers=headers_auth)
        r.raise_for_status()

        dataset_id = r.json()['id']
        return dataset_id
    
    def create_dashboard(self, title):
        payload = {
            "dashboard_title": title
        }

        headers_auth = {
            'Authorization': 'Bearer ' + self.access_token
        }

        r = requests.post(url=self.base_url + "/dashboard", json=payload, headers=headers_auth)
        r.raise_for_status()

        dashboard_id = r.json()['id']
        return dashboard_id
    
    def create_chart(self, dashboard_ids: list, datasource_id:int, datasource_name:str, params:str, slice_name:str, viz_type:str):
        payload = {
            "dashboards": dashboard_ids,
            "datasource_id": datasource_id,
            "datasource_name": datasource_name,
            "datasource_type": "table",
            "params": params,
            "slice_name": slice_name,
            "viz_type": viz_type
        }

        headers_auth = {
            'Authorization': 'Bearer ' + self.access_token
        }

        r = requests.post(url=self.base_url + "/chart", json=payload, headers=headers_auth)
        r.raise_for_status()

        chart_id = r.json()['id']
        return chart_id
