# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
################################################

Testcase_PrepareCondition:

Testcase_TestSteps:

Testcase_ExpectedResult:

"""
import os
import pytest
from tests.common.base import TestBase
from tests.common.test_run.less_run import less_run


############################################################
# TestCase= class: put to tests/*/
############################################################
class TestCase(TestBase):
    def setup(self):
        case_name = "test_auto_less_001"
        case_path = os.getcwd()

        # params init
        self.params_init(case_name, case_path)

        self.caseresult = True
        self._log.info("============= {0} Setup case============".format(self.casename))
        self.testarg = [
            # caseflag,testfuncname,testRunArgs, dimArgs
            ("001_less", less_run, (((128,), (128,)), "float16", "less")),
            ("002_less", less_run, (((128, 128), (1, 128)), "float16", "less")),
            ("003_less", less_run, (((4,), (4,)), "float16", "less")),
            ("004_less", less_run, (((128,), (128,)), "float32", "less")),
            ("005_less", less_run, (((128, 128), (128, 128)), "float32", "less")),
            ("006_less", less_run, (((4,), (4,)), "float32", "less")),
            ("007_less", less_run, (((128,), (128,)), "int32", "less")),
            ("008_less", less_run, (((128, 128), (128, 128)), "int32", "less")),
            ("009_less", less_run, (((4,), (4,)), "int32", "less")),
        ]
        self.testarg_rpc_cloud = [
            # caseflag,testfuncname,testRunArgs, dimArgs
            ("001_less", less_run, (((128,), (128,)), "float16", "less")),
            ("002_less", less_run, (((128, 128), (128, 128)), "float16", "less")),
            ("003_less", less_run, (((4,), (4,)), "float16", "less")),
            ("004_less", less_run, (((128,), (128,)), "float32", "less")),
            ("005_less", less_run, (((128, 128), (128, 128)), "float32", "less")),
            ("006_less", less_run, (((4,), (4,)), "float32", "less")),
            ("007_less", less_run, (((128,), (128,)), "int32", "less")),
            ("008_less", less_run, (((128, 128), (128, 128)), "int32", "less")),
            ("009_less", less_run, (((4,), (4,)), "int32", "less")),
        ]
        return

    @pytest.mark.level0
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.env_onecard
    def test_run(self):
        self.common_run(self.testarg)

    def test_run_rpc_cloud(self):
        self.common_run(self.testarg_rpc_cloud)

    def teardown(self):
        self._log.info("============= {0} Teardown============".format(self.casename))
        return
