import numpy as np
from config import * 

def rotate(pos, angle):
    pos = np.array(pos)
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s], [s, c]])
    return np.matmul(R, pos)

def rotate_all(positions, theta):
    rotated_positions = []
    for position in positions:
        rotated_position = rotate(position, theta)
        rotated_positions.append(rotated_position)
    return rotated_positions

def _get_marble_positions(n):
    def flower(dist, n, k):
        positions = []
        for i in range(k):
            positions.append(rotate((0, dist), 2*i/n*np.pi))
        return positions

    positions = []
    if n == 1:
        positions.append((0, 0))
    if n == 2:
        dist = 0.375 * MARBLE_SIZE
        positions.extend(flower(dist, n, n))
    if n == 3:
        dist = 0.45 * MARBLE_SIZE
        positions.extend(flower(dist, n, n))
    if n == 4:
        dist = 0.55 * MARBLE_SIZE
        positions.extend(flower(dist, n, n))
    if n == 5:
        dist = 0.65 * MARBLE_SIZE
        positions.extend(flower(dist, n, n))
    if n == 6:
        dist = 0.8 * MARBLE_SIZE
        positions.append((0, 0))
        positions.extend(flower(dist, n, 5))
    if n == 7:
        dist = 0.8 * MARBLE_SIZE
        positions.append((0, 0))
        positions.extend(flower(dist, n, 6))
    if n == 8:
        dist = 0.8 * MARBLE_SIZE
        positions.append((0, 0))
        positions.extend(flower(dist, 7, 7))
    if n > 8:
        for i in range(int(n/8)):
            positions.extend(rotate_all(_get_marble_positions(8), (i+1)*np.pi*1.618))
        positions.extend(_get_marble_positions(n%8))

    return positions

def get_marble_positions(n, idx, directions):
    def transform(positions):
        transformed_position = []
        for position in positions:
            offset = CIRCLE_RADIUS - MARBLE_SIZE / 2
            transformed_position.append(position + np.array([offset, offset]))
        return transformed_position
    positions = _get_marble_positions(n)
    return transform(rotate_all(positions, directions[idx]))

def get_hole_positions(i, j):
    global MID_PADDING, HOLE_PADDING, CIRCLE_RADIUS
    y_padding = (i > 1) * MID_PADDING
    x = j*(CIRCLE_RADIUS + HOLE_PADDING)*2+HOLE_PADDING
    y = i*(CIRCLE_RADIUS + HOLE_PADDING)*2+HOLE_PADDING+y_padding
    return x, y

