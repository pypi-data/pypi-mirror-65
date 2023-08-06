from pulseapi import *
from math import sqrt, atan2, cos, sin, fabs, tan
from math import pi
import numpy as np

def getproportionpoint(point, segment, length, dx, dy):
    factor = segment / length
    return [point[0] - dx * factor,
            point[1] - dy * factor]


def get_length(dx, dy):
    return sqrt(dx * dx + dy * dy)


def calculate_start_and_end_angle(p1, p, p2, radius):
    dx1 = p[0] - p1[0]
    dy1 = p[1] - p1[1]

    dx2 = p[0] - p2[0]
    dy2 = p[1] - p2[1]

    angle = atan2(dy1, dx1) - atan2(dy2, dx2)
    segment = radius / fabs(tan(angle / 2))
    length1 = get_length(dx1, dy1)
    length2 = get_length(dx2, dy2)

    length = min(length1, length2)

    if segment > length:
        segment = length
        radius = length * fabs(tan(angle))

    c1 = getproportionpoint(p, segment, length1, dx1, dy1)
    c2 = getproportionpoint(p, segment, length2, dx2, dy2)

    dx = p[0] * 2 - c1[0] - c2[0]
    dy = p[1] * 2 - c1[1] - c2[1]

    L = get_length(dx, dy)
    d = get_length(segment, radius)

    circlePoint = getproportionpoint(p, d, L, dx, dy)

    startAngle = atan2((c1[1] - circlePoint[1]), (c1[0] - circlePoint[0]))
    endAngle = atan2((c2[1] - circlePoint[1]), (c2[0] - circlePoint[0]))

    sweepAngle = endAngle - startAngle

    if sweepAngle <= -pi:
        sweepAngle = -(sweepAngle + pi)
    if sweepAngle >= pi:
        sweepAngle = pi - sweepAngle

    return startAngle, sweepAngle, circlePoint, radius


def convert_position2list(position):
    return [list(position.to_dict()['point'].values()),
            list(position.to_dict()['rotation'].values())]


def points_of_rounding(startAngle, sweepAngle, radius, circlePoint, target):
    sign = np.sign(sweepAngle)
    points = []
    degreeFactor = 180 / pi
    r = int(fabs(sweepAngle * degreeFactor))

    for i in range(0, r, 2):
        pointx = circlePoint[0] + cos(startAngle + sign * i / degreeFactor) * radius
        pointy = circlePoint[1] + sin(startAngle + sign * i / degreeFactor) * radius
        points.append(position([pointx, pointy, convert_position2list(target)[0][2]], convert_position2list(target)[1],
                               target.to_dict()['actions']))

    return points


def rounding_motion(target_list):
    new_target_list = []

    for i in range(len(target_list)):
        if len(target_list[i]) == 2 and target_list[i][1][0] != 0:
            startAngle, sweepAngle, circlePoint, radius = calculate_start_and_end_angle(convert_position2list(target_list[i - 1][0])[0],
                                                                convert_position2list(target_list[i][0])[0],
                                                                convert_position2list(target_list[i + 1][0])[0],
                                                                target_list[i][1][0])
            new_target_list.extend(
                points_of_rounding(startAngle, sweepAngle, radius, circlePoint, target_list[i][0]))
        else:
            new_target_list.append(target_list[i][0])
    return new_target_list
