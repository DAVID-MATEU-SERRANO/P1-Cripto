# test_race.py
import unittest
import tempfile
import os
import json
import base64
from unittest.mock import Mock, patch
import sys

sys.path.append('.')

import race

class TestRaceFunctions(unittest.TestCase):

    def setUp(self):
        """Configuración antes de cada test"""
        # Crear directorio temporal para pruebas
        self.test_dir = tempfile.mkdtemp()
        self.test_races_path = os.path.join(self.test_dir, "races")
        self.test_users_path = os.path.join(self.test_dir, "users.json")
        os.makedirs(self.test_races_path, exist_ok=True)
        
        # Configurar paths de prueba
        race.RACES_PATH = self.test_races_path + "/"
        race.USERS_PATH = self.test_users_path
        
        # Mock del terminal
        self.mock_terminal = Mock()
        self.mock_terminal.delete = Mock()
        
        # Mocks de claves
        self.mock_user_key = b"fake_user_key_32_bytes_123456789"
        self.mock_msg_key = b"fake_msg_key_32_bytes_1234567890"
        
        # Datos de prueba
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
                }
            ],
            "points": 100000
        }
        
        self.sample_race_car = {
            "brand": "Nissan",
            "model": "Skyline",
            "stats": {
                "speed": 75,
                "handling": 80,
                "acceleration": 70,
                "braking": 75
            },
            "upgrades": []
        }
        
        # Crear archivo de usuarios de prueba
        with open(self.test_users_path, 'w') as f:
            json.dump({
                "rival_user": {"salt_password": "test", "salt_key": "test", "hash": "test"},
                "another_user": {"salt_password": "test", "salt_key": "test", "hash": "test"}
            }, f)

    def tearDown(self):
        """Limpieza después de cada test"""
        import shutil
        shutil.rmtree(self.test_dir)
        race.selected_race = 0

    # Tests para create_race
    @patch('race.store_data')
    @patch('race.load_data')
    @patch('race.encrypt_data')
    @patch('race.type_text')
    def test_create_race_success(self, mock_type_text, mock_encrypt, mock_load_data, mock_store_data):
        """Test: Creación exitosa de carrera"""
        mock_load_data.return_value = []
        mock_cipher = Mock()
        mock_cipher.nonce = b'16_bytes_nonce__'
        mock_encrypt.return_value = (mock_cipher, b'ciphertext', b'16_bytes_tag__')
        
        race.create_race("rival_user", self.sample_race_car, "testuser", self.mock_terminal, self.mock_msg_key)
        
        mock_load_data.assert_called_once()
        mock_encrypt.assert_called_once()
        mock_store_data.assert_called_once()
        mock_type_text.assert_called_with(self.mock_terminal, "Carrera enviada correctamente\n")

    @patch('race.store_data')
    @patch('race.load_data')
    @patch('race.encrypt_data')
    def test_create_race_with_existing_races(self, mock_encrypt, mock_load_data, mock_store_data):
        """Test: Creación de carrera cuando ya existen carreras"""
        existing_races = [{"rival": "other_user", "race_car": "existing_data"}]
        mock_load_data.return_value = existing_races
        mock_cipher = Mock()
        mock_cipher.nonce = b'16_bytes_nonce__'
        mock_encrypt.return_value = (mock_cipher, b'ciphertext', b'16_bytes_tag__')
        
        race.create_race("rival_user", self.sample_race_car, "testuser", self.mock_terminal, self.mock_msg_key)
        
        # Verificar que se añadió a la lista existente
        saved_races = mock_store_data.call_args[0][0]
        self.assertEqual(len(saved_races), 2)
        self.assertEqual(saved_races[1]["rival"], "testuser")

    # Tests para send_race
    @patch('race.type_text')
    def test_send_race_empty_fields(self, mock_type_text):
        """Test: Envío de carrera con campos vacíos"""
        race.send_race("", "", "testuser", self.mock_terminal, "path", self.mock_user_key, self.mock_msg_key)
        mock_type_text.assert_called_with(self.mock_terminal, "Complete todos los campos por favor\n")

    @patch('race.type_text')
    def test_send_race_invalid_msg_key(self, mock_type_text):
        """Test: Envío de carrera con clave de mensaje inválida"""
        race.send_race("rival_user", "Supra", "testuser", self.mock_terminal, "path", self.mock_user_key, b"short_key")
        mock_type_text.assert_called_with(
            self.mock_terminal, 
            "La clave de cifrado debe tener 32 caracteres y debe ser la misma que la de descifrado\n"
        )

    @patch('race.type_text')
    def test_send_race_self_race(self, mock_type_text):
        """Test: Envío de carrera contra uno mismo"""
        race.send_race("testuser", "Supra", "testuser", self.mock_terminal, "path", self.mock_user_key, self.mock_msg_key)
        mock_type_text.assert_called_with(
            self.mock_terminal, 
            "No puedes hacer una carrera contra ti mismo\nIntroduzca uno válido\n"
        )

    @patch('race.user_exists')
    @patch('race.type_text')
    def test_send_race_user_not_exists(self, mock_type_text, mock_user_exists):
        """Test: Envío de carrera a usuario inexistente"""
        mock_user_exists.return_value = False
        race.send_race("nonexistent_user", "Supra", "testuser", self.mock_terminal, "path", self.mock_user_key, self.mock_msg_key)
        mock_type_text.assert_called_with(
            self.mock_terminal, 
            "Username no encontrado\nIntroduzca uno válido\n"
        )

    @patch('race.load_encrypted_data')
    @patch('race.car_exists')
    @patch('race.user_exists')
    @patch('race.type_text')
    def test_send_race_car_not_exists(self, mock_type_text, mock_user_exists, mock_car_exists, mock_load_encrypted):
        """Test: Envío de carrera con coche inexistente"""
        mock_user_exists.return_value = True
        mock_load_encrypted.return_value = self.sample_user_data
        mock_car_exists.return_value = (False, 0)
        
        race.send_race("rival_user", "NonexistentCar", "testuser", self.mock_terminal, "path", self.mock_user_key, self.mock_msg_key)
        mock_type_text.assert_called_with(
            self.mock_terminal, 
            "No tienes este coche\nConsulta tu garage y elige uno\n"
        )

    @patch('race.create_race')
    @patch('race.load_encrypted_data')
    @patch('race.car_exists')
    @patch('race.user_exists')
    def test_send_race_success(self, mock_user_exists, mock_car_exists, mock_load_encrypted, mock_create_race):
        """Test: Envío de carrera exitoso"""
        mock_user_exists.return_value = True
        mock_load_encrypted.return_value = self.sample_user_data
        mock_car_exists.return_value = (True, 0)
        
        race.send_race("rival_user", "Supra", "testuser", self.mock_terminal, "path", self.mock_user_key, self.mock_msg_key)
        
        mock_create_race.assert_called_once_with(
            "rival_user", 
            self.sample_user_data["garage"][0], 
            "testuser", 
            self.mock_terminal, 
            self.mock_msg_key
        )

    # Tests para type_race
    @patch('race.type_text')
    def test_type_race_invalid_msg_key(self, mock_type_text):
        """Test: Visualización de carrera con clave inválida"""
        race.type_race("testuser", self.mock_terminal, b"short_key")
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "La clave de descifrado debe tener 32 caracteres y debe ser la misma que la de cifrado\n"
        )

    @patch('race.type_text')
    def test_type_race_no_msg_key(self, mock_type_text):
        """Test: Visualización de carrera sin clave"""
        race.type_race("testuser", self.mock_terminal, b"")
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "Por favor introduzca la clave de cifrado\n"
        )

    @patch('race.type_text')
    @patch('race.load_data')
    def test_type_race_no_races(self, mock_load_data, mock_type_text):
        """Test: Visualización cuando no hay carreras"""
        mock_load_data.return_value = {}
        race.type_race("testuser", self.mock_terminal, self.mock_msg_key)
        mock_type_text.assert_called_with(self.mock_terminal, "Vaya, nadie te ha desafiado aún\n")

    @patch('race.desencrypt_data')
    @patch('race.load_data')
    @patch('race.type_text')
    def test_type_race_with_upgrades(self, mock_type_text, mock_load_data, mock_desencrypt):
        """Test: Visualización de carrera con mejoras"""
        # Crear datos base64 VÁLIDOS para race_car
        valid_base64_data = base64.b64encode(b"fake_encrypted_data_16_bytes").decode('ascii')
        
        race_data = [{"rival": "opponent", "race_car": valid_base64_data}]
        car_with_upgrades = {
            "brand": "Toyota",
            "model": "Supra",
            "stats": {"speed": 80, "handling": 70, "acceleration": 85, "braking": 65},
            "upgrades": [{"name": "Turbo"}, {"name": "Nitrous"}]
        }
        mock_load_data.return_value = race_data
        mock_desencrypt.return_value = car_with_upgrades
        
        race.type_race("testuser", self.mock_terminal, self.mock_msg_key)
        
        mock_type_text.assert_called_once()
        call_args = mock_type_text.call_args[0][1]
        self.assertIn("- Turbo", call_args)
        self.assertIn("- Nitrous", call_args)

    # Tests para navegación
    @patch('race.type_race')
    def test_next_race(self, mock_type_race):
        """Test: Navegación a siguiente carrera"""
        initial_position = race.selected_race
        race.next_race("testuser", self.mock_terminal, self.mock_msg_key)
        self.assertEqual(race.selected_race, initial_position + 1)
        mock_type_race.assert_called_once_with("testuser", self.mock_terminal, self.mock_msg_key)

    @patch('race.type_race')
    def test_previous_race(self, mock_type_race):
        """Test: Navegación a carrera anterior"""
        race.selected_race = 1
        race.previous_race("testuser", self.mock_terminal, self.mock_msg_key)
        self.assertEqual(race.selected_race, 0)
        mock_type_race.assert_called_once_with("testuser", self.mock_terminal, self.mock_msg_key)

    # Tests para race (ejecución de carrera)
    @patch('race.type_text')
    def test_race_invalid_msg_key(self, mock_type_text):
        """Test: Ejecución de carrera con clave inválida"""
        race.race("testuser", "path", self.mock_user_key, self.mock_terminal, "Supra", b"short_key")
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "La clave de descifrado debe tener 32 caracteres y debe ser la misma que la de cifrado\n"
        )

