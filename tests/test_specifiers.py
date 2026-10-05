"""Tests for the specifiers module."""

from conda.models.version import VersionSpec
from packaging.specifiers import SpecifierSet

from conda_pypi.specifiers import specifier_bounds_to_conda


def test_converted_exclusive_upper_bound_excludes_prereleases():
    """Appending ``a0`` to exclusive upper bounds causes conda version to exclude pre-releases consistent with PEP 440."""
    pep_spec = VersionSpec(">=2.0,<3.12")
    assert pep_spec.match("3.12.0rc1")
    conda_spec = VersionSpec(">=2.0,<3.12a0")
    assert not conda_spec.match("3.12.0rc1")


def test_specifier_bounds_to_conda_appends_to_exclusive_upper_bound():
    spec = SpecifierSet("<3.12,>=2.0")
    new_bounds = specifier_bounds_to_conda(spec)
    assert "<3.12a0" in new_bounds


def test_specifier_bounds_to_conda_ignores_prereleases():
    spec = SpecifierSet("<3.12.0rc1,>=2.0")
    new_bounds = specifier_bounds_to_conda(spec)
    assert "a0" not in new_bounds


def test_specifier_bounds_to_conda_ignores_inclusive_upper_bound():
    spec = SpecifierSet("<=3.12.0rc1,>=2.0")
    new_bounds = specifier_bounds_to_conda(spec)
    assert "a0" not in new_bounds
