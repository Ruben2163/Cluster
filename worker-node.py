# Compute moving average for a data chunk
def compute_moving_average(data, window):
    result = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        avg = sum(window_data) / window
        result.append(avg)
    return result