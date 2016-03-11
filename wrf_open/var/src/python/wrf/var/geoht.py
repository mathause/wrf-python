from wrf.var.constants import Constants
from wrf.var.destag import destagger
from wrf.var.decorators import convert_units
from wrf.var.util import extract_vars

__all__ = ["get_geopt", "get_height"]

def _get_geoht(wrfnc, timeidx, height=True, msl=True):
    """Return the geopotential in units of m2 s-2 if height is False,
    otherwise return the geopotential height in meters.  If height is True,
    then if msl is True the result will be in MSL, otherwise AGL (the terrain
    height is subtracted).
    
    """
    
    try:
        ph_vars = extract_vars(wrfnc, timeidx, varnames=("PH", "PHB", "HGT"))
    except KeyError:
        try:
            ght_vars = extract_vars(wrfnc, timeidx, varnames=("GHT", "HGT_U"))
        except KeyError:
            raise RuntimeError("Cannot calculate height with variables in "
                               "NetCDF file")
        else:
            geopt_unstag = ght_vars["GHT"] * Constants.G
            hgt = destagger(ght_vars["HGT_U"], -1)
    else:
        ph = ph_vars["PH"]
        phb = ph_vars["PHB"]
        hgt = ph_vars["HGT"]
        geopt = ph + phb
        geopt_unstag = destagger(geopt, -3)
    
    if height:
        if msl:
            return geopt_unstag / Constants.G
        else:
            # Due to broadcasting with multifile/multitime, the 2D terrain
            # array needs to be reshaped to a 3D array so the right dims
            # line up
            new_dims = list(hgt.shape)
            new_dims.insert(-2,1)
            hgt = hgt.reshape(new_dims)
            
            return (geopt_unstag / Constants.G) - hgt
    else:
        return geopt_unstag

def get_geopt(wrfnc, timeidx=0):
    return _get_geoht(wrfnc, timeidx, False)

@convert_units("height", "m")
def get_height(wrfnc, timeidx=0, msl=True, units="m"):
    z = _get_geoht(wrfnc, timeidx, True, msl)
    return z

