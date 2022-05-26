from typing import Dict, List, Iterator
from useq import MDAEvent, MDASequence, Channel
from collections import defaultdict


def update_event_exp(
    mda: MDASequence,
    expByPosition: Dict[str, List[float]],
):
    n_pos = mda.shape[mda.axis_order.index("p")]
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

    def iter_chunked(self, over: str) -> Iterator[List[MDAEvent]]:
        """
        Generate events in chunks where only the given *over* index changes

        Parameters
        ----------
        seq : MDASequence
        over : str
            The index keys over which to allow grouping. E.g. 'z' to return
            all events in the z stack for a given time point, position and channel.

        yields
        ------
        chunk : list of events
        """

        over = over.lower()

        def extract_index(event):
            return tuple(
                event.index.get(key) for key in event.index.keys() if key not in over
            )

        events = self.iter_events()
        e = next(events)
        cur_chunk = extract_index(e)

        chunk = [e]
        for e in events:
            if extract_index(e) == cur_chunk:
                chunk.append(e)
            else:
                yield chunk
                chunk = [e]
                cur_chunk = extract_index(e)
        if len(chunk) > 0:
            # ensure we always return all events
            yield chunk


def genSequence() -> fakeSequence:
    events, mda = gen_events()
    return fakeSequence(events, mda)
