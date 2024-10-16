#include <iostream>
#include <vector>
#include <string>
#include <openssl/sha.h>
#include <sstream>  // Pour stringstream
#include <iomanip>  // Pour setw et setfill
#include <fstream>  // Pour l'écriture dans des fichiers

// Fonction pour calculer le hash SHA256 d'une chaîne de caractères
std::string sha256(const std::string& data) {
    // Tableau pour stocker le résultat du hash
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    // Initialisation de la structure SHA256
    SHA256_Init(&sha256);
    // Mise à jour du contexte SHA256 avec les données à hasher
    SHA256_Update(&sha256, data.c_str(), data.size());
    // Finalisation du calcul du hash
    SHA256_Final(hash, &sha256);

    // Conversion du tableau d'octets en chaîne de caractères hexadécimale
    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        // Ajout de chaque octet sous forme hexadécimale dans la chaîne
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

// Structure représentant un nœud de l'arbre de Merkle
struct MerkleNode {
    std::string hash;  // Le hash du nœud
    MerkleNode* left;  // Pointeur vers le fils gauche
    MerkleNode* right; // Pointeur vers le fils droit

    // Constructeur pour initialiser un nœud feuille avec des données
    MerkleNode(const std::string& data) : hash(sha256(data)), left(nullptr), right(nullptr) {}
};

// Fonction pour construire l'arbre de Merkle à partir d'une liste de blocs de données
MerkleNode* buildMerkleTree(std::vector<std::string>& dataBlocks) {
    std::vector<MerkleNode*> nodes;

    // Création des nœuds feuilles (un nœud pour chaque bloc de données)
    for (const std::string& data : dataBlocks) {
        nodes.push_back(new MerkleNode(data));
    }

    // Construction de l'arbre de bas en haut
    while (nodes.size() > 1) {
        std::vector<MerkleNode*> newLevel;

        for (size_t i = 0; i < nodes.size(); i += 2) {
            if (i + 1 < nodes.size()) {
                // Combiner les hashs de deux nœuds enfants
                std::string combinedHash = sha256(nodes[i]->hash + nodes[i + 1]->hash);
                MerkleNode* parent = new MerkleNode(combinedHash);
                // Le nœud parent pointe vers les deux enfants
                parent->left = nodes[i];
                parent->right = nodes[i + 1];
                newLevel.push_back(parent);
            } else {
                // Si le nombre de nœuds est impair, on monte le dernier nœud à l'étage supérieur
                newLevel.push_back(nodes[i]);
            }
        }
        // Passer au niveau supérieur
        nodes = newLevel;
    }

    // Retourner la racine de l'arbre (le dernier nœud restant)
    return nodes[0];
}

// Fonction pour écrire l'arbre de Merkle dans un fichier DOT pour visualisation
void writeDotFile(MerkleNode* node, std::ofstream& dotFile) {
    if (node) {
        // Créer un nœud dans le format DOT
        dotFile << "    \"" << node->hash << "\";\n";
        if (node->left) {
            // Écrire les relations entre le parent et les enfants
            dotFile << "    \"" << node->hash << "\" -> \"" << node->left->hash << "\";\n";
            writeDotFile(node->left, dotFile);
        }
        if (node->right) {
            dotFile << "    \"" << node->hash << "\" -> \"" << node->right->hash << "\";\n";
            writeDotFile(node->right, dotFile);
        }
    }
}

// Fonction pour générer le fichier DOT récursivement
void generateDotHelper(MerkleNode* node, std::ofstream& file) {
    if (node->left && node->right) {
        file << "\"" << node->hash << "\" -> \"" << node->left->hash << "\";\n";
        file << "\"" << node->hash << "\" -> \"" << node->right->hash << "\";\n";
        generateDotHelper(node->left, file);
        generateDotHelper(node->right, file);
    }
}

// Fonction pour générer un fichier DOT à partir de l'arbre de Merkle
void generateDot(MerkleNode* root, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file " << filename << std::endl;
        return;
    }
    file << "digraph MerkleTree {\n";
    generateDotHelper(root, file);
    file << "}\n";
    file.close();
}

int main() {
    // Exemple de blocs de données
    std::vector<std::string> dataBlocks = {
        "Block1", "Block2", "Block3", "Block4"
    };

    // Construire l'arbre de Merkle
    MerkleNode* root = buildMerkleTree(dataBlocks);

    // Générer un fichier DOT pour la visualisation
    generateDot(root, "merkle_tree.dot");

    // Indiquer à l'utilisateur que l'arbre de Merkle a été sauvegardé
    std::cout << "Merkle Tree sauvegardé sous merkle_tree.dot" << std::endl;

    return 0;
}