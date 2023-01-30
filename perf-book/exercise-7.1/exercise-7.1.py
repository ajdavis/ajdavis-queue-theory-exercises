from random import random


r2 = 10
mu1 = 1/.1
mu2 = 1/.05


def trial(r1: float) -> bool:
    completions1 = completions2 = completions = jobs_at1 = jobs_at2 = 0

    # Ticks of the simulation.
    ticks = int(1e5)
    unstable_q_size = ticks / 100
    for _ in range(ticks):
        # Outside arrivals.
        jobs_at1 += r1
        jobs_at2 += r2

        # Jobs complete.
        c1 = min(mu1, jobs_at1)
        jobs_at1 -= c1
        completions1 += c1

        c2 = min(mu2, jobs_at2)
        jobs_at2 -= c2
        completions2 += c2

        # Jobs circulate.
        jobs_at2 += .3 * c1
        completions += .7 * c1

        jobs_at1 += .5 * c2
        completions += .5 * c2

        if jobs_at1 > unstable_q_size or jobs_at2 > unstable_q_size:
            return False

    return True


for r1_ in [3 + i / 100 for i in range(100)]:
    success = trial(r1_)
    print(f"r1: {r1_:.2f}, success {success}")
