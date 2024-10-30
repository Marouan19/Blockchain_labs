# 🔗 Blockchain Labs
Série de travaux pratiques et d'implémentations sur la blockchain, réalisés dans le cadre du cours de Blockchain à la FST de Tanger.

## 📚 Table des Matières
1. [Description](#-description)
2. [Structure du Dépôt](#-structure-du-dépôt)
3. [Technologies Utilisées](#-technologies-utilisées)
4. [Installation](#-installation)
5. [Ateliers](#-ateliers)
6. [Contributions](#-contributions)
7. [Auteur](#-auteur)

## 📖 Description
Ce dépôt contient une collection de laboratoires pratiques explorant différents aspects de la technologie blockchain, notamment :
- Implémentations d'algorithmes de hachage
- Mécanismes de consensus (PoW, PoS)
- Structures de données blockchain
- Analyses de performance et benchmarking

## 📂 Structure du Dépôt
```
Blockchain_labs/
├── Atelier1/
│   └── [Implémentations d'algorithmes de hachage]
├── Atelier2/
│   └── [Structures de données blockchain]
├── Benchmarking_PoW_&_PoS/
│   └── [Comparaison des mécanismes de consensus]
└── README.md
```

## 💻 Technologies Utilisées
- **Python 3.8+**
- **Bibliothèques principales** :
  - `hashlib` - Pour les fonctions de hachage cryptographique
  - `time` - Pour les mesures de performance
  - `matplotlib` - Pour la visualisation des données
  - `statistics` - Pour l'analyse statistique
  - `logging` - Pour la journalisation des événements

## 🔧 Installation
1. Clonez le dépôt :
```bash
git clone https://github.com/Marouan19/Blockchain_labs.git
```

2. Créez et activez un environnement virtuel :
```bash
cd Blockchain_labs
python -m venv .venv
source .venv/bin/activate  # Sur Unix/macOS
# ou
.\.venv\Scripts\activate  # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📘 Ateliers

### 🔍 Atelier 1 : Algorithmes de Hachage
- Implémentation de MetroHash64
- Analyse de performance
- Tests de distribution
- [Documentation détaillée](./Atelier1/README.md)

### 🏗️ Atelier 2 : Structures Blockchain
- Implémentation de blocks
- Chaînage des blocks
- Vérification d'intégrité
- [Documentation détaillée](./Atelier2/README.md)

### ⚡ Benchmarking PoW & PoS
- Implémentation de Proof of Work
- Implémentation de Proof of Stake
- Analyse comparative des performances
- Visualisation des résultats
- [Documentation détaillée](./Benchmarking_PoW_&_PoS/README.md)

## 🔬 Résultats et Observations
### Proof of Work vs Proof of Stake
```plaintext
PoW :
- Nonce trouvé: 5858
- Hash: 000049b5a9ba4e09b6dc6d40c1e3583d1654061fad84f77156e9d7b4fac95327
- Temps: 0.0040 secondes

PoS :
- Validateur: Address3
- Temps: 0.0000 secondes
```

### MetroHash64
```plaintext
Exemple de hash :
- Input: "je suis Marouan Daghmoumi"
- Output: 7b83b3e6d86bdcca
```

## 🤝 Contributions
Les contributions sont les bienvenues ! Pour contribuer :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 👨‍💻 Auteur
- **DAGHMOUMI Marouan**
  - MST: Intelligence Artificielle et Science des Données
  - Faculté des Sciences et Techniques - Tanger
  - Université Abdelmalek Essaâdi

### Encadré par
- **Pr. Ikram Ben abdel ouahab**

---
*Ce projet est développé dans le cadre du cours de Blockchain à la FST de Tanger.*
