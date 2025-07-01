from harmonies_ai.game_state import GameState
from rich.console import Console
from harmonies_ai.ai.greedy import simulate_game

console = Console()


def main():
    results = []
    for _ in range(100):
        results.append(simulate_game(GameState()))
    return results


if __name__ == "__main__":
    main()
