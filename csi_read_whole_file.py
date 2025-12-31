import csiread
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Load your CSI data file
csifile = "output.dat"
csidata = csiread.Intel(csifile, nrxnum=3, ntxnum=3, pl_size=10)
csidata.read()
csi = csidata.get_scaled_csi()

# Get timestamps and convert to actual datetime
timestamps = csidata.timestamp_low

# Get system boot time
with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])

boot_time = datetime.now() - timedelta(seconds=uptime_seconds)

# Convert timestamps to datetime objects
time_points = [boot_time + timedelta(microseconds=int(ts)) for ts in timestamps]

num_subcarriers = csi.shape[1]
print(f"Total packets: {len(csi)}")
print(f"Number of subcarriers: {num_subcarriers}")
print(f"Collection started: {time_points[0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
print(f"Collection ended:   {time_points[-1].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

# Loop through each subcarrier
for sc in range(num_subcarriers):
    # Create figure for this subcarrier
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Collect data for all 3 antennas for this subcarrier
    antenna_0 = []
    antenna_1 = []
    antenna_2 = []
    
    for packet in csi:
        antenna_0.append(np.abs(packet[sc, 0, 0]))
        antenna_1.append(np.abs(packet[sc, 1, 0]))
        antenna_2.append(np.abs(packet[sc, 2, 0]))
    
    # Plot all 3 antenna streams with time on x-axis
    ax.plot(time_points, antenna_0, linewidth=0.8, label='Antenna 0', alpha=0.8)
    ax.plot(time_points, antenna_1, linewidth=0.8, label='Antenna 1', alpha=0.8)
    ax.plot(time_points, antenna_2, linewidth=0.8, label='Antenna 2', alpha=0.8)
    
    ax.set_title(f'Subcarrier {sc} - 3 Antenna Streams')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_ylim(0, 60)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis to show time nicely
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()  # Rotate date labels
    
    plt.tight_layout()
    filename = f'csi_subcarrier_{sc:02d}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {filename}")
    plt.close()

print(f"Created {num_subcarriers} images (one per subcarrier), each showing 3 antenna streams")

# Create heatmaps for each antenna
print("\nGenerating heatmaps...")

for antenna in range(3):
    # Prepare amplitude matrix for this antenna
    amplitude_matrix = np.zeros((len(csi), num_subcarriers))
    
    for i, packet in enumerate(csi):
        for sc in range(num_subcarriers):
            amplitude_matrix[i, sc] = np.abs(packet[sc, antenna, 0])
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(amplitude_matrix.T, aspect='auto', cmap='viridis',
                   origin='lower', interpolation='nearest', vmin=0, vmax=60,
                   extent=[mdates.date2num(time_points[0]), mdates.date2num(time_points[-1]),
                          0, num_subcarriers])
    
    ax.set_title(f'Antenna {antenna}: CSI Amplitude Heatmap (All Subcarriers)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Subcarrier Index')
    
    # Format x-axis to show time
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    
    cbar = plt.colorbar(im, ax=ax, label='Amplitude')
    
    plt.tight_layout()
    filename = f'csi_heatmap_antenna_{antenna}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Heatmap saved as {filename}")
    plt.close()

print(f"\nTotal files created: {num_subcarriers} line plots + 3 heatmaps")
