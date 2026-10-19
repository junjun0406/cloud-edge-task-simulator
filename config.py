# シミュレーションの基本設定


# Edgeサーバ数
NUM_EDGES = 3

# EdgeサーバのID
EDGES = list(range(NUM_EDGES))

# タスク到着を受け付けるスロット数
H = 20

# 1スロットの長さ [s]
DELTA = 1.0

# ランダム割り当て用の乱数シード
RANDOM_SEED = 42

# 到着から割り当てまでの遅延 [スロット]
# 現在は次のスロットで割り当てる
ASSIGNMENT_DELAY_SLOTS = 1


# ==================================================

# Edgeサーバの計算能力

# 各Edgeサーバの計算能力 [cycles/s]
# F[e] が Edge e の計算能力 f_e に対応
F = [5.0, 5.0, 5.0]


# ==================================================

# 通信パラメータ

# 通信レート [bit/s]
# R[e_from][e_to]
R = [
    [0.0, 5.0, 5.0],
    [5.0, 0.0, 5.0],
    [5.0, 5.0, 0.0],
]

# 通信帯域上限 [bit/s]
# B[e_from][e_to]
B = [
    [0.0, 10.0, 10.0],
    [10.0, 0.0, 10.0],
    [10.0, 10.0, 0.0],
]


# ==================================================

# データの設定

# データID
DATA_IDS = [0, 1, 2]

# データサイズ sigma_d [bit]
DATA_SIZES = {
    0: 10.0,
    1: 15.0,
    2: 20.0,
}

# データの計算密度 gamma_d [cycles/bit]
DATA_DENSITIES = {
    0: 1.0,
    1: 1.0,
    2: 1.0,
}

# データ配置 a_de
DATA_PLACEMENT = {
    0: [0],
    1: [1],
    2: [2],
}


# ==================================================

# タスクの設定

# タスク情報
# id            : タスクID i
# arrival_time  : 到着スロット tau_i
# origin        : 発生元Edge o_i
# required_data : 必要データ r_i
# size          : タスクサイズ eta_i [bit]
# rho           : タスクの計算密度 rho_i [cycles/bit]

TASK_CONFIGS = [
    {
        "id": 0,
        "arrival_time": 0,
        "origin": 0,
        "required_data": 1,
        "size": 10.0,
        "rho": 1.0,
    },
    {
        "id": 1,
        "arrival_time": 0,
        "origin": 0,
        "required_data": 2,
        "size": 10.0,
        "rho": 1.0,
    },
    {
        "id": 2,
        "arrival_time": 1,
        "origin": 1,
        "required_data": 0,
        "size": 15.0,
        "rho": 1.0,
    },
    {
        "id": 3,
        "arrival_time": 2,
        "origin": 2,
        "required_data": 1,
        "size": 10.0,
        "rho": 1.0,
    },
    {
        "id": 4,
        "arrival_time": 19,
        "origin": 0,
        "required_data": 2,
        "size": 15.0,
        "rho": 1.0,
    },
]


# ==================================================

# 結果出力の設定

# 各スロットの状態を表示するか
VERBOSE = True

# 結果を保存するディレクトリ
RESULTS_DIR = "results"
