import numpy as np

def generate_ar(order, variance, length):
    length = 4*length
    coeffs = np.random.random(order) - 0.5
    coeffs = np.append(1, -coeffs)

    while np.max(np.abs(np.roots(coeffs))) > 1:
        coeffs = np.random.random(order) - 0.5
        coeffs = np.append(1, -coeffs)

    coeffs = coeffs[1:]
        
    ts = np.zeros((length))

    ts[:order] = np.random.randn(order)

    for i in range(order,length):
        for j in range(order):
            ts[i] += ts[i-(j+1)]*coeffs[j]

        ts[i] += np.random.randn(1)*variance

    length = length / 4
    return coeffs, ts[3*length:]

def generate_ma(order, variance, length):
    length = 4*length
    coeffs = np.random.random(order) - 0.5

    inputs = np.random.randn(length)
    
    ts = np.zeros((length))

    ts[:order] = inputs[:order]

    for i in range(order,length):
        for j in range(order):
            ts[i] += inputs[i-(j+1)]*coeffs[j]

        ts[i] += inputs[i]*variance

    length = length / 4
    return coeffs, ts[3*length:]

def generate_arma(ar_order, ma_order, variance, length):
    length = 4*length
    ma_coeffs = np.random.random(ma_order) - 0.5

    coeffs = np.random.random(order) - 0.5
    coeffs = np.append(1, -coeffs)

    while np.max(np.abs(np.roots(coeffs))) > 1:
        coeffs = np.random.random(order) - 0.5
        coeffs = np.append(1, -coeffs)

    inputs = np.random.randn(length)
        
    ts = np.zeros((length))

    ts[:order] = inputs[:order]
        
    for i in range(order,length):
        for j in range(order):
            ts[i] += ts[i-(j+1)]*ar_coeffs[j]
            ts[i] += inputs[i-(j+1)]*ma_coeffs[j]

        ts[i] += inputs[i]*variance
