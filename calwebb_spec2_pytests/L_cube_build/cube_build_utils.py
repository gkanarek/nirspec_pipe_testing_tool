"""
This file contains the functions which will be used to test the cube build step
of the JWST Calibration Pipeline.

"""


### VERIFICATION FUNCTIONS

def s_ifucub_exists(output_hdul):
    """
    This function checks that the keyword S_IFUCUB was added.
    Args:
        outout_hdul: the HDU list of the header keywords

    Returns:
        result: boolean, true if the keyword was indeed added
    """
    result = "S_IFUCUB" in output_hdul
    return result



