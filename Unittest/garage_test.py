# test_garage.py
import unittest
from unittest.mock import Mock, patch
import sys
import tkinter as tk

sys.path.append('.')

import garage

class TestGarageFunctions(unittest.TestCase):

    def setUp(self):
        """Configuración antes de cada test"""
        # Mock del terminal
        self.mock_terminal = Mock()
        self.mock_terminal.delete = Mock()
        
        # Mock de user_key
        self.mock_user_key = b"fake_user_key_32_bytes_123456789"
        
        # Datos de usuario de prueba
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
                    "upgrades": [
                        {"name": "Turbo Boost"},
                        {"name": "Sports Exhaust"}
                    ]
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
                    "upgrades": [
                        {"name": "Cold Air Intake"}
                    ]
                }
            ],
            "points": 100000
        }
        
        # Resetear variable global antes de cada test
        garage.selected_garage_car = 0

    def tearDown(self):
        """Limpieza después de cada test"""
        garage.selected_garage_car = 0

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_success(self, mock_load_data, mock_type_text):
        """Test: Visualización exitosa de coche en garage"""
        mock_load_data.return_value = self.sample_user_data
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Verificar que se limpió el terminal
        self.mock_terminal.delete.assert_called_with("1.0", tk.END)
        
        # Verificar que se cargaron los datos
        mock_load_data.assert_called_once_with("fake_path", self.mock_user_key, self.mock_terminal)
        
        # Verificar que se mostró el coche
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        
        # Verificar contenido del mensaje
        self.assertIn("Toyota Supra", call_args)
        self.assertIn("Velocidad: 80", call_args)
        self.assertIn("Manejo: 70", call_args)
        self.assertIn("Aceleración: 85", call_args)
        self.assertIn("Frenada: 65", call_args)
        self.assertIn("- Turbo Boost", call_args)
        self.assertIn("- Sports Exhaust", call_args)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_no_cars(self, mock_load_data, mock_type_text):
        """Test: Garage sin coches"""
        user_data_no_cars = {
            "username": "testuser",
            "garage": [],
            "points": 100000
        }
        mock_load_data.return_value = user_data_no_cars
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_with(self.mock_terminal, "Actualmente no tienes coches\n")

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_no_upgrades(self, mock_load_data, mock_type_text):
        """Test: Coche sin mejoras"""
        mock_load_data.return_value = self.sample_user_data
        
        # Cambiar al segundo coche (Nissan Skyline sin mejoras)
        garage.selected_garage_car = 1
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("Nissan Skyline", call_args)
        self.assertIn("Mejoras:     (Sin mejoras)", call_args)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_load_data_fails(self, mock_load_data, mock_type_text):
        """Test: Fallo al cargar datos encriptados"""
        mock_load_data.return_value = None  # Simular fallo
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # No debería llamar a type_text si load_encrypted_data falla
        mock_type_text.assert_not_called()

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_index_boundary_upper(self, mock_load_data, mock_type_text):
        """Test: Navegación en límite superior del índice"""
        mock_load_data.return_value = self.sample_user_data
        
        # Establecer índice al final
        garage.selected_garage_car = 3  # Más allá del último índice
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Debería resetear a 0
        self.assertEqual(garage.selected_garage_car, 0)
        mock_type_text.assert_called_once()

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_type_garage_car_index_boundary_lower(self, mock_load_data, mock_type_text):
        """Test: Navegación en límite inferior del índice"""
        mock_load_data.return_value = self.sample_user_data
        
        # Establecer índice negativo
        garage.selected_garage_car = -1
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Debería ir al último coche
        self.assertEqual(garage.selected_garage_car, len(self.sample_user_data["garage"]) - 1)
        mock_type_text.assert_called_once()

    @patch('garage.type_garage_car')
    def test_next_garage_car(self, mock_type_garage):
        """Test: Navegación al siguiente coche"""
        initial_position = garage.selected_garage_car
        
        garage.next_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Verificar que se incrementó el índice
        self.assertEqual(garage.selected_garage_car, initial_position + 1)
        # Verificar que se llamó a type_garage_car
        mock_type_garage.assert_called_once_with("fake_path", self.mock_terminal, self.mock_user_key)

    @patch('garage.type_garage_car')
    def test_previous_garage_car(self, mock_type_garage):
        """Test: Navegación al coche anterior"""
        initial_position = garage.selected_garage_car
        
        garage.previous_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Verificar que se decrementó el índice
        self.assertEqual(garage.selected_garage_car, initial_position - 1)
        # Verificar que se llamó a type_garage_car
        mock_type_garage.assert_called_once_with("fake_path", self.mock_terminal, self.mock_user_key)

    @patch('garage.type_garage_car')
    def test_navigation_sequence(self, mock_type_garage):
        """Test: Secuencia completa de navegación"""
        # Navegar hacia adelante varias veces
        garage.next_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        self.assertEqual(garage.selected_garage_car, 1)
        
        garage.next_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        self.assertEqual(garage.selected_garage_car, 2)
        
        # Navegar hacia atrás
        garage.previous_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        self.assertEqual(garage.selected_garage_car, 1)
        
        # Verificar que se llamó a type_garage_car cada vez
        self.assertEqual(mock_type_garage.call_count, 3)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_garage_car_display_format(self, mock_load_data, mock_type_text):
        """Test: Formato de visualización del coche"""
        mock_load_data.return_value = self.sample_user_data
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Verificar el formato completo del mensaje
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        
        expected_lines = [
            "--- Toyota Supra ---",
            "Velocidad: 80",
            "Manejo: 70", 
            "Aceleración: 85",
            "Frenada: 65",
            "Mejoras:",
            "    - Turbo Boost",
            "    - Sports Exhaust"
        ]
        
        for line in expected_lines:
            self.assertIn(line, call_args)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_single_car_garage(self, mock_load_data, mock_type_text):
        """Test: Garage con un solo coche"""
        single_car_data = {
            "username": "testuser",
            "garage": [
                {
                    "brand": "Mazda",
                    "model": "RX-7",
                    "stats": {
                        "speed": 85,
                        "handling": 90,
                        "acceleration": 80,
                        "braking": 70
                    },
                    "upgrades": []
                }
            ],
            "points": 50000
        }
        mock_load_data.return_value = single_car_data
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("Mazda RX-7", call_args)
        self.assertIn("Mejoras:     (Sin mejoras)", call_args)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_navigation_wrap_around(self, mock_load_data, mock_type_text):
        """Test: Navegación que da la vuelta a la lista"""
        mock_load_data.return_value = self.sample_user_data
        
        # Test 1: Del último al primero (wrap around forward)
        garage.selected_garage_car = 2  # Último coche
        
        # next_garage_car incrementa a 3 y llama a type_garage_car
        garage.next_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # type_garage_car corrige 3 a 0 (porque 3 == len(garage) que es 3)
        self.assertEqual(garage.selected_garage_car, 0)
        
        # Verificar que se mostró el primer coche
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("Toyota Supra", call_args)
        
        # Test 2: Del primero al último (wrap around backward)
        mock_type_text.reset_mock()
        garage.selected_garage_car = 0  # Primer coche
        
        # previous_garage_car decrementa a -1 y llama a type_garage_car
        garage.previous_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        # type_garage_car corrige -1 a 2 (último coche)
        self.assertEqual(garage.selected_garage_car, 2)
        
        # Verificar que se mostró el último coche
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("Honda Civic", call_args)

    @patch('garage.type_text')
    @patch('garage.load_encrypted_data')
    def test_empty_upgrades_list_display(self, mock_load_data, mock_type_text):
        """Test: Visualización correcta de lista de mejoras vacía"""
        car_with_empty_upgrades = {
            "username": "testuser",
            "garage": [
                {
                    "brand": "Subaru",
                    "model": "Impreza",
                    "stats": {
                        "speed": 78,
                        "handling": 85,
                        "acceleration": 82,
                        "braking": 75
                    },
                    "upgrades": []  # Lista vacía explícita
                }
            ],
            "points": 75000
        }
        mock_load_data.return_value = car_with_empty_upgrades
        
        garage.type_garage_car("fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("Mejoras:     (Sin mejoras)", call_args)

if __name__ == '__main__':
    unittest.main()