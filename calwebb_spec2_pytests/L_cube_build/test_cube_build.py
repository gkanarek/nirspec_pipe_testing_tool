
"""
py.test module for unit testing the cube_build step.
"""

import pytest
import os
import time

from jwst.cube_build.cube_build_step import CubeBuildStep
from .. import core_utils
from . import cube_build_utils


# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

# Default names of pipeline input and output files
@pytest.fixture(scope="module")
def set_inandout_filenames(request, config):
    step = "cube_build"
    step_info = core_utils.set_inandout_filenames(step, config)
    step_input_filename, step_output_filename, in_file_suffix, out_file_suffix, True_steps_suffix_map = step_info
    return step, step_input_filename, step_output_filename, in_file_suffix, out_file_suffix, True_steps_suffix_map


# fixture to read the output file header
@pytest.fixture(scope="module")
def output_hdul(set_inandout_filenames, config):
    set_inandout_filenames_info = core_utils.read_info4outputhdul(config, set_inandout_filenames)
    step, txt_name, step_input_file, step_output_file, run_calwebb_spec2, outstep_file_suffix = set_inandout_filenames_info
    skip_runing_pipe_step = config.getboolean("tests_only", "_".join((step, "tests")))
    # Only run step if data is IFU
    inhdu = core_utils.read_hdrfits(step_input_file, info=False, show_hdr=False)
    end_time = '0.0'
    if core_utils.check_IFU_true(inhdu):
        stp = CubeBuildStep()
        # if run_calwebb_spec2 is True calwebb_spec2 will be called, else individual steps will be ran
        step_completed = False
        if not run_calwebb_spec2:
            if config.getboolean("steps", step):
                print ("*** Step "+step+" set to True")
                if os.path.isfile(step_input_file):
                    if not skip_runing_pipe_step:
                        # start the timer to compute the step running time
                        start_time = time.time()
                        result = stp.call(step_input_file)
                        result.save(step_output_file)
                        # end the timer to compute the step running time
                        end_time = repr(time.time() - start_time)   # this is in seconds
                        print("Step "+step+" took "+end_time+" seconds to finish")
                    step_completed = True
                    core_utils.add_completed_steps(txt_name, step, outstep_file_suffix, step_completed, end_time)
                    hdul = core_utils.read_hdrfits(step_output_file, info=False, show_hdr=False)
                    return hdul
                else:
                    core_utils.add_completed_steps(txt_name, step, outstep_file_suffix, step_completed, end_time)
                    pytest.skip("Skipping "+step+" because the input file does not exist.")
            else:
                core_utils.add_completed_steps(txt_name, step, outstep_file_suffix, step_completed, end_time)
                pytest.skip("Skipping "+step+". Step set to False in configuration file.")
    else:
        pytest.skip("Skipping "+step+" because data is not IFU.")



# Unit tests

def test_s_ifucub_exists(output_hdul):
    assert cube_build_utils.s_ifucub_exists(output_hdul), "The keyword S_IFUCUB was not added to the header --> IFU cube_build step was not completed."

