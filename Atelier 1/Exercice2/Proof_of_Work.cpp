#include <iostream>
#include <sstream>
#include <string>
#include <openssl/sha.h>
#include <iomanip>
#include <ctime>
#include <chrono>
#include <vector>  // Ajout nécessaire pour std::vector

// Fonction pour calculer le hash SHA256 d'une chaîne de caractères
std::string sha256(const std::string& data) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, data.c_str(), data.size());
    SHA256_Final(hash, &sha256);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

// Classe Block représentant un bloc dans la blockchain
class Block {
public:
    int index;                 // Numéro du bloc
    std::string data;          // Données du bloc
    std::string prevHash;      // Hash du bloc précédent
    std::string hash;          // Hash du bloc actuel
    int nonce;                 // Nonce utilisé pour le proof of work

    Block(int idx, const std::string& d, const std::string& prev)
        : index(idx), data(d), prevHash(prev), nonce(0) {
        hash = calculateHash();
    }

    // Calculer le hash du bloc en utilisant les données et le nonce
    std::string calculateHash() const {
        std::stringstream ss;
        ss << index << data << prevHash << nonce;
        return sha256(ss.str());
    }

    // Proof of Work : trouver un hash commençant par un certain nombre de zéros (difficulté)
    void mineBlock(int difficulty) {
        std::string target(difficulty, '0');
        while (hash.substr(0, difficulty) != target) {
            nonce++;
            hash = calculateHash();
        }
        std::cout << "Block miné : " << hash << std::endl;
    }
};

// Classe Blockchain représentant la chaîne de blocs
class Blockchain {
public:
    std::vector<Block> chain;  // Ajout du vector ici
    int difficulty;

    Blockchain(int diff) : difficulty(diff) {
        chain.emplace_back(Block(0, "Bloc Genesis", "0"));
    }

    // Ajouter un bloc à la blockchain
    void addBlock(Block newBlock) {
        newBlock.prevHash = getLastBlock().hash;
        auto start = std::chrono::high_resolution_clock::now();
        newBlock.mineBlock(difficulty);
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duration = end - start;
        std::cout << "Temps pour miner : " << duration.count() << " secondes\n";
        chain.push_back(newBlock);
    }

    // Retourner le dernier bloc de la chaîne
    Block getLastBlock() const {
        return chain.back();
    }
};

int main() {
    // Créer une blockchain avec une difficulté de 4 (par exemple)
    Blockchain bChain(4);

    std::cout << "Ajout du bloc 1..." << std::endl;
    bChain.addBlock(Block(1, "Données du bloc 1", bChain.getLastBlock().hash));

    std::cout << "Ajout du bloc 2..." << std::endl;
    bChain.addBlock(Block(2, "Données du bloc 2", bChain.getLastBlock().hash));

    std::cout << "Ajout du bloc 3..." << std::endl;
    bChain.addBlock(Block(3, "Données du bloc 3", bChain.getLastBlock().hash));

    return 0;
}