import numpy as np
from numpy import testing as npt
from numpy.linalg import norm
from nose.tools import assert_less_equal, assert_almost_equal
from simtools import utils

np.set_printoptions(precision=4, suppress=True)

def test_azimuth_elevation():
    """
    Getting a vector from its azimuth and elevation
    :return:
    """
    v = utils.az_el_vec(0, 0)
    npt.assert_almost_equal(v,(1,0,0))

    v = utils.az_el_vec(np.pi / 2.0, 0)
    npt.assert_almost_equal(v,(0,1,0))

    v = utils.az_el_vec(np.pi / 2, np.pi / 4)
    npt.assert_almost_equal(v,(0,0.5*np.sqrt(2),0.5*np.sqrt(2)))


def test_clip_norm():
    """
    Ensure that we can clip the magnitude of a vector
    or list of vectors
    :return:
    """
    vecs = np.random.randn(5,3)
    clip = 0.4
    vecs_clip = utils.clip_norm(vecs, clip)
    for i,vclip in enumerate(vecs_clip):
        # Norm is less than our clip within machine epsilon
        vclip_norm = norm(vclip)
        assert_less_equal(vclip_norm - 2*np.spacing(vclip_norm), clip)

        # Vectors point in the same direction
        vfull = vecs[i]
        cos = vclip.dot(vfull) / (norm(vclip) * norm(vfull))
        assert_almost_equal(cos, 1.0)

        # Try the 1D version
        vclip1d = utils.clip_norm(vfull, clip)
        vclip1d_norm = norm(vclip1d)
        assert_less_equal(vclip1d_norm - 2*np.spacing(vclip1d_norm), clip)
        cos = vfull.dot(vclip1d) / (norm(vclip1d) * norm(vfull))
        assert_almost_equal(cos, 1.0)

def test_vecs2rot_same():
    v1 = np.random.randn(3)
    v2 = v1 * 1.563
    q = utils.vecs2rot(v1, v2)
    npt.assert_almost_equal(q.rotation_matrix, np.eye(3))

def test_vecs2rot_random():
    for _ in range(10):
        v1 = utils.normalize(np.random.randn(3))
        v2 = utils.normalize(np.random.randn(3))
        q = utils.vecs2rot(v1, v2)
        vrot = q.rotate(v1)
        npt.assert_almost_equal(vrot, v2)


def test_vec_reject():
    V = np.array([
        [2.0,2.0],
        [-3.0,3.0]
    ])

    F = np.array([
        [1.0,0],
        [0,1.0]
    ])

    Fr = utils.vec_reject(V, F)
    npt.assert_almost_equal(Fr,
                            np.array([
                                [0.5,-0.5],
                                [0.5,0.5]
                            ]))

def test_wrap_pi():
    angles = (np.random.rand(100)-0.5)*8*np.pi
    wrapped = utils.wraptopi(angles)
    npt.assert_array_less(wrapped, 2*np.pi)
    npt.assert_array_less(-2*np.pi, wrapped)

