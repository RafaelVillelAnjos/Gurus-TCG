from typing import List, Optional, Any
from dataclasses import dataclass, replace
from random import choice, randint, sample, shuffle
from time import sleep

# ---- ESTRUTURAS DE DADOS ----
# PILHA DE COMPRA
class Stack:
    def __init__(self):
        self._data: List[Any] = []

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        try:
            if not self._data:
                raise IndexError("A pilha de compra está vazia")
            return self._data.pop()
        except IndexError as e:
            print(e)
        return None

    def peek(self) -> Any:
        try:
            if not self._data:
                raise IndexError("A pilha de compra está vazia")
            return self._data[-1]
        except IndexError as e:
            print(e)
        return None

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

# PILHA DE DESCARTE
class Queue:
    def __init__(self):
        self._data: List[Any] = []

    def enqueue(self, item: Any) -> None:
        self._data.append(item)

    def dequeue(self) -> Any:
        try:
            if not self._data:
                raise IndexError("Dequeue from empty queue")
            return self._data.pop(0)
        except IndexError as e:
            print(e)
        return None

    def peek(self) -> Any:
        try:
            if not self._data:
                raise IndexError("Peek from empty queue")
            return self._data[0]
        except IndexError as e:
            print(e)
        return None
    
    def is_empty(self) -> bool:
        return len(self._data) == 0

# CAMPO DE BATALHA (FILA DE PRIORIDADE)
@dataclass
class ElementPriority:
    item: Any
    priority: int


class PriorityQueue:
    """Fila de prioridade: o maior valor de prioridade fica na frente.
    Em caso de empate, quem entrou primeiro continua na frente."""

    def __init__(self, capacity: Optional[int] = None):
        self._data: List[ElementPriority] = []
        self.capacity = capacity

    def enqueue(self, item: Any, priority: int) -> bool:
        if self.is_full():
            print("A fila de prioridade está cheia")
            return False

        # Procura a primeira posição cujo elemento tem prioridade menor
        position = len(self._data)
        for i, element in enumerate(self._data):
            if priority > element.priority:
                position = i
                break

        self._data.insert(position, ElementPriority(item, priority))
        return True

    def dequeue(self) -> Any:
        try:
            if not self._data:
                raise IndexError("O campo de batalha está vazio")
            return self._data.pop(0).item
        except IndexError as e:
            print(e)
        return None

    def peek(self) -> Any:
        try:
            if not self._data:
                raise IndexError("O campo de batalha está vazio")
            return self._data[0].item
        except IndexError as e:
            print(e)
        return None

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def is_full(self) -> bool:
        return self.capacity is not None and len(self._data) >= self.capacity

    def size(self) -> int:
        return len(self._data)

    def to_list(self) -> List[Any]:
        """Itens na ordem da fila, sem removê-los (usado para exibir)."""
        return [element.item for element in self._data]


# ---- CARTAS ----
TOTAL_POINTS = 15
MIN_POINTS = 1
MAX_POINTS = 10
MIN_FOCUS_POINTS = 7

ATTACK_MIN, ATTACK_MAX = 6, 10
DEFENSE_MIN, DEFENSE_MAX = 9, 15
SPEED_MIN, SPEED_MAX = 1, 10

CARD_NAMES = [
    "Cavaleiro", "Dragão", "Aranha Gigante", "Gigante", "Clériga",
    "Assassino", "Arqueira", "Mago", "Morto-Vivo", "Esqueleto",
    "Bárbaro", "Alcateia de Lobos", "Piromante", "Ladrão", "Feiticeira",
    "Caçador", "Rei", "Slime Grande", "Minotauro", "Fada",
    "Espírito da Floresta", "Druída", "Urso", "Golem de Pedra",
    "Homem-Peixe", "Anão", "Duende", "Elfo", "Orc", "Ogro", "Diabrete",
    "Demônio", "Draconato", "Centauro", "Grupo de Goblins",
]

