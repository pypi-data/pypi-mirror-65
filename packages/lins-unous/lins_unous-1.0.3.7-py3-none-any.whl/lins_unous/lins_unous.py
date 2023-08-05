import os
import requests
import json


class ApiUnous:
    grant_type = os.environ.get('GRANT_TYPE')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    client_id = os.environ.get('CLIENT_ID')
    url_metrics = os.environ.get('URL_METRICS')
    url_content = os.environ.get('URL_CONTENT')
    url_token = os.environ.get('URL_TOKEN')
    headers = ''

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_token()}'
        }

    def integrar_produtos(self, list):
        for produto in list:
            self._integrar(produto, '/api/product/post', self.url_content)

    def integrar_produtos_tamanhos(self, list):
        for tamanho in list:
            self._integrar(tamanho, '/api/productSize/post', self.url_content)

    def integrar_fornecedores(self, list):
        for fornecedor in list:
            self._integrar(fornecedor, '/api/openOrder/post', self.url_metrics)

    def integrar_pedidos(self, list):
        self._limpar_pedidos()
        for pedido in list:
            self._integrar(pedido, '/api/Supplier/post', self.url_content)

    def integrar_lojas(self, list):
        for loja in list:
            self._integrar(loja, '/api/Location/Post', self.url_content)

    def integrar_lojas_info(self, list):
        for loja_info in list:
            self._integrar(loja_info, '/api/StoreInfo/Post', self.url_content)

    def integrar_metricas(self, list):
        for metrica in list:
            self._integrar(metrica, '/api/Metric/Post', self.url_content)

    def _integrar(self, data, integrar, url):
        url = url + integrar
        requests.post(url=url, data=json.dumps(data), headers=self.headers)

    def _limpar_pedidos(self):
        url = self.url_content + '/api/Supplier/GetClearAllData'
        requests.get(url=url, headers=self.headers)

    def _get_token(self):
        response = requests.get(url=self.url_token, data={
            "grant_type": self.grant_type,
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id
        })
        return json.loads(response.text).get('access_token')


if __name__ == '__main__':
    unou = ApiUnous()
    unou.integrar_produtos()
