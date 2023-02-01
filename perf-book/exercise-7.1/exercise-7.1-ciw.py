import ciw
import matplotlib.pyplot as plt
import math
import time
from collections import defaultdict
from dataclasses import dataclass

r1 = 3.5
r2 = 10
s1 = .1
s2 = .05
p12 = .3  # P(job goes from Server 1 to 2).
p21 = .7  # P(job goes from Server 2 to 1).

routing_probabilities = [
    # To Server 1, Server 2.
    [0, p12],  # From Server 1.
    [p21, 0],  # From Server 2.
]

N = ciw.create_network(
    arrival_distributions=[
        ciw.dists.Deterministic(1 / r1),  # Arrivals at Server 1.
        ciw.dists.Deterministic(1 / r2),  # Arrivals at Server 2.
    ],
    service_distributions=[
        ciw.dists.Deterministic(s1),  # Service rate at Server 1.
        ciw.dists.Deterministic(s2),  # Service rate at Server 2.
    ],
    routing=routing_probabilities,
    # One server at each node (Server 1 and 2 are each single).
    number_of_servers=[1, 1],
)
ciw.seed(10)
Q = ciw.Simulation(N)
start = time.time()
Q.simulate_until_max_time(1e3)
print(f"Utilization Server 1: {Q.nodes[1].server_utilisation}")
print(f"Utilization Server 2: {Q.nodes[2].server_utilisation}")
print(f"Real time for simulation: {time.time() - start:.0f} seconds")

recs = Q.get_all_records()


@dataclass
class Individual:
    system_arrival_date: float | None = None
    system_exit_date: float | None = None


individuals = defaultdict(Individual)

for r in recs:
    i = individuals[r.id_number]
    if i.system_arrival_date is None:
        i.system_arrival_date = r.arrival_date
    else:
        i.system_arrival_date = min(i.system_arrival_date, r.arrival_date)

    if i.system_exit_date is None:
        i.system_exit_date = r.exit_date
    else:
        i.system_exit_date = max(i.system_exit_date, r.exit_date)

system_residence_times = [i.system_exit_date - i.system_arrival_date
                          for i in individuals.values()]
plt.hist(x=system_residence_times,
         bins=int(math.ceil(max(system_residence_times))),
         cumulative=True,
         density=True)
plt.title("Residence times CDF")
plt.show()
