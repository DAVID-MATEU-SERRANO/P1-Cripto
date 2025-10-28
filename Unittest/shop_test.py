# test_shop.py
import unittest
from unittest.mock import Mock, patch
import sys
import tkinter as tk

sys.path.append('.')

import shop

class TestShopFunctions(unittest.TestCase):

    def setUp(self):
        """Configuración antes de cada test"""
        self.mock_terminal = Mock()
        self.mock_terminal.delete = Mock()
        
        self.mock_user_key = b"fake_user_key_32_bytes_123456789"
        
        self.sample_car_data = [
            {
                "brand": "Toyota",
                "model": "Supra",
                "stats": {
                    "speed": 80,
                    "handling": 70,
                    "acceleration": 85, 
                    "braking": 65
                },
                "cost": 50000,
                "upgrades": []
            },
            {
                "brand": "Nissan",
                "model": "Skyline", 
                "stats": {
                    "speed": 75,
                    "handling": 80,
                    "acceleration": 70,
                    "braking": 75
                },
                "cost": 45000,
                "upgrades": []
            },
            {
                "brand": "Honda",
                "model": "Civic",
                "stats": {
                    "speed": 65,
                    "handling": 75,
                    "acceleration": 80,
                    "braking": 70
                },
                "cost": 30000,
                "upgrades": []
            }
        ]
        
        self.sample_upgrade_data = [
            {
                "name": "Turbo Boost",
                "effects": {
                    "speed": 15,
                    "handling": 5,
                    "acceleration": 10,
                    "braking": 0
                },
                "cost": 15000
            },
            {
                "name": "Sports Suspension",
                "effects": {
                    "speed": 5,
                    "handling": 15,
                    "acceleration": 5,
                    "braking": 10
                },
                "cost": 12000
            },
            {
                "name": "Nitrous Oxide",
                "effects": {
                    "speed": 10,
                    "handling": 0,
                    "acceleration": 20,
                    "braking": -5
                },
                "cost": 20000
            }
        ]
        
        self.sample_user_data = {
            "username": "testuser",
            "garage": [
                {
                    "brand": "Toyota",
                    "model": "Supra",
                    "stats": {
                        "speed": 80,
                        "handling": 70,
                        "acceleration": 85,
                        "braking": 65
                    },
                    "upgrades": []
                }
            ],
            "points": 100000
        }
        
        shop.selected_car = 0
        shop.selected_upgrade = 0

    def tearDown(self):
        """Limpieza después de cada test"""
        shop.selected_car = 0
        shop.selected_upgrade = 0

    # Tests para funciones de coches
    @patch('shop.type_text')
    def test_type_car_success(self, mock_type_text):
        """Test: Visualización exitosa de coche"""
        shop.type_car(self.sample_car_data, self.mock_terminal)
        
        self.mock_terminal.delete.assert_called_with("1.0", tk.END)
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        
        self.assertIn("Toyota Supra", call_args)
        self.assertIn("Velocidad: 80", call_args)
        self.assertIn("Manejo: 70", call_args)
        self.assertIn("Aceleración: 85", call_args)
        self.assertIn("Frenada: 65", call_args)
        self.assertIn("Precio: 50000 puntos", call_args)

    @patch('shop.type_car')
    def test_next_car(self, mock_type_car):
        """Test: Navegación al siguiente coche"""
        shop.next_car(self.sample_car_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_car, 1)
        mock_type_car.assert_called_once_with(self.sample_car_data, self.mock_terminal)

    @patch('shop.type_car')
    def test_next_car_wrap_around(self, mock_type_car):
        """Test: Navegación al siguiente coche con wrap around"""
        shop.selected_car = len(self.sample_car_data) - 1  
        
        shop.next_car(self.sample_car_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_car, 0)  
        mock_type_car.assert_called_once()

    @patch('shop.type_car')
    def test_previous_car(self, mock_type_car):
        """Test: Navegación al coche anterior"""
        shop.selected_car = 1
        
        shop.previous_car(self.sample_car_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_car, 0)
        mock_type_car.assert_called_once_with(self.sample_car_data, self.mock_terminal)

    @patch('shop.type_car')
    def test_previous_car_wrap_around(self, mock_type_car):
        """Test: Navegación al coche anterior con wrap around"""
        shop.selected_car = 0 
        
        shop.previous_car(self.sample_car_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_car, len(self.sample_car_data) - 1)  
        mock_type_car.assert_called_once()

    @patch('shop.type_text')
    @patch('shop.store_encrypted_data')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_car_success(self, mock_load_data, mock_car_exists, mock_store_encrypted, mock_type_text):
        """Test: Compra exitosa de coche"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (False, 0)  
        
        shop.selected_car = 1  
        shop.buy_car(self.sample_car_data, "fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_store_encrypted.assert_called_once()
        saved_data = mock_store_encrypted.call_args[0][0]
        
        # Verificar cambios
        self.assertEqual(len(saved_data["garage"]), 2)  
        self.assertEqual(saved_data["points"], 100000 - 45000)  
        self.assertEqual(saved_data["garage"][1]["model"], "Skyline")  
        
        mock_type_text.assert_called_with(self.mock_terminal, "Nissan Skyline añadido a tu garaje\n")

    @patch('shop.type_text')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_car_already_owned(self, mock_load_data, mock_car_exists, mock_type_text):
        """Test: Compra de coche ya comprado"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (True, 0)  
        
        shop.buy_car(self.sample_car_data, "fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_with(self.mock_terminal, "Ya has comprado este coche.\nElige otro\n")

    @patch('shop.type_text')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_car_insufficient_points(self, mock_load_data, mock_car_exists, mock_type_text):
        """Test: Compra de coche sin puntos suficientes"""
        user_data_low_points = self.sample_user_data.copy()
        user_data_low_points["points"] = 10000  
        
        mock_load_data.return_value = user_data_low_points
        mock_car_exists.return_value = (False, 0)
        
        shop.selected_car = 0  
        shop.buy_car(self.sample_car_data, "fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "No tienes suficientes puntos para comprar este coche\nTe faltan 40000 puntos\n."
        )

    # Tests para funciones de mejoras
    @patch('shop.type_text')
    def test_type_upgrade_success(self, mock_type_text):
        """Test: Visualización exitosa de mejora"""
        shop.type_upgrade(self.sample_upgrade_data, self.mock_terminal)
        
        self.mock_terminal.delete.assert_called_with("1.0", tk.END)
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        
        self.assertIn("Turbo Boost", call_args)
        self.assertIn("Velocidad: 15", call_args)
        self.assertIn("Manejo: 5", call_args)
        self.assertIn("Aceleración: 10", call_args)
        self.assertIn("Frenada: 0", call_args)
        self.assertIn("Precio: 15000 puntos", call_args)

    @patch('shop.type_upgrade')
    def test_next_upgrade(self, mock_type_upgrade):
        """Test: Navegación a siguiente mejora"""
        shop.next_upgrade(self.sample_upgrade_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_upgrade, 1)
        mock_type_upgrade.assert_called_once_with(self.sample_upgrade_data, self.mock_terminal)

    @patch('shop.type_upgrade')
    def test_next_upgrade_wrap_around(self, mock_type_upgrade):
        """Test: Navegación a siguiente mejora con wrap around"""
        shop.selected_upgrade = len(self.sample_upgrade_data) - 1 
        
        shop.next_upgrade(self.sample_upgrade_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_upgrade, 0) 
        mock_type_upgrade.assert_called_once()

    @patch('shop.type_upgrade')
    def test_previous_upgrade(self, mock_type_upgrade):
        """Test: Navegación a mejora anterior"""
        shop.selected_upgrade = 1
        
        shop.previous_upgrade(self.sample_upgrade_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_upgrade, 0)
        mock_type_upgrade.assert_called_once_with(self.sample_upgrade_data, self.mock_terminal)

    @patch('shop.type_upgrade')
    def test_previous_upgrade_wrap_around(self, mock_type_upgrade):
        """Test: Navegación a mejora anterior con wrap around"""
        shop.selected_upgrade = 0  
        
        shop.previous_upgrade(self.sample_upgrade_data, self.mock_terminal)
        
        self.assertEqual(shop.selected_upgrade, len(self.sample_upgrade_data) - 1) 
        mock_type_upgrade.assert_called_once()

    @patch('shop.type_text')
    @patch('shop.store_encrypted_data')
    @patch('shop.upgrade_exists')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_upgrade_success(self, mock_load_data, mock_car_exists, mock_upgrade_exists, 
                                mock_store_encrypted, mock_type_text):
        """Test: Compra exitosa de mejora"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (True, 0)  
        mock_upgrade_exists.return_value = False  
        
        shop.selected_upgrade = 0  
        shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "Supra", self.mock_user_key)
        
        mock_store_encrypted.assert_called_once()
        saved_data = mock_store_encrypted.call_args[0][0]
        
        self.assertEqual(len(saved_data["garage"][0]["upgrades"]), 1)  
        self.assertEqual(saved_data["points"], 100000 - 15000)  
        self.assertEqual(saved_data["garage"][0]["upgrades"][0]["name"], "Turbo Boost")  
        
        self.assertEqual(saved_data["garage"][0]["stats"]["speed"], 80 + 15)
        self.assertEqual(saved_data["garage"][0]["stats"]["handling"], 70 + 5)
        self.assertEqual(saved_data["garage"][0]["stats"]["acceleration"], 85 + 10)
        self.assertEqual(saved_data["garage"][0]["stats"]["braking"], 65 + 0)
        
        mock_type_text.assert_called_with(self.mock_terminal, "Turbo Boost añadido a tu Toyota Supra\n")

    @patch('shop.type_text')
    @patch('shop.upgrade_exists')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_upgrade_already_installed(self, mock_load_data, mock_car_exists, mock_upgrade_exists, mock_type_text):
        """Test: Compra de mejora ya instalada"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (True, 0)
        mock_upgrade_exists.return_value = True  
        
        shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "Supra", self.mock_user_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "Tu Supra ya cuenta con Turbo Boost\n"
        )

    @patch('shop.type_text')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_upgrade_car_not_exists(self, mock_load_data, mock_car_exists, mock_type_text):
        """Test: Compra de mejora para coche inexistente"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (False, 0)  
        
        shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "Skyline", self.mock_user_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "No tienes este coche en tu garaje\n"
        )

    @patch('shop.type_text')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_upgrade_empty_car_selected(self, mock_load_data, mock_car_exists, mock_type_text):
        """Test: Compra de mejora sin especificar coche"""
        mock_load_data.return_value = self.sample_user_data
        
        shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "", self.mock_user_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "Indique el coche al que quiere instalar la mejora\n"
        )

    @patch('shop.type_text')
    @patch('shop.upgrade_exists')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_upgrade_insufficient_points(self, mock_load_data, mock_car_exists, mock_upgrade_exists, mock_type_text):
        """Test: Compra de mejora sin puntos suficientes"""
        user_data_low_points = self.sample_user_data.copy()
        user_data_low_points["points"] = 10000  
        
        mock_load_data.return_value = user_data_low_points
        mock_car_exists.return_value = (True, 0)
        mock_upgrade_exists.return_value = False
        
        shop.selected_upgrade = 0  
        shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "Supra", self.mock_user_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "No tienes suficientes puntos para comprar este coche\nTe faltan 5000 puntos\n."
        )


    # Tests para casos edge
    @patch('shop.type_text')
    @patch('shop.store_encrypted_data')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_car_negative_stats_upgrade(self, mock_load_data, mock_car_exists, mock_store_encrypted, mock_type_text):
        """Test: Compra de mejora con estadísticas negativas"""
        mock_load_data.return_value = self.sample_user_data
        mock_car_exists.return_value = (True, 0)
        
        with patch('shop.upgrade_exists') as mock_upgrade_exists:
            mock_upgrade_exists.return_value = False
            
            shop.selected_upgrade = 2 
            shop.buy_upgrade(self.sample_upgrade_data, self.mock_terminal, "fake_path", "Supra", self.mock_user_key)

            saved_data = mock_store_encrypted.call_args[0][0]
            self.assertEqual(saved_data["garage"][0]["stats"]["braking"], 65 - 5) 

    @patch('shop.type_text')
    @patch('shop.store_encrypted_data')
    @patch('shop.car_exists')
    @patch('shop.load_encrypted_data')
    def test_buy_car_empty_garage(self, mock_load_data, mock_car_exists, mock_store_encrypted, mock_type_text):
        """Test: Compra de coche con garage vacío"""
        user_data_empty_garage = {
            "username": "testuser",
            "garage": [],
            "points": 100000
        }
        
        mock_load_data.return_value = user_data_empty_garage
        mock_car_exists.return_value = (False, 0)
        
        shop.buy_car(self.sample_car_data, "fake_path", self.mock_terminal, self.mock_user_key)
        
        saved_data = mock_store_encrypted.call_args[0][0]
        self.assertEqual(len(saved_data["garage"]), 1)
        self.assertEqual(saved_data["garage"][0]["model"], "Supra")

if __name__ == '__main__':
    unittest.main()