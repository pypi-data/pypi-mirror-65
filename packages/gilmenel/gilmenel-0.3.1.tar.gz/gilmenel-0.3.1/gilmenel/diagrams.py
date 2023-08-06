from collections import namedtuple
from typing import (
    Any,
    List,
)

import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.coordinates import (
    Longitude,
    Latitude,
    SkyCoord,
)

from matplotlib.patches import Circle

from gilmenel.instruments import (
    Star,
    BaseInstrument,
    GapInstrument,
)

Circle9 = namedtuple('Circle9', 'x y radius width color label')
Box9 = namedtuple('Box9', 'x y width height rotation color label')


def create_drawing(
    instr: BaseInstrument, stars: List[Star], best_stars: List[Star]
) -> List[Any]:
    # TODO: add hooks to BaseInstrument class so that each instrument and
    # telescope can define its own debug output

    target_ra = instr.target.ra.to_value(u.deg)
    target_dec = instr.target.dec.to_value(u.deg)

    shapes = []

    # setup some fiducials as guides, these are specific to SALT
    # 4.0 arcmin
    shapes.append(Circle9(target_ra, target_dec, 240, 1, 'green', '4 arcmin'))
    # 5.0 arcmin
    shapes.append(Circle9(target_ra, target_dec, 300, 1, 'green', '5 arcmin'))

    # draw inner exclusion distance
    radius = instr.inner_excl_distance.to_value(u.arcmin)
    label = f"{radius} arcmin"
    shapes.append(Circle9(target_ra, target_dec, radius * 60, 1, 'red', label))

    # the actual target/centre of search; in pink so it stands out!
    shapes.append(Circle9(target_ra, target_dec, 10, 3, 'magenta', "target"))

    # a line near the target to make sure the slit gap width is OK
    if isinstance(instr, GapInstrument):
        gap_width = instr.slit_gap_radius.to_value(u.arcmin) * 2
        pa = instr.slit_gap_angle.to_value(u.rad)
        shapes.append(Box9(target_ra, target_dec, gap_width, 10, pa, 'red', ""))

    # TODO: make these colours editable too
    merit_colours = {
        -1: "grey",  # not processed
        0: "red",  # out of range
        1: "orange",  # nearby stars
        2: "yellow",  # too dim
        3: "yellow",  # too bright
        4: "green",  # good candidate
    }

    for s in stars:
        if s.merit > -1:  # exclude faint stars that were not evaluated
            # the colour reflects the star's suitability
            colour = merit_colours[s.merit]
            shapes.append(
                Circle9(
                    s.ra.to_value(u.deg),
                    s.dec.to_value(u.deg),
                    2,
                    1,
                    colour,
                    f"{s.g_mag:.2f}",
                )
            )

    # indicate the best stars
    for s in best_stars:
        if s is not None:
            shapes.append(
                Circle9(
                    s.ra.to_value(u.deg),
                    s.dec.to_value(u.deg),
                    10,
                    2,
                    'cyan',
                    "best star",
                )
            )

    return shapes


def produce_ds9_region(
    instr: BaseInstrument, stars: List[Star], best_stars: List[Star]
) -> str:
    # create a ds9 region to help visualise things - for testing purposes...
    # note this must be written to disk as a region file that must be loaded
    # from file by ds9 later with a system command

    def draw_circle(r, label, c, x, y, width):
        rline = (
            f"circle {x:.6f}d {y:.6f}d {r}\" "
            f"# text={{{label}}} color={c} width={width}\n"
        )
        return rline

    shapes = create_drawing(instr, stars, best_stars)

    output = "global color=white\n"
    output += "fk5\n"

    # draw shapes
    for sh in shapes:
        if isinstance(sh, Circle9):
            output += draw_circle(sh.radius, sh.label, sh.color, sh.x, sh.y, sh.width)

        elif isinstance(sh, Box9):
            output += (
                f"box {sh.x} {sh.y} {sh.width}' {sh.height}' {sh.rotation}r #"
                f" fill=0 color={sh.color}\n"
            )

    return output


