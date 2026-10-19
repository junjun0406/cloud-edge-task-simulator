from simulator import Simulator
import config


def main():

    # ==============================================

    # シミュレーションの実行

    simulator = Simulator()

    tasks = simulator.run()

    # ==============================================

    # 各タスクの結果を表示

    print("\n========== Task Results ==========")

    for task in tasks:

        processing_time = task.processing_time(
            config.DELTA
        )

        print(f"\nTask {task.id}")
        print(f"  Arrival time       : {task.arrival_time}")
        print(f"  Assignment time    : {task.assignment_time}")
        print(f"  Origin             : {task.origin}")
        print(f"  Destination        : {task.destination}")
        print(f"  Required data      : {task.required_data}")
        print(f"  Data source        : {task.data_source}")
        print(f"  Offload finish     : {task.offload_finish_time}")
        print(f"  Data finish        : {task.data_finish_time}")
        print(f"  Compute start      : {task.compute_start_time}")
        print(f"  Finish time        : {task.finish_time}")
        print(f"  Processing time    : {processing_time:.2f} s")

    # ==============================================

    # 最大処理時間の計算

    processing_times = [
        task.processing_time(config.DELTA)
        for task in tasks
    ]

    if processing_times:

        max_processing_time = max(processing_times)
        average_processing_time = (
            sum(processing_times) / len(processing_times)
        )

        print("\n========== Summary ==========")
        print(f"Number of tasks         : {len(tasks)}")
        print(f"Maximum processing time : {max_processing_time:.2f} s")
        print(f"Average processing time : {average_processing_time:.2f} s")
        print(f"Simulation end slot     : {simulator.current_time}")

    else:
        print("\nNo tasks were generated.")


if __name__ == "__main__":
    main()
