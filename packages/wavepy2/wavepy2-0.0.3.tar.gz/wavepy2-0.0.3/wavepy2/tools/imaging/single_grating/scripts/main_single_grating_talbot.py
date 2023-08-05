# #########################################################################
# Copyright (c) 2020, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2020. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

from wavepy2.tools.imaging.single_grating.bl.single_grating_talbot import create_single_grating_talbot_manager, \
    CALCULATE_DPC_CONTEXT_KEY, CORRECT_ZERO_DPC_CONTEXT_KEY, RECROP_DPC_CONTEXT_KEY, REMOVE_LINEAR_FIT_CONTEXT_KEY, FIT_RADIUS_DPC_CONTEXT_KEY, \
    INTEGRATION_CONTEXT_KEY, CALCULATE_THICKNESS_CONTEXT_KEY, CALCULATE_2ND_ORDER_COMPONENT_OF_THE_PHASE, REMOVE_2ND_ORDER

from wavepy2.tools.imaging.single_grating.bl.dpc_profile_analysis import DPC_PROFILE_ANALYSYS_CONTEXT_KEY

from wavepy2.util.ini.initializer import get_registered_ini_instance, register_ini_instance, IniMode
from wavepy2.util.log.logger import register_logger_single_instance, LoggerMode
from wavepy2.util.plot.qt_application import get_registered_qt_application_instance, register_qt_application_instance, QtApplicationMode
from wavepy2.util.plot.plotter import get_registered_plotter_instance, register_plotter_instance, PlotterMode

SCRIPT_LOGGER_MODE = LoggerMode.FULL
INI_MODE           = IniMode.LOCAL_FILE
INI_FILE_NAME      = ".single_grating_talbot.ini"

import sys

def arguments_single_grating_talbot(sys_argv):
    args_sgt = {}
    if len(sys_argv) > 2:
        if sys_argv[2] == "--h":
            print("\n'python -m wavepy2.tools img-sgt -l<logger mode> -p<plotter mode>\n")
            print("* Available logger modes:\n" +
                  "    0 Full (Message, Warning, Error)\n" +
                  "    1 Warning (Warning, Error)\n" +
                  "    2 Error\n" +
                  "    3 None\n\n")
            print("* Available plotter modes:\n" +
                  "    0 Full (Display, Save Images)\n" +
                  "    1 Display Only\n" +
                  "    2 Save Images Only\n" +
                  "    3 None\n")
            sys.exit(0)
        else:
            for i in range(2, len(sys_argv)):
                if   "-l" == sys_argv[i][:-1]: args_sgt["LOGGER_MODE"] = int(sys_argv[i][-1])
                elif "-p" == sys_argv[i][:-1]: args_sgt["PLOTTER_MODE"] = int(sys_argv[i][-1])

    return args_sgt

def run_single_grating_talbot(LOGGER_MODE=LoggerMode.FULL, PLOTTER_MODE=PlotterMode.FULL):
    print("Logger Mode: " + LoggerMode.get_logger_mode(LOGGER_MODE))
    print("Plotter Mode: " + PlotterMode.get_plotter_mode(PLOTTER_MODE))

    # ==========================================================================
    # %% Script initialization
    # ==========================================================================

    register_logger_single_instance(logger_mode=LOGGER_MODE)
    register_ini_instance(INI_MODE, ini_file_name=".single_grating_talbot.ini" if INI_MODE == IniMode.LOCAL_FILE else None)
    register_plotter_instance(plotter_mode=PLOTTER_MODE)
    register_qt_application_instance(QtApplicationMode.SHOW if PLOTTER_MODE in [PlotterMode.FULL, PlotterMode.DISPLAY_ONLY] else QtApplicationMode.HIDE)

    plotter = get_registered_plotter_instance()

    single_grating_talbot_manager = create_single_grating_talbot_manager()

    # ==========================================================================
    # %% Initialization parameters
    # ==========================================================================

    initialization_parameters = single_grating_talbot_manager.get_initialization_parameters(SCRIPT_LOGGER_MODE)

    # ==========================================================================
    # %% DPC Analysis
    # ==========================================================================

    dpc_result = single_grating_talbot_manager.calculate_dpc(initialization_parameters)
    plotter.show_context_window(CALCULATE_DPC_CONTEXT_KEY)

    # ==========================================================================

    recrop_dpc_result = single_grating_talbot_manager.recrop_dpc(dpc_result, initialization_parameters)
    plotter.show_context_window(RECROP_DPC_CONTEXT_KEY)

    # ==========================================================================

    correct_zero_dpc_result = single_grating_talbot_manager.correct_zero_dpc(recrop_dpc_result, initialization_parameters)
    plotter.show_context_window(CORRECT_ZERO_DPC_CONTEXT_KEY)

    # ==========================================================================

    remove_linear_fit_result = single_grating_talbot_manager.remove_linear_fit(correct_zero_dpc_result, initialization_parameters)
    plotter.show_context_window(REMOVE_LINEAR_FIT_CONTEXT_KEY)

    # ==========================================================================

    dpc_profile_analysis_result = single_grating_talbot_manager.dpc_profile_analysis(remove_linear_fit_result, initialization_parameters)
    plotter.show_context_window(DPC_PROFILE_ANALYSYS_CONTEXT_KEY)

    # ==========================================================================

    fit_radius_dpc_result = single_grating_talbot_manager.fit_radius_dpc(dpc_profile_analysis_result, initialization_parameters)
    plotter.show_context_window(FIT_RADIUS_DPC_CONTEXT_KEY)

    # ==========================================================================
    # %% Integration
    # ==========================================================================

    integration_result = single_grating_talbot_manager.do_integration(fit_radius_dpc_result, initialization_parameters)
    plotter.show_context_window(INTEGRATION_CONTEXT_KEY)

    # ==========================================================================

    integration_result = single_grating_talbot_manager.calc_thickness(integration_result, initialization_parameters)
    plotter.show_context_window(CALCULATE_THICKNESS_CONTEXT_KEY)

    # ==========================================================================

    integration_result = single_grating_talbot_manager.calc_2nd_order_component_of_the_phase(integration_result, initialization_parameters)
    plotter.show_context_window(CALCULATE_2ND_ORDER_COMPONENT_OF_THE_PHASE)

    # ==========================================================================

    integration_result = single_grating_talbot_manager.remove_2nd_order(integration_result, initialization_parameters)
    plotter.show_context_window(REMOVE_2ND_ORDER)

    # ==========================================================================
    # %% Final Operations
    # ==========================================================================

    get_registered_ini_instance().push()
    get_registered_qt_application_instance().show_application_closer()

    # ==========================================================================

    get_registered_qt_application_instance().run_qt_application()


if __name__=="__main__":
    print("\n********** Warning *************:\n\nTo run this script, type:")
    arguments_single_grating_talbot(["", "", "--h"])
