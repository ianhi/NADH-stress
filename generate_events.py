from typing import Dict, List, Iterator
from useq import MDAEvent, MDASequence, Channel
from collections import defaultdict


def update_event_exp(
    mda: MDASequence,
    defaultExposures: Dict[str, float],
    expByPosition: Dict[str, List[float]],
):
    channels = list(defaultExposures.keys())

    exp_dict = defaultdict(lambda: defaultExposures)
    stage_positions = [(100, 100, 30), (200, 150, 35), (250, 150, 35)]
    FITC_by_pos = [0.1, 5, 10]

    for p in range(len(stage_positions)):
        for c, exps in expByPosition.items():
            exp_dict[p][c] = exps[p]

    mda = MDASequence(
        stage_positions=stage_positions,
        channels=channels,
        time_plan={"interval": 1, "loops": 5},
        axis_order="tpcz",
    )
    events = []
    for e in mda.iter_events():
        # e.exposure = 400
        try:
            exp = expByPosition[e.channel.config][e.index["p"]]
            e.exposure = exp
        except KeyError:
            pass
        events.append(e)
        # exp = exp_dict[e.index["p"]][e.channel.config]
        # # print(e.index)
        # # print(e.channel.config)
        # # print(exp)
        # events.append(e)
    # for e in events:
    #     pass
        # print(e)
    return events, mda


class fakeSequence:
    def __init__(self, events: List[MDAEvent], orig_sequence: str):
        self.orig = orig_sequence
        self.events = events

    def iter_events(self, axis_order=None):

        for e in self.events:
            yield e

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self.orig, name)

    def __iter__(self) -> Iterator[MDAEvent]:  # type: ignore
        yield from self.iter_events()


def genSequence() -> fakeSequence:
    events, mda = gen_events()
    return fakeSequence(events, mda)
