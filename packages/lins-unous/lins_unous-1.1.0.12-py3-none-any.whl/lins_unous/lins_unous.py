import os
import requests
import json


class ApiUnous:
    _grant_type = 'password'
    _client_id = 'userIntegration'
    _mindset_user = os.environ.get('MINDSET_USER')
    _mindset_pass = os.environ.get('MINDSET_PASS')
    _mindset_url = os.environ.get('MINDSET_URL')

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_token()}'
        }

    def integrar_produtos(self, list):
        return self._integrar(list, '/StageContent/api/Product/Post')

    def integrar_produtos_tamanhos(self, list):
        return self._integrar(list, '/StageContent/api/ProductSize/Post')

    def integrar_fornecedores(self, list):
        return self._integrar(list, '/StageContent/api/Supplier/Post')

    def integrar_pedidos(self, list):
        self._limpar_pedidos()
        return self._integrar(list, '/StageMetrics/api/OpenOrder/Post')

    def integrar_lojas(self, list):
        return self._integrar(list, '/StageContent/api/Location/Post')

    def integrar_lojas_info(self, list):
        return self._integrar(list, '/StageContent/api/StoreInfo/Post')

    def integrar_metricas(self, list):
        return self._integrar(list, '/StageMetrics/api/Metric/Post')

    def _integrar(self, data, url_endpoint):
        url = self._mindset_url + url_endpoint
        offset = 0
        limit = 10000
        for i in range(int(len(data) / limit) + 1):
            response = requests.post(url=url, data=json.dumps(data[offset:offset + limit]), headers=self.headers)
            if not response.ok:
                break
            offset += limit
        return response.ok, response.json()

    def _limpar_pedidos(self):
        url = self._mindset_url + '/StageContent/api/Supplier/GetClearAllData'
        requests.get(url=url, headers=self.headers)

    def _get_token(self):
        response = requests.get(url=self._mindset_url + '/Auth/token', data={
            "grant_type": self._grant_type,
            "username": self._mindset_user,
            "password": self._mindset_pass,
            "client_id": self._client_id
        })
        return json.loads(response.text).get('access_token')


if __name__ == '__main__':
    unou = ApiUnous()
    produtos = [{'ProductCode': '201',
'BriefDescription': 'VALE MERCADORIA',
'Description': 'PONTA DE ESTOQUE VALE MERCADORIA VALE MERCADORIA', 'SizeCode': 1,
'SupplierCode': None,
'ColorCode': 1,
'ColorDescription': None,
'SupplierProductReference': '',
'LevelCode1': 1,
'LevelDescription1': 'POMPEIA',
'LevelCode2': 3,
'LevelDescription2': 'MIUDEZAS',
'LevelCode3': 1,
'LevelDescription3': 'CONFECCAO INTIMA',
'LevelCode4': 12,
'LevelDescription4': 'PONTA DE ESTOQUE',
'LevelCode5': 1,
'LevelDescription5': 'PONTA DE ESTOQUE',
'CodigoSazonalidade': 1,
'DescricaoSazonalidade': 'PERMANENTE',
'CodigoComprador': 2,
'NomeComprador': 'PATRICIA'}, {'ProductCode': '201035908', 'BriefDescription': 'VALE MERCADORIA', 'Description': 'PONTA DE ESTOQUE VALE MERCADORIA VALE MERCADORIA', 'SizeCode': None, 'SupplierCode': None, 'ColorCode': None, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '202', 'BriefDescription': 'PROMOCAO 2,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 2,00 PONTA ESTOQUE', 'SizeCode': 2, 'SupplierCode': None, 'ColorCode': 2, 'ColorDescription': 'INDEFINIDA', 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '20972806', 'BriefDescription': 'PROMOCAO 2,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 2,00 PONTA ESTOQUE', 'SizeCode': None, 'SupplierCode': None, 'ColorCode': None, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '20972803', 'BriefDescription': 'PROMOCAO 2,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 2,00 PONTA ESTOQUE', 'SizeCode': None, 'SupplierCode': None, 'ColorCode': None, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '20972804', 'BriefDescription': 'PROMOCAO 2,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 2,00 PONTA ESTOQUE', 'SizeCode': None, 'SupplierCode': None, 'ColorCode': None, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '20972805', 'BriefDescription': 'PROMOCAO 2,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 2,00 PONTA ESTOQUE', 'SizeCode': None, 'SupplierCode': None, 'ColorCode': None, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '203', 'BriefDescription': 'PROMOCAO 3,00', 'Description': 'PONTA DE ESTOQUE PROMOCAO 3,00 PONTA ESTOQUE', 'SizeCode': 3, 'SupplierCode': None, 'ColorCode': 3, 'ColorDescription': 'SORTIDAS', 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 3, 'LevelDescription2': 'MIUDEZAS', 'LevelCode3': 1, 'LevelDescription3': 'CONFECCAO INTIMA', 'LevelCode4': 12, 'LevelDescription4': 'PONTA DE ESTOQUE', 'LevelCode5': 1, 'LevelDescription5': 'PONTA DE ESTOQUE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 2, 'NomeComprador': 'PATRICIA'}, {'ProductCode': '20310585', 'BriefDescription': 'CABIDE PRETO KIT 12 PECAS', 'Description': 'CABIDE CABIDE PRETO KIT 12 PECAS CABIDES', 'SizeCode': 4, 'SupplierCode': None, 'ColorCode': 4, 'ColorDescription': 'VERMELHO/MARROM', 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 5, 'LevelDescription2': 'CASA', 'LevelCode3': 4, 'LevelDescription3': 'DECORACAO', 'LevelCode4': 7, 'LevelDescription4': 'CABIDE', 'LevelCode5': 1, 'LevelDescription5': 'CABIDE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 4, 'NomeComprador': 'CLAUDIA'}, {'ProductCode': '204', 'BriefDescription': 'CABIDE PRETO KIT 12 PECAS', 'Description': 'CABIDE CABIDE PRETO KIT 12 PECAS CABIDES', 'SizeCode': 0, 'SupplierCode': None, 'ColorCode': 0, 'ColorDescription': None, 'SupplierProductReference': '', 'LevelCode1': 1, 'LevelDescription1': 'POMPEIA', 'LevelCode2': 5, 'LevelDescription2': 'CASA', 'LevelCode3': 4, 'LevelDescription3': 'DECORACAO', 'LevelCode4': 7, 'LevelDescription4': 'CABIDE', 'LevelCode5': 1, 'LevelDescription5': 'CABIDE', 'CodigoSazonalidade': 1, 'DescricaoSazonalidade': 'PERMANENTE', 'CodigoComprador': 4, 'NomeComprador': 'CLAUDIA'}]
    unou.integrar_produtos(produtos)


