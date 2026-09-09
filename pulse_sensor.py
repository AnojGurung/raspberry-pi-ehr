import spidev
import time
import statistics


def read_channel(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

def get_heart_rate():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    
    print("Place your finger on the pulse sensor.")
    print("Keep your finger still.")
    print("Caliberating for 5 seconds.")
    
    caliberation_values = []
    
    start = time.time()
    
    while time.time() - start < 5:
        value = read_channel(spi, 0)
        caliberation_values.append(value)
        time.sleep(0.02)
        
    minimum = min(caliberation_values)
    maximum = max(caliberation_values)
    average = sum(caliberation_values) / len(caliberation_values)
    
    
    threshold_high = average+ ((maximum - average) * 0.55 )
    
    print("\nMinimum: ", minimum)
    print("Maximum: ", maximum)
    print("Average: ", average)
    print("Threshold: ", round(threshold_high, 1))
    
    
    print("\nMeasuring heart rate for 30 seconds...")
    
    samples = []
    beat_times = []
    
    last_beat_time = 0
    
    previous = None
    previous_previous = None
    
    start = time.time()
    
    while time.time() - start < 30:
        raw_value = read_channel(spi, 0)
        samples.append(raw_value)
        
        if len(samples) > 5:
            samples.pop(0)
            
        smooth_value = sum(samples) / len(samples)
        
        current_time = time.time()
        
        if previous_previous is not None:
            if (
                previous > previous_previous
                and previous > smooth_value
                and previous > threshold_high
                ):
                
                if current_time - last_beat_time > 0.55:
                    beat_times.append(current_time)
                    last_beat_time = current_time
                    
                    print("Beat Detected")
                    
                    
        previous_previous = previous
        previous = smooth_value
        
        time.sleep(0.02)
        
    spi.close()

    if len(beat_times) < 2:
        print("Not enough heartbeats detected.")
        return None


    intervals = []
        
    for i in range(1, len(beat_times)):
        interval = beat_times[i] - beat_times[i-1]
        intervals.append(interval)
        
        
    median_interval = statistics.median(intervals)
        
    bpm = 60/median_interval
    bpm = round(bpm)
    
    print("\n---RESULT---")
    print("Beats Detected: ", len(beat_times))
    print("Median time between beats: ", round(median_interval, 2), "seconds")
    print("Estimated heart rate: ", bpm, "BPM")
        
    return bpm
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    