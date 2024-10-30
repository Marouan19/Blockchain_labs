# MetroHash64

Une implémentation Python de l'algorithme de hachage non cryptographique MetroHash64, optimisé pour la vitesse et la distribution des hash.

## 🔍 Qu'est-ce que MetroHash64 ?

MetroHash64 est un algorithme de hachage non cryptographique qui :
- Produit une sortie sur 64 bits
- Est optimisé pour la performance
- Offre une excellente distribution des valeurs de hachage
- Est simple à implémenter et à comprendre
- Utilise des opérations bit à bit pour une efficacité maximale

## 📥 Clone du projet

```bash
git clone https://github.com/Marouan19/Blockchain_labs.git
cd "Blockchain_labs/Atelier 3"
```

## 🔧 Étapes d'implémentation

L'algorithme MetroHash64 est implémenté dans `hashage.py` avec les étapes suivantes :

### 1. Constantes de hachage
```python
k0 = 0xC83A91E1
k1 = 0x8648DBDB
k2 = 0x7BDEC03B
k3 = 0x2F5870A5
```

### 2. Processus de hachage
```python
def metrohash64(text, seed=0):
    # Initialisation avec la longueur du texte
    length = len(text)
    hash_value = seed ^ (k0 * length)
    
    # Traitement par blocs de 4 octets
    for i in range(0, len(text) - len(text) % 4, 4):
        block = int.from_bytes(text[i:i+4].encode('utf-8'), 'little')
        hash_value += block * k1
        hash_value = ((hash_value << 13) | (hash_value >> (32 - 13)))
        hash_value *= k2
```

### 3. Principales étapes :
1. **Initialisation**
   - Calcul de la longueur du texte
   - Initialisation du hash avec seed ⊕ (k0 × length)

2. **Traitement principal**
   - Division du texte en blocs de 4 octets
   - Pour chaque bloc :
     * Conversion en entier (little-endian)
     * Multiplication par k1
     * Rotation à gauche de 13 bits
     * Multiplication par k2

3. **Traitement des restes**
   - Gestion des octets restants avec k3
   - Application de la rotation finale

4. **Finalisation**
   - Opérations XOR successives
   - Multiplications finales
   - Application du masque 64 bits

## 📊 Résultats

Exemple avec le texte "je suis Marouan Daghmoumi" :

```python
text = "je suis Marouan Daghmoumi"
hash_result = metrohash64(text)

# Résultats :
# Hash (hexadécimal) : 7b83b3e6d86bdcca
# Hash (décimal)     : 8900155092669029578
```

## 🔄 Diagramme de Transformation

Le processus de transformation pour le texte "je suis Marouan Daghmoumi" :

```
Input (25 caractères)
    ↓
[Bloc 1: "je s"] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Bloc 2: "uis "] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Bloc 3: "Maro"] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Bloc 4: "uan "] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Bloc 5: "Dagh"] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Bloc 6: "moum"] → UTF-8 → × k1 → ROT13 → × k2
    ↓
[Reste: "i"] → UTF-8 → × k3 → ROT13 → × k0
    ↓
Finalisation (XOR et multiplications)
    ↓
Hash final: 7b83b3e6d86bdcca
```

## 👨‍💻 Auteur
- **DAGHMOUMI Marouan**
  - MST: Intelligence Artificielle et Science des Données
  - Faculté des Sciences et Techniques - Tanger
  - Université Abdelmalek Essaâdi

### Encadré par
- **Pr. Ikram Ben abdel ouahab**

## 📝 Note
Cette implémentation fait partie du cours de Blockchain et est destinée à des fins éducatives. Elle démontre les principes fondamentaux de l'algorithme MetroHash64.

---
*Pour plus d'informations sur les autres ateliers Blockchain, visitez le [dépôt principal](https://github.com/Marouan19/Blockchain_labs).*