def produce_png(instr: BaseInstrument, stars: List[Star], best_stars: List[Star]):
    def red_or_blue(star):
        # calculate an approximate colour for the star
        # ideal: C = BP - RP -> 0.5 = blue, 2.0 = green/grey, 3.5 = red

        if star.rp_mag:
            return star.g_mag - star.rp_mag - 0.9  # more positive = more red

        return 0

    def equitorial(target, coords):
        ''' Convert ICRS coordinates in degrees to
            equitorially equivalent coordinates
        '''
        ra = (coords.ra - target.ra) * np.cos(coords.dec.radian)
        dec = coords.dec - target.dec

        return ra.to_value(u.deg), dec.to_value(u.deg)

        #     return ra.ra.to_value(u.deg) / np.cos(
        #         np.radians(ra.dec.to_value(u.deg)))

        # return ra / np.cos(np.radians(target_dec))

    def icrs(target, coords):
        ''' Convert equitorially equivalent coordinates in degrees to
            ICRS coordinates
        '''
        ra = coords.ra / np.cos(coords.dec.radian) + target.ra
        dec = coords.dec + target.dec

        return ra.wrap_at(360 * u.deg).degree, dec.degree

    target = instr.target

    # get brightest star
    brightest = min(s.g_mag for s in stars)

    # discard stars that are dimmer by x magnitudes
    stars = [s for s in stars if s.g_mag <= brightest + 8]

    ra, dec = zip(*[equitorial(target, s) for s in stars])
    colour = [red_or_blue(s) for s in stars]
    g_mag = [s.g_mag for s in stars]
    merit = [s.merit for s in stars]

    # 'brightness' for star size on scatter plot
    # 20 -> 1
    # 15 -> 5
    # 10 -> 25
    # = 5 ** ((20 - g) / 5)
    brightness = [(3 ** ((20 - s.g_mag) / 5)) ** 2.0 for s in stars]
    halo = [(3 ** ((20 - s.g_mag) / 5)) ** 2.5 for s in stars]

    fig, ax = plt.subplots(figsize=(12.5, 10))
    ax.set_facecolor('#111111')

    # halo
    ax.scatter(
        ra,
        dec,
        c=colour,
        s=halo,
        alpha=0.4,
        marker='o',
        edgecolors="none",
        cmap=plt.cm.RdYlBu_r,
        vmin=-1.5,
        vmax=1.5,
    )
    # centers
    sc = ax.scatter(
        ra,
        dec,
        c=colour,
        s=brightness,
        alpha=0.9,
        marker='D',
        # marker="$\u25b2$",
        edgecolors="none",
        cmap=plt.cm.RdYlBu_r,
        vmin=-1.5,
        vmax=1.5,
        label="Guide Stars",
    )

    # TODO: make these colours editable too
    merit_colours = {
        -1: "grey",  # not processed
        0: "#FF0000",  # out of range
        1: "#FF5500",  # nearby stars
        2: "#C0CA33",  # too dim
        3: "#FFFF00",  # too bright
        4: "#00FF00",  # good candidate
    }

    text_offset = 4 * 10 ** -3
    # the colour reflects the star's suitability
    merit_colour = [merit_colours[s.merit] for s in stars]
    for r, d, g, m in zip(ra, dec, g_mag, merit):
        if m > -1:
            ax.annotate(
                f"{g:.2f}", (r, d + text_offset), color=merit_colours[m], ha='center',
            )

    # add fiducials

    # transform to equatorial equivalent coordinates
    one_arcmin = 1 / 60

    # SCAM
    ax.add_artist(Circle((0, 0), 5 * one_arcmin, color='#00ff00', fill=False,))
    # RSS
    ax.add_artist(Circle((0, 0), 4 * one_arcmin, color='#00ff00', fill=False,))
    # Target Exclusion
    exclusion = instr.inner_excl_distance.to_value(u.arcmin)
    ax.add_artist(Circle((0, 0), exclusion * one_arcmin, color='#990000', fill=False,))
    # Slit exclusion
    if isinstance(instr, GapInstrument):
        # TODO: add slit rectangle that rotates with PA
        pass
    # Target
    ax.add_artist(Circle((0, 0), 10 / 60 * one_arcmin, color='#ff00ff', fill=False,))

    # Guide Stars
    text_offset = 4 * 10 ** -3
    for r, d in [equitorial(instr.target, s) for s in best_stars if s is not None]:
        ax.add_artist(Circle((r, d), 10 / 60 * one_arcmin, color='cyan', fill=False,))
        ax.annotate(
            "Guide Star", (r + text_offset, d), color='cyan', ha='right',
        )

    # set axis limits
    ax.set_xlim(5.25 * one_arcmin, -5.25 * one_arcmin)
    ax.set_ylim(-5.25 * one_arcmin, 5.25 * one_arcmin)
    # set ticks
    ra_ticks = [
        Longitude(icrs(target, SkyCoord(t * u.deg, 0 * u.deg))[0], u.deg).to_string(
            unit=u.hour, precision=0
        )
        for t in ax.get_xticks()
    ]
    ax.set_xticklabels(ra_ticks)
    dec_ticks = [
        Latitude(icrs(target, SkyCoord(0 * u.deg, t * u.deg))[1], u.deg).to_string(
            unit=u.deg, precision=0
        )
        for t in ax.get_yticks()
    ]
    ax.set_yticklabels(dec_ticks)
    # label axes
    ax.set_xlabel(r'$RA$', fontsize=12)
    ax.set_ylabel(r'$Dec$', fontsize=12)
    ax.set_title("Guide Stars (SCAM Display)")
    # add colourbar
    cbar = plt.colorbar(sc)
    cbar.ax.set_ylabel("Source Colour")
    # output figure
    fig.tight_layout()
    plt.savefig("./charts/current.png", bbox_inches='tight')
    plt.close()
