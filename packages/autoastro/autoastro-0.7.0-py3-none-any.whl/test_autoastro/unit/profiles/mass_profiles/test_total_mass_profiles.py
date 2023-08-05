import autofit as af
import autoarray as aa
from autoarray.structures import grids
import autoastro as aast
import numpy as np
import pytest
import os


@pytest.fixture(autouse=True)
def reset_config():
    """
    Use configuration from the default path. You may want to change this to set a specific path.
    """
    af.conf.instance = af.conf.default


grid = aa.GridIrregular.manual_1d([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


class TestPointMass:
    def test__constructor_and_units(self):
        point_mass = aast.mp.PointMass(centre=(1.0, 2.0), einstein_radius=2.0)

        assert point_mass.centre == (1.0, 2.0)
        assert isinstance(point_mass.centre[0], aast.dim.Length)
        assert isinstance(point_mass.centre[1], aast.dim.Length)
        assert point_mass.centre[0].unit == "arcsec"
        assert point_mass.centre[1].unit == "arcsec"

        assert point_mass.einstein_radius == 2.0
        assert isinstance(point_mass.einstein_radius, aast.dim.Length)
        assert point_mass.einstein_radius.unit_length == "arcsec"

    # def test__converence__correct_values(self):
    #
    #     grid = aa.GridIrregular.manual_1d([[0.0, -1.0], [0.0, 0.0], [0.0, 1.0]])
    #
    #     point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)
    #
    #     convergence = point_mass.convergence_from_grid(
    #         grid=grid)
    #
    #     assert convergence == pytest.approx(np.array([0.0, np.pi, 0.0]), 1e-3)
    #
    #     point_mass = aast.mp.PointMass(centre=(0.0, 0.8), einstein_radius=2.0)
    #
    #     convergence = point_mass.convergence_from_grid(
    #         grid=grid)
    #
    #     assert convergence == pytest.approx(np.array([0.0, 0.0, 4.0*np.pi]), 1e-3)
    #
    #     grid = aa.Grid.uniform(shape_2d=(5,5), pixel_scales=1.0, sub_size=2)
    #
    #     point_mass = aast.mp.PointMass(centre=(1.0, -1.0), einstein_radius=1.0)
    #
    #     convergence = point_mass.convergence_from_grid(
    #         grid=grid)
    #
    #     assert convergence[14] == 0.0
    #     assert convergence[24] == np.pi

    def test__deflections__correct_values(self):

        # The radial coordinate at (1.0, 1.0) is sqrt(2)
        # This is decomposed into (y,x) angles of sin(45) = cos(45) = sqrt(2) / 2.0
        # Thus, for an EinR of 1.0, the deflection angle is (1.0 / sqrt(2)) * (sqrt(2) / 2.0)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        )
        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=2.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        )
        assert deflections[0, 0] == pytest.approx(2.0, 1e-3)
        assert deflections[0, 1] == pytest.approx(2.0, 1e-3)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 2.0]])
        )
        assert deflections[0, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.25, 1e-3)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 1.0]])
        )
        assert deflections[0, 0] == pytest.approx(0.4, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.2, 1e-3)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=2.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[4.0, 9.0]])
        )
        assert deflections[0, 0] == pytest.approx(16.0 / 97.0, 1e-3)
        assert deflections[0, 1] == pytest.approx(36.0 / 97.0, 1e-3)

        point_mass = aast.mp.PointMass(centre=(1.0, 2.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 3.0]])
        )
        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

    def test__deflections__change_geometry(self):

        point_mass_0 = aast.mp.PointMass(centre=(0.0, 0.0))
        point_mass_1 = aast.mp.PointMass(centre=(1.0, 1.0))
        deflections_0 = point_mass_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        )
        deflections_1 = point_mass_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        point_mass_0 = aast.mp.PointMass(centre=(0.0, 0.0))
        point_mass_1 = aast.mp.PointMass(centre=(0.0, 0.0))
        deflections_0 = point_mass_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        )
        deflections_1 = point_mass_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__multiple_coordinates_in__multiple_coordinates_out(self):

        point_mass = aast.mp.PointMass(centre=(1.0, 2.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 3.0], [2.0, 3.0], [2.0, 3.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)
        assert deflections[1, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 1] == pytest.approx(0.5, 1e-3)

        point_mass = aast.mp.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections = point_mass.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d(
                [[1.0, 1.0], [2.0, 2.0], [1.0, 1.0], [2.0, 2.0]]
            )
        )

        assert deflections[0, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.5, 1e-3)

        assert deflections[1, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.25, 1e-3)

        assert deflections[2, 0] == pytest.approx(0.5, 1e-3)
        assert deflections[2, 1] == pytest.approx(0.5, 1e-3)

        assert deflections[3, 0] == pytest.approx(0.25, 1e-3)
        assert deflections[3, 1] == pytest.approx(0.25, 1e-3)

    def test__deflections_of_profile__dont_use_interpolate_and_cache_decorators(self):
        point_mass = aast.mp.PointMass(centre=(-0.3, 0.2), einstein_radius=1.0)

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = point_mass.deflections_from_grid(grid=regular_with_interp)

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = point_mass.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        point_mass = aast.mp.PointMass()

        deflections = point_mass.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)


