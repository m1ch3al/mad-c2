import math


def calculate_pitch_roll(accel_x, accel_y, accel_z):
    pitch_rad = math.atan2(accel_x, math.sqrt(math.pow(accel_y, 2) + math.pow(accel_z, 2)))
    pitch_deg = pitch_rad * 180 / math.pi

    roll_rad = math.atan2(accel_y, math.sqrt(math.pow(accel_x, 2) + math.pow(accel_z, 2)))
    roll_deg = roll_rad * 180 / math.pi

    return pitch_deg, roll_deg
