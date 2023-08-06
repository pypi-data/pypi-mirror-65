import numpy as np
from numpy.linalg import norm
import pyquaternion
from math import sin,cos

"""
Random useful utilities that don't belong to any 
particular Python module 
"""

import time

class IntervalTimer(object):
    """
    A surprisingly useful class to schedule something at even intervals
    """

    def __init__(self, interval, skip_lags = True, force_skip = 10, rostime=False, fake_time=False):
        """
        :param interval: Interval to delay for
        :param skip_lags: Don't catch up to missed intervals. If this is false and you fail to check in
                        on the ready() function for a while, ready() will repeatedly return true
                        to make up for the missed intervals.
        :param force_skip: If not using skip lags and we get behind more than this many seconds, skip everything
        :param rostime: Use ROS time. You'll need this if running in tandem with a Gazebo simulation that slows
        :param fake_time: Manually input your own time
        down time.
        """
        if rostime:
            import rospy
            self._time_fn = rospy.get_time
        elif fake_time:
            self._time_fn = lambda: self.get_time()
        else:
            self._time_fn = time.time

        self._interval = interval
        self._skip_lags = skip_lags
        self._force_skip = force_skip
        self._fake_time = 0
        self._use_fake_time = fake_time
        self._next = self._time_fn() + interval

    def ready(self, fake_time=None):
        """
        Non-blocking check of whether the timer has tripped or not.
        This will return true exactly once when the timer has tripped, and then
        false until the next interval comes.

        :param fake_time: Custom time, if using param fake_time
        :return: Bool, whether the timer has tripped or not
        """
        if self._use_fake_time:
            assert self._fake_time is not None, "You need to manually input the time when using fake_time"
            assert self._fake_time >= self._fake_time
            self._fake_time = fake_time

        if self._time_fn() >= self._next:
            if self._skip_lags:
                self._next = self._time_fn() + self._interval
            else:
                self._next += self._interval
                if self._time_fn() - self._next > self._force_skip:
                    self._next = self._time_fn()
            return True
        return False

    def get_time(self):
        return self._fake_time

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, i):
        self._interval = i



def normalize(vec):
    """
    Make the magnitude of a vector or list of vectors 1

    :param vec:
    :return:
    """
    if vec.ndim==1:
        n = norm(vec)
        if n==0:
            n=1
        return vec / n
    n = norm(vec,axis=1)
    n[n==0] = 1
    n = np.expand_dims(n, axis=1)
    return vec / n

def cosdist(A,B):
    """
    Cosine of angle between A and B
    :param A:
    :param B:
    :return:
    """
    return np.dot(normalize(A), normalize(B))



def vec_reject(V, F):
    """
    (This operates rowwise on V and F)
    Get the normal component of the vector F along V
    All rows in the result should be orthogonal to V

    :param V:
    :param F:
    :return: Component of F not on V
    """
    vh = normalize(V)
    dots = np.expand_dims(np.sum(F*vh,axis=1),axis=1)
    return F - dots*vh


def clip_norm(vec, nmax):
    """
    For an (N x M) array, clip the 2-norm
    of each row

    :param vec:
    :param nmax:
    :return:
    """
    if vec.ndim==1:
        n = norm(vec)
        if n==0:
            n=1
        nvec = vec / n
        n = np.clip(n, 0, nmax)
        return nvec * n
    n = np.expand_dims(norm(vec,axis=1), axis=1)
    n[n==0]=1
    nvec = vec / n
    n = np.clip(n, 0, nmax)
    return nvec * n


def az_el_vec(azimuth, elevation):
    """
    Return a vector that points in the given azimuth and elevation

    :param azimuth:
    :param elevation:
    :return:
    """

    q1 = pyquaternion.Quaternion(axis=[0, 1, 0], angle=-elevation)
    q2 = pyquaternion.Quaternion(axis=[0, 0, 1], angle=azimuth)
    v = np.array([1.0, 0, 0])
    q = q2 * q1
    vrot = q.rotate(v)
    return vrot

def vecs2rot(v1,v2):
    """
    Get the rotation that would have to be applied to
    vector v1 to result in v2

    :param v1:
    :param v2:
    :return: pyquaternion
    """
    denom = norm(v1) * norm(v2)
    c = np.dot(v1, v2) / denom
    if abs(c-1) < 1e-8:
        # No rotation present, return null quaternion
        return pyquaternion.Quaternion()
    s = norm(np.cross(v1, v2)) / denom
    angle = np.arctan2(s,c)
    axis = normalize(np.cross(v1,v2))
    return pyquaternion.Quaternion(axis=axis, radians=angle)


def cart2sph(xyz):
    """
    Convert rectangular to spherical coordinates
    The

    :param xyz: An N x 3 array of rectangular coordinates
    :return: azimuth, elevation, radius

    """
    x=xyz[:,0]
    y=xyz[:,1]
    z=xyz[:,2]
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(hxy, z)
    az = np.arctan2(y, x)
    return az, el, r

def cart2pol(x, y):
    """
    Cartesian to polar coordinates

    :param x:
    :param y:
    :return:
    """
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho

def pol2cart(theta, rho, units="radians"):
    """
    Polar to cartesian

    :param theta:
    :param rho:
    :param radians:
    :return:
    """
    if units=="degrees":
        theta = np.radians(theta)
    else:
        assert units=="radians","Unknown angle units"

    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return np.array([x, y], dtype=float)


def rotation_matrix(angle):
    """
    Make a 2x2 2d rotation matrix from an angle

    :param angle:
    :return:
    """
    c = cos(angle)
    s = sin(angle)

    tf = np.array([
        [c,-s],
        [s,c]
    ], dtype=np.float64)
    return tf

def make_lattice(*iterables):
    grids = np.meshgrid(*iterables)
    flat = [g.flatten() for g in grids]
    return np.array(flat).T

def wraptopi(angles):
    """
    Put all angles (in radians) in the range -2 pi..2 pi

    :param angles: numpy vector or array
    :return:
    """
    return (angles + np.pi) % (2 * np.pi ) - np.pi