ATTACK_BY_POINTS = {
    1: 6, 2: 6,
    3: 7, 4: 7,
    5: 8, 6: 8,
    7: 9, 8: 9,
    9: 10, 10: 10,
}

DEFENSE_BY_POINTS = {
    1: 9,
    2: 10,
    3: 11, 4: 11,
    5: 12,
    6: 13, 7: 13,
    8: 14,
    9: 15, 10: 15,
}


@dataclass(frozen=True)
class Card:
    attack: int
    defense: int
    speed: int
    attack_points: int
    defense_points: int
    speed_points: int
    focus: str = "balanceada"
    nome: str = ""

    @property
    def total_points(self) -> int:
        return self.attack_points + self.defense_points + self.speed_points

    @property
    def stats_key(self) -> tuple[int, int, int]:
        return self.attack, self.defense, self.speed

    def __str__(self) -> str:
        return (
            f"{self.nome:20s} | "
            f"ATQ={self.attack:2d} | DEF={self.defense:2d} | "
            f"VEL={self.speed:2d} | "
            f"foco={self.focus} |"
        )

@dataclass(frozen=True)
class AttackResult:
    die_1: int
    die_2: int
    attack_total: int
    hit: bool
    critical: Optional[str] = None

    def __str__(self) -> str:
        if self.critical == "critical_miss":
            result = "ERRO CRÍTICO"
        elif self.critical == "critical_hit":
            result = "ACERTO CRÍTICO"
        elif self.hit:
            result = "ACERTO"
        else:
            result = "ERRO"

        return (
            f"dados={self.die_1}+{self.die_2} | "
            f"ataque final={self.attack_total} | {result}"
        )


def build_all_allocations() -> list[tuple[int, int, int]]:
    """Gera as 73 distribuições válidas de 15 pontos."""
    allocations = []

    for pa in range(MIN_POINTS, MAX_POINTS + 1):
        for pd in range(MIN_POINTS, MAX_POINTS + 1):
            pv = TOTAL_POINTS - pa - pd

            if MIN_POINTS <= pv <= MAX_POINTS:
                allocations.append((pa, pd, pv))

    return allocations


ALL_ALLOCATIONS = build_all_allocations()


def card_from_allocation(
    attack_points: int,
    defense_points: int,
    speed_points: int,
    focus: str = "balanceada",
    nome: str = "",
) -> Card:
    """Converte pontos internos em atributos visíveis."""

    points = (attack_points, defense_points, speed_points)

    if any(p < MIN_POINTS or p > MAX_POINTS for p in points):
        raise ValueError("Cada atributo deve receber entre 1 e 10 pontos.")

    if sum(points) != TOTAL_POINTS:
        raise ValueError(f"A distribuição precisa somar {TOTAL_POINTS} pontos.")

    return Card(
        attack=ATTACK_BY_POINTS[attack_points],
        defense=DEFENSE_BY_POINTS[defense_points],
        speed=speed_points,
        attack_points=attack_points,
        defense_points=defense_points,
        speed_points=speed_points,
        focus=focus,
        nome=nome,
    )


FOCUS_INDEX = {
    "ataque": 0,
    "defesa": 1,
    "veloz": 2,
}


def normalize_focus(focus: str) -> str:
    aliases = {
        "ataque": "ataque",
        "atq": "ataque",
        "defesa": "defesa",
        "def": "defesa",
        "veloz": "veloz",
        "velocidade": "veloz",
        "vel": "veloz",
    }

    key = focus.strip().lower()

    if key not in aliases:
        raise ValueError("Tipo inválido. Use ataque, defesa ou veloz.")

    return aliases[key]


def build_focus_pool(focus: str) -> list[Card]:
    """
    Cria o pool de um tipo.

    O atributo principal:
        >= 7 pontos
        > cada um dos demais atributos
    """

    focus = normalize_focus(focus)
    index = FOCUS_INDEX[focus]
    unique: dict[tuple[int, int, int], Card] = {}

    for allocation in ALL_ALLOCATIONS:
        main = allocation[index]

        if main < MIN_FOCUS_POINTS:
            continue

        if any(main <= allocation[i] for i in range(3) if i != index):
            continue

        card = card_from_allocation(*allocation, focus=focus)
        unique.setdefault(card.stats_key, card)

    return list(unique.values())


