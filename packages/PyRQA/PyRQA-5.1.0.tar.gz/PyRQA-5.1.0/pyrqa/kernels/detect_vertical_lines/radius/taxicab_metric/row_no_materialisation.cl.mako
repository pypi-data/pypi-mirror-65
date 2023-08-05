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

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void detect_vertical_lines_fixed_radius(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const ${fp_type} e,
    __global uint* recurrence_points,
    __global uint* vertical_frequency_distribution,
    __global uint* vertical_carryover,
    __global uint* white_vertical_frequency_distribution,
    __global uint* white_vertical_carryover
)
{
    uint global_id_x = get_global_id(0);

    if (global_id_x < dim_x)
    {
        ${fp_type} sum;

        uint points = recurrence_points[global_id_x];
        uint vertical = vertical_carryover[global_id_x];
        uint white_vertical = white_vertical_carryover[global_id_x];

        #pragma unroll loop_unroll
        for (uint global_id_y = 0; global_id_y < dim_y; ++global_id_y)
        {
            sum = 0.0f;
            for (uint i = 0; i < m; ++i)
            {
                sum += fabs(vectors_x[(global_id_x * m) + i] - vectors_y[(global_id_y * m) + i]);
            }

            if (sum < e)
            {
                points++;
                vertical++;

                if (white_vertical > 0)
                {
                    atomic_inc(&white_vertical_frequency_distribution[white_vertical - 1]);
                }

                white_vertical = 0;
            }
            else
            {
                white_vertical++;

                if (vertical > 0)
                {
                    atomic_inc(&vertical_frequency_distribution[vertical - 1]);
                }

                vertical = 0;
            }
        }

        recurrence_points[global_id_x] = points;
        vertical_carryover[global_id_x] = vertical;
        white_vertical_carryover[global_id_x] = white_vertical;
    }
}

__kernel void detect_vertical_lines_radius_corridor(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const ${fp_type} e_in,
    const ${fp_type} e_out,
    __global uint* recurrence_points,
    __global uint* vertical_frequency_distribution,
    __global uint* vertical_carryover,
    __global uint* white_vertical_frequency_distribution,
    __global uint* white_vertical_carryover
)
{
    uint global_id_x = get_global_id(0);

    if (global_id_x < dim_x)
    {
        ${fp_type} sum;

        uint points = recurrence_points[global_id_x];
        uint vertical = vertical_carryover[global_id_x];
        uint white_vertical = white_vertical_carryover[global_id_x];

        #pragma unroll loop_unroll
        for (uint global_id_y = 0; global_id_y < dim_y; ++global_id_y)
        {
            sum = 0.0f;
            for (uint i = 0; i < m; ++i)
            {
                sum += fabs(vectors_x[(global_id_x * m) + i] - vectors_y[(global_id_y * m) + i]);
            }

            if (e_in < sum && sum < e_out)
            {
                points++;
                vertical++;

                if (white_vertical > 0)
                {
                    atomic_inc(&white_vertical_frequency_distribution[white_vertical - 1]);
                }

                white_vertical = 0;
            }
            else
            {
                white_vertical++;

                if (vertical > 0)
                {
                    atomic_inc(&vertical_frequency_distribution[vertical - 1]);
                }

                vertical = 0;
            }
        }

        recurrence_points[global_id_x] = points;
        vertical_carryover[global_id_x] = vertical;
        white_vertical_carryover[global_id_x] = white_vertical;
    }
}
