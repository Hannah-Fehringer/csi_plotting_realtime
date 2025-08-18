import csiread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os

# Path to CSI data file
csifile = "../linux-80211n-csitool-supplementary/netlink/csi.dat"

# Selected subcarriers
selected_subcarriers = [5, 10, 15, 20, 25, 29]
history_length = 100

# Initialize history
subcarrier_history = {sc: [] for sc in selected_subcarriers}

# Set up plot
fig, ax = plt.subplots(figsize=(10, 6))
lines = {sc: ax.plot([], [], label=f"Subcarrier {sc}")[0] for sc in selected_subcarriers}
ax.set_xlim(0, history_length)
ax.set_ylim(0, 1)
ax.set_title("Real-Time CSI Magnitude Over Time")
ax.set_xlabel("Packet Index")
ax.set_ylabel("Magnitude")
ax.legend()
ax.grid(True)
plt.tight_layout()

# Track last file size to detect changes
last_filesize = 0

def update(frame):
    global last_filesize

    try:
        current_filesize = os.path.getsize(csifile)
        if current_filesize != last_filesize:
            last_filesize = current_filesize

            csidata = csiread.Intel(csifile, nrxnum=3, ntxnum=2, pl_size=10)
            csidata.read()
            csi = csidata.get_scaled_csi()

            if len(csi) == 0:
                return list(lines.values())

            latest_packet = csi[-1]
            for sc in selected_subcarriers:
                magnitude = np.mean(np.abs(latest_packet[sc]))
                subcarrier_history[sc].append(magnitude)
                if len(subcarrier_history[sc]) > history_length:
                    subcarrier_history[sc].pop(0)

            for sc in selected_subcarriers:
                lines[sc].set_data(range(len(subcarrier_history[sc])), subcarrier_history[sc])

            ax.set_xlim(0, max(len(subcarrier_history[sc]) for sc in selected_subcarriers))
            max_mag = max(max(subcarrier_history[sc]) for sc in selected_subcarriers)
            ax.set_ylim(0, max_mag * 1.2 if max_mag > 0 else 1)

    except Exception as e:
        print(f"Error reading CSI data: {e}")

    return list(lines.values())

# Match ping interval: 200ms
ani = FuncAnimation(fig, update, interval=200, blit=False)
plt.show()

