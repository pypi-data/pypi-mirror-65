import numpy as np

from psyneulink.core.components.functions.transferfunctions import Linear, Logistic
from psyneulink.core.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.core.components.process import Process
from psyneulink.core.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.core.components.system import System
from psyneulink.core.globals.keywords import FULL_CONNECTIVITY_MATRIX, LEARNING, LEARNING_PROJECTION
from psyneulink.core.globals.preferences.basepreferenceset import REPORT_OUTPUT_PREF, VERBOSE_PREF
from psyneulink.library.components.mechanisms.processing.objective.comparatormechanism import MSE


class TestStroop:

    def test_stroop_model(self):
        process_prefs = {
            REPORT_OUTPUT_PREF: False,
            VERBOSE_PREF: False
        }

        # system_prefs = {
        #     REPORT_OUTPUT_PREF: True,
        #     VERBOSE_PREF: False
        # }

        colors = TransferMechanism(
            size=2,
            function=Linear,
            name="Colors",
        )

        words = TransferMechanism(
            default_variable=[0, 0],
            size=2,
            function=Linear,
            name="Words",
        )

        response = TransferMechanism(
            default_variable=[0, 0],
            function=Logistic,
            name="Response",
        )

        color_naming_process = Process(
            default_variable=[1, 2.5],
            pathway=[colors, FULL_CONNECTIVITY_MATRIX, response],
            learning=LEARNING_PROJECTION,
            target=[0, 1],
            name='Color Naming',
            prefs=process_prefs,
        )

        word_reading_process = Process(
            default_variable=[.5, 3],
            pathway=[words, FULL_CONNECTIVITY_MATRIX, response],
            name='Word Reading',
            learning=LEARNING_PROJECTION,
            target=[1, 0],
            prefs=process_prefs,
        )

        # s = System(
        #     processes=[color_naming_process, word_reading_process],
        #     name='Stroop Model',
        #     targets=[0, 0],
        #     prefs=system_prefs,
        # )

        # stim_dict = {
        #     colors: [
        #         [1,0],
        #         [0,1]
        #     ],
        #     words: [
        #         [0,1],
        #         [1,0]
        #     ]
        # }
        # target_dict = {
        #     response: [
        #         [1,0],
        #         [0,1]
        #     ]
        # }

        # results = s.run(
        #     num_trials=10,
        #     inputs=stim_dict,
        #     targets=target_dict,
        # )
        expected_color_results = [
            np.array([0.88079708, 0.88079708]),
            np.array([0.85997037, 0.88340023]),
            np.array([0.83312329, 0.88585176]),
            np.array([0.79839127, 0.88816536]),
            np.array([0.75384913, 0.89035312]),
            np.array([0.69835531, 0.89242571]),
            np.array([0.63303376, 0.89439259]),
            np.array([0.56245802, 0.8962622 ]),
            np.array([0.49357614, 0.89804208]),
            np.array([0.43230715, 0.89973899]),
        ]

        expected_word_results = [
            np.array([0.88079708, 0.88079708]),
            np.array([0.88340023, 0.85997037]),
            np.array([0.88585176, 0.83312329]),
            np.array([0.88816536, 0.79839127]),
            np.array([0.89035312, 0.75384913]),
            np.array([0.89242571, 0.69835531]),
            np.array([0.89439259, 0.63303376]),
            np.array([0.8962622, 0.56245802]),
            np.array([0.89804208, 0.49357614]),
            np.array([0.89973899, 0.43230715]),
        ]

        for i in range(10):
            cr = color_naming_process.execute(input=[1, 1], target=[0, 1])
            wr = word_reading_process.execute(input=[1, 1], target=[1, 0])

            np.testing.assert_allclose(cr, expected_color_results[i], atol=1e-08, err_msg='Failed on expected_color_results[{0}]'.format(i))
            np.testing.assert_allclose(wr, expected_word_results[i], atol=1e-08, err_msg='Failed on expected_word_results[{0}]'.format(i))

    def test_stroop_model_learning(self):
        process_prefs = {
            REPORT_OUTPUT_PREF: True,
            VERBOSE_PREF: False,
        }
        system_prefs = {
            REPORT_OUTPUT_PREF: True,
            VERBOSE_PREF: False,
        }

        colors = TransferMechanism(
            default_variable=[0, 0],
            function=Linear,
            name="Colors",
        )
        words = TransferMechanism(
            default_variable=[0, 0],
            function=Linear,
            name="Words",
        )
        hidden = TransferMechanism(
            default_variable=[0, 0],
            function=Logistic,
            name="Hidden",
        )
        response = TransferMechanism(
            default_variable=[0, 0],
            function=Logistic(),
            name="Response",
        )
        TransferMechanism(
            default_variable=[0, 0],
            function=Logistic,
            name="Output",
        )

        CH_Weights_matrix = np.arange(4).reshape((2, 2))
        WH_Weights_matrix = np.arange(4).reshape((2, 2))
        HO_Weights_matrix = np.arange(4).reshape((2, 2))

        CH_Weights = MappingProjection(
            name='Color-Hidden Weights',
            matrix=CH_Weights_matrix,
        )
        WH_Weights = MappingProjection(
            name='Word-Hidden Weights',
            matrix=WH_Weights_matrix,
        )
        HO_Weights = MappingProjection(
            name='Hidden-Output Weights',
            matrix=HO_Weights_matrix,
        )

        color_naming_process = Process(
            default_variable=[1, 2.5],
            pathway=[colors, CH_Weights, hidden, HO_Weights, response],
            learning=LEARNING,
            target=[2, 2],
            name='Color Naming',
            prefs=process_prefs,
        )

        word_reading_process = Process(
            default_variable=[.5, 3],
            pathway=[words, WH_Weights, hidden],
            name='Word Reading',
            learning=LEARNING,
            target=[3, 3],
            prefs=process_prefs,
        )

        s = System(
            processes=[color_naming_process, word_reading_process],
            targets=[20, 20],
            name='Stroop Model',
            prefs=system_prefs,
        )

        def show_target():
            print('\nColor Naming\n\tInput: {}\n\tTarget: {}'.format([np.ndarray.tolist(item.parameters.value.get(s)) for item in colors.input_ports], s.targets))
            print('Wording Reading:\n\tInput: {}\n\tTarget: {}\n'.format([np.ndarray.tolist(item.parameters.value.get(s)) for item in words.input_ports], s.targets))
            print('Response: \n', response.output_port.parameters.value.get(s))
            print('Hidden-Output:')
            print(HO_Weights.get_mod_matrix(s))
            print('Color-Hidden:')
            print(CH_Weights.get_mod_matrix(s))
            print('Word-Hidden:')
            print(WH_Weights.get_mod_matrix(s))

        stim_list_dict = {
            colors: [[1, 1]],
            words: [[-2, -2]]
        }

        target_list_dict = {response: [[1, 1]]}

        results = s.run(
            num_trials=2,
            inputs=stim_list_dict,
            targets=target_list_dict,
            call_after_trial=show_target,
        )

        results_list = []
        for elem in s.results:
            for nested_elem in elem:
                nested_elem = nested_elem.tolist()
                try:
                    iter(nested_elem)
                except TypeError:
                    nested_elem = [nested_elem]
                results_list.extend(nested_elem)

        objective_response = s.mechanisms[3]
        objective_hidden = s.mechanisms[7]
        from pprint import pprint
        pprint(CH_Weights.__dict__)
        print(CH_Weights._parameter_ports["matrix"].value)
        print(CH_Weights.get_mod_matrix(s))
        expected_output = [
            (colors.output_ports[0].parameters.value.get(s), np.array([1., 1.])),
            (words.output_ports[0].parameters.value.get(s), np.array([-2., -2.])),
            (hidden.output_ports[0].parameters.value.get(s), np.array([0.13227553, 0.01990677])),
            (response.output_ports[0].parameters.value.get(s), np.array([0.51044657, 0.5483048])),
            (objective_response.output_ports[0].parameters.value.get(s), np.array([0.48955343, 0.4516952])),
            (objective_response.output_ports[MSE].parameters.value.get(s), np.array(0.22184555903789838)),
            (CH_Weights.get_mod_matrix(s), np.array([
                [ 0.02512045, 1.02167245],
                [ 2.02512045, 3.02167245],
            ])),
            (WH_Weights.get_mod_matrix(s), np.array([
                [-0.05024091, 0.9566551 ],
                [ 1.94975909, 2.9566551 ],
            ])),
            (HO_Weights.get_mod_matrix(s), np.array([
                [ 0.03080958, 1.02830959],
                [ 2.00464242, 3.00426575],
            ])),
            (results, [[np.array([0.50899214, 0.54318254])], [np.array([0.51044657, 0.5483048])]]),
        ]

        for i in range(len(expected_output)):
            val, expected = expected_output[i]
            # setting absolute tolerance to be in accordance with reference_output precision
            # if you do not specify, assert_allcose will use a relative tolerance of 1e-07,
            # which WILL FAIL unless you gather higher precision values to use as reference
            np.testing.assert_allclose(val, expected, atol=1e-08, err_msg='Failed on expected_output[{0}]'.format(i))

        # KDM 10/16/18: Comparator Mechanism for Hidden is not executed by the system, because it's not associated with
        # an output mechanism. So it actually should be None instead of previously [0, 0] which was likely
        # a side effect with of conflation of different execution contexts
        assert objective_hidden.output_ports[0].parameters.value.get(s) is None
