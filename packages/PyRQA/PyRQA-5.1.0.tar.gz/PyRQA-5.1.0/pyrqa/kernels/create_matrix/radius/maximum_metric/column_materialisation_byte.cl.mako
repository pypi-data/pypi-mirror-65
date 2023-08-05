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
    __global const ${fp_type}* time_series_x,
    __global const ${fp_type}* time_series_y,
    const uint dim_x,
    const uint m,
    const uint t_x,
    const uint t_y,
    const ${fp_type} e,
    __global uchar* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} max = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            max = fmax(fabs(time_series_x[global_id_x + (i * t_x)] - time_series_y[global_id_y + (i * t_y)]), max);
        }

        if (max < e)
        {
            matrix[global_id_y * dim_x + global_id_x] = 1;
        }
        else
        {
            matrix[global_id_y * dim_x + global_id_x] = 0;
        }
    }
}

__kernel void create_matrix_radius_corridor(
    __global const ${fp_type}* time_series_x,
    __global const ${fp_type}* time_series_y,
    const uint dim_x,
    const uint m,
    const uint t_x,
    const uint t_y,
    const ${fp_type} e_in,
    const ${fp_type} e_out,
    __global uchar* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} max = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            max = fmax(fabs(time_series_x[global_id_x + (i * t_x)] - time_series_y[global_id_y + (i * t_y)]), max);
        }

        if (e_in < max && max < e_out)
        {
            matrix[global_id_y * dim_x + global_id_x] = 1;
        }
        else
        {
            matrix[global_id_y * dim_x + global_id_x] = 0;
        }
    }
}
