#!/usr/bin/env python

import os
import sys
import argparse

import logging
import numpy as np


#: fits file alignment block size in bytes
ALIGN = 2880
#: NAXIS1 in original data
NAXIS1 = 30220
#: Number of frequency channels in original data
NCHAN = 384
#: Number of time samples per subint in original data
NSAMP = 500
#: Number of seconds per subint in original data
TSUBINT = 1.024


def get_header(fname):
    """
    Read header from fits file, assuming there are 2 HDUs

    :param str fname: Path to fits file
    :return: raw header (bytes), header size in bytes (int)
    """
    # read increasinly bigger parts of the file until we encounter two END cards
    # an END card is on a line of its own
    # Each line is 80 characters, so we are looking for END plus 77 spaces
    end_card = b'END' + b' ' * 77
    hdr_size_guess = 0
    while True:
        # Load raw header as bytes
        raw_header_guess = np.fromfile(fname, dtype='B', count=hdr_size_guess).tobytes()
        try:
            ind = raw_header_guess.index(end_card)
        except ValueError:
            # not found, increase guess for header size
            # step should be smaller than align value, to avoid overshooting
            hdr_size_guess += ALIGN - 1
            continue
        # repeat for the second END card, ensuring to start search after first END card
        try:
            raw_header_guess[ind + 3:].index(end_card)
        except ValueError:
            # not found, increase guess for header size again
            hdr_size_guess += ALIGN - 1
            continue
        # Second END card found, we now have the full header
        break

    # Round size up to ALIGN value so we have the full header as written to disk
    hdr_size = int(np.ceil(hdr_size_guess / float(ALIGN)) * ALIGN)
    # Read the full header
    header = np.fromfile(fname, dtype='B', count=hdr_size).tostring().decode()
    # split into lines
    header_split = '\n'.join([header[i:i + 80] for i in range(0, hdr_size, 80)])

    logging.info("Header size: {} bytes".format(hdr_size))
    logging.debug("Raw header:\n{}".format(header_split))
    return header, hdr_size


def get_data(fname, hdr_size):
    """
    Read raw data

    :param str fname: Path to fits file
    :param int hdr_size: Header size in bytes, aligned to fits block
    :return: raw data (bytes), padding (bytes), derived naxis2 (int)
    """

    # derive total data size
    raw_data_size = os.path.getsize(fname) - hdr_size
    # this is rounded up to align value, use naxis1 to get the actual number of subints (=naxis2)
    # rounding down works as long as naxis2 is larger than align block,
    # which is always the case for ARTS data
    naxis2 = int(raw_data_size / float(NAXIS1))
    # actual data size without padding
    data_size = NAXIS1 * naxis2

    # padding is the remainder to get to raw_data_size
    padding_size = raw_data_size - data_size
    # Actual padding bytes are spaces
    padding = b' ' * padding_size

    # Load the raw data
    data = np.fromfile(fname, dtype='B', count=data_size, offset=hdr_size)

    logging.info("Data size: {}  bytes with padding of {} bytes".format(data_size, padding_size))
    logging.info("NAXIS2: {}".format(naxis2))
    logging.info("Observation duration: {}s".format(naxis2 * TSUBINT))

    return data, padding, naxis2


def fix_header(header, naxis2, force=False):
    """
    Fix the header: replace NAXIS2 = 0 by correct value and replaces
    data column bits by bytes

    :param str header: full header, including padding, as single string
    :param int naxis2: new NAXIS2 value
    :param bool force: Overwrite NAXIS2 even if original value was not zero
    :return: fixed header (bytes)
    """
    # NAXIS2 fix
    # exact key we are looking for in header
    key = "NAXIS2  ="
    try:
        key_ind = header.index(key)
    except ValueError:
        logging.error("NAXIS2 key not found in header")
        sys.exit(1)
    # from the key index keep reading header until we find the associated value
    ind = key_ind + len(key)
    char = ' '
    while char == ' ':
        ind += 1
        char = header[ind]
    # NAXIS2 is zero for a broken header, check if this is indeed the case
    if char != '0':
        if force:
            logging.warning("Original NAXIS2 is not zero; forcing application of fix")
        else:
            logging.error("Original NAXIS2 is not zero, fits file should be ok already"
                          "Re-run with --force to apply the fix anyway")
            sys.exit(1)
    # ind is now the location of the zero in the header
    # extract the old header line including key and value
    old_line = header[key_ind:ind + 1]
    # find the number of padding spaces between key and value
    nspace = ind - (key_ind + len(key))
    # calculate padding for new naxis2 key
    nspace_new = nspace - len(str(naxis2)) + 1
    # construct the new line
    new_line = key + ' ' * nspace_new + str(naxis2)
    # replace in header
    header_fixed = header.replace(old_line, new_line)
    logging.debug("Old header line: {}".format(old_line))
    logging.debug("New header line: {}".format(new_line))

    # bit to bytes fix
    # assume the old value is unique enough to appear anywhere else in the header
    old_value = '{}X'.format(NSAMP * NCHAN)
    # new value has one space to make length the same as old value
    new_value = '{}B '.format(int((NCHAN * NSAMP) / 8))
    logging.debug("Replacing {} by {} in header".format(old_value, new_value))
    header_fixed = header_fixed.replace(old_value, new_value)

    return header_fixed.encode()


