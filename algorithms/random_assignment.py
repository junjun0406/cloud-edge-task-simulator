import random

from models import Task, Edge


# ==================================================

# ランダム割り当て

def assign_task(
    task: Task,
    edges: list[Edge],
    data_placement: dict[int, list[int]],
    rng: random.Random
) -> None:

    # --------------------------------------------------

    # 処理先Edgeサーバの決定

    if not edges:
        raise ValueError("Edgeサーバが存在しません。")

    destination = rng.choice(edges)

    task.destination = destination.id

    # --------------------------------------------------

    # データ転送元Edgeサーバの決定

    # 必要データを保持しているEdgeサーバ
    data_locations = data_placement[task.required_data]

    # 処理先に必要データが存在する場合
    if task.destination in data_locations:
        task.data_source = None

    # 処理先に必要データが存在しない場合
    else:
        if not data_locations:
            raise ValueError(
                f"データ{task.required_data}の配置先がありません。"
            )

        task.data_source = rng.choice(data_locations)
