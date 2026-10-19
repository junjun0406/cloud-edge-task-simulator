from dataclasses import dataclass

from models import Task, Link


# ==================================================

# 転送要求

@dataclass
class TransferRequest:
    task: Task
    transfer_type: str
    source: int
    destination: int

    @property
    def priority(self):

        # 転送要求の優先順位を返す。

        type_order = {
            "offload": 0,
            "data": 1
        }

        return (
            self.task.assignment_time,
            self.task.id,
            type_order[self.transfer_type]
        )


# ==================================================

# 2. 転送要求の取得

def get_transfer_requests(
    tasks: list[Task],
    current_time: int
) -> list[TransferRequest]:

    # 現在のスロットで未完了の転送要求を取得する。

    requests = []

    for task in tasks:

        # 割り当て前のタスクは通信しない
        if (
                task.assignment_time is None
                or task.assignment_time > current_time
        ):
            continue

        # 処理先が未決定なら対象外
        if task.destination is None:
            continue

        # ------------------------------------------

        # タスク転送

        if not task.offload_completed:

            requests.append(
                TransferRequest(
                    task=task,
                    transfer_type="offload",
                    source=task.origin,
                    destination=task.destination
                )
            )

        # ------------------------------------------

        # データ転送

        if not task.data_completed:

            if task.data_source is None:
                raise ValueError(
                    f"タスク{task.id}のデータ転送元が未設定です。"
                )

            requests.append(
                TransferRequest(
                    task=task,
                    transfer_type="data",
                    source=task.data_source,
                    destination=task.destination
                )
            )

    return requests


# ==================================================

# 通信スケジューリング

def schedule_transfers(
    tasks: list[Task],
    links: list[Link],
    current_time: int
) -> list[TransferRequest]:

    # すべてのタスクの通信実行状態をリセット
    for task in tasks:
        task.is_offloading = False
        task.is_data_transferring = False

    # 未完了の転送要求を取得
    requests = get_transfer_requests(
        tasks,
        current_time
    )

    # 実行する転送要求
    active_requests = []

    # ----------------------------------------------

    # 各リンクでスケジューリング

    for link in links:

        # このリンクを使用する転送要求を抽出
        link_requests = [
            request
            for request in requests
            if (
                request.source == link.source
                and request.destination == link.destination
            )
        ]

        # 優先順位で並び替え
        link_requests.sort(
            key=lambda request: request.priority
        )

        # 同時転送可能数
        max_transfers = link.max_parallel_transfers

        # 優先順位の高い要求から選択
        selected_requests = link_requests[:max_transfers]

        # 実行状態を更新
        for request in selected_requests:

            if request.transfer_type == "offload":
                request.task.is_offloading = True

            elif request.transfer_type == "data":
                request.task.is_data_transferring = True

        active_requests.extend(selected_requests)

    return active_requests
