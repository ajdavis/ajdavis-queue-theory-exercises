r2 = 10
s1 = .1
s2 = .05


def trial(r1: float) -> (bool, float, float):
    mu1 = 1 / s1
    mu2 = 1 / s2
    completions1 = completions2 = completions = jobs_at1 = jobs_at2 = 0

    # Ticks of the simulation.
    ticks = int(1e5)
    unstable_q_size = ticks / 100
    tick = 0
    for tick in range(ticks):
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
            return (False,  # Success.
                    completions1 * s1 / tick,  # Utilization of Server 1.
                    completions2 * s2 / tick)  # Utilization of Server 2.

    return (True,  # Success.
            completions1 * s1 / tick,  # Utilization of Server 1.
            completions2 * s2 / tick)  # Utilization of Server 2.


for r1_ in [3 + i / 100 for i in range(100)]:
    success, utilization1, utilization2 = trial(r1_)
    print(f"r1: {r1_:.2f}, success {success}, util 1: {utilization1:.4f},"
          f" util 2: {utilization2:.4f}")
