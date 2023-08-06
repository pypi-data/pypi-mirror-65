import logging

import numpy as np

from psyneulink.core.components.functions.transferfunctions import Logistic
from psyneulink.core.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.core.components.process import Process
from psyneulink.core.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.core.components.system import System
from psyneulink.core.globals.keywords import SOFT_CLAMP
from psyneulink.core.globals.preferences.basepreferenceset import REPORT_OUTPUT_PREF, VERBOSE_PREF


logger = logging.getLogger(__name__)


class TestNoLearning:

    def test_multilayer(self):
        Input_Layer = TransferMechanism(
            name='Input Layer',
            function=Logistic,
            default_variable=np.zeros((2,)),
        )

        Hidden_Layer_1 = TransferMechanism(
            name='Hidden Layer_1',
            function=Logistic(),
            default_variable=np.zeros((5,)),
        )

        Hidden_Layer_2 = TransferMechanism(
            name='Hidden Layer_2',
            function=Logistic(),
            default_variable=[0, 0, 0, 0],
        )

        Output_Layer = TransferMechanism(
            name='Output Layer',
            function=Logistic,
            default_variable=[0, 0, 0],
        )

        Input_Weights_matrix = (np.arange(2 * 5).reshape((2, 5)) + 1) / (2 * 5)

        # TEST PROCESS.LEARNING WITH:
        # CREATION OF FREE STANDING PROJECTIONS THAT HAVE NO LEARNING (Input_Weights, Middle_Weights and Output_Weights)
        # INLINE CREATION OF PROJECTIONS (Input_Weights, Middle_Weights and Output_Weights)
        # NO EXPLICIT CREATION OF PROJECTIONS (Input_Weights, Middle_Weights and Output_Weights)

        # This projection will be used by the process below by referencing it in the process' pathway;
        #    note: sender and receiver args don't need to be specified
        Input_Weights = MappingProjection(
            name='Input Weights',
            matrix=Input_Weights_matrix,
        )

        p = Process(
            default_variable=[0, 0],
            pathway=[
                Input_Layer,
                # The following reference to Input_Weights is needed to use it in the pathway
                #    since it's sender and receiver args are not specified in its declaration above
                Input_Weights,
                Hidden_Layer_1,
                # No projection specification is needed here since the sender arg for Middle_Weights
                #    is Hidden_Layer_1 and its receiver arg is Hidden_Layer_2
                # Middle_Weights,
                Hidden_Layer_2,
                # Output_Weights does not need to be listed for the same reason as Middle_Weights
                # If Middle_Weights and/or Output_Weights is not declared above, then the process
                #    will assign a default for missing projection
                # Output_Weights,
                Output_Layer
            ],
            clamp_input=SOFT_CLAMP,
            target=[0, 0, 1],
            prefs={
                VERBOSE_PREF: False,
                REPORT_OUTPUT_PREF: True
            }
        )

        s = System(processes=[p])

        s.reportOutputPref = True

        stim_list = {Input_Layer: [[-1, 30]]}

        s.run(
            num_trials=10,
            inputs=stim_list,
        )

        expected_Output_Layer_output = [np.array([0.97988347, 0.97988347, 0.97988347])]

        np.testing.assert_allclose(expected_Output_Layer_output, Output_Layer.get_output_values(s))