FOCUS_POOLS = {
    focus: build_focus_pool(focus)
    for focus in FOCUS_INDEX
}


def take_random_cards(cards: list[Card], amount: int) -> list[Card]:
    result = []

    while amount > 0:
        cycle_size = min(amount, len(cards))
        result.extend(sample(cards, cycle_size))
        amount -= cycle_size

    return result


def generate_cards(amount: int) -> list[Card]:
    focuses = ["ataque", "defesa", "veloz"]
    base, remainder = divmod(amount, 3)

    counts = {focus: base for focus in focuses}

    extra_focuses = focuses.copy()
    shuffle(extra_focuses)

    for focus in extra_focuses[:remainder]:
        counts[focus] += 1

    result = []

    for focus in focuses:
        result.extend(
            take_random_cards(
                FOCUS_POOLS[focus],
                counts[focus],
            )
        )

    nomes = sample(CARD_NAMES, amount)
    result = [replace(card, nome=nome) for card, nome in zip(result, nomes)]

    shuffle(result)
    return result


def attack_test(attacker: Card, defender: Card) -> AttackResult:
    d1 = randint(1, 4)
    d2 = randint(1, 4)
    attack_total = attacker.attack + d1 + d2

    if d1 == 1 and d2 == 1:
        return AttackResult(
            d1, d2, attack_total,
            hit=False,
            critical="critical_miss",
        )

    if d1 == 4 and d2 == 4:
        return AttackResult(
            d1, d2, attack_total,
            hit=True,
            critical="critical_hit",
        )

    return AttackResult(
        d1,
        d2,
        attack_total,
        hit=attack_total > defender.defense,
    )


def print_cards(cards: list[Card]) -> None:
    for i, card in enumerate(cards, start=1):
        print(f"{i:3d}. {card}")


def menu_generate_many() -> list[Card]:
    """Gera o baralho aleatório de um jogador e devolve a lista de cartas."""
    amount = 30
    cards = generate_cards(amount)

    counts = {"ataque": 0, "defesa": 0, "veloz": 0}

    for card in cards:
        counts[card.focus] += 1

    print("\nDistribuição:")
    for focus, count in counts.items():
        print(f"  {focus:7s}: {count}")

    return cards


# ---- INFOS JOGADORES ----
MAX_MAO = 10
MAX_CAMPO = 5
CARTAS_INICIAIS = 10
PAUSA_ENTRE_TURNOS = 3


class Jogador:
    def __init__(self, nome, vida=20):
        self.nome = nome
        self.vida = vida
        self.pilhaCompra = Stack()
        self.mao = []
        self.pilhaDescarte = Queue()
        self.campo = PriorityQueue(MAX_CAMPO)

    def comprar_carta(self, acao) -> bool:
        if len(self.mao) >= MAX_MAO:
            print(f'{self.nome} já está com a mão cheia ({MAX_MAO} cartas).')
            return False

        if acao == '2':
            if self.pilhaDescarte.is_empty():
                print(f'{self.nome} não tem mais cartas na pilha de descarte.')
                return False

            self.mao.append(self.pilhaDescarte.pop())
            return True
        
        else:
            if self.pilhaCompra.is_empty():
                print(f'{self.nome} não tem mais cartas na pilha de compra.')
                return False

            self.mao.append(self.pilhaCompra.pop())
            return True
        
    def jogar_no_campo(self, numero: int) -> Card:
        if self.campo.is_full():
            raise ValueError(
                f'Seu campo de batalha está cheio ({MAX_CAMPO} cartas).'
            )

        if not 1 <= numero <= len(self.mao):
            raise ValueError(
                f'Número inválido. Escolha uma carta de 1 a {len(self.mao)}.'
            )

        carta = self.mao.pop(numero - 1)
        self.campo.enqueue(carta, carta.speed)
        return carta


