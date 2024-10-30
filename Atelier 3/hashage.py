def metrohash64(text, seed=0):
    # 1. Définition des constantes de hachage (valeurs magiques)
    k0 = 0xC83A91E1
    k1 = 0x8648DBDB
    k2 = 0x7BDEC03B
    k3 = 0x2F5870A5

    # 2. Calcul de la longueur du texte d'entrée
    length = len(text)

    # 3. Initialisation de la valeur de hachage avec le seed
    # XOR avec le produit de k0 et la longueur
    hash_value = seed ^ (k0 * length)

    # 4. Traitement principal - blocs de 4 octets
    # Parcours du texte par blocs de 4 caractères
    for i in range(0, len(text) - len(text) % 4, 4):
        # Conversion du bloc de texte en entier (little-endian)
        block = int.from_bytes(text[i:i + 4].encode('utf-8'), 'little')

        # Multiplication par k1
        hash_value += block * k1

        # Rotation à gauche de 13 bits
        hash_value = ((hash_value << 13) | (hash_value >> (32 - 13)))

        # Multiplication par k2
        hash_value *= k2

    # 5. Traitement des octets restants
    remaining_bytes = len(text) % 4
    if remaining_bytes > 0:
        # Conversion des derniers octets en entier
        last_block = int.from_bytes(text[-remaining_bytes:].encode('utf-8'), 'little')

        # Application de k3
        hash_value += last_block * k3

        # Rotation à gauche de 13 bits
        hash_value = ((hash_value << 13) | (hash_value >> (32 - 13)))

        # Multiplication par k0
        hash_value *= k0

    # 6. Finalisation - mélange final du hash
    # Série d'opérations XOR et multiplications
    hash_value ^= hash_value >> 16
    hash_value *= 0x85EBCA6B
    hash_value ^= hash_value >> 13
    hash_value *= 0xC2B2AE35
    hash_value ^= hash_value >> 16

    # 7. Retour du résultat final sur 64 bits
    return hash_value & 0xFFFFFFFFFFFFFFFF


# Exemple d'utilisation
def demo_metrohash64():
    # Texte de test
    text = "je suis Marouan Daghmoumi"

    # Calcul du hash
    hash_result = metrohash64(text)

    # Affichage des résultats
    print(f"Texte d'entrée: {text}")
    print(f"Hash (64-bit hex): {hash_result:016x}")
    print(f"Hash (décimal): {hash_result}")


# Exécution de la démonstration
if __name__ == "__main__":
    demo_metrohash64()