class TestBrokenPowerLaw:
    def test__convergence_correct_values(self):
        broken_power_law = aast.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )
        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        ) == pytest.approx(0.0355237, 1e-4)

        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0], [0.5, 1.0]])
        ) == pytest.approx([0.0355237, 0.0355237], 1e-4)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.8,
            phi=30.0,
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        ) == pytest.approx(0.05006035, 1e-4)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.7,
            phi=160.0,
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )
        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        ) == pytest.approx(0.034768, 1e-4)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.7,
            phi=250.0,
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )
        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        ) == pytest.approx(0.03622852, 1e-4)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.7,
            phi=310.0,
            einstein_radius=1.0,
            inner_slope=1.8,
            outer_slope=2.2,
            break_radius=0.1,
        )
        assert broken_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        ) == pytest.approx(0.026469, 1e-4)

    def test__deflections__correct_values(self):

        broken_power_law = aast.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )
        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )
        assert deflections[0, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.808152, 1e-3)

        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0], [0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.808152, 1e-3)
        assert deflections[1, 0] == pytest.approx(0.404076, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.808152, 1e-3)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.8,
            phi=30.0,
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.40392, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.811619, 1e-3)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.8,
            phi=110.0,
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.4005338, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.8067221, 1e-3)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.8,
            phi=220.0,
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.399651, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.813372, 1e-3)

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            axis_ratio=0.6,
            phi=300.0,
            einstein_radius=1.0,
            inner_slope=1.5,
            outer_slope=2.5,
            break_radius=0.1,
        )

        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        assert deflections[0, 0] == pytest.approx(0.402629, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.798795, 1e-3)

    def test__convergence__change_geometry(self):
        broken_power_law_0 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = aast.mp.SphericalBrokenPowerLaw(centre=(1.0, 1.0))
        assert broken_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        ) == broken_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )

        broken_power_law_0 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        assert broken_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == broken_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

        broken_power_law_0 = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=0.0
        )
        broken_power_law_1 = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0
        )
        assert broken_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == broken_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

    def test__deflections__change_geometry(self):
        broken_power_law_0 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = aast.mp.SphericalBrokenPowerLaw(centre=(1.0, 1.0))
        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        broken_power_law_0 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        broken_power_law_1 = aast.mp.SphericalBrokenPowerLaw(centre=(0.0, 0.0))
        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

        broken_power_law_0 = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=0.0
        )
        broken_power_law_1 = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0
        )
        deflections_0 = broken_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        )
        deflections_1 = broken_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__deflections__compare_to_power_law(self):

        broken_power_law = aast.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=1.999,
            outer_slope=2.0001,
            break_radius=0.0001,
        )
        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        # Use of ratio avoids normalization definition difference effects

        broken_yx_ratio = deflections[0, 0] / deflections[0, 1]

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0, 0), einstein_radius=2.0, slope=2.0
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        power_law_yx_ratio = deflections[0, 0] / deflections[0, 1]

        assert broken_yx_ratio == pytest.approx(power_law_yx_ratio, 1.0e-4)

        broken_power_law = aast.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=2.399,
            outer_slope=2.4001,
            break_radius=0.0001,
        )
        deflections = broken_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        # Use of ratio avoids normalization difference effects

        broken_yx_ratio = deflections[0, 0] / deflections[0, 1]

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0, 0), einstein_radius=2.0, slope=2.4
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.5, 1.0]])
        )

        power_law_yx_ratio = deflections[0, 0] / deflections[0, 1]

        assert broken_yx_ratio == pytest.approx(power_law_yx_ratio, 1.0e-4)

    def test__deflections_of_both_profiles__dont_use_interpolate_and_cache_decorators(
        self
    ):
        broken_power_law = aast.mp.SphericalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=2.399,
            outer_slope=2.4001,
            break_radius=0.0001,
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)
        true_deflections = broken_power_law.deflections_from_grid(grid=grid)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = broken_power_law.deflections_from_grid(
            grid=regular_with_interp
        )
        assert np.max(true_deflections[:, 0] - interp_deflections[:, 0]) < 0.1
        assert np.max(true_deflections[:, 1] - interp_deflections[:, 1]) < 0.1

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = broken_power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

        broken_power_law = aast.mp.EllipticalBrokenPowerLaw(
            centre=(0, 0),
            einstein_radius=2.0,
            inner_slope=2.399,
            outer_slope=2.4001,
            break_radius=0.0001,
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)
        true_deflections = broken_power_law.deflections_from_grid(grid=grid)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = broken_power_law.deflections_from_grid(
            grid=regular_with_interp
        )
        assert np.max(true_deflections[:, 0] - interp_deflections[:, 0]) < 0.1
        assert np.max(true_deflections[:, 1] - interp_deflections[:, 1]) < 0.1

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = broken_power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_power_law = aast.mp.EllipticalBrokenPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)

        cored_power_law = aast.mp.SphericalBrokenPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)


