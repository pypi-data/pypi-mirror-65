import numpy as np

def extract_data(data, infos=None):
    """
    Method to extract data

      (1) Extract full data volume (if infos is None)
      (2) Extract data centered at point with provided shape

    """
    infos = check_infos(infos)

    if infos is None:
        return data[:]

    # --- Create shapes / points 
    dshape = np.array(data.shape[:3])
    points = np.array(infos['point']) * (dshape - 1) 
    points = np.round(points)

    # --- Create slice bounds 
    shapes = np.array([i if i > 0 else d for i, d in zip(infos['shape'], dshape)])
    slices = points - np.floor(shapes / 2) 
    slices = np.stack((slices, slices + shapes)).T

    # --- Create padding values
    padval = np.stack((0 - slices[:, 0], slices[:, 1] - dshape)).T
    padval = padval.clip(min=0).astype('int')
    slices[:, 0] += padval[:, 0]
    slices[:, 1] -= padval[:, 1]

    # --- Create slices
    slices = [tuple(s.astype('int')) if i > 0 else (0, d) for s, i, d in zip(slices, shapes, dshape)] 
    slices = [slice(s[0], s[1]) for s in slices]

    data = data[slices[0], slices[1], slices[2]]

    # --- Pad array if needed
    if padval.any():
        pad_width = [(b, a) for b, a in zip(padval[:, 0], padval[:, 1])] + [(0, 0)]
        data = np.pad(data, pad_width=pad_width, mode='constant', constant_values=np.min(data))

    return data

def check_infos(infos):

    if infos is not None:

        assert type(infos) is dict

        DEFAULTS = {
            'point': [0.5, 0.5, 0.5],
            'shape': [0, 0, 0]}

        infos = {**DEFAULTS, **infos}

        assert len(infos['point']) == 3
        assert len(infos['shape']) == 3

    return infos
