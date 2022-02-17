from typing import Dict, List, Iterator
from useq import MDAEvent, MDASequence, Channel
from collections import defaultdict


def update_event_exp(
    mda: MDASequence,
    expByPosition: Dict[str, List[float]],
):
    n_pos = mda.shape[mda.axis_order.index('p')]
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
    return events


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
