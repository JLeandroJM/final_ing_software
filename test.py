import unittest
from app import routes
from app import app



class TestBilletera(unittest.TestCase):
    #exito
    def test_realizar_pago_exitoso(self):
        
        
        with app.test_client() as client:
            response = client.get('/billetera/pagar?minumero=123&numerodestino=456&valor=50')
            data = response.get_json()
            self.assertEqual(data, {"message": "Pago realizado correctamente"})
    
    def test_saldo_insuficiente(self):
        # error - saldo insuficinete
        with app.test_client() as client:
            response = client.get('/billetera/pagar?minumero=456&numerodestino=789&valor=1000')
            data = response.get_json()
            self.assertEqual(data, {"message": "Cuenta no encontrada"})

    #error - cuenta inexistente
    def test_cuenta_origen_inexistente(self):
      
        with app.test_client() as client:
            response = client.get('/billetera/pagar?minumero=999&numerodestino=123&valor=20')
            data = response.get_json()
            self.assertEqual(data, {"message": "Cuenta no encontrada"})

    #error - cuenta de destino inexistente
    def test_cuenta_destino_inexistente(self):
        
        with app.test_client() as client:
            response = client.get('/billetera/pagar?minumero=123&numerodestino=888&valor=30')
            data = response.get_json()
            self.assertEqual(data, {"message": "Cuenta no encontrada"})

    

