import time
import hashlib
import random
import logging
import statistics
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Block:
    """
    Structure de données représentant un bloc dans la blockchain.

    Attributes:
        data (str): Les données contenues dans le bloc
        timestamp (float): Horodatage de la création du bloc
        previous_hash (str): Hash du bloc précédent (chaînage)
    """
    data: str
    timestamp: float
    previous_hash: str = ""


@dataclass
class BenchmarkResult:
    """
    Structure pour stocker les résultats des benchmarks.

    Attributes:
        algorithm (str): Nom de l'algorithme testé
        execution_times (List[float]): Liste des temps d'exécution
        parameters (Dict): Paramètres utilisés pour le benchmark
    """
    algorithm: str
    execution_times: List[float]
    parameters: Dict

    @property
    def avg_time(self) -> float:
        """Calcule le temps moyen d'exécution."""
        return statistics.mean(self.execution_times)

    @property
    def std_dev(self) -> float:
        """Calcule l'écart-type des temps d'exécution."""
        return statistics.stdev(self.execution_times) if len(self.execution_times) > 1 else 0


class ProofOfWork:
    """
    Implémentation de l'algorithme de consensus Proof of Work.

    Le PoW nécessite la résolution d'un puzzle cryptographique : trouver un nonce
    qui, combiné avec les données du bloc, produit un hash commençant par un
    nombre spécifique de zéros.
    """

    def __init__(self, difficulty: int):
        """
        Initialise le système PoW.

        Args:
            difficulty: Nombre de zéros requis au début du hash

        Raises:
            ValueError: Si la difficulté est hors limites
        """
        if not 0 <= difficulty <= 64:
            raise ValueError("La difficulté doit être entre 0 et 64")
        self.difficulty = difficulty
        self.max_nonce = 2 ** 32  # Limite pour éviter une boucle infinie

    def _calculate_hash(self, block: Block, nonce: int) -> str:
        """
        Calcule le hash SHA-256 du bloc avec le nonce donné.

        Args:
            block: Le bloc à hasher
            nonce: La valeur du nonce à utiliser

        Returns:
            Le hash hexadécimal
        """
        block_content = f"{block.data}-{block.timestamp}-{block.previous_hash}-{nonce}".encode()
        return hashlib.sha256(block_content).hexdigest()

    def mine(self, block: Block) -> Tuple[int, str]:
        """
        Mine un bloc en trouvant un nonce valide.

        Args:
            block: Le bloc à miner

        Returns:
            Tuple contenant (nonce trouvé, hash correspondant)

        Raises:
            RuntimeError: Si aucun nonce valide n'est trouvé
        """
        target = "0" * self.difficulty

        for nonce in range(self.max_nonce):
            block_hash = self._calculate_hash(block, nonce)

            if block_hash.startswith(target):
                logger.info(f"Block miné avec succès: nonce={nonce}, hash={block_hash}")
                return nonce, block_hash

        raise RuntimeError("Échec du minage: nonce valide non trouvé")


class ProofOfStake:
    """
    Implémentation de l'algorithme de consensus Proof of Stake.

    Le PoS sélectionne les validateurs en fonction de leur mise (stake).
    Plus la mise est importante, plus la probabilité d'être sélectionné est grande.
    """

    def __init__(self, minimum_stake: float = 1.0):
        """
        Initialise le système PoS.

        Args:
            minimum_stake: Mise minimum requise pour être validateur
        """
        self.stakers: Dict[str, float] = {}
        self.minimum_stake = minimum_stake
        self.total_stake: float = 0

    def add_staker(self, address: str, stake: float) -> None:
        """
        Ajoute ou met à jour un validateur.

        Args:
            address: Adresse du validateur
            stake: Montant de la mise

        Raises:
            ValueError: Si la mise est inférieure au minimum
        """
        if stake < self.minimum_stake:
            raise ValueError(f"Mise minimum requise: {self.minimum_stake}")

        self.total_stake += stake - self.stakers.get(address, 0)
        self.stakers[address] = stake
        logger.info(f"Validateur ajouté: {address} avec mise={stake}")

    def remove_staker(self, address: str) -> None:
        """
        Retire un validateur du système.

        Args:
            address: Adresse du validateur à retirer
        """
        if address in self.stakers:
            self.total_stake -= self.stakers[address]
            del self.stakers[address]
            logger.info(f"Validateur retiré: {address}")

    def select_validator(self) -> Optional[str]:
        """
        Sélectionne un validateur de façon aléatoire pondérée par les mises.

        Returns:
            L'adresse du validateur sélectionné ou None si aucun validateur
        """
        if not self.stakers:
            return None

        rand_value = random.uniform(0, self.total_stake)
        cumulative = 0

        for address, stake in self.stakers.items():
            cumulative += stake
            if cumulative >= rand_value:
                return address

        return list(self.stakers.keys())[-1]

    def validate_block(self, block: Block) -> Tuple[str, str]:
        """
        Valide un bloc en sélectionnant un validateur.

        Args:
            block: Le bloc à valider

        Returns:
            Tuple contenant (adresse du validateur, message de validation)

        Raises:
            RuntimeError: Si aucun validateur n'est disponible
        """
        validator = self.select_validator()
        if not validator:
            raise RuntimeError("Aucun validateur disponible")

        validation_message = (
            f"Bloc validé par {validator} | "
            f"Données: {block.data} | "
            f"Timestamp: {block.timestamp}"
        )
        logger.info(f"Validation réussie: {validation_message}")

        return validator, validation_message


