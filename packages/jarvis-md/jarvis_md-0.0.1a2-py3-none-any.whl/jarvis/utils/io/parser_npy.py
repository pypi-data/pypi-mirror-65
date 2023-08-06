import os, numpy as np

def load_npy(fname, **kwargs):
    """
    Method to load *.npy files

    """
    data = add_axes(np.load(fname))

    # --- Check for corresponding affine.npy or dims.npy file
    dims = load_affine(fname)

    return data, {'affine': np.eye(4)} 

def load_npz(fname, **kwargs):
    """
    Method to load *.npz files

    """
    o = np.load(fname)
    data = add_axes(o[o.files[0]])

    # --- Check for corresponding affine.npy or dims.npy file
    affine = load_affine(fname)

    return data, {'affine': affine} 

def load_affine(fname):
    """
    Method to load corresponding affine.npy or dims.npy file if present

    """
    affine = np.eye(4)

    # --- Check for affine
    fname_affine = '%s/affine.npy' % os.path.dirname(fname)
    if os.path.exists(fname_affine):
        affine = np.load(fname_affine)
        return affine 

    # --- Check for dims 
    fname_dims = '%s/dims.npy' % os.path.dirname(fname)
    if os.path.exists(fname_dims):
        dims = np.load(fname_dims)
        affine[np.arange(3), np.arange(3)] = dims
        return affine 

    return affine

def add_axes(data):
    """
    Method to ensure data is 4D array 

    """
    if data.ndim == 2:
        data = np.expand_dims(data, axis=0)

    if data.ndim == 3:
         data = np.expand_dims(data, axis=-1)

    return data 

def save_npy(fname, data, **kwargs):

    np.save(fname, data)

def save_npz(fname, data, **kwargs):

    np.savez_compressed(fname, data)

