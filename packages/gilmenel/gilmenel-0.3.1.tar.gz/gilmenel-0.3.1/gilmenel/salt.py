from astropy import units as u

from gilmenel import gilmenel


class GuiderSingle(gilmenel.BaseInstrument):
    def best_stars(self, stars):
        return [s for s in stars if s.merit >= 4][:1]


fif = GuiderSingle(
    'FIF',  # instr_name
    5 * u.arcmin - 20 * u.arcsec,  # instr_fov, arcminutes radius
    1.5 * u.arcmin,  # inner_excl_distance, arcminutes
    10 * u.arcsec,  # probe_fov, arcseconds
    8,  # bright limit
    14,  # faint limit
)


class GuiderDual(gilmenel.GapInstrument):
    def _score_star(self, star):
        '''
        rank each star linearly by magnitude and distance from exclusion zone
        favours bright stars at the edge of the field
        '''
        radius = (star.radius - self.inner_excl_distance) / (
            self.instr_fov - self.inner_excl_distance - self.nearby_limit
        )
        mag = 1 - (star.g_mag - self.bright_limit) / (
            self.faint_limit - self.bright_limit
        )
        return radius * mag

    def _group_by_side(self, stars):
        '''
        groups stars into left and right of gap
        '''
        stars_left = [
            s for s in stars if s.merit >= 4 and s.instr_coord.lon.to_value(u.deg) < 0
        ]
        stars_right = [
            s for s in stars if s.merit >= 4 and s.instr_coord.lon.to_value(u.deg) > 0
        ]

        return stars_left, stars_right

    def _furthest_pair(self, stars_left, stars_right):
        '''
        compare distances between the top 3 stars on each list
        to get longest distance between a star pair
        '''
        furthest_pair = (0, None, None)  # seperation, s, t
        for s in stars_left[:3]:
            for t in stars_right[:3]:
                sep = s.instr_coord.separation(t.instr_coord)
                if sep > furthest_pair[0]:
                    furthest_pair = sep, s, t

        return furthest_pair

    def criteria(self, stars):
        self.filter_geometry(stars)
        self.filter_nearby_pairs([s for s in stars if s.merit == 1])
        self.filter_magnitudes([s for s in stars if s.merit == 2])

        # check if enough stars have been found
        if len([s for s in stars if s.merit >= 4]) > 6:
            return True

    def best_stars(self, stars):
        # split all stars into left and right
        stars_left, stars_right = self._group_by_side(stars)

        # sort in place by star score
        stars_left.sort(key=lambda s: self._score_star(s), reverse=True)
        stars_right.sort(key=lambda s: self._score_star(s), reverse=True)

        # choose the stars with the greatest seperation
        _, star_left, star_right = self._furthest_pair(stars_left, stars_right)

        return star_left, star_right


pfgs = GuiderDual(
    'PFGS',  # instr_name
    5 * u.arcmin - 22 * u.arcsec,  # instr_fov, arcminutes radius
    1.0 * u.arcmin,  # inner_excl_distance, arcminutes
    11 * u.arcsec,  # probe_fov, arcseconds
    9,  # bright limit
    16.5,  # faint limit
    0.65 * u.arcmin,  # arcmin
    0 * u.deg,  # degrees
)
pfgs.inner_excl_shape = 'square'
