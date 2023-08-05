# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
import nwae.utils.UnitTest as uthelper
import nwae.ml.config.Config as cf
from nwae.utils.ObjectPersistence import UnitTestObjectPersistence
from nwae.lang.NwaeLangUnitTest import NwaeLangUnitTest
from nwae.math.NwaeMathUnitTest import NwaeMathUnitTest
from nwae.ml.text.preprocessing.TrDataPreprocessorUnitTest import TrDataPreprocessorUnitTest
from nwae.ml.metricspace.ut.UtMetricSpaceModel import UnitTestMetricSpaceModel
import nwae.ml.ModelHelper as modelHelper


#
# We run all the available unit tests from all modules here
# PYTHONPATH=".:/usr/local/git/nwae/nwae.utils/src:/usr/local/git/nwae/mex/src" /usr/local/bin/python3.6 nwae/ut/UnitTest.py
#
class NwaeMlUnitTest:

    def __init__(self, ut_params):
        self.ut_params = ut_params
        if self.ut_params is None:
            # We only do this for convenience, so that we have access to the Class methods in UI
            self.ut_params = uthelper.UnitTestParams()
        return

    def run_unit_tests(self):
        res_final = uthelper.ResultObj(count_ok=0, count_fail=0)

        res = UnitTestObjectPersistence(ut_params=None).run_unit_test()
        res_final.update(other_res_obj=res)
        Log.critical('Object Persistence Unit Test PASSED ' + str(res.count_ok) + ', FAILED ' + str(res.count_fail))

        res = NwaeLangUnitTest(ut_params=ut_params).run_unit_tests()
        res_final.update(other_res_obj=res)
        Log.critical('Project <<nwae.lang>> Unit Test PASSED ' + str(res.count_ok) + ', FAILED ' + str(res.count_fail))

        res = NwaeMathUnitTest(ut_params=None).run_unit_tests()
        res_final.update(other_res_obj=res)
        Log.critical('Project <<nwae.math>>  Unit Test PASSED ' + str(res.count_ok) + ', FAILED ' + str(res.count_fail))

        res = TrDataPreprocessorUnitTest(ut_params=self.ut_params).run_unit_test()
        res_final.update(other_res_obj=res)
        Log.critical('TD Data Preprocessor Unit Test PASSED ' + str(res.count_ok) + ', FAILED ' + str(res.count_fail))

        res = UnitTestMetricSpaceModel(
            ut_params = self.ut_params,
            identifier_string = 'demo_ut1',
            model_name = modelHelper.ModelHelper.MODEL_NAME_HYPERSPHERE_METRICSPACE
        ).run_unit_test()
        res_final.update(other_res_obj=res)
        Log.critical('MetricSpaceModel Unit Test PASSED ' + str(res.count_ok) + ', FAILED ' + str(res.count_fail))

        Log.critical('PROJECT <<nwae.ml>> TOTAL PASS = ' + str(res_final.count_ok) + ', TOTAL FAIL = ' + str(res_final.count_fail))
        return res_final


if __name__ == '__main__':
    config = cf.Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class       = cf.Config,
        default_config_file = cf.Config.CONFIG_FILE_DEFAULT
    )

    ut_params = uthelper.UnitTestParams(
        dirpath_wordlist     = config.get_config(param=cf.Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=cf.Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=cf.Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_SYNONYMLIST),
        dirpath_model        = config.get_config(param=cf.Config.PARAM_MODEL_DIR)
    )
    Log.important('Unit Test Params: ' + str(ut_params.to_string()))

    Log.LOGLEVEL = Log.LOG_LEVEL_ERROR

    res = NwaeMlUnitTest(ut_params=ut_params).run_unit_tests()
    exit(res.count_fail)
