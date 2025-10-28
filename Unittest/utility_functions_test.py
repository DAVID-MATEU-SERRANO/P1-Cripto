# test_utility_functions.py
import unittest
import tempfile
import os
import json
import base64
from unittest.mock import Mock, patch
import sys
from Crypto.Cipher import AES 

sys.path.append('.')

import utility_functions as uf

class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        """Configuración antes de cada test"""
        self.test_dir = tempfile.mkdtemp()
        self.mock_terminal = Mock()
        self.mock_terminal.delete = Mock()
        self.mock_terminal.insert = Mock()
        self.mock_terminal.see = Mock()
        self.mock_terminal.after = Mock()

    def tearDown(self):
        """Limpieza después de cada test"""
        import shutil
        shutil.rmtree(self.test_dir)
        # Resetear variables globales
        uf.typing_after_id = None
        uf.typing_queue.clear()

    # Tests para hash_password
    def test_hash_password_generates_salt_when_none(self):
        """Test: hash_password genera salt cuando no se proporciona"""
        salt_password, salt_key, hash_b64 = uf.hash_password("TestPassword123-")
        
        self.assertIsNotNone(salt_password)
        self.assertIsNotNone(salt_key)
        self.assertIsNotNone(hash_b64)
        # Verificar que son strings base64 válidos
        self.assertEqual(len(base64.b64decode(salt_password)), 16)
        self.assertEqual(len(base64.b64decode(salt_key)), 16)
        self.assertEqual(len(base64.b64decode(hash_b64)), 32)

    def test_hash_password_uses_provided_salt(self):
        """Test: hash_password usa salt proporcionado"""
        provided_salt = b"provided_salt_16"
        salt_password, salt_key, hash_b64 = uf.hash_password("TestPassword123-", provided_salt)
        
        # Verificar que usa el salt proporcionado
        decoded_salt = base64.b64decode(salt_password)
        self.assertEqual(decoded_salt, provided_salt)

    def test_hash_password_deterministic_with_same_salt(self):
        """Test: hash_password es determinístico con mismo salt y password"""
        salt = b"test_salt_16_bytes"
        password = "TestPassword123-"
        
        _, _, result1 = uf.hash_password(password, salt)
        _, _, result2 = uf.hash_password(password, salt)
        
        # Deben ser idénticos
        self.assertEqual(result1, result2)

    # Tests para generate_user_key
    def test_generate_user_key_returns_32_bytes(self):
        """Test: generate_user_key retorna clave de 32 bytes"""
        salt = b"test_salt_16_bytes"
        key = uf.generate_user_key("TestPassword123-", salt)
        
        self.assertEqual(len(key), 32)  # AES-256 key

    def test_generate_user_key_deterministic(self):
        """Test: generate_user_key es determinístico"""
        salt = b"test_salt_16_bytes"
        password = "TestPassword123-"
        
        key1 = uf.generate_user_key(password, salt)
        key2 = uf.generate_user_key(password, salt)
        
        self.assertEqual(key1, key2)

    # Tests para encrypt_data y desencrypt_data
    def test_encrypt_decrypt_round_trip(self):
        """Test: encrypt_data y desencrypt_data funcionan correctamente"""
        key = b"test_key_32_bytes_12345678901234"
        plaintext = b"Test plaintext message"
        
        # Encriptar
        cipher, ciphertext, tag = uf.encrypt_data(key, plaintext)
        
        # Verificar que se generaron componentes
        self.assertIsNotNone(cipher.nonce)
        self.assertIsNotNone(ciphertext)
        self.assertIsNotNone(tag)
        
        # Desencriptar CORRECTAMENTE usando AES.new
        cipher2 = AES.new(key, AES.MODE_GCM, nonce=cipher.nonce)
        decrypted = cipher2.decrypt_and_verify(ciphertext, tag)
        
        self.assertEqual(decrypted, plaintext)

    @patch('utility_functions.type_text')
    def test_desencrypt_data_success(self, mock_type_text):
        """Test: desencrypt_data exitosa"""
        key = b"test_key_32_bytes_12345678901234"
        test_data = {"test": "data", "number": 123}
        plaintext = json.dumps(test_data).encode('utf-8')
        
        # Encriptar datos de prueba
        cipher = uf.encrypt_data(key, plaintext)
        file_bytes = cipher[0].nonce + cipher[2] + cipher[1]  # nonce + tag + ciphertext
        
        # Desencriptar
        result = uf.desencrypt_data(file_bytes, key, self.mock_terminal)
        
        # Verificar resultado
        self.assertEqual(result, test_data)
        self.assertTrue(mock_type_text.called)

    @patch('utility_functions.type_text')
    def test_desencrypt_data_failure(self, mock_type_text):
        """Test: desencrypt_data con error"""
        key = b"test_key_32_bytes_12345678901234"
        wrong_key = b"wrong_key_32_bytes_1234567890123"
        test_data = {"test": "data"}
        plaintext = json.dumps(test_data).encode('utf-8')
        
        # Encriptar con una clave
        cipher = uf.encrypt_data(key, plaintext)
        file_bytes = cipher[0].nonce + cipher[2] + cipher[1]
        
        # Intentar desencriptar con clave diferente
        result = uf.desencrypt_data(file_bytes, wrong_key, self.mock_terminal)
        
        # Verificar que retorna None y muestra error
        self.assertIsNone(result)
        mock_type_text.assert_called_with(
            self.mock_terminal,
            "ERROR GRAVE: las claves de cifrado y descifrado no coinciden o alguien ha modificado el archivo\n"
        )

    # Tests para load_data y store_data
    def test_store_and_load_data(self):
        """Test: store_data y load_data funcionan correctamente"""
        test_path = os.path.join(self.test_dir, "test.json")
        test_data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        
        # Guardar datos
        uf.store_data(test_data, test_path)
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(test_path))
        
        # Cargar datos
        loaded_data = uf.load_data(test_path)
        
        # Verificar que son iguales
        self.assertEqual(loaded_data, test_data)

    def test_load_data_file_not_found(self):
        """Test: load_data con archivo que no existe"""
        non_existent_path = os.path.join(self.test_dir, "nonexistent.json")
        
        # Debería retornar diccionario vacío
        result = uf.load_data(non_existent_path)
        self.assertEqual(result, {})

    def test_load_data_invalid_json(self):
        """Test: load_data con JSON inválido"""
        invalid_json_path = os.path.join(self.test_dir, "invalid.json")
        
        # Crear archivo con JSON inválido
        with open(invalid_json_path, 'w') as f:
            f.write("{invalid json")
        
        # Debería lanzar excepción
        with self.assertRaises(Exception) as context:
            uf.load_data(invalid_json_path)
        
        self.assertIn("Error leyendo el archivo", str(context.exception))

    # Tests para user_exists
    def test_user_exists_true(self):
        """Test: user_exists retorna True cuando usuario existe"""
        test_path = os.path.join(self.test_dir, "users.json")
        users_data = {"user1": {"data": "value1"}, "user2": {"data": "value2"}}
        
        with open(test_path, 'w') as f:
            json.dump(users_data, f)
        
        self.assertTrue(uf.user_exists("user1", test_path))
        self.assertTrue(uf.user_exists("user2", test_path))

    def test_user_exists_false(self):
        """Test: user_exists retorna False cuando usuario no existe"""
        test_path = os.path.join(self.test_dir, "users.json")
        users_data = {"user1": {"data": "value1"}}
        
        with open(test_path, 'w') as f:
            json.dump(users_data, f)
        
        self.assertFalse(uf.user_exists("nonexistent", test_path))

    def test_user_exists_file_not_found(self):
        """Test: user_exists con archivo que no existe"""
        non_existent_path = os.path.join(self.test_dir, "nonexistent.json")
        self.assertFalse(uf.user_exists("anyuser", non_existent_path))

    # Tests para car_exists
    def test_car_exists_true(self):
        """Test: car_exists encuentra coche existente"""
        user_data = {
            "garage": [
                {"brand": "Toyota", "model": "Supra"},
                {"brand": "Nissan", "model": "Skyline"},
                {"brand": "Honda", "model": "Civic"}
            ]
        }
        
        exists, position = uf.car_exists("Skyline", user_data)
        self.assertTrue(exists)
        self.assertEqual(position, 1)

    def test_car_exists_false(self):
        """Test: car_exists no encuentra coche inexistente"""
        user_data = {
            "garage": [
                {"brand": "Toyota", "model": "Supra"}
            ]
        }
        
        exists, _ = uf.car_exists("Ferrari", user_data)
        self.assertFalse(exists)

    def test_car_exists_empty_garage(self):
        """Test: car_exists con garage vacío"""
        user_data = {"garage": []}
        
        exists, position = uf.car_exists("AnyCar", user_data)
        self.assertFalse(exists)
        self.assertEqual(position, 0)

    # Tests para upgrade_exists
    def test_upgrade_exists_true(self):
        """Test: upgrade_exists encuentra mejora existente"""
        user_data = {
            "garage": [
                {
                    "brand": "Toyota",
                    "model": "Supra", 
                    "upgrades": [
                        {"name": "Turbo Boost"},
                        {"name": "Nitrous Oxide"}
                    ]
                }
            ]
        }
        
        exists = uf.upgrade_exists("Turbo Boost", user_data, 0)
        self.assertTrue(exists)

    def test_upgrade_exists_false(self):
        """Test: upgrade_exists no encuentra mejora inexistente"""
        user_data = {
            "garage": [
                {
                    "brand": "Toyota",
                    "model": "Supra",
                    "upgrades": [
                        {"name": "Turbo Boost"}
                    ]
                }
            ]
        }
        
        exists = uf.upgrade_exists("Spoiler", user_data, 0)
        self.assertFalse(exists)

    def test_upgrade_exists_no_upgrades(self):
        """Test: upgrade_exists sin mejoras"""
        user_data = {
            "garage": [
                {
                    "brand": "Toyota", 
                    "model": "Supra",
                    "upgrades": []
                }
            ]
        }
        
        exists = uf.upgrade_exists("AnyUpgrade", user_data, 0)
        self.assertFalse(exists)

if __name__ == '__main__':
    unittest.main()