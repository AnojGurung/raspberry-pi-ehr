import spidev
import time


def read_channel(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value


spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


print("KEEP FINGER OFF SENSOR")
print("Reading for 10 seconds...\n")

start = time.time()

while time.time() - start < 10:
    value = read_channel(spi, 0)
    print(value)
    time.sleep(0.1)


input("\nNow place finger on sensor and press Enter...")


print("\nReading WITH finger for 10 seconds...\n")

start = time.time()

while time.time() - start < 10:
    value = read_channel(spi, 0)
    print(value)
    time.sleep(0.1)


spi.close()