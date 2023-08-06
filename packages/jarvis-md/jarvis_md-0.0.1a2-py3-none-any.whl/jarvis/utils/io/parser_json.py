import json, numpy as np

def load_json(fname, index_column=False, **kwargs):
    """
    Method to load JSON (meta-only) files

    """
    unique = json.load(open(fname, 'r'))

    # --- Attempt to load data (stored in group-label pair)
    data = None
    if 'arrays' in unique:
        d = unique['arrays']

        # --- Infer group
        if 'group_' in d:
            data = next(iter(d['group_'].values()))
            data = np.array(data)

        else:
            DEFAULTS = ['group', 'label', 'dtype', 'fname', 'stats', 'xtags']
            groups = [k for k in d if k not in DEFAULTS and k[:5] != '_hash']
            if len(groups) > 0:
                data = next(iter(d[sorted(groups)[0]].values()))
                data = np.array(data)

    # --- Format data
    if data is not None:

        if not index_column:
            data = data[:, :-1]

        if data.ndim == 2:
            data = np.expand_dims(data, 0)

        if data.ndim == 3:
            data = np.expand_dims(data, -1)

    return data, {'unique': unique} 
