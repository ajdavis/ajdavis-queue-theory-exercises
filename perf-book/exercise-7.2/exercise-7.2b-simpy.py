from dataclasses import dataclass

import simpy


def trial(server_2_service_rate):
    multi_programming_level = 6

    env = simpy.Environment()
    current_server_id = 0

    @dataclass
    class Server:
        service_rate: int
        queue: simpy.Resource
        completions: int = 0

    servers = [Server(3, simpy.Resource(env)),
               Server(server_2_service_rate, simpy.Resource(env))]

    def job():
        nonlocal current_server_id

        while True:
            # Deterministically alternate servers.
            chosen_server_id = current_server_id
            current_server_id = (current_server_id + 1) % len(servers)
            chosen_server = servers[chosen_server_id]
            with chosen_server.queue.request() as request:
                yield request
                yield env.timeout(chosen_server.service_rate)
                chosen_server.completions += 1

    def print_state():
        print(f"{env.now:>4}"
              f" Server 1: qlen {len(servers[0].queue.queue):>2}"
              f" completed {servers[0].completions:>2},"
              f" Server 2: qlen {len(servers[1].queue.queue):>2}"
              f" completed {servers[1].completions:>2}")

    for i in range(multi_programming_level):
        env.process(job())

    until = 20
    now = env.now
    while env.peek() < until:
        env.step()
        if env.now != now:
            print_state()
            now = env.now

    throughput = (servers[0].completions + servers[1].completions) / env.now
    print(f"Throughput: {throughput:.2}")


for rate in (3, 1.5):
    print(f"Server 2 service rate: {rate}")
    trial(rate)
    print("-----------------------------")