class TestCoredPowerLaw:
    def test__constructor_and_units(self):
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            slope=2.2,
            core_radius=0.1,
        )

        assert cored_power_law.centre == (1.0, 2.0)
        assert isinstance(cored_power_law.centre[0], aast.dim.Length)
        assert isinstance(cored_power_law.centre[1], aast.dim.Length)
        assert cored_power_law.centre[0].unit == "arcsec"
        assert cored_power_law.centre[1].unit == "arcsec"

        assert cored_power_law.axis_ratio == 0.5
        assert isinstance(cored_power_law.axis_ratio, float)

        assert cored_power_law.phi == 45.0
        assert isinstance(cored_power_law.phi, float)

        assert cored_power_law.einstein_radius == 1.0
        assert isinstance(cored_power_law.einstein_radius, aast.dim.Length)
        assert cored_power_law.einstein_radius.unit_length == "arcsec"

        assert cored_power_law.slope == 2.2
        assert isinstance(cored_power_law.slope, float)

        assert cored_power_law.core_radius == 0.1
        assert isinstance(cored_power_law.core_radius, aast.dim.Length)
        assert cored_power_law.core_radius.unit_length == "arcsec"

        assert cored_power_law.einstein_radius_rescaled == pytest.approx(
            0.53333333, 1.0e-4
        )

        cored_power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(1.0, 2.0), einstein_radius=1.0, slope=2.2, core_radius=0.1
        )

        assert cored_power_law.centre == (1.0, 2.0)
        assert isinstance(cored_power_law.centre[0], aast.dim.Length)
        assert isinstance(cored_power_law.centre[1], aast.dim.Length)
        assert cored_power_law.centre[0].unit == "arcsec"
        assert cored_power_law.centre[1].unit == "arcsec"

        assert cored_power_law.axis_ratio == 1.0
        assert isinstance(cored_power_law.axis_ratio, float)

        assert cored_power_law.phi == 0.0
        assert isinstance(cored_power_law.phi, float)

        assert cored_power_law.einstein_radius == 1.0
        assert isinstance(cored_power_law.einstein_radius, aast.dim.Length)
        assert cored_power_law.einstein_radius.unit_length == "arcsec"

        assert cored_power_law.slope == 2.2
        assert isinstance(cored_power_law.slope, float)

        assert cored_power_law.core_radius == 0.1
        assert isinstance(cored_power_law.core_radius, aast.dim.Length)
        assert cored_power_law.core_radius.unit_length == "arcsec"

        assert cored_power_law.einstein_radius_rescaled == pytest.approx(0.4, 1.0e-4)

    def test__convergence_correct_values(self):
        cored_power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(1, 1), einstein_radius=1.0, slope=2.2, core_radius=0.1
        )
        assert cored_power_law.convergence_func(grid_radius=1.0) == pytest.approx(
            0.39762, 1e-4
        )

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=0.0,
            einstein_radius=1.0,
            slope=2.3,
            core_radius=0.2,
        )
        assert cored_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.45492, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=0.0,
            einstein_radius=2.0,
            slope=1.7,
            core_radius=0.2,
        )
        assert cored_power_law.convergence_from_grid(
            grid=aa.Coordinates([[(0.0, 1.0)]])
        )[0][0] == pytest.approx(1.3887, 1e-3)

    def test__potential_correct_values(self):
        power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.0, slope=1.8, core_radius=0.2
        )
        assert power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        ) == pytest.approx(0.54913, 1e-3)

        power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(0.2, -0.2), einstein_radius=0.5, slope=2.4, core_radius=0.5
        )
        assert power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        ) == pytest.approx(0.01820, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.2, -0.2),
            axis_ratio=0.6,
            phi=120.0,
            einstein_radius=0.5,
            slope=2.4,
            core_radius=0.5,
        )
        assert cored_power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        ) == pytest.approx(0.02319, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )
        assert cored_power_law.potential_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )[0][0] == pytest.approx(0.71185, 1e-3)

    def test__deflections__correct_values(self):
        power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.0, slope=1.8, core_radius=0.2
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.80677, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.30680, 1e-3)

        power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(0.2, -0.2), einstein_radius=0.5, slope=2.4, core_radius=0.5
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-0.00321, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.09316, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )
        deflections = cored_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.9869, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.54882, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.2, -0.2),
            axis_ratio=0.6,
            phi=120.0,
            einstein_radius=0.5,
            slope=2.4,
            core_radius=0.5,
        )

        deflections = cored_power_law.deflections_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )
        assert deflections[0][0][0] == pytest.approx(0.01111, 1e-3)
        assert deflections[0][0][1] == pytest.approx(0.11403, 1e-3)

    def test__convergence__change_geometry(self):
        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))
        assert cored_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        ) == cored_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )

        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        assert cored_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == cored_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

        cored_power_law_0 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=0.0
        )
        cored_power_law_1 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0
        )
        assert cored_power_law_0.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == cored_power_law_1.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

    def test__potential__change_geometry(self):
        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))
        assert cored_power_law_0.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        ) == cored_power_law_1.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )

        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        assert cored_power_law_0.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == cored_power_law_1.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

        cored_power_law_0 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=0.0
        )
        cored_power_law_1 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0
        )
        assert cored_power_law_0.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == cored_power_law_1.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )

    def test__deflections__change_geometry(self):
        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(1.0, 1.0))
        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 1.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 0.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        cored_power_law_0 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        cored_power_law_1 = aast.mp.SphericalCoredPowerLaw(centre=(0.0, 0.0))
        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

        cored_power_law_0 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=0.0
        )
        cored_power_law_1 = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0
        )
        deflections_0 = cored_power_law_0.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        )
        deflections_1 = cored_power_law_1.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        )
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-5)

    def test__multiple_coordinates_in__multiple_quantities_out(self):
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=0.0,
            einstein_radius=1.0,
            slope=2.3,
            core_radius=0.2,
        )
        assert cored_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0], [0.0, 1.0]])
        )[0] == pytest.approx(0.45492, 1e-3)
        assert cored_power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0], [0.0, 1.0]])
        )[1] == pytest.approx(0.45492, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.2, -0.2),
            axis_ratio=0.6,
            phi=120.0,
            einstein_radius=0.5,
            slope=2.4,
            core_radius=0.5,
        )
        assert cored_power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625], [0.1625, 0.1625]])
        )[0] == pytest.approx(0.02319, 1e-3)
        assert cored_power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625], [0.1625, 0.1625]])
        )[1] == pytest.approx(0.02319, 1e-3)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )
        deflections = cored_power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625], [0.1625, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.9869, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.54882, 1e-3)
        assert deflections[1, 0] == pytest.approx(0.9869, 1e-3)
        assert deflections[1, 1] == pytest.approx(-0.54882, 1e-3)

    def test__spherical_and_elliptical_match(self):
        elliptical = aast.mp.EllipticalCoredPowerLaw(
            centre=(1.1, 1.1),
            axis_ratio=1.0,
            phi=0.0,
            einstein_radius=3.0,
            slope=2.2,
            core_radius=0.1,
        )
        spherical = aast.mp.SphericalCoredPowerLaw(
            centre=(1.1, 1.1), einstein_radius=3.0, slope=2.2, core_radius=0.1
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__deflections_of_elliptical_profile__use_interpolate_and_cache_decorators(
        self
    ):
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            slope=1.8,
            core_radius=0.2,
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)
        true_deflections = cored_power_law.deflections_from_grid(grid=grid)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = cored_power_law.deflections_from_grid(
            grid=regular_with_interp
        )
        assert np.max(true_deflections[:, 0] - interp_deflections[:, 0]) < 0.1
        assert np.max(true_deflections[:, 1] - interp_deflections[:, 1]) < 0.1

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = cored_power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y == interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x == interp_deflections[:, 1]).all()

    def test__deflections_of_spherical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        cored_power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=1.8, core_radius=0.2
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)
        true_deflections = cored_power_law.deflections_from_grid(grid=grid)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = cored_power_law.deflections_from_grid(
            grid=regular_with_interp
        )
        assert np.max(true_deflections[:, 0] - interp_deflections[:, 0]) < 0.1
        assert np.max(true_deflections[:, 1] - interp_deflections[:, 1]) < 0.1

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = cored_power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__summarize_in_units(self):

        test_path = "{}/config/summary".format(
            os.path.dirname(os.path.realpath(__file__))
        )
        af.conf.instance = af.conf.Config(config_path=test_path)

        cored_power_law = aast.mp.SphericalCoredPowerLaw(
            centre=(0.0, 0.0), einstein_radius=1.0, core_radius=0.0, slope=2.0
        )

        summary_text = cored_power_law.summarize_in_units(
            radii=[aast.dim.Length(10.0), aast.dim.Length(500.0)],
            prefix="pl_",
            unit_length="arcsec",
            unit_mass="angular",
            whitespace=50,
        )

        i = 0

        assert summary_text[i] == "Mass Profile = SphericalCoredPowerLaw\n"
        i += 1
        assert (
            summary_text[i]
            == "pl_einstein_radius                                1.00 arcsec"
        )
        i += 1
        assert (
            summary_text[i]
            == "pl_einstein_mass                                  3.1308e+00 angular"
        )
        i += 1
        assert (
            summary_text[i]
            == "pl_mass_within_10.00_arcsec                       3.1416e+01 angular"
        )
        i += 1
        assert (
            summary_text[i]
            == "pl_mass_within_500.00_arcsec                      1.5708e+03 angular"
        )
        i += 1

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_power_law = aast.mp.EllipticalCoredPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = cored_power_law.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)

        cored_power_law = aast.mp.SphericalCoredPowerLaw()

        convergence = cored_power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = cored_power_law.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = cored_power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)


