/*
Author: Tobias Rawald
Copyright: Copyright 2015-2020 The PyRQA project
Credits: Tobias Rawald, Mike Sips
License: Apache-2.0
Maintainer: Tobias Rawald
Email: pyrqa@gmx.net
Status: Development
*/

#ifdef cl_khr_fp16
    #pragma OPENCL EXTENSION cl_khr_fp16 : enable
#endif

#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#endif

__kernel void create_matrix_fixed_radius(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const ${fp_type} e,
    const uint size,
    __global uint* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} diff;
        ${fp_type} sum = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            diff = vectors_x[(global_id_x * m) + i] - vectors_y[(global_id_y * m) + i];
            sum += diff * diff;
        }

        if (sum < e*e)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}

__kernel void create_matrix_radius_corridor(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const ${fp_type} e_in,
    const ${fp_type} e_out,
    const uint size,
    __global uint* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} diff;
        ${fp_type} sum = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            diff = vectors_x[(global_id_x * m) + i] - vectors_y[(global_id_y * m) + i];
            sum += diff * diff;
        }

        if (e_in*e_in < sum && sum < e_out*e_out)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}
