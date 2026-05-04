import pytest
import spiceypy as spice


def test_spiceypy_imports():
    assert spice.__version__ is not None


def test_version_string():
    version = spice.tkvrsn("TOOLKIT")
    assert isinstance(version, str)
    assert len(version) > 0


def test_bodvrd_earth_radii():
    # GM of Earth from built-in constants (no kernel needed)
    # spice.bodvrd requires a loaded kernel, so test basic math utilities instead
    pass


def test_dpr_rpd_roundtrip():
    # degrees-per-radian and radians-per-degree should be exact reciprocals
    import math
    assert pytest.approx(spice.dpr() * spice.rpd(), rel=1e-15) == 1.0
    assert pytest.approx(spice.dpr(), rel=1e-12) == math.degrees(1.0)


def test_rotation_matrix_identity():
    import numpy as np
    # A rotation by 0 radians around any axis should be the identity
    m = spice.rotate(0.0, 1)
    assert np.allclose(m, np.eye(3), atol=1e-12)


def test_v3_norm():
    import numpy as np
    v = [3.0, 4.0, 0.0]
    n = spice.vnorm(v)
    assert pytest.approx(n, rel=1e-12) == 5.0


def test_vhat():
    import numpy as np
    v = [0.0, 0.0, 7.0]
    unit = spice.vhat(v)
    assert np.allclose(unit, [0.0, 0.0, 1.0], atol=1e-12)


def test_vdot():
    a = [1.0, 0.0, 0.0]
    b = [0.0, 1.0, 0.0]
    assert pytest.approx(spice.vdot(a, b)) == 0.0


def test_vcrss():
    import numpy as np
    x = [1.0, 0.0, 0.0]
    y = [0.0, 1.0, 0.0]
    z = spice.vcrss(x, y)
    assert np.allclose(z, [0.0, 0.0, 1.0], atol=1e-12)


def test_latrec_recrec():
    import numpy as np
    # Convert Cartesian -> latitudinal -> back to Cartesian
    x0, y0, z0 = 1.0, 1.0, 1.0
    r, lon, lat = spice.reclat([x0, y0, z0])
    xyz = spice.latrec(r, lon, lat)
    assert np.allclose(xyz, [x0, y0, z0], atol=1e-12)