def cadastro_jogador() -> list[Jogador]:
    jogadores = []

    for i in range(2):
        nomeJogador = input(f'Jogador {i + 1}, digite seu nome:\n')

        jogador = Jogador(nomeJogador)

        cartas = menu_generate_many()
        for carta in cartas:
            jogador.pilhaCompra.push(carta)

        print(f'\nNome de jogador: {jogador.nome}')
        print('Baralho de jogador:')
        print_cards(cartas)
        print()

        jogadores.append(jogador)

    input('Pressione enter para iniciar o jogo')
    return jogadores


def mostrar_campo(titulo: str, jogador: Jogador) -> None:
    print(f'\n[{titulo}] ({jogador.campo.size()}/{MAX_CAMPO})')
    if jogador.campo.is_empty():
        print('  (vazio)')
    else:
        print_cards(jogador.campo.to_list())


# ---- JOGO ----
def Main():
    print('Bem vindo ao Gurus TCG ' \
        '\nAperte enter para iniciar')
    input()

    print('---- CRIAÇÃO DE JOGADOR ----')
    jogadores = cadastro_jogador()

    for jogador in jogadores:
        for _ in range(CARTAS_INICIAIS):
            jogador.comprar_carta(acao=0)

    turno = 0
    indice = 0

    while all(j.vida > 0 for j in jogadores):
        turno += 1
        jogador = jogadores[indice]
        inimigo = jogadores[1 - indice]

        comprou = False
        jogou = False

        while True:
            print(f'\n===== Turno {turno} =====')
            print(f'Vez de: {jogador.nome}')

            mostrar_campo(f'Campo de {inimigo.nome} (inimigo)', inimigo)
            mostrar_campo(f'Campo de {jogador.nome} (você)', jogador)

            print(f'\nCartas na pilha de compra: {jogador.pilhaCompra.size()}')
            print(f'Cartas na mão: {len(jogador.mao)}')
            print_cards(jogador.mao)

            print(
                '\n1 - Comprar carta da pilha de compra'
                '\n2 - Comprar carta da pilha de descarte'
                '\n3 - Adicionar carta no campo de batalha'
                '\n4 - Passar a vez'
            )

            acao = input('Escolha sua ação: ').strip()

            try:
                if acao == '1':
                    if comprou:
                        print('Você já comprou uma carta neste turno.')
                    elif jogador.comprar_carta(acao):
                        comprou = True
                elif acao == '2':
                    if comprou:
                        print('Você já comprou uma carta nesse turno.')
                    elif jogador.comprar_carta(acao):
                        comprou = True
                elif acao == '3':
                    if jogou:
                        print('Você já adicionou uma carta ao campo neste turno.')
                    elif jogador.campo.is_full():
                        print(f'Seu campo de batalha está cheio ({MAX_CAMPO} cartas).')
                    elif not jogador.mao:
                        print('Você não tem cartas na mão.')
                    else:
                        entrada = input(
                            'Qual carta deseja colocar em campo? (número): '
                        ).strip()

                        if not entrada.isdigit():
                            print('Digite um número válido.')
                        else:
                            carta = jogador.jogar_no_campo(int(entrada))
                            jogou = True
                            print(f'{carta.nome} foi colocada no campo!')
                elif acao == '4':
                    break
                else:
                    print('Opção inválida.')
            except ValueError as erro:
                print(erro)

            sleep(1)

        indice = 1 - indice

        if all(j.vida > 0 for j in jogadores):
            print(f'\nPróxima vez: {jogadores[indice].nome}')
            for segundos in range(PAUSA_ENTRE_TURNOS, 0, -1):
                print(f'{segundos}...')
                sleep(1)

    for j in jogadores:
        if j.vida > 0:
            print(f'\nFim de jogo! {j.nome} venceu!')

    return jogadores

if __name__ == "__main__":
    Main()