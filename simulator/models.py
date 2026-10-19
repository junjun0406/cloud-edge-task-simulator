from dataclasses import dataclass, field


# ==================================================

# タスク


@dataclass
class Task:
    # タスクの基本情報
    id: int
    arrival_time: int
    origin: int
    required_data: int
    size: float
    rho: float

    # タスクの割り当て時刻 s_i
    assignment_time: int | None = None

    # タスクの割り当て結果
    destination: int | None = None
    data_source: int | None = None

    # 総計算量 C_i [cycles]
    total_compute: float = 0.0

    # 残り処理量
    remaining_compute: float = 0.0
    remaining_offload: float = 0.0
    remaining_data: float = 0.0

    # 完了時刻（スロット境界）
    offload_finish_time: int | None = None
    data_finish_time: int | None = None
    compute_start_time: int | None = None
    finish_time: int | None = None

    # 各スロットでの状態
    is_computing: bool = False
    is_offloading: bool = False
    is_data_transferring: bool = False

    # 数値誤差対策
    EPS: float = field(default=1e-9, init=False, repr=False)

    def initialize(self, data_sizes, data_densities):

        # タスク到着時に総計算量を初期化する。
        # C_i = eta_i * rho_i + sigma_ri * gamma_ri

        data_size = data_sizes[self.required_data]
        data_density = data_densities[self.required_data]

        self.total_compute = (
            self.size * self.rho
            + data_size * data_density
        )
        self.remaining_compute = self.total_compute

    def initialize_transfers(self, data_placement, data_sizes):

        # 割り当て決定後に転送量を初期化する。

        if self.destination is None:
            raise ValueError("処理先が決定されていません。")

        # タスク転送
        if self.destination == self.origin:
            self.remaining_offload = 0.0
        else:
            self.remaining_offload = self.size

        # データ転送
        if self.destination in data_placement[self.required_data]:
            self.remaining_data = 0.0
            self.data_source = None
        else:
            if self.data_source is None:
                raise ValueError("データ転送元が決定されていません。")
            if self.data_source not in data_placement[self.required_data]:
                raise ValueError("データ転送元に必要なデータがありません。")

            self.remaining_data = data_sizes[self.required_data]

    # --------------------------------------------------
    # 完了状態

    @property
    def offload_completed(self):
        return self.remaining_offload <= self.EPS

    @property
    def data_completed(self):
        return self.remaining_data <= self.EPS

    @property
    def compute_completed(self):
        return (
            self.finish_time is not None
        )

    @property
    def ready_to_compute(self):

        # タスク転送とデータ転送が両方完了しているか。

        return (
            self.assignment_time is not None
            and self.offload_completed
            and self.data_completed
            and not self.compute_completed
        )

    # --------------------------------------------------
    # 状態更新

    def update_offload(self, amount):

        # 残りタスク転送量を更新する。

        self.remaining_offload = max(
            0.0,
            self.remaining_offload - amount
        )

    def update_data(self, amount):

        # 残りデータ転送量を更新する。

        self.remaining_data = max(
            0.0,
            self.remaining_data - amount
        )

    def update_compute(self, amount):

        # 残り計算量を更新する。

        self.remaining_compute = max(
            0.0,
            self.remaining_compute - amount
        )

    def processing_time(self, delta):

        # タスクの到着から処理完了までの時間 T_i [s]

        if self.finish_time is None:
            return None

        return (
            self.finish_time - self.arrival_time
        ) * delta


# ==================================================

# Edgeサーバ

@dataclass
class Edge:
    id: int

    # 計算能力 f_e [cycles/s]
    compute_capacity: float

    # 初期配置されているデータID
    stored_data: set[int] = field(default_factory=set)


# ==================================================

# 通信リンク

@dataclass
class Link:
    source: int
    destination: int

    # 通信レート R_e'e [bit/s]
    rate: float

    # 帯域上限 B_e'e [bit/s]
    bandwidth: float

    @property
    def max_parallel_transfers(self):

        # 同時に実行できる転送の最大数
        # N_e'e = floor(B_e'e / R_e'e)

        return int(
            (self.bandwidth / self.rate) + 1e-9
        )