def benchmark_pow(pow_instance: ProofOfWork, block: Block, num_runs: int = 10) -> BenchmarkResult:
    """
    Effectue un benchmark de l'algorithme PoW.

    Args:
        pow_instance: Instance de ProofOfWork à tester
        block: Bloc à miner
        num_runs: Nombre d'exécutions pour le benchmark

    Returns:
        Résultats du benchmark
    """
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        pow_instance.mine(block)
        times.append(time.time() - start_time)

    return BenchmarkResult(
        algorithm="PoW",
        execution_times=times,
        parameters={"difficulty": pow_instance.difficulty}
    )


def benchmark_pos(pos_instance: ProofOfStake, block: Block, num_runs: int = 100) -> BenchmarkResult:
    """
    Effectue un benchmark de l'algorithme PoS.

    Args:
        pos_instance: Instance de ProofOfStake à tester
        block: Bloc à valider
        num_runs: Nombre d'exécutions pour le benchmark

    Returns:
        Résultats du benchmark
    """
    times = []
    validator_selections = {}

    for _ in range(num_runs):
        start_time = time.time()
        validator, _ = pos_instance.validate_block(block)
        times.append(time.time() - start_time)
        validator_selections[validator] = validator_selections.get(validator, 0) + 1

    # Calculer la distribution des validateurs sélectionnés
    total_runs = sum(validator_selections.values())
    distribution = {k: v / total_runs * 100 for k, v in validator_selections.items()}

    return BenchmarkResult(
        algorithm="PoS",
        execution_times=times,
        parameters={"validator_distribution": distribution}
    )


def run_comprehensive_benchmark():
    """
    Exécute un benchmark complet des deux algorithmes et affiche les résultats.
    """
    # Création d'un bloc de test
    test_block = Block(
        data="Données de test benchmark",
        timestamp=time.time(),
        previous_hash="0000000000000000000000000000000000000000000000000000000000000000"
    )

    # Benchmark PoW avec différentes difficultés
    pow_results = {}
    for difficulty in range(3, 6):
        pow = ProofOfWork(difficulty=difficulty)
        result = benchmark_pow(pow, test_block, num_runs=5)
        pow_results[difficulty] = result
        logger.info(
            f"PoW (difficulté={difficulty}): "
            f"Temps moyen={result.avg_time:.4f}s, "
            f"Écart-type={result.std_dev:.4f}s"
        )

    # Configuration et benchmark PoS
    pos = ProofOfStake(minimum_stake=5.0)
    stakes = {
        "Validateur1": 10.0,
        "Validateur2": 20.0,
        "Validateur3": 30.0
    }
    for addr, stake in stakes.items():
        pos.add_staker(addr, stake)

    pos_result = benchmark_pos(pos, test_block, num_runs=100)
    logger.info(
        f"PoS: Temps moyen={pos_result.avg_time:.4f}s, "
        f"Écart-type={pos_result.std_dev:.4f}s"
    )
    logger.info(
        "Distribution des validateurs: "
        f"{pos_result.parameters['validator_distribution']}"
    )

    # Visualisation des résultats
    plt.figure(figsize=(12, 6))

    # Graphique pour PoW
    plt.subplot(1, 2, 1)
    difficulties = list(pow_results.keys())
    avg_times = [result.avg_time for result in pow_results.values()]
    plt.plot(difficulties, avg_times, 'bo-')
    plt.xlabel('Difficulté')
    plt.ylabel('Temps moyen (s)')
    plt.title('Performance PoW vs Difficulté')
    plt.grid(True)

    # Graphique pour distribution PoS
    plt.subplot(1, 2, 2)
    distribution = pos_result.parameters['validator_distribution']
    plt.bar(distribution.keys(), distribution.values())
    plt.xlabel('Validateurs')
    plt.ylabel('Pourcentage de sélection (%)')
    plt.title('Distribution des validateurs PoS')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def main():
    """
    Point d'entrée principal du programme.
    """
    # Test simple des algorithmes
    test_block = Block(
        data="Données de test",
        timestamp=time.time(),
        previous_hash="0000000000000000000000000000000000000000000000000000000000000000"
    )

    # Test PoW
    pow = ProofOfWork(difficulty=4)
    start_time = time.time()
    try:
        nonce, pow_hash = pow.mine(test_block)
        pow_time = time.time() - start_time
        logger.info(f"PoW: Nonce={nonce}, Hash={pow_hash}, Temps={pow_time:.4f}s")
    except RuntimeError as e:
        logger.error(f"Erreur PoW: {e}")

    # Test PoS
    pos = ProofOfStake(minimum_stake=5.0)
    pos.add_staker("Validateur1", 10.0)
    pos.add_staker("Validateur2", 20.0)
    pos.add_staker("Validateur3", 30.0)

    start_time = time.time()
    try:
        validator, result = pos.validate_block(test_block)
        pos_time = time.time() - start_time
        logger.info(f"PoS: {result}, Temps={pos_time:.4f}s")
    except RuntimeError as e:
        logger.error(f"Erreur PoS: {e}")

    # Exécuter le benchmark complet
    run_comprehensive_benchmark()


if __name__ == "__main__":
    main()