class TestPowerLaw:
    def test__constructor_and_units(self):
        power_law = aast.mp.EllipticalPowerLaw(
            centre=(1.0, 2.0), axis_ratio=0.5, phi=45.0, einstein_radius=1.0, slope=2.0
        )

        assert power_law.centre == (1.0, 2.0)
        assert isinstance(power_law.centre[0], aast.dim.Length)
        assert isinstance(power_law.centre[1], aast.dim.Length)
        assert power_law.centre[0].unit == "arcsec"
        assert power_law.centre[1].unit == "arcsec"

        assert power_law.axis_ratio == 0.5
        assert isinstance(power_law.axis_ratio, float)

        assert power_law.phi == 45.0
        assert isinstance(power_law.phi, float)

        assert power_law.einstein_radius == 1.0
        assert isinstance(power_law.einstein_radius, aast.dim.Length)
        assert power_law.einstein_radius.unit_length == "arcsec"

        assert power_law.slope == 2.0
        assert isinstance(power_law.slope, float)

        assert power_law.core_radius == 0.0
        assert isinstance(power_law.core_radius, aast.dim.Length)
        assert power_law.core_radius.unit_length == "arcsec"

        assert power_law.einstein_radius_rescaled == pytest.approx(0.6666666666, 1.0e-4)

        power_law = aast.mp.SphericalPowerLaw(
            centre=(1.0, 2.0), einstein_radius=1.0, slope=2.0
        )

        assert power_law.centre == (1.0, 2.0)
        assert isinstance(power_law.centre[0], aast.dim.Length)
        assert isinstance(power_law.centre[1], aast.dim.Length)
        assert power_law.centre[0].unit == "arcsec"
        assert power_law.centre[1].unit == "arcsec"

        assert power_law.axis_ratio == 1.0
        assert isinstance(power_law.axis_ratio, float)

        assert power_law.phi == 0.0
        assert isinstance(power_law.phi, float)

        assert power_law.einstein_radius == 1.0
        assert isinstance(power_law.einstein_radius, aast.dim.Length)
        assert power_law.einstein_radius.unit_length == "arcsec"

        assert power_law.slope == 2.0
        assert isinstance(power_law.slope, float)

        assert power_law.core_radius == 0.0
        assert isinstance(power_law.core_radius, aast.dim.Length)
        assert power_law.core_radius.unit_length == "arcsec"

        assert power_law.einstein_radius_rescaled == pytest.approx(0.5, 1.0e-4)

    def test__convergence_correct_values(self):
        isothermal = aast.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=1.0, slope=2.0
        )
        assert isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == pytest.approx(0.5, 1e-3)

        isothermal = aast.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=2.0, slope=2.2
        )
        assert isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 0.0]])
        ) == pytest.approx(0.4, 1e-3)

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=2.0, slope=2.2
        )
        assert power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[2.0, 0.0]])
        ) == pytest.approx(0.4, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0, slope=2.3
        )
        assert power_law.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.466666, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=0.0, einstein_radius=2.0, slope=1.7
        )
        assert power_law.convergence_from_grid(grid=aa.Coordinates([[(0.0, 1.0)]]))[0][
            0
        ] == pytest.approx(1.4079, 1e-3)

    def test__potential_correct_values(self):
        power_law = aast.mp.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=2.3
        )
        assert power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        ) == pytest.approx(1.90421, 1e-3)

        power_law = aast.mp.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=1.8
        )
        assert power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        ) == pytest.approx(0.93758, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3, slope=2.2
        )
        assert power_law.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        ) == pytest.approx(1.53341, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3, slope=1.8
        )
        assert power_law.potential_from_grid(grid=aa.Coordinates([[(0.1625, 0.1625)]]))[
            0
        ][0] == pytest.approx(0.96723, 1e-3)

    def test__deflections__correct_values(self):

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=2.0
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-0.31622, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.94868, 1e-3)

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=2.5
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-1.59054, 1e-3)
        assert deflections[0, 1] == pytest.approx(-4.77162, 1e-3)

        power_law = aast.mp.SphericalPowerLaw(
            centre=(0.2, 0.2), einstein_radius=1.0, slope=1.5
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-0.06287, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.18861, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0, 0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0, slope=2.0
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.50734, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0, 0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0, slope=2.5
        )

        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(1.29641, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.99629, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0, 0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0, slope=1.5
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.48036, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.26729, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3, slope=1.9
        )
        deflections = power_law.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )

        # assert deflections[0, 0] == pytest.approx(1.12841, 1e-3)
        # assert deflections[0, 1] == pytest.approx(-0.60205, 1e-3)

        power_law = aast.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=150.0,
            einstein_radius=1.3,
            slope=2.2,
        )

        deflections = power_law.deflections_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )

        assert deflections[0][0][0] == pytest.approx(1.25995, 1e-3)
        assert deflections[0][0][1] == pytest.approx(-0.35096, 1e-3)

    def test__compare_to_cored_power_law(self):
        power_law = aast.mp.EllipticalPowerLaw(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=45.0, einstein_radius=1.0, slope=2.3
        )
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            slope=2.3,
            core_radius=0.0,
        )

        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = aast.mp.EllipticalPowerLaw(
            centre=(1.1, 1.1),
            axis_ratio=0.9999,
            phi=0.0,
            einstein_radius=3.0,
            slope=2.4,
        )
        spherical = aast.mp.SphericalPowerLaw(
            centre=(1.1, 1.1), einstein_radius=3.0, slope=2.4
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__deflections_of_elliptical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        power_law = aast.mp.EllipticalPowerLaw(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3, slope=1.8
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = power_law.deflections_from_grid(grid=regular_with_interp)

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__deflections_of_spherical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        power_law = aast.mp.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=1.8
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = power_law.deflections_from_grid(grid=regular_with_interp)

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        power_law = aast.mp.EllipticalPowerLaw()

        convergence = power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = power_law.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)

        power_law = aast.mp.SphericalPowerLaw()

        convergence = power_law.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = power_law.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = power_law.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)


