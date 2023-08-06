# ARTS tools
[![Build Status](https://travis-ci.com/loostrum/arts_tools.svg?branch=master)](https://travis-ci.com/loostrum/arts_tools)  
Processing scripts for Apertif Radio Transient System data

## Requirements
* Python >= 3.6
* Numpy >= 1.17

## Installation
`pip install arts_tools`

## Fixing archival FITS files
FITS files retrieved from the Apertif Long-Term Archive (ALTA) from before 2020/04/08 can be made readable using `arts_fix_fits`. Four fixes are applied:
1. The NAXIS2 value in the header is changed from zero to the correct value
2. The data size is expressed in bytes instead of bits
2. The frequency and time axes of the data are swapped
3. The frequency order of the data and weights, scales, offsets, and frequencies columns is flipped

By default, the script appends `_fixed` to the filename. Run `arts_fix_fits -h` for more options.
