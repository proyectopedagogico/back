# generate_admin_hash.py
import bcrypt
import getpass # To securely get password input without echoing to screen

def generate_password_hash():
    """
    Prompts for a password and generates a bcrypt hash for it.
    """
    password = getpass.getpass("Introduce la contraseña para el administrador: ")
    password_confirm = getpass.getpass("Confirma la contraseña: ")

    if password != password_confirm:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        return None

    if not password:
        print("La contraseña no puede estar vacía.")
        return None

    # Encode the password to bytes, required by bcrypt
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Decode the hashed password to a string for storage (optional, but common)
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    
    print("\n--- Hash de Contraseña Generado ---")
    print("Guarda este hash de forma segura. Lo necesitarás para insertarlo en la base de datos.")
    print(f"Hash: {hashed_password_str}")
    print("----------------------------------")
    return hashed_password_str

if __name__ == '__main__':
    generate_password_hash()
