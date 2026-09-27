import spidev
import time
import statistics


SAMPLE_DELAY = 0.02       # About 50 samples/second
CHANNEL = 0


def read_channel(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value


def collect_values(spi, seconds):
    values = []

    start = time.time()

    while time.time() - start < seconds:
        value = read_channel(spi, CHANNEL)
        values.append(value)
        time.sleep(SAMPLE_DELAY)

    return values


def detect_finger(spi):

    print("\nChecking no-finger baseline...")
    print("Keep your finger OFF the sensor for 2 seconds.")

    baseline_values = collect_values(spi, 2)

    baseline_average = statistics.mean(
        baseline_values
    )

    baseline_std = statistics.pstdev(
        baseline_values
    )

    print(
        "Baseline average:",
        round(baseline_average, 1)
    )

    print(
        "Baseline variation:",
        round(baseline_std, 1)
    )

    # Finger signal should normally vary
    # considerably more than no-finger noise.
    finger_variation_threshold = max(
        30,
        baseline_std * 2
    )

    print("\nPlace your finger on the sensor.")
    print("Waiting for finger...")

    recent_values = []

    stable_detection_count = 0

    while True:

        value = read_channel(spi, CHANNEL)

        recent_values.append(value)

        # Keep approximately 2 seconds
        # of recent readings.
        if len(recent_values) > 100:
            recent_values.pop(0)

        if len(recent_values) == 100:

            current_std = statistics.pstdev(
                recent_values
            )

            current_range = (
                max(recent_values)
                - min(recent_values)
            )

            # We use variability rather than
            # average signal change.
            if (
                current_std
                > finger_variation_threshold
                and current_range > 120
            ):
                stable_detection_count += 1

            else:
                stable_detection_count = 0

            # Require the condition to remain true
            # for multiple consecutive readings.
            if stable_detection_count >= 20:

                print("Finger detected.")
                print(
                    "Finger signal variation:",
                    round(current_std, 1)
                )

                print("Stabilizing signal...")

                time.sleep(1)

                return {
                    "baseline_average":
                        baseline_average,

                    "baseline_std":
                        baseline_std
                }

        time.sleep(SAMPLE_DELAY)


def get_heart_rate():

    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    # --------------------------------
    # AUTOMATIC FINGER DETECTION
    # --------------------------------

    finger_info = detect_finger(spi)

    # --------------------------------
    # INITIAL FINGER CALIBRATION
    # --------------------------------

    print("\nCalibrating finger signal for 5 seconds.")
    print("Keep your finger still.")

    calibration_values = collect_values(
        spi,
        5
    )

    minimum = min(calibration_values)
    maximum = max(calibration_values)

    average = statistics.mean(
        calibration_values
    )

    signal_std = statistics.pstdev(
        calibration_values
    )

    signal_range = maximum - minimum

    print("\n--- CALIBRATION ---")

    print(
        "Minimum:",
        minimum
    )

    print(
        "Maximum:",
        maximum
    )

    print(
        "Average:",
        round(average, 1)
    )

    print(
        "Signal range:",
        signal_range
    )

    print(
        "Signal variation:",
        round(signal_std, 1)
    )

    # Reject extremely weak signals.
    if (
        signal_std < 20
        or signal_range < 80
    ):

        print(
            "\nPulse signal is too weak."
        )

        print(
            "Adjust your finger and try again."
        )

        spi.close()

        return None

    # --------------------------------
    # HEARTBEAT MEASUREMENT
    # --------------------------------

    print(
        "\nMeasuring heart rate for 30 seconds..."
    )

    fast_window = []
    slow_window = []

    adaptive_window = []

    beat_times = []

    last_beat_time = 0

    previous = None
    previous_previous = None

    beat_armed = True

    start = time.time()

    while time.time() - start < 30:

        raw_value = read_channel(
            spi,
            CHANNEL
        )

        # -----------------------------
        # FAST MOVING AVERAGE
        # -----------------------------

        fast_window.append(raw_value)

        if len(fast_window) > 5:
            fast_window.pop(0)

        fast_average = statistics.mean(
            fast_window
        )

        # -----------------------------
        # SLOW MOVING AVERAGE
        # -----------------------------

        slow_window.append(raw_value)

        if len(slow_window) > 50:
            slow_window.pop(0)

        slow_average = statistics.mean(
            slow_window
        )

        # Difference between fast and slow
        # signals removes much of the changing
        # baseline.
        pulse_signal = (
            fast_average
            - slow_average
        )

        # -----------------------------
        # ADAPTIVE THRESHOLD
        # -----------------------------

        adaptive_window.append(
            pulse_signal
        )

        # Approximately 2 seconds
        if len(adaptive_window) > 100:
            adaptive_window.pop(0)

        # Don't attempt beat detection until
        # enough recent signal exists.
        if len(adaptive_window) >= 50:

            signal_center = statistics.median(
                adaptive_window
            )

            signal_variation = (
                statistics.pstdev(
                    adaptive_window
                )
            )

            # Threshold automatically changes
            # with current pulse amplitude.
            adaptive_threshold = (
                signal_center
                + max(
                    8,
                    signal_variation * 0.8
                )
            )

            current_time = time.time()

            # -------------------------
            # PEAK DETECTION
            # -------------------------

            if (
                previous_previous
                is not None
            ):

                if beat_armed:

                    if (
                        previous
                        > previous_previous

                        and previous
                        > pulse_signal

                        and previous
                        > adaptive_threshold
                    ):

                        # Prevent duplicate detection
                        # of the same pulse.
                        if (
                            current_time
                            - last_beat_time
                            > 0.40
                        ):

                            beat_times.append(
                                current_time
                            )

                            last_beat_time = (
                                current_time
                            )

                            print(
                                "Beat Detected"
                            )

                            beat_armed = False

                else:

                    # Re-arm only after the pulse
                    # waveform falls back below
                    # its recent center.
                    if (
                        pulse_signal
                        < signal_center
                    ):

                        beat_armed = True

            previous_previous = previous
            previous = pulse_signal

        else:

            previous_previous = previous
            previous = pulse_signal

        time.sleep(SAMPLE_DELAY)

    spi.close()

    # --------------------------------
    # CHECK NUMBER OF BEATS
    # --------------------------------

    print(
        "\nBeats detected:",
        len(beat_times)
    )

    if len(beat_times) < 10:

        print(
            "Too few beats were detected."
        )

        print(
            "Measurement is unreliable."
        )

        return None

    # --------------------------------
    # BEAT-TO-BEAT INTERVALS
    # --------------------------------

    intervals = []

    for i in range(
        1,
        len(beat_times)
    ):

        interval = (
            beat_times[i]
            - beat_times[i - 1]
        )

        intervals.append(interval)

    # Use only intervals corresponding
    # roughly to 40–180 BPM.
    valid_intervals = [
        interval
        for interval in intervals
        if 0.33 <= interval <= 1.50
    ]

    print(
        "Total intervals:",
        len(intervals)
    )

    print(
        "Valid intervals:",
        len(valid_intervals)
    )

    # We need enough good intervals
    # to trust the result.
    if len(valid_intervals) < 8:

        print(
            "Too few valid heartbeat intervals."
        )

        print(
            "Measurement is unreliable."
        )

        return None

    # --------------------------------
    # ROBUST BPM CALCULATION
    # --------------------------------

    median_interval = statistics.median(
        valid_intervals
    )

    bpm = round(
        60 / median_interval
    )

    # --------------------------------
    # INTERVAL CONSISTENCY
    # --------------------------------

    deviations = [
        abs(
            interval
            - median_interval
        )
        for interval
        in valid_intervals
    ]

    median_deviation = (
        statistics.median(
            deviations
        )
    )

    relative_variation = (
        median_deviation
        / median_interval
    )

    print(
        "Interval variation:",
        round(
            relative_variation,
            3
        )
    )

    # Very inconsistent detection usually
    # means movement/noise or missed peaks.
    if relative_variation > 0.30:

        print(
            "\nHeartbeat intervals are "
            "too inconsistent."
        )

        print(
            "Measurement is unreliable."
        )

        return None

    # --------------------------------
    # FINAL RESULT
    # --------------------------------

    print("\n--- RESULT ---")

    print(
        "Median time between beats:",
        round(
            median_interval,
            3
        ),
        "seconds"
    )

    print(
        "Estimated heart rate:",
        bpm,
        "BPM"
    )

    print(
        "Signal quality: acceptable"
    )

    return {
        "bpm": bpm,
        "beat_times": beat_times,
        "intervals": intervals,
        "median_interval":
            median_interval
    }