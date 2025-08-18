
import csiread
import matplotlib.pyplot as plt
import numpy as np

# Load CSI data
csifile = "../linux-80211n-csitool-supplementary/netlink/csi.dat"
csidata = csiread.Intel(csifile, nrxnum=3, ntxnum=2, pl_size=10)
csidata.read()
csi = csidata.get_scaled_csi()

# Choose subcarriers to track (e.g., 5, 15, 25)
selected_subcarriers = [5,10, 15,20, 25,29]
num_packets = len(csi)

# Collect magnitude data over time
subcarrier_magnitudes = {sc: [] for sc in selected_subcarriers}
for packet in csi:
    for sc in selected_subcarriers:
        # Average magnitude across RX-TX pairs for each subcarrier
        magnitude = np.mean(np.abs(packet[sc]))
        subcarrier_magnitudes[sc].append(magnitude)

# Plot
plt.figure(figsize=(10, 6))
for sc in selected_subcarriers:
    plt.plot(subcarrier_magnitudes[sc], label=f"Subcarrier {sc}")

plt.title("CSI Magnitude Over Time for Selected Subcarriers")
plt.xlabel("Packet Index")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

