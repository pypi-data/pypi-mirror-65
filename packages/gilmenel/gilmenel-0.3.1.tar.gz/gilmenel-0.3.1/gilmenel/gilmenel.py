from typing import List

from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.vizier import Vizier

from gilmenel import astroquery as asterquery
from gilmenel.exceptions import NoStarsFoundError
from gilmenel.diagrams import (
    produce_ds9_region,
    produce_png,
)
from gilmenel.instruments import (
    Star,
    BaseInstrument,
    GapInstrument,
)

Catalog = None


def init(use_local_catalogue=False, catalog_url=None):
    global Catalog

    if use_local_catalogue:
        Catalog = asterquery.Local
        asterquery.catalog_url = catalog_url
    else:
        Catalog = Vizier
        print("Using remote Vizier catalogue")


def view_sky(instr: BaseInstrument, max_stars: int = -1) -> List[Star]:
    # Query the GAIA DR2 vizier catalogue (catalogue identifier: I/345/gaia2)
    # The '+' in "+Gmag" sorts the list by the brightest first, which is useful
    # for us later when it comes to picking the best candidate stars.
    # The '_r' column gives a handy radial distance of the star from the search
    # position ra_deg, dec_deg

    # The proper motion (pmRA and pmDE) filter is needed to remove some stars
    # that may be fast moving, e.g. block_id 78169 is an interesting test!
    # - There's a 13.5 mag star with high proper motion!
    # This is not so much a problem *now*, soon after GAIA catalogue was made,
    # but is more important for future proofing this code...
    # Limits of +-50mas/yr are selected in RA and Dec.
    global Catalog

    query = Catalog(
        columns=["_r", 'Source', 'RA_ICRS', 'DE_ICRS', '+Gmag', 'RPmag'],
        column_filters={
            "Gmag": (f"<={instr.faint_limit + 2:.2f}"),
            "pmRA": ("> -50 && < 50"),
            "pmDE": ("> -50 && < 50"),
        },
        # column_filters={"Gmag":(">=13.0 && <=17.0")},
        row_limit=max_stars,
    )
    results = query.query_region(
        instr.target, radius=instr.instr_fov, catalog="I/345/gaia2"
    )[0]

    # if we find no stars in the field, raise an error
    if len(results) == 0:
        raise NoStarsFoundError(
            f"No stars returned in field "
            f"'{instr.target.to_string(style='hmsdms')}' "
            f"with radius {instr.instr_fov:.2f}"
        )
    else:
        stars = []
        for row in results:
            stars.append(
                Star(
                    ra=row['RA_ICRS'] * u.deg,
                    dec=row['DE_ICRS'] * u.deg,
                    radius=row['_r'] * u.arcmin,
                    g_mag=row['Gmag'],
                    rp_mag=row['RPmag'],
                )
            )

    return stars


def find_best_stars(instr: BaseInstrument, stars: List[Star]) -> List[Star]:
    '''
    Return the best stars as defined by the instrument's best_stars function
    '''
    stars = instr.filter(stars)

    return instr.best_stars(stars)
