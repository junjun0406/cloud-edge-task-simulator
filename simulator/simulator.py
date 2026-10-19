import random

import config

from models import Task, Edge, Link
from assignment import assign_task
from scheduler import schedule_transfers


class Simulator:

    # ==================================================

    # 初期化

    def __init__(self):

        # シミュレーション設定
        self.delta = config.DELTA
        self.horizon = config.H
        self.verbose = config.VERBOSE

        # 乱数生成器
        self.rng = random.Random(config.RANDOM_SEED)

        # 現在のスロット
        self.current_time = 0

        # ----------------------------------------------

        # Edgeサーバの生成

        self.edges = []

        for e in config.EDGES:

            stored_data = {
                d
                for d, locations in config.DATA_PLACEMENT.items()
                if e in locations
            }

            edge = Edge(
                id=e,
                compute_capacity=config.F[e],
                stored_data=stored_data
            )

            self.edges.append(edge)

        # ----------------------------------------------

        # 有向リンクの生成

        self.links = []

        for source in config.EDGES:
            for destination in config.EDGES:

                if source == destination:
                    continue

                link = Link(
                    source=source,
                    destination=destination,
                    rate=config.R[source][destination],
                    bandwidth=config.B[source][destination]
                )

                self.links.append(link)

        # リンク検索用
        self.link_dict = {
            (link.source, link.destination): link
            for link in self.links
        }

        # ----------------------------------------------

        # タスクの生成

        self.tasks = []

        for task_config in config.TASK_CONFIGS:

            task = Task(**task_config)

            self.tasks.append(task)

        # 到着順に並べる
        self.tasks.sort(
            key=lambda task: (task.arrival_time, task.id)
        )

        # 到着済みタスク
        self.arrived_tasks = []

    # ==================================================

    # タスクの到着と割り当て

    def handle_arrivals(self, t):

        for task in self.tasks:

            if task.arrival_time != t:
                continue

            # 到着時に総計算量を初期化
            task.initialize(
                config.DATA_SIZES,
                config.DATA_DENSITIES
            )

            self.arrived_tasks.append(task)

            if self.verbose:
                print(
                    f"[t={t}] Task {task.id} arrived: "
                    f"origin={task.origin}"
                )

    def handle_assignments(self, t):

        # このスロットで割り当てるタスク
        tasks_to_assign = [
            task
            for task in self.arrived_tasks
            if (
                    task.assignment_time is None
                    and task.arrival_time
                    + config.ASSIGNMENT_DELAY_SLOTS == t
            )
        ]

        for task in tasks_to_assign:

            # 処理先とデータ転送元を決定
            assign_task(
                task,
                self.edges,
                config.DATA_PLACEMENT,
                self.rng
            )

            # 割り当て時刻を記録
            task.assignment_time = t

            # 割り当て後に転送量を初期化
            task.initialize_transfers(
                config.DATA_PLACEMENT,
                config.DATA_SIZES
            )

            # 転送が不要な場合は割り当て時点で完了
            if task.offload_completed:
                task.offload_finish_time = t

            if task.data_completed:
                task.data_finish_time = t

            if self.verbose:
                print(
                    f"[t={t}] Task {task.id} assigned: "
                    f"destination={task.destination}, "
                    f"data_source={task.data_source}"
                )

    # ==================================================

    # 1スロットの実行

    def step(self):

        t = self.current_time

        # ----------------------------------------------

        # 新しいタスクの到着

        if t < self.horizon:
            self.handle_arrivals(t)

        # 到着済みタスクの割り当て

        self.handle_assignments(t)

        # ----------------------------------------------

        # 通信スケジューリング

        active_requests = schedule_transfers(
            self.arrived_tasks,
            self.links,
            t
        )

        # ----------------------------------------------

        # 計算可能タスクの決定

        # この時点の転送完了状態で判定する
        computing_tasks = {
            edge.id: []
            for edge in self.edges
        }

        for task in self.arrived_tasks:

            task.is_computing = False

            if task.ready_to_compute:
                computing_tasks[task.destination].append(task)

        # ----------------------------------------------

        # 通信量の更新

        for request in active_requests:

            link = self.link_dict[
                (request.source, request.destination)
            ]

            # 1スロットで転送可能なデータ量
            transfer_amount = link.rate * self.delta

            if request.transfer_type == "offload":

                request.task.update_offload(
                    transfer_amount
                )

                if request.task.offload_completed:
                    request.task.offload_finish_time = t + 1

            elif request.transfer_type == "data":

                request.task.update_data(
                    transfer_amount
                )

                if request.task.data_completed:
                    request.task.data_finish_time = t + 1

        # ----------------------------------------------

        # 計算量の更新

        for edge in self.edges:

            tasks_on_edge = computing_tasks[edge.id]

            # 計算可能なタスク数
            k = len(tasks_on_edge)

            if k == 0:
                continue

            # 各タスクに均等配分する計算量
            compute_amount = (
                edge.compute_capacity * self.delta / k
            )

            for task in tasks_on_edge:

                task.is_computing = True

                if task.compute_start_time is None:
                    task.compute_start_time = t

                task.update_compute(
                    compute_amount
                )

                # 計算完了
                if task.remaining_compute <= task.EPS:

                    task.finish_time = t + 1

                    if self.verbose:
                        print(
                            f"[t={t + 1}] "
                            f"Task {task.id} completed"
                        )

        # ----------------------------------------------

        # 次のスロットへ

        self.current_time += 1

    # ==================================================

    # シミュレーション実行

    def run(self):

        if self.verbose:
            print("Simulation started")

        while True:

            # 全タスクが到着し、処理が完了したか
            all_completed = all(
                task.compute_completed
                for task in self.tasks
            )

            # 到着期間終了後、全タスク完了なら終了
            if (
                self.current_time >= self.horizon
                and all_completed
            ):
                break

            self.step()

        if self.verbose:
            print("Simulation finished")

        return self.tasks
