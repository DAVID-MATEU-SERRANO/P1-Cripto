# test_points.py
import unittest
from unittest.mock import Mock, patch
import sys

sys.path.append('.')

import points

class TestPointsFunctions(unittest.TestCase):

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
                    "stats": {"speed": 80, "handling": 70, "acceleration": 85, "braking": 65},
                    "upgrades": []
                }
            ],
            "points": 100000
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('points.type_text')
    @patch('points.load_encrypted_data')
    def test_type_points_success(self, mock_load_data, mock_type_text):
        """Test: Visualización exitosa de puntos"""
        mock_load_data.return_value = self.sample_user_data
        
        points.type_points("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Verificar que se cargaron los datos
        mock_load_data.assert_called_once_with("fake_path", self.mock_user_key, self.mock_terminal)
        
        # Verificar que se mostraron los puntos
        mock_type_text.assert_called_once_with(
            self.mock_terminal, 
            "->Actualmente tienes un total de 100000 puntos<-"
        )

    @patch('points.type_text')
    @patch('points.load_encrypted_data')
    def test_type_points_zero_points(self, mock_load_data, mock_type_text):
        """Test: Visualización de 0 puntos"""
        user_data_zero = {
            "username": "testuser",
            "garage": [],
            "points": 0
        }
        mock_load_data.return_value = user_data_zero
        
        points.type_points("fake_path", self.mock_terminal, self.mock_user_key)
        
        mock_type_text.assert_called_once_with(
            self.mock_terminal,
            "->Actualmente tienes un total de 0 puntos<-"
        )

    @patch('points.type_text')
    @patch('points.load_encrypted_data')
    def test_type_points_load_data_fails(self, mock_load_data, mock_type_text):
        """Test: Fallo al cargar datos encriptados"""
        mock_load_data.return_value = None  # Simular fallo
        
        points.type_points("fake_path", self.mock_terminal, self.mock_user_key)
        
        # No debería llamar a type_text si load_encrypted_data falla
        mock_type_text.assert_not_called()


    @patch('points.type_text')
    @patch('points.load_encrypted_data')
    def test_type_points_empty_user_data(self, mock_load_data, mock_type_text):
        """Test: Datos de usuario vacíos"""
        user_data_empty = {}
        mock_load_data.return_value = user_data_empty
        
        points.type_points("fake_path", self.mock_terminal, self.mock_user_key)
        
        # Debería manejar datos vacíos sin crashear

    @patch('points.type_text')
    @patch('points.load_encrypted_data')
    def test_type_points_format_consistency(self, mock_load_data, mock_type_text):
        """Test: Consistencia del formato del mensaje"""
        test_cases = [
            (0, "->Actualmente tienes un total de 0 puntos<-"),
            (100, "->Actualmente tienes un total de 100 puntos<-"),
            (1234567, "->Actualmente tienes un total de 1234567 puntos<-"),
            (-100, "->Actualmente tienes un total de -100 puntos<-")
        ]
        
        for points_value, expected_message in test_cases:
            with self.subTest(points=points_value):
                mock_load_data.reset_mock()
                mock_type_text.reset_mock()
                
                user_data = {
                    "username": "testuser",
                    "garage": [],
                    "points": points_value
                }
                mock_load_data.return_value = user_data
                
                points.type_points("fake_path", self.mock_terminal, self.mock_user_key)
                
                mock_type_text.assert_called_once_with(self.mock_terminal, expected_message)


if __name__ == '__main__':
    unittest.main()