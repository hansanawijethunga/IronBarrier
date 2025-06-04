import math
import random

G = 9.81  # gravity constant


def simulate_once(missile_speed, missile_angle_deg, interceptor_speed, detection_range,
                   target_x=1000, dt=0.05, intercept_radius=10):
    """Simulate one missile launch and interceptor attempt.

    Returns True if the interceptor destroys the missile before it
    reaches the target.
    """
    theta = math.radians(missile_angle_deg)
    mx, my = 0.0, 0.0
    mvx = missile_speed * math.cos(theta)
    mvy = missile_speed * math.sin(theta)

    interceptor_active = False
    ix, iy = target_x, 0.0

    t = 0.0
    while mx <= target_x and my >= 0:
        # update missile position
        mx += mvx * dt
        mvy -= G * dt
        my += mvy * dt
        t += dt

        # launch interceptor when missile enters radar range
        if not interceptor_active and mx >= target_x - detection_range:
            interceptor_active = True
            ix, iy = target_x, 0.0

        # move interceptor if active
        if interceptor_active:
            dx = mx - ix
            dy = my - iy
            dist = math.hypot(dx, dy)
            if dist <= intercept_radius:
                return True
            if dist > 0:
                ix += interceptor_speed * dt * dx / dist
                iy += interceptor_speed * dt * dy / dist

    return False


def run_experiments(num_trials=50):
    missile_speeds = [80, 120, 160]
    interceptor_speeds = [120, 180, 240]
    detection_ranges = [200, 400, 600]
    angles = (30, 60)  # range of launch angles in degrees

    for ms in missile_speeds:
        for ispeed in interceptor_speeds:
            for dr in detection_ranges:
                successes = 0
                for _ in range(num_trials):
                    ang = random.uniform(*angles)
                    if simulate_once(ms, ang, ispeed, dr):
                        successes += 1
                rate = successes / num_trials
                print(
                    f"Missile {ms} m/s, Interceptor {ispeed} m/s, Radar {dr} m -> success rate {rate:.2f}"
                )


if __name__ == "__main__":
    run_experiments()