class TestCoredIsothermal:
    def test__constructor_and_units(self):
        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(1.0, 2.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            core_radius=0.1,
        )

        assert cored_isothermal.centre == (1.0, 2.0)
        assert isinstance(cored_isothermal.centre[0], aast.dim.Length)
        assert isinstance(cored_isothermal.centre[1], aast.dim.Length)
        assert cored_isothermal.centre[0].unit == "arcsec"
        assert cored_isothermal.centre[1].unit == "arcsec"

        assert cored_isothermal.axis_ratio == 0.5
        assert isinstance(cored_isothermal.axis_ratio, float)

        assert cored_isothermal.phi == 45.0
        assert isinstance(cored_isothermal.phi, float)

        assert cored_isothermal.einstein_radius == 1.0
        assert isinstance(cored_isothermal.einstein_radius, aast.dim.Length)
        assert cored_isothermal.einstein_radius.unit_length == "arcsec"

        assert cored_isothermal.slope == 2.0
        assert isinstance(cored_isothermal.slope, float)

        assert cored_isothermal.core_radius == 0.1
        assert isinstance(cored_isothermal.core_radius, aast.dim.Length)
        assert cored_isothermal.core_radius.unit_length == "arcsec"

        assert cored_isothermal.einstein_radius_rescaled == pytest.approx(
            0.6666666666, 1.0e-4
        )

        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(1.0, 2.0), einstein_radius=1.0, core_radius=0.1
        )

        assert cored_isothermal.centre == (1.0, 2.0)
        assert isinstance(cored_isothermal.centre[0], aast.dim.Length)
        assert isinstance(cored_isothermal.centre[1], aast.dim.Length)
        assert cored_isothermal.centre[0].unit == "arcsec"
        assert cored_isothermal.centre[1].unit == "arcsec"

        assert cored_isothermal.axis_ratio == 1.0
        assert isinstance(cored_isothermal.axis_ratio, float)

        assert cored_isothermal.phi == 0.0
        assert isinstance(cored_isothermal.phi, float)

        assert cored_isothermal.einstein_radius == 1.0
        assert isinstance(cored_isothermal.einstein_radius, aast.dim.Length)
        assert cored_isothermal.einstein_radius.unit_length == "arcsec"

        assert cored_isothermal.slope == 2.0
        assert isinstance(cored_isothermal.slope, float)

        assert cored_isothermal.core_radius == 0.1
        assert isinstance(cored_isothermal.core_radius, aast.dim.Length)
        assert cored_isothermal.core_radius.unit_length == "arcsec"

        assert cored_isothermal.einstein_radius_rescaled == pytest.approx(0.5, 1.0e-4)

    def test__convergence_correct_values(self):
        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(1, 1), einstein_radius=1.0, core_radius=0.1
        )
        assert cored_isothermal.convergence_func(grid_radius=1.0) == pytest.approx(
            0.49752, 1e-4
        )

        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(1, 1), einstein_radius=1.0, core_radius=0.1
        )
        assert cored_isothermal.convergence_func(grid_radius=1.0) == pytest.approx(
            0.49752, 1e-4
        )

        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0, core_radius=0.2
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == pytest.approx(0.49029, 1e-3)

        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=2.0, core_radius=0.2
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[1.0, 0.0]])
        ) == pytest.approx(2.0 * 0.49029, 1e-3)

        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0, core_radius=0.2
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.49029, 1e-3)

        # axis ratio changes only einstein_rescaled, so wwe can use the above value and times by 1.0/1.5.
        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=0.0,
            einstein_radius=1.0,
            core_radius=0.2,
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.49029 * 1.33333, 1e-3)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            einstein_radius=2.0,
            core_radius=0.2,
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(2.0 * 0.49029, 1e-3)

        # for axis_ratio = 1.0, the factor is 1/2
        # for axis_ratio = 0.5, the factor is 1/(1.5)
        # So the change in the value is 0.5 / (1/1.5) = 1.0 / 0.75
        # axis ratio changes only einstein_rescaled, so wwe can use the above value and times by 1.0/1.5.
        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=0.0,
            einstein_radius=1.0,
            core_radius=0.2,
        )
        assert cored_isothermal.convergence_from_grid(
            grid=aa.Coordinates([[(0.0, 1.0)]])
        )[0][0] == pytest.approx((1.0 / 0.75) * 0.49029, 1e-3)

    def test__potential__correct_values(self):
        isothermal_core = aast.mp.SphericalCoredIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3, core_radius=0.2
        )
        assert isothermal_core.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        ) == pytest.approx(0.72231, 1e-3)

        isothermal_core = aast.mp.SphericalCoredIsothermal(
            centre=(0.2, -0.2), einstein_radius=0.5, core_radius=0.5
        )
        assert isothermal_core.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        ) == pytest.approx(0.03103, 1e-3)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            core_radius=0.2,
        )
        assert cored_isothermal.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        ) == pytest.approx(0.74354, 1e-3)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(0.2, -0.2),
            axis_ratio=0.6,
            phi=120.0,
            einstein_radius=0.5,
            core_radius=0.5,
        )
        assert cored_isothermal.potential_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )[0][0] == pytest.approx(0.04024, 1e-3)

    def test__deflections__correct_values(self):
        isothermal_core = aast.mp.SphericalCoredIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3, core_radius=0.2
        )
        deflections = isothermal_core.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.98582, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.37489, 1e-3)

        isothermal_core = aast.mp.SphericalCoredIsothermal(
            centre=(0.2, -0.2), einstein_radius=0.5, core_radius=0.5
        )
        deflections = isothermal_core.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-0.00559, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.16216, 1e-3)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            core_radius=0.2,
        )
        deflections = cored_isothermal.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.95429, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.52047, 1e-3)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(0.2, -0.2),
            axis_ratio=0.6,
            phi=120.0,
            einstein_radius=0.5,
            core_radius=0.5,
        )
        deflections = cored_isothermal.deflections_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )
        assert deflections[0][0][0] == pytest.approx(0.02097, 1e-3)
        assert deflections[0][0][1] == pytest.approx(0.20500, 1e-3)

    def test__compare_to_cored_power_law(self):
        power_law = aast.mp.EllipticalCoredIsothermal(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            core_radius=0.1,
        )
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            slope=2.0,
            core_radius=0.1,
        )

        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert power_law.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = aast.mp.EllipticalCoredIsothermal(
            centre=(1.1, 1.1),
            axis_ratio=0.9999,
            phi=0.0,
            einstein_radius=3.0,
            core_radius=1.0,
        )
        spherical = aast.mp.SphericalCoredIsothermal(
            centre=(1.1, 1.1), einstein_radius=3.0, core_radius=1.0
        )

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__deflections_of_elliptical_profile__use_interpolate_and_cache_decorators(
        self
    ):
        cored_isothermal = aast.mp.EllipticalCoredIsothermal(
            centre=(-0.7, 0.5),
            axis_ratio=0.7,
            phi=60.0,
            einstein_radius=1.3,
            core_radius=0.2,
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = cored_isothermal.deflections_from_grid(
            grid=regular_with_interp
        )
        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = cored_isothermal.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y == interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x == interp_deflections[:, 1]).all()

    def test__deflections_of_spherical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        cored_isothermal = aast.mp.SphericalCoredIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3, core_radius=0.2
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = cored_isothermal.deflections_from_grid(
            grid=regular_with_interp
        )
        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = cored_isothermal.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        cored_isothermal = aast.mp.EllipticalCoredIsothermal()

        convergence = cored_isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = cored_isothermal.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = cored_isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)

        cored_isothermal = aast.mp.SphericalCoredIsothermal()

        convergence = cored_isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = cored_isothermal.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = cored_isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)


