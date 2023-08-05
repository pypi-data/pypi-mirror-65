"""
Functions to create and process rotation and transformation matrices.
Some conversions to and from Euler angles.
"""
import numpy as np
from .quaternion import Quaternion


def rot_x(alfa):
    return np.array(
        [[1, 0, 0], [0, np.cos(alfa), -np.sin(alfa)], [0, np.sin(alfa), np.cos(alfa)]]
    )


def rot_y(alfa):
    return np.array(
        [[np.cos(alfa), 0, np.sin(alfa)], [0, 1, 0], [-np.sin(alfa), 0, np.cos(alfa)]]
    )


def rot_z(alfa):
    return np.array(
        [[np.cos(alfa), -np.sin(alfa), 0], [np.sin(alfa), np.cos(alfa), 0], [0, 0, 1]]
    )


def translation(x, y, z):
    return np.array(
        [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]], dtype="float64"
    )


def pose_x(alfa, x, y, z):
    """ Homogenous transform with rotation around x-axis and translation. """
    return np.array(
        [
            [1, 0, 0, x],
            [0, np.cos(alfa), -np.sin(alfa), y],
            [0, np.sin(alfa), np.cos(alfa), z],
            [0, 0, 0, 1],
        ]
    )


def pose_y(alfa, x, y, z):
    """ Homogenous transform with rotation around y-axis and translation. """
    return np.array(
        [
            [np.cos(alfa), 0, np.sin(alfa), x],
            [0, 1, 0, y],
            [-np.sin(alfa), 0, np.cos(alfa), z],
            [0, 0, 0, 1],
        ]
    )


def pose_z(alfa, x, y, z):
    """ Homogenous transform with rotation around z-axis and translation. """
    return np.array(
        [
            [np.cos(alfa), -np.sin(alfa), 0, x],
            [np.sin(alfa), np.cos(alfa), 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ]
    )


def quat_distance(qa: Quaternion, qb: Quaternion):
    """ Half of the rotation angle to bring qa to qb."""
    return np.arccos(np.abs(qa.elements @ qb.elements))


def tf_inverse(T):
    """ Efficient inverse of a homogenous transform.
    (Normal matrix inversion would be a bad idea.)
    Returns a copy, not inplace!
    """
    Ti = np.eye(4)
    Ti[:3, :3] = T[:3, :3].transpose()
    Ti[:3, 3] = np.dot(-Ti[:3, :3], T[:3, 3])
    return Ti


def rpy_to_rot_mat(rxyz):
    """ Convert roll, pitch and yaw angles to a rotation matrix."""
    r_x, r_y, r_z = rxyz[0], rxyz[1], rxyz[2]
    return rot_x(r_x) @ rot_y(r_y) @ rot_z(r_z)


def rotation_matrix_to_rpy(R):
    """
    Convert Roll, pitch and yaw angles to a rotation matrix
    (intrinsic XYZ Euler angles).

    I'm not sure if this is the best implementation.
    Look into the one scipy provides.
    """
    r11, r12, r13 = R[0]
    _, _, r23 = R[1]
    _, _, r33 = R[2]

    r_x = np.arctan2(-r23, r33)
    r_y = np.arctan2(r13, np.sqrt(r11 ** 2 + r12 ** 2))
    r_z = np.arctan2(-r12, r11)

    return [r_x, r_y, r_z]
