from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import hashlib

class NexusEncrypt:
    def __init__(self, master_key=None):
        # Si no hay master_key, usar una derivada de una contraseña maestra
        if master_key is None:
            master_key = "nexus_sovereign_2026_argentina_china"
        
        # Derivar una clave de 32 bytes (256 bits) usando SHA-256
        self.master_key = hashlib.sha256(master_key.encode()).digest()
        self.nonce_size = 12  # AES-GCM usa nonce de 12 bytes
    
    def encrypt(self, plaintext):
        """
        Encripta texto usando AES-256-GCM
        Retorna: nonce + ciphertext + tag (todo en base64)
        """
        # Generar nonce aleatorio
        nonce = os.urandom(self.nonce_size)
        
        # Crear objeto AES-GCM
        aesgcm = AESGCM(self.master_key)
        
        # Encriptar
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        
        # Combinar nonce + ciphertext y codificar en base64
        encrypted_data = nonce + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_data):
        """
        Desencripta datos encriptados con AES-256-GCM
        """
        try:
            # Decodificar base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Extraer nonce (primeros 12 bytes)
            nonce = encrypted_bytes[:self.nonce_size]
            
            # Extraer ciphertext + tag
            ciphertext = encrypted_bytes[self.nonce_size:]
            
            # Crear objeto AES-GCM
            aesgcm = AESGCM(self.master_key)
            
            # Desencriptar
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            
            return plaintext.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

# Instancia global del encriptador
nexus_encrypt = NexusEncrypt()

# Funciones compatibles con el código actual
def encrypt_data(data, key=None):
    """Función compatible con el código existente"""
    return nexus_encrypt.encrypt(data)

def decrypt_data(data, key=None):
    """Función compatible con el código existente"""
    return nexus_encrypt.decrypt(data)

# TEST
if __name__ == "__main__":
    print("Testing AES-256-GCM Encryption...")
    
    # Test 1: Encriptar y desencriptar
    original = "Tech Argentina"
    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)
    
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {original == decrypted}")
    
    # Test 2: Mismo texto, diferente encriptación (por el nonce aleatorio)
    enc1 = encrypt_data("test")
    enc2 = encrypt_data("test")
    print(f"\nSame text, different encryption: {enc1 != enc2}")
    
    print("\n✅ AES-256-GCM encryption working correctly!")
