
import time


class Time:
    desired_fps = 100
    fixed_delta_time = 1.0 / 200.0
    delta_time = 0.0

    _acumulator = 0.0
    _time = time.time()
    _frame_time = time.time()

    @staticmethod
    def update():
        new_time = time.time()
        Time.delta_time = new_time - Time._time
        Time._time = new_time
        Time._acumulator += Time.delta_time

    @staticmethod
    def has_physics_time():
        return Time._acumulator > Time.fixed_delta_time

    @staticmethod
    def fixed_update():
        Time._acumulator -= Time.fixed_delta_time

    @staticmethod
    def wait_fps():
        frame_duration = time.time() - Time._frame_time
        time_to_wait = max(0, (1 / Time.desired_fps) - frame_duration)
        time.sleep(time_to_wait)
        Time._frame_time = time.time()
