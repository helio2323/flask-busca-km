import unittest
import requests

class TestAPI(unittest.TestCase):
    def test_call_api_multiple_times(self):
        url = 'http://127.0.0.1:5000/km/jundiai/guarulhos'  # Substitua pela sua URL
        for _ in range(10):
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)  # Verifica se a chamada foi bem-sucedida
            print(response.json())  # Imprime o JSON retornado pela API

if __name__ == '__main__':
    unittest.main()
