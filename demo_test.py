from pymmcore_plus import CMMCorePlus
from loguru import logger
from useq import MDAEvent
import napari

from pymmcore_mda_writers import zarr_MDA_writer

from generate_events import fakeSequence, update_event_exp

v = napari.Viewer()
dw, main_window = v.window.add_plugin_dock_widget("napari-micromanager")

mmc: CMMCorePlus = main_window._mmc

# load demo config
mmc.loadSystemConfiguration()

print(mmc.getAvailableConfigGroups())
print(mmc.getAvailableConfigs("Channel"))


im = mmc.snap()
writer = zarr_MDA_writer(mmc, "test.zarr", im.shape, im.dtype)


def new_frame(img, event: MDAEvent):
    print(list(event.index.values()))

mmc.events.frameReady.connect(new_frame)
from useq import MDASequence
channels = ["DAPI", "FITC"]
stage_positions = [(1,2,3), (4,5,6), (7, 8, 9)]

mda = MDASequence(
    stage_positions=stage_positions,
    channels=channels,
    time_plan={"interval": 1, "loops": 5},
    axis_order="tpcz",
)
expByPosition = {
    "FITC" : {0: .1, 1: 1, 2:10}
}

events = update_event_exp(mda, expByPosition)
seq = fakeSequence(events, mda)


@mmc.events.sequenceStarted.connect
def started(seq):
    v.add_image(writer._z)


v.window._qt_viewer.console.push(locals())
napari.run()
