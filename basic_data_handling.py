from jddb.file_repo import FileRepo
from jddb.processor import Shot
import numpy as np
import matplotlib.pyplot as plt

file_repo = FileRepo("../tod/HL-2A data/JDDB_repo_2A_5k//")
shot_list = file_repo.get_all_shots()
shot = shot_list[20]
print(file_repo.read_labels(shot))

# plot ip and some diagnostics.
# read one signal with tag
channel_name = "DS-EMD-MP:MPOL-01"
signals = file_repo.read_data(shot, [channel_name])
data = signals[channel_name]

# read start time and sampling rate to generate x-axis
attribute_list = ["StartTime", "SampleRate"]
attributes = file_repo.read_attributes(shot, channel_name, attribute_list)
start = attributes["StartTime"]
sr = attributes["SampleRate"]
stop = start + len(data) / sr
time_axis = np.linspace(start, stop, num=len(data), endpoint=True)
#
# plt.figure()
# plt.plot(time_axis, data)
# plt.show()

# %%
# an alternative way to read a shot using processing package
# create a shot object
example_shot = Shot(shot, file_repo)
# plot some plasma parameters in one figure
plot_tags = ["CCO-LFB:LFEX-IP", "CCO-LFB:LFBBT", "CCO-LFB:LFDH", "CCO-LFB:LFDV", "CCO-DF:DENSITY1", "CCO-LFB:LFBIRF",
             "CCO-LFB:LFBBOH", "CCO-LFB:LFBBV", "CCO-LFB:LFBMP1", "CCO-LFB:LFBMP2", "CCO-DF:GASFBOUT", "DS-TMP:PUFFCTRL",
             "DS-EMD-ROG:VL-FILTER", "DS-BM-AB:BOLD03", "DS-BM-AB:BOLD09", "DS-SXR-SXA:SX03", "DS-SXR-SXA:SX09",
             "DS-EMD-MP:MPOL-04", "DS-EMD-MP:MPOL-13", "DS-EMD-MP:NPOL-04", "DS-EMD-MP:NPOL-09"]
plot_tags = ["DS-EMD-MP:MPOL-04", "DS-EMD-MP:MPOL-13", "DS-EMD-MP:NPOL-04", "DS-EMD-MP:NPOL-09", "RotatingModeProxy"]
f, axs = plt.subplots(nrows=5, ncols=5, sharex=True)
axs = np.reshape(axs, -1)
for i, tag in enumerate(plot_tags):
    if example_shot.labels[tag] == 1:
        data = example_shot.get_signal(tag)
        axs[i].plot(data.time, data.data)
