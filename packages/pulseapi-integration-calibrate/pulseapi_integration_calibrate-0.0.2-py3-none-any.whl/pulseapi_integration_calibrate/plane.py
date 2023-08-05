from pulseapi_integration_calibrate.robodk import *
import numpy as np

# Reference frame calibration methods
CALIBRATE_FRAME_3P_P1_ON_X = 0  # Calibrate by 3 points: [X, X+, Y+] (p1 on X axis)
CALIBRATE_FRAME_3P_P1_ORIGIN = 1  # Calibrate by 3 points: [Origin, X+, XY+] (p1 is origin)
CALIBRATE_FRAME_6P = 2  # Calibrate by 6 points


def calibrate_reference_frame(points, method=CALIBRATE_FRAME_3P_P1_ORIGIN):
    if method == CALIBRATE_FRAME_3P_P1_ON_X:
        print('нету алгоритма')
        return []
    elif method == CALIBRATE_FRAME_3P_P1_ORIGIN:
        return __three_point_p1_origin_method(points)
    elif method == CALIBRATE_FRAME_6P:
        print('нету алгоритма')
        return []


def __three_point_p1_origin_method(points):
    """
    Calibrate a reference frame given a number of points and following a specific algorithm/method.
    https: // www.researchgate.net / publication / 221104984_3
    _Points_Calibration_Method_of_Part_Coordinates_for_Arc_Welding_Robot
    :return:
    """
    M1 = points[0]
    M2 = points[1]
    M3 = points[2]
    px = M1[0]
    py = M1[1]
    pz = M1[2]

    if M3[1] < py and M2[0] < px or M2[0] > px and M3[1] > py:
        if M3[1] == py:
            return [points[0], [0, 0, 0]]

        phi = atan2(M2[1] - py, M2[0] - px)
        theta = atan2(pz - M2[2], (M2[1] - py) / sin(phi))

        F1 = cos(theta) * cos(theta) + sin(phi) * sin(theta)
        F2 = cos(phi) / sin(theta)

        S1 = M3[1] - cos(theta) * pz + M3[2] - py
        S2 = M3[0] - cos(phi) * cos(theta) * (pz + M3[2]) / sin(theta) - px

        Mc = (F2 * S1 - F1 * S2) / (F2 * cos(phi) + F1 * sin(phi))
        Ms = (S1 - Mc * cos(phi)) / F1

        psi = atan2(Ms, Mc)
        T = np.array([[cos(phi) * cos(theta), cos(phi) * sin(theta) * sin(psi) - sin(phi) * cos(psi),
                       cos(phi) * sin(theta) * cos(psi) + sin(phi) * sin(psi), points[0][0]],
                      [sin(phi) * cos(theta), sin(phi) * sin(theta) * sin(psi) + cos(phi) * cos(psi),
                       sin(phi) * sin(theta) * cos(psi) - cos(phi) * sin(psi), points[0][1]],
                      [-sin(theta), cos(theta) * sin(psi), cos(theta) * cos(psi), points[0][2]],
                      [0, 0, 0, 1]])

        return [points[0], [psi, theta, phi]]
    else:

        phi = atan2(M2[1] - py, M2[0] - px)
        theta = atan2(pz - M2[2], (M2[1] - py) / sin(phi))

        F1 = cos(theta) * cos(theta) + sin(phi) * sin(theta)
        F2 = cos(phi) / sin(theta)

        S1 = M3[1] - cos(theta) * pz + M3[2] - py
        S2 = M3[0] - cos(phi) * cos(theta) / sin(theta) * (pz + M3[2]) - px

        Mc = (F2 * S1 - F1 * S2) / (F2 * cos(phi) + F1 * sin(phi))
        Ms = (S1 - Mc * cos(phi)) / F1

        psi = atan2(Ms, Mc)

        return [points[0], [-psi + pi, theta, phi]]