def fix_data(data, naxis2):
    """
    Fix the data: Swap time and frequency axis, reverse frequency ordering

    :param bytes data: raw data, without padding
    :param int naxis2: NAXIS2 value
    :return: fixed data (bytes)
    """
    # Define data columns. Could attempt to get this from the raw header, but this is always the same anyway
    dtype = np.dtype([('TSUBINT', 'f8'),
                      ('OFFS_SUB', 'f8'),
                      ('LST_SUB', 'f8'),
                      ('RA_SUB', 'f8'),
                      ('DEC_SUB', 'f8'),
                      ('GLON_SUB', 'f8'),
                      ('GLAT_SUB', 'f8'),
                      ('FD_ANG', 'f4'),
                      ('POS_ANG', 'f4'),
                      ('PAR_ANG', 'f4'),
                      ('TEL_AZ', 'f4'),
                      ('TEL_ZEN', 'f4'),
                      ('DAT_FREQ', '{}f4'.format(NCHAN)),
                      ('DAT_WTS', '{}f4'.format(NCHAN)),
                      ('DAT_OFFS', '{}f4'.format(NCHAN)),
                      ('DAT_SCL', '{}f4'.format(NCHAN)),
                      ('DATA', '{}B'.format(int((NCHAN * NSAMP) / 8)))])
    # parse the raw data
    subintdata = np.frombuffer(data, dtype=dtype)
    # sanity check: number of rows should be NAXIS2
    if len(subintdata) != naxis2:
        logging.error("Unexpected mismatch: NAXIS2 ({}) and number of subints ({}) should be equal".format(
                      naxis2, len(subintdata)))
        sys.exit(1)

    # flip the frequency ordering in columns that have a value of each frequency
    for key in ('DAT_FREQ', 'DAT_SCL', 'DAT_OFFS', 'DAT_WTS'):
        subintdata[key] = subintdata[key][:, ::-1]

    # unpack the data, FITS uses big-endian
    data_unpacked = np.unpackbits(subintdata['DATA'], bitorder='big')
    # transpose to time-frequency order, original axes are (subint, chan, time)
    # then flip the frequency axis
    data_unpacked = np.swapaxes(data_unpacked.reshape((naxis2, NCHAN, NSAMP)), 1, 2)[:, :, ::-1]
    # pack into bytes. This flattens the array, restore the subint axis
    data_packed = np.packbits(data_unpacked, bitorder='big').reshape((naxis2, -1))
    # replace data column of subintdata
    subintdata['DATA'] = data_packed
    # return as byte array
    return subintdata.tobytes()


def write_file(fname, *args):
    """
    Write output file

    :param fname: path to output file
    :param *args: byte array to write to file, usually header, data, and padding
    """
    try:
        with open(fname, 'wb') as f:
            for arg in args:
                f.write(arg)
    except Exception as e:
        logging.error("Failed to write output file {}: {}".format(fname, e))
        sys.exit(1)
    logging.info("Wrote output to {}".format(fname))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--output', help="Output file "
                                         "(Default: input.fits -> input_fixed.fits)")
    parser.add_argument('--force', action='store_true', help="Apply fix even if FITS file seems good")
    parser.add_argument('--verbose', '-v', action='store_true', help="Increase verbosity")
    parser.add_argument('file', help="Path to input FITS file")

    # print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # set log verbosity
    if args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging_level, stream=sys.stderr)

    # set output file name
    if args.output is None:
        args.output = args.file.replace('.fits', '_fixed.fits')

    # Verify fits file exists
    if not os.path.isfile(args.file):
        logging.error("File does not exist: {}".format(args.file))
        sys.exit(1)

    logging.info("Reading file {}".format(args.file))
    # read the header
    header, hdr_size = get_header(args.file)
    # read the data
    raw_data, padding, naxis2 = get_data(args.file, hdr_size)
    # fix the header
    header_fixed = fix_header(header, naxis2, args.force)
    # fix the data
    data_fixed = fix_data(raw_data, naxis2)
    # write the output file
    write_file(args.output, header_fixed, data_fixed, padding)
