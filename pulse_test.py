import spidev
import time
import statistics

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value


print("Place your finger on the pulse sensor.")
print("Keep your finger still.")
print("Calibrating for 5 seconds...")


# -------------------------
# CALIBRATION
# -------------------------

calibration_values = []

start = time.time()

while time.time() - start < 5:
    value = read_channel(0)
    calibration_values.append(value)
    time.sleep(0.02)


minimum = min(calibration_values)
maximum = max(calibration_values)
average = sum(calibration_values) / len(calibration_values)

threshold_high = average + ((maximum - average) * 0.55)


print("\n--- CALIBRATION ---")
print("Minimum:", minimum)
print("Maximum:", maximum)
print("Average:", round(average, 1))
print("Threshold:", round(threshold_high, 1))


# -------------------------
# HEARTBEAT DETECTION
# -------------------------

print("\nMeasuring heart rate for 30 seconds...")

samples = []

beat_times = []

last_beat_time = 0

previous = None
previous_previous = None

start = time.time()


while time.time() - start < 30:

    raw_value = read_channel(0)

    # Store recent readings
    samples.append(raw_value)

    # Keep only last 5 readings
    if len(samples) > 5:
        samples.pop(0)

    # Moving average
    smooth_value = sum(samples) / len(samples)

    current_time = time.time()


    # We need at least 3 points to detect a peak
    if previous_previous is not None:

        # Detect local peak
        if (
            previous > previous_previous
            and previous > smooth_value
            and previous > threshold_high
        ):

            # Reject peaks that are too close together
            if current_time - last_beat_time > 0.55:

                beat_times.append(current_time)

                last_beat_time = current_time

                print("Beat detected ❤️")


    previous_previous = previous
    previous = smooth_value

    time.sleep(0.02)


spi.close()


# -------------------------
# BPM CALCULATION
# -------------------------

print("\n--- RESULT ---")

print("Beats detected:", len(beat_times))


if len(beat_times) >= 2:

    intervals = []

    for i in range(1, len(beat_times)):

        interval = beat_times[i] - beat_times[i - 1]

        intervals.append(interval)


    median_interval = statistics.median(intervals)

    bpm = 60 / median_interval


    print(
        "Median time between beats:",
        round(median_interval, 2),
        "seconds"
    )

    print(
        "Estimated heart rate:",
        round(bpm),
        "BPM"
    )


else:

    print("Not enough valid heartbeats detected.")