@patch('race.load_data')
@patch('race.load_encrypted_data')
@patch('race.car_exists')
@patch('race.type_text')
def test_race_car_not_exists(self, mock_type_text, mock_car_exists, mock_load_encrypted, mock_load_data):
    """Test: Ejecución de carrera con coche inexistente"""
    # Mock de datos de carrera válidos
    valid_base64_data = base64.b64encode(b"fake_encrypted_car_data_16b").decode('ascii')
    race_data = [{"rival": "opponent", "race_car": valid_base64_data}]
    
    mock_load_data.return_value = race_data
    mock_load_encrypted.return_value = self.sample_user_data
    mock_car_exists.return_value = (False, 0)
    
    # También necesitamos mockear desencrypt_data
    with patch('race.desencrypt_data') as mock_desencrypt:
        mock_desencrypt.return_value = {
            "brand": "Nissan", "model": "Skyline",
            "stats": {"speed": 70, "handling": 60, "acceleration": 65, "braking": 55},
            "upgrades": []
        }
        
        race.race("testuser", "path", self.mock_user_key, self.mock_terminal, "NonexistentCar", self.mock_msg_key)
        
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "No tienes este coche\nConsulta tu garage y elige uno\n"
        )

    @patch('random.randint')
    @patch('race.store_encrypted_data')
    @patch('race.store_data')
    @patch('race.load_data')
    @patch('race.desencrypt_data')
    @patch('race.load_encrypted_data')
    @patch('race.car_exists')
    @patch('race.type_text')
    def test_race_user_wins(self, mock_type_text, mock_car_exists, mock_load_encrypted, 
                        mock_desencrypt, mock_load_data, mock_store_data, 
                        mock_store_encrypted, mock_randint):
        """Test: Usuario gana la carrera"""
        mock_car_exists.return_value = (True, 0)
        mock_load_encrypted.return_value = self.sample_user_data
        
        # Oponente con menos puntos
        opponent_car = {
            "brand": "Nissan", "model": "Skyline",
            "stats": {"speed": 70, "handling": 60, "acceleration": 65, "braking": 55},  # Total: 250
            "upgrades": []
        }
        
        mock_desencrypt.return_value = opponent_car
        mock_load_data.return_value = [{"rival": "opponent", "race_car": "data"}]
        mock_randint.return_value = 5  # Sin adelantamiento sorpresa
        
        race.selected_race = 0
        race.race("testuser", "path", self.mock_user_key, self.mock_terminal, "Supra", self.mock_msg_key)
        
        # Verificar que se actualizaron los puntos (+200)
        updated_user_data = mock_store_encrypted.call_args[0][0]
        self.assertEqual(updated_user_data["points"], 100000 + 200)
        
        # Verificar que se eliminó la carrera - CORREGIDO
        from unittest.mock import ANY
        mock_store_data.assert_called_once_with([], ANY)

    @patch('random.randint')
    @patch('race.store_encrypted_data')
    @patch('race.store_data')
    @patch('race.load_data')
    @patch('race.desencrypt_data')
    @patch('race.load_encrypted_data')
    @patch('race.car_exists')
    @patch('race.type_text')
    def test_race_user_loses(self, mock_type_text, mock_car_exists, mock_load_encrypted,
                           mock_desencrypt, mock_load_data, mock_store_data,
                           mock_store_encrypted, mock_randint):
        """Test: Usuario pierde la carrera"""
        mock_car_exists.return_value = (True, 0)
        
        # Usuario con menos puntos
        user_data_losing = self.sample_user_data.copy()
        user_data_losing["points"] = 100000
        mock_load_encrypted.return_value = user_data_losing
        
        # Oponente con más puntos
        opponent_car = {
            "brand": "Nissan", "model": "Skyline",
            "stats": {"speed": 90, "handling": 80, "acceleration": 85, "braking": 75},  # Total: 330
            "upgrades": []
        }
        
        mock_desencrypt.return_value = opponent_car
        mock_load_data.return_value = [{"rival": "opponent", "race_car": "data"}]
        mock_randint.return_value = 5  # Sin adelantamiento sorpresa
        
        race.selected_race = 0
        race.race("testuser", "path", self.mock_user_key, self.mock_terminal, "Supra", self.mock_msg_key)
        
        # Verificar que se actualizaron los puntos (-200)
        updated_user_data = mock_store_encrypted.call_args[0][0]
        self.assertEqual(updated_user_data["points"], 100000 - 200)

if __name__ == '__main__':
    unittest.main()