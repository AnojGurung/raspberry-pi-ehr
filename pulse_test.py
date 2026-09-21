from pulse_sensor import get_heart_rate

result = get_heart_rate()

if result is not None:
    print("\nReturned data:")
    print(result)