import pkg_resources
import os, numpy as np
from ..general import printd
from . import parser_hdf5, parser_json, parser_npy

def parse_ext(fname):
    """
    Method to parse file extension

    """
    file_type = 'unknown'

    # --- (1) If fname is a path string
    if type(fname) is str:

        file_type = fname.split('.')[-1]

        if file_type[-1] == '/':
            file_type = 'dcm'

    # --- (2) If fname is a list of DICOM files 
    elif type(fname) is list:
        file_type = 'dcm'

    return file_type

def load(fname, json_safe=False, **kwargs):
    """
    Method to load a single file and return in NHWC format.

    :params

      (str) fname: path to file

    :return

      (np.array) data: data in NHWC format
      (JSON obj) meta: metadata object (varies by file format)

    """
    verbose = kwargs.get('verbose', True)

    # --- Check if file exists
    if type(fname) is str:
        if not os.path.exists(fname):
            printd('ERROR file does not exist: %s' % fname, verbose=verbose)
            return None, None

    # --- Check file ext
    file_type = parse_ext(fname)

    if file_type not in load_funcs:
        printd('ERROR file format not recognized: %s' % file_type, verbose=verbose)
        return None, None

    # --- Load
    data, meta = load_funcs[file_type](fname, **kwargs)
    meta = {**{'header': None, 'affine': None, 'unique': None}, **meta}

    # --- Convert np.ndarrays to list if needed
    if json_safe:
        convert_meta_to_json_safe(meta)

    return data, meta

def convert_meta_to_json_safe(meta):

    if 'affine' in meta:
        meta['affine'] = meta['affine'].ravel()[:12].tolist()

    for k, v in meta.items():
        if type(v) is np.ndarray:
            meta[k] = v.tolist()

def save(fname, data, **kwargs):
    """
    Method to save a single file in format implied by file extension 

    :params

      (str) fname: path to file

    """
    # --- Check file ext
    file_type = parse_ext(fname)

    if file_type not in save_funcs:
        printd('ERROR file format not recognized: %s' % file_type)

    # --- Save 
    save_funcs[file_type](fname, data, **kwargs)

# ========================================================================
# JARVIS LOAD / SAVE API 
# =========================================================================
# 
# The following Python dicts are used to register file exts
# with implemented load / save functions:
# 
# =========================================================================

load_funcs = {
    'npy': parser_npy.load_npy,
    'npz': parser_npy.load_npz,
    'hdf5': parser_hdf5.load_hdf5,
    'json': parser_json.load_json}

save_funcs = {
    'npy': parser_npy.save_npy,
    'npz': parser_npy.save_npz,
    'hdf5': parser_hdf5.save_hdf5}

for entry_point in pkg_resources.iter_entry_points('load_funcs'):
    load_funcs[entry_point.name] = entry_point.load()

for entry_point in pkg_resources.iter_entry_points('save_funcs'):
    save_funcs[entry_point.name] = entry_point.load()
