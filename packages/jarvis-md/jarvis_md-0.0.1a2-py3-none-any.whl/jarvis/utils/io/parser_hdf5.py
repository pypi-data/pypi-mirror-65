import os, shutil, h5py
import numpy as np
from .utils import extract_data
from ..general import printd

def save(fname, data, meta={}, chunks=None, compression='gzip', **kwargs):
    """
    Method to save data and affine matrix in HDF5 format

    :params

      (str)       fname : path to file
      (np.ndarray) data : a 4D Numpy array
      (dict)       meta : {'affine': ...}
      (tuple)    chunks : (z, y, x, c) shape of chunks; by default 1 x Y x X x C
      (str) compression : either 'gzip' or 'lzf' or None (no compression)

    """
    # --- Initialize
    fname, meta, kwargs = init_save(fname, data, meta, chunks=chunks, compression=compression, **kwargs)

    # --- Temporary file if fname already exists
    exists = os.path.exists(fname)
    if exists:
        fname = fname[:-5] + '_.hdf5'

    # --- Make required folder(s) 
    os.makedirs(os.path.dirname(fname), exist_ok=True)

    # --- Save file
    with h5py.File(fname, 'w') as f:

        f.create_dataset(**kwargs)

        # --- Save attributes
        for k, v in meta.items():
            f.attrs[k] = v 

    # --- Overwrite existing file 
    if exists:
        shutil.move(src=fname, dst=fname[:-6] + '.hdf5')

def init_save(fname, data, meta, **kwargs):
    """
    Method to initialize save parameters to default values if needed

    Note that to properly initialize affine matrix, it is recommended to load data first via an Array() object

    """
    # --- Assertions 
    assert type(fname) is str, 'Error fname is not str'
    assert type(data) is np.ndarray, 'Error data is not a NumPy array'
    assert data.ndim == 4, 'Error data is not a 4D array'

    if kwargs.get('compression', None) is not None:
        assert kwargs['compression'] in ['gzip', 'lzf'], 'Error specified compression type %s is not supported' % compression

    # --- Warnings
    if str(data.dtype) not in ['int16', 'uint8']:
        printd('Warning data dtype is %s' % data.dtype)

    # --- Initialize fname
    if fname[-5:] != '.hdf5':
        fname += '.hdf5'

    parse_dict = lambda d, keys : {k: d[k] for k in d if k in keys}

    # =================================================================
    # INITIALIZE META
    # =================================================================
    DEFAULTS = {
        'affine': np.eye(4, dtype='float32')}

    meta = {**DEFAULTS, **parse_dict(meta, ['affine'])}

    if type(meta['affine']) is list:
        affine = np.eye(4, dtype='float32')
        affine.ravel()[:12] = meta['affine']
        meta['affine'] = affine

    # =================================================================
    # INITIALIZE KWARGS (name, data, chunks, compression) 
    # =================================================================
    DEFAULTS = {
        'name': 'data',
        'data': data,
        'chunks': tuple([1, data.shape[1], data.shape[2], data.shape[3]])}

    kwargs = {**DEFAULTS, **parse_dict(kwargs, ['chunks', 'compression'])}

    return fname, meta, kwargs 

def load(fname, infos=None, **kwargs):
    """
    Method to load full array and meta dictionary

    :params

      (dict) infos : determines coord location and shape of loaded array

        infos['coord'] ==> 3D coord (normalized) for center of loaded array
        infos['shape'] ==> 3D tuple for shape of loaded array

        For any infos['shape'] values that are 0, the entire axes is loaded

        If infos is None, the entire volume is loaded

    """
    if not os.path.exists(fname):
        return None, {} 

    with h5py.File(fname, 'r') as f:

        # --- Extract data
        data = extract_data(f['data'], infos)

        # --- Extract meta
        meta = {'affine': f.attrs['affine']}

    return data, meta

def load_meta(fname):
    """
    Method to load meta dictionary containing:
    
      (1) shape
      (2) affine matrix

    """
    if not os.path.exists(fname):
        return {} 

    with h5py.File(fname, 'r') as f:

        meta = {
            'shape': f['data'].shape,
            'affine': f.attrs['affine']}

    return meta

# ========================================================================
# JARVIS LOAD / SAVE API 
# =========================================================================
# 
# The following wrappers conform to the Jarvis load / save APIs:
# 
#   * load(fname, **kwargs): ...
#   * save(fname, data, **kwargs): ...
# 
# Set the following entrypoint functions in setup.py to register each 
# corresponding load and save function.
# 
# ========================================================================

def load_hdf5(fname, **kwargs):
    """
    Method to load HDF5 files according to fileio.py API

    """
    return load(fname=fname, **kwargs)

def save_hdf5(fname, data, meta=None, chunks=None, compression='gzip', **kwargs):
    """
    Method to save HDF5 files according to fileio.py API

    """

    meta = meta or {}
    save(fname, data=data, meta=meta, chunks=chunks, compression=compression)
