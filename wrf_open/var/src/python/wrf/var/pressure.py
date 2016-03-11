
from wrf.var.decorators import convert_units
from wrf.var.util import extract_vars

__all__ = ["get_pressure", "get_pressure_hpa"]

@convert_units("pressure", "pa")
def get_pressure(wrfnc, timeidx=0, units="pa"):

    try:
        p_vars = extract_vars(wrfnc, timeidx, varnames=("P", "PB"))
    except KeyError:
        try:
            pres_vars = extract_vars(wrfnc, timeidx, varnames="PRES")
        except:
            raise RuntimeError("pressure variable not found in NetCDF file")
        else:
            pres = pres_vars["PRES"]
    else:
        p = p_vars["P"]
        pb = p_vars["PB"]
        pres = p + pb
    
    return pres

def get_pressure_hpa(wrfnc, timeidx=0, units="hpa"):
    return get_pressure(wrfnc, timeidx, units=units)


    
    