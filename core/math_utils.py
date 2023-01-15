from math import sqrt, degrees, atan2


def distance(x1, y1, x2, y2) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calc_heading(org, food) -> float:
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.rotation
    if abs(theta_d) > 180:
        theta_d += 360
    return theta_d / 180
