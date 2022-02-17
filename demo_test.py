from pymmcore_plus import CMMCorePlus
from loguru import logger
from useq import MDAEvent
import napari

from pymmcore_mda_writers import zarr_MDA_writer

from generate_events import genSequence

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
seq = genSequence()
v.window._qt_viewer.console.push(locals())


@mmc.events.sequenceStarted.connect
def started(seq):
    v.add_image(writer._z)


napari.run()
