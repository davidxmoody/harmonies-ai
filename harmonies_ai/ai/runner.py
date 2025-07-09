from harmonies_ai.game_state import GameState
from rich.console import Console
from harmonies_ai.ai.greedy import simulate_game
import pandas as pd
from tqdm import tqdm

console = Console()


# %%
def results_to_df(results: list[GameState]):
    return pd.DataFrame({"score": gs.score.total} for gs in results)


# %%
results = []
for _ in tqdm(range(100), desc="Playing games"):
    results.append(simulate_game(GameState()))
df = results_to_df(results)
