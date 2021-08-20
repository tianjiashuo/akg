# Copyright 2020-2021 Huawei Technologies Co., Ltd
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
# limitations under the License
from copy import deepcopy

from tests.common.base import get_rtol_atol
from tests.common.tensorio import compare_tensor
from akg.utils import kernel_exec as utils
from akg.ops.array_gpu import gather_nd
from akg.utils.result_analysis import gpu_profiling
from akg.utils.format_transform import to_tvm_nd_array
from tests.common.gen_random import random_gaussian, gen_indices_gather_nd
from tests.common.test_utils import gather_nd_np
import numpy as np


def gen_data(shape1, dtype1, shape2, dtype2):
    params = random_gaussian(shape1).astype(dtype1)
    out_dim1 = 1
    for i in range(len(shape2) - 1):
        out_dim1 = out_dim1 * shape2[i]

    indices = gen_indices_gather_nd(shape1, shape2, dtype2)
    expect = gather_nd_np(params, indices)

    return params, indices, expect

def test_ms_gather_nd(shape1, dtype1, shape2, dtype2, axis, poly_sch=False):
    # op_attrs = [axis]
    if poly_sch:
        mod = utils.op_build_test(gather_nd.gather_nd,
                                                               [shape1, shape2], [dtype1, dtype2], #op_attrs=op_attrs,
                                                               attrs={"target": "cuda"}, kernel_name="gather_nd")

    # gen data
    params, indices, expect = gen_data(shape1, dtype1, shape2, dtype2)
    output_shape = expect.shape

    if len(expect.shape) == 0:
        output_shape = (1, )
    output = np.zeros(output_shape, expect.dtype)
    output = utils.mod_launch(mod, (params, indices, output), expect = expect)

    atol, rtol = get_rtol_atol("gather_nd", dtype1)
    res = compare_tensor(output, expect, rtol=rtol, atol=atol)
    print("Test {}".format("Pass" if res else "Failed"))
    if not res:
        print("Error cuda:========================")
        print(mod.imported_modules[0].get_source())
        raise AssertionError("Test fail")

    params, indices, output, expect = to_tvm_nd_array(
        [params, indices, output, expect])
    gpu_profiling(mod, params, indices, output, expect, repeat_time=400)