class TestIsothermal:
    def test__constructor_and_units(self):
        isothermal = aast.mp.EllipticalIsothermal(
            centre=(1.0, 2.0), axis_ratio=0.5, phi=45.0, einstein_radius=1.0
        )

        assert isothermal.centre == (1.0, 2.0)
        assert isinstance(isothermal.centre[0], aast.dim.Length)
        assert isinstance(isothermal.centre[1], aast.dim.Length)
        assert isothermal.centre[0].unit == "arcsec"
        assert isothermal.centre[1].unit == "arcsec"

        assert isothermal.axis_ratio == 0.5
        assert isinstance(isothermal.axis_ratio, float)

        assert isothermal.phi == 45.0
        assert isinstance(isothermal.phi, float)

        assert isothermal.einstein_radius == 1.0
        assert isinstance(isothermal.einstein_radius, aast.dim.Length)
        assert isothermal.einstein_radius.unit_length == "arcsec"

        assert isothermal.slope == 2.0
        assert isinstance(isothermal.slope, float)

        assert isothermal.core_radius == 0.0
        assert isinstance(isothermal.core_radius, aast.dim.Length)
        assert isothermal.core_radius.unit_length == "arcsec"

        assert isothermal.einstein_radius_rescaled == pytest.approx(
            0.6666666666, 1.0e-4
        )

        isothermal = aast.mp.SphericalIsothermal(centre=(1.0, 2.0), einstein_radius=1.0)

        assert isothermal.centre == (1.0, 2.0)
        assert isinstance(isothermal.centre[0], aast.dim.Length)
        assert isinstance(isothermal.centre[1], aast.dim.Length)
        assert isothermal.centre[0].unit == "arcsec"
        assert isothermal.centre[1].unit == "arcsec"

        assert isothermal.axis_ratio == 1.0
        assert isinstance(isothermal.axis_ratio, float)

        assert isothermal.phi == 0.0
        assert isinstance(isothermal.phi, float)

        assert isothermal.einstein_radius == 1.0
        assert isinstance(isothermal.einstein_radius, aast.dim.Length)
        assert isothermal.einstein_radius.unit_length == "arcsec"

        assert isothermal.slope == 2.0
        assert isinstance(isothermal.slope, float)

        assert isothermal.core_radius == 0.0
        assert isinstance(isothermal.core_radius, aast.dim.Length)
        assert isothermal.core_radius.unit_length == "arcsec"

        assert isothermal.einstein_radius_rescaled == pytest.approx(0.5, 1.0e-4)

    def test__convergence__correct_values(self):
        # eta = 1.0
        # kappa = 0.5 * 1.0 ** 1.0
        isothermal = aast.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=2.0)
        assert isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.5 * 2.0, 1e-3)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, einstein_radius=1.0
        )
        assert isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.5, 1e-3)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, einstein_radius=2.0
        )
        assert isothermal.convergence_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.0, 1.0]])
        ) == pytest.approx(0.5 * 2.0, 1e-3)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0
        )
        assert isothermal.convergence_from_grid(grid=aa.Coordinates([[(0.0, 1.0)]]))[0][
            0
        ] == pytest.approx(0.66666, 1e-3)

    def test__potential__correct_values(self):
        isothermal = aast.mp.SphericalIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3
        )
        assert isothermal.potential_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        ) == pytest.approx(1.23435, 1e-3)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3
        )
        assert isothermal.potential_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )[0][0] == pytest.approx(1.19268, 1e-3)

    def test__deflections__correct_values(self):
        isothermal = aast.mp.SphericalIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3
        )
        deflections = isothermal.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(1.21510, 1e-4)
        assert deflections[0, 1] == pytest.approx(-0.46208, 1e-4)

        isothermal = aast.mp.SphericalIsothermal(
            centre=(-0.1, 0.1), einstein_radius=5.0
        )
        deflections = isothermal.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(4.88588, 1e-4)
        assert deflections[0, 1] == pytest.approx(1.06214, 1e-4)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0, 0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0
        )
        deflections = isothermal.deflections_from_grid(
            grid=aa.GridIrregular.manual_1d([[0.1625, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.50734, 1e-3)

        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0, 0), axis_ratio=0.5, phi=0.0, einstein_radius=1.0
        )
        deflections = isothermal.deflections_from_grid(
            grid=aa.Coordinates([[(0.1625, 0.1625)]])
        )
        assert deflections[0][0][0] == pytest.approx(0.79421, 1e-3)
        assert deflections[0][0][1] == pytest.approx(0.50734, 1e-3)

    def test__compare_to_cored_power_law(self):
        isothermal = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), axis_ratio=0.5, phi=45.0, einstein_radius=1.0
        )
        cored_power_law = aast.mp.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0),
            axis_ratio=0.5,
            phi=45.0,
            einstein_radius=1.0,
            core_radius=0.0,
        )

        assert isothermal.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert isothermal.potential_from_grid(grid=grid) == pytest.approx(
            cored_power_law.potential_from_grid(grid=grid), 1e-3
        )
        assert isothermal.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )
        assert isothermal.deflections_from_grid(grid=grid) == pytest.approx(
            cored_power_law.deflections_from_grid(grid=grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):
        elliptical = aast.mp.EllipticalIsothermal(
            centre=(1.1, 1.1), axis_ratio=0.9999, phi=0.0, einstein_radius=3.0
        )
        spherical = aast.mp.SphericalIsothermal(centre=(1.1, 1.1), einstein_radius=3.0)

        assert elliptical.convergence_from_grid(grid=grid) == pytest.approx(
            spherical.convergence_from_grid(grid=grid), 1e-4
        )
        assert elliptical.potential_from_grid(grid=grid) == pytest.approx(
            spherical.potential_from_grid(grid=grid), 1e-4
        )
        assert elliptical.deflections_from_grid(grid=grid) == pytest.approx(
            spherical.deflections_from_grid(grid=grid), 1e-4
        )

    def test__radius_of_critical_curve(self):
        sis = aast.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=2.0)
        assert sis.average_convergence_of_1_radius_in_units(
            unit_length="arcsec"
        ) == pytest.approx(2.0, 1e-4)

        sie = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0, axis_ratio=0.8, phi=0.0
        )
        assert sie.average_convergence_of_1_radius_in_units(
            unit_length="arcsec"
        ) == pytest.approx(1.0, 1e-4)

        sie = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=3.0, axis_ratio=0.5, phi=0.0
        )
        assert sie.average_convergence_of_1_radius_in_units(
            unit_length="arcsec"
        ) == pytest.approx(3.0, 1e-4)

        sie = aast.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=8.0, axis_ratio=0.2, phi=0.0
        )
        assert sie.average_convergence_of_1_radius_in_units(
            unit_length="arcsec"
        ) == pytest.approx(8.0, 1e-4)

    def test__deflections_of_elliptical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        isothermal = aast.mp.EllipticalIsothermal(
            centre=(-0.7, 0.5), axis_ratio=0.7, phi=60.0, einstein_radius=1.3
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = isothermal.deflections_from_grid(grid=regular_with_interp)
        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = isothermal.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__deflections_of_spherical_profile__dont_use_interpolate_and_cache_decorators(
        self
    ):
        isothermal = aast.mp.SphericalIsothermal(
            centre=(-0.7, 0.5), einstein_radius=1.3
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, pixel_scales=(1.0, 1.0), sub_size=1)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = isothermal.deflections_from_grid(grid=regular_with_interp)
        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = isothermal.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()

    def test__output_are_autoarrays(self):

        grid = aa.Grid.uniform(shape_2d=(2, 2), pixel_scales=1.0, sub_size=1)

        isothermal = aast.mp.EllipticalIsothermal()

        convergence = isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = isothermal.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)

        isothermal = aast.mp.SphericalIsothermal()

        convergence = isothermal.convergence_from_grid(grid=grid)

        assert convergence.shape_2d == (2, 2)

        potential = isothermal.potential_from_grid(grid=grid)

        assert potential.shape_2d == (2, 2)

        deflections = isothermal.deflections_from_grid(grid=grid)

        assert deflections.shape_2d == (2, 2)
