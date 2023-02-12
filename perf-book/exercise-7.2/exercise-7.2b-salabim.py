import argparse
import random
from typing import Optional

import salabim as sim

MPL = 6  # Multiprogramming level, number of jobs.
NUM_SERVERS = 2


class Server(sim.Component):
    def __init__(self, *, server_id: int, service_duration: float, **kwargs):
        super().__init__(name=f"Server {server_id}", **kwargs)
        self._server_id = server_id
        self._service_duration: float = service_duration
        self._q = sim.Queue(f"{self.name()} q")
        self._job: Optional["Job"] = None
        self._completions = 0

    @property
    def server_id(self):
        return self._server_id

    @property
    def q(self):
        return self._q

    @property
    def completions(self):
        return self._completions

    def enqueue(self, component: sim.Component):
        component.enter(self._q)
        if not self._job:
            self.activate()

    def animate(self, id: str, x: int, y: int):
        def text():
            return f"{self.name()} {self._job.name() if self._job else 'idle'}"

        sim.AnimateText(x=x + 58, y=y + 30, textcolor="white", text=text,
                        text_anchor="se")
        sim.AnimateCircle(x=x + 50, y=y + 8, radius=16, fillcolor=id)
        sim.AnimateQueue(x=x, y=y, queue=self._q, direction="w", id=id)

    def print_statistics(self):
        self._q.print_statistics()
        print(f"Completions: {self._completions}")

    def process(self):
        while True:
            while len(self._q) == 0:
                yield self.passivate()
            self._job = self._q.pop()
            yield self.hold(self._service_duration)
            self._completions += 1
            self._job.activate()
            self._job = None


class Job(sim.Component):
    def __init__(self, *, servers: list[Server], **kwargs):
        super().__init__(**kwargs)
        self._servers = servers

    def animation_objects(self, id):
        """Callback for AnimateQueue."""
        if id == "text":
            ao0 = sim.AnimateText(text=self.name(), textcolor="fg",
                                  text_anchor="nw")
            return 0, 16, ao0
        else:
            ao0 = sim.AnimateRectangle((-20, 0, 20, 20),
                                       text=self.name(), fillcolor=id,
                                       textcolor="white", arg=self)
            return 45, 0, ao0

    def process(self):
        previous_server = None
        while True:
            server: Server = random.choice(self._servers)
            server.enqueue(self)
            env = sim.default_env()
            if env.animate() and previous_server:
                # TODO: awful hack.
                y_from = server_id_to_y_coord(previous_server.server_id)
                y_to = server_id_to_y_coord(server.server_id)
                sim.Animate(line0=(540, y_from, 300, y_to), t1=env.now() + 1,
                            keep=False, linecolor0="#ffffffff",
                            linecolor1="#ffffff44")

            previous_server = server
            yield self.passivate()


def server_id_to_y_coord(server_id: int):
    return 250 - server_id * 100


def main(server_2_service_rate: float, animate: bool):
    env = sim.Environment(trace=False)
    servers = [Server(server_id=1, service_duration=3),
               Server(server_id=2, service_duration=server_2_service_rate)]
    jobs = [Job(servers=servers) for _ in range(MPL)]
    env.modelname("Exercise 7.2b")
    seed = hash("A. Jesse Jiryu Davis") % 2 ** 32
    sim.random_seed(seed)
    random.seed(seed)

    if animate:
        servers[0].animate(id="blue", x=500, y=server_id_to_y_coord(1))
        servers[1].animate(id="red", x=500, y=server_id_to_y_coord(2))
        env.background_color("20%gray")
        env.animation_parameters(speed=4, animate=True, x1=600, height=400)
        env.run(till=100)
    else:
        env.run(till=100000)

    for server in servers:
        server.print_statistics()

    print(f"{sum(s.completions for s in servers) / env.now()} jobs/unit time")


parser = argparse.ArgumentParser()
parser.add_argument("SERVER_2_SERVICE_RATE", type=float)
parser.add_argument("--animate", action="store_true")
args = parser.parse_args()
main(args.SERVER_2_SERVICE_RATE, args.animate)
