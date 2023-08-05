/*
Author: Tobias Rawald
Copyright: Copyright 2015-2020 The PyRQA project
Credits: Tobias Rawald, Mike Sips
License: Apache-2.0
Maintainer: Tobias Rawald
Email: pyrqa@gmx.net
Status: Development
*/

__kernel void clear_buffer_uint8(
    __global uchar* buffer,
    const uchar value
)
{
    buffer[get_global_id(0)] = value;
}

__kernel void clear_buffer_uint32(
    __global uint* buffer,
    const uint value
)
{
    buffer[get_global_id(0)] = value;
}
