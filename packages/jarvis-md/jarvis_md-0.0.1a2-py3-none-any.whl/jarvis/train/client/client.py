import os, glob, yaml
import numpy as np, pandas as pd
from ...utils import io
from ...utils.db import DB
from ...utils.general import *
from ...utils.general import tools as jtools
from ...utils.display import interleave

class Client():

    def __init__(self, client=None, configs=None, pattern='client*', load=None, *args, **kwargs):
        """
        Method to initialize client

        """
        # --- Serialization attributes
        self.ATTRS = ['_id', '_db', 'current', 'batch', 'specs']

        # --- Initialize existing settings from *.yml
        self.load_yml(client, configs, pattern)

        # --- Initialize db
        self.load_db()

        # --- Initialize batch composition 
        self.prepare_batch()

        # --- Initialize normalization functions
        self.init_normalization()

        # --- Initialize custom functions
        self.load_func = load or io.load
        self.daug_func = kwargs.get('augment', None)
        self.prep_func = kwargs.get('preprocess', None)

        # --- Initialize in-memory
        if self.specs['in_memory']:
            self.load_data_in_memory()

    def load_yml(self, client, configs, pattern):
        """
        Method to load metadata from YML

        """
        DEFAULTS = {
            '_id': {'project': None, 'version': None},
            '_db': None,
            'data_in_memory': {},
            'indices': {'train': {}, 'valid': {}},
            'current': {'train': {}, 'valid': {}},
            'batch': {'fold': -1, 'size': None, 'sampling': None, 'training': {'train': 0.8, 'valid': 0.2}},
            'specs': {'xs': {}, 'ys': {}, 'load_kwargs': {}, 'in_memory': False, 'tiles': [False] * 4}}

        # --- Attempt to find default client
        if client is None:
            project_id, version_id, paths, files = jtools.autodetect(pattern=pattern)
            client = '{}{}'.format(paths['code'], files['yml']) if files['yml'] is not None else './client.yml'

        configs = configs or {}
        if os.path.exists(client):
            with open(client, 'r') as y:
                configs = {**yaml.load(y, Loader=yaml.FullLoader), **configs}

        # --- Initialize default values
        for key, d in DEFAULTS.items():
            configs[key] = {**DEFAULTS[key], **configs.get(key, {})} if type(d) is dict else \
                configs.get(key, None) or DEFAULTS[key]

        # --- Set attributes
        for attr, config in configs.items():
            setattr(self, attr, config)

        # --- Set (init) specs
        self.set_specs()

    def load_db(self, *args, **kwargs): 

        # --- Find full path 
        full = self._db
        if not os.path.exists(full or ''):
            if self._id['project'] is not None:
                paths = jtools.get_paths(self._id['project'], self._id['version']) 
                full = '{}{}'.format(paths['code'], full)

        # --- Load
        self.db = DB(*(*args, *(full,)), **kwargs)

    def to_dict(self):
        """
        Method to create dictionary of metadata

        """
        return {attr: getattr(self, attr) for attr in self.ATTRS}

    def to_yml(self, fname='./client.yml', **kwargs):
        """
        Method to serialize metadata to YML 

        """
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, 'w') as y:
            yaml.dump(self.to_dict(), y, sort_keys=False, **kwargs)

    def check_data_is_loaded(func):
        """
        Method (decorator) to ensure the self.data / self.meta is loaded

        """
        def wrapper(self, *args, **kwargs):

            if self.db.fnames.size == 0:
                self.db.load_csv()

            return func(self, *args, **kwargs)

        return wrapper

    @check_data_is_loaded
    def load_data_in_memory(self, MAX_SIZE=32):
        """
        Method to load all required fnames into memory

        """
        # --- Find exams used in current training 
        mask = np.zeros(self.db.fnames.shape[0], dtype='bool') 
        for key, rate in self.batch['sampling'].items():
            if rate > 0:
                mask = mask | self.db.header[key].to_numpy()

        # --- Find keys to load
        to_load = self.fnames_to_load()

        # --- TODO: Check if dataset exceeds MAX_SIZE

        # --- Load exams into self.data_in_memory
        for sid, fnames, header in self.db.cursor(mask=mask, drop_duplicates=True, subset=to_load):
            for key in to_load:
                if fnames[key] not in self.data_in_memory:
                    load_kwargs = self.get_load_kwargs(full_res=True) 
                    self.data_in_memory[fnames[key]] = self.load_func(fnames[key], **load_kwargs)
                    if type(self.data_in_memory[fnames[key]]) is tuple:
                        self.data_in_memory[fnames[key]] = self.data_in_memory[fnames[key]][0]

        # --- Change default load function
        self.load_func = self.find_data_in_memory

    def fnames_to_load(self):
        """
        Method to return list of fnames column entries to load

        """
        to_load = []
        to_load += [v['loads'] for v in self.specs['xs'].values() if v['loads'] in self.db.fnames]
        to_load += [v['loads'] for v in self.specs['ys'].values() if v['loads'] in self.db.fnames]

        return to_load

    def find_data_in_memory(self, fname, infos=None, **kwargs):
        """
        Method to retrieve loaded data 

        """
        data = self.data_in_memory.get(fname, None)

        return io.extract_data(data, infos)
        
    @check_data_is_loaded
    def prepare_batch(self, fold=None, sampling_rates=None, training_rates={'train': 0.8, 'valid': 0.2}):
        """
        Method to prepare composition of data batches

        :params

          (int)  fold           : fold to use as validation 
          (dict) sampling_rates : rate to load each stratified cohort
          (dict) training_rates : rate to load from train / valid splits

        """
        # --- Set rates
        self.set_training_rates(training_rates)
        self.set_sampling_rates(sampling_rates)

        # --- Set default fold
        fold = fold or self.batch['fold']

        for split in ['train', 'valid']:

            # --- Determine mask corresponding to current split 
            if fold == -1:
                mask = np.ones(self.db.header.shape[0], dtype='bool')
            elif split == 'train': 
                mask = self.db.header['valid'] != fold
                mask = mask.to_numpy()
            elif split == 'valid':
                mask = self.db.header['valid'] == fold
                mask = mask.to_numpy()

            # --- Find indices for current cohort / split 
            for key in self.batch['sampling']:
                self.indices[split][key] = np.nonzero(np.array(self.db.header[key]) & mask)[0]

            for cohort in self.indices[split]:

                # --- Randomize indices for next epoch
                if cohort not in self.current[split]:
                    self.current[split][cohort] = {'epoch': -1, 'count': 0}
                    self.prepare_next_epoch(split=split, cohort=cohort)

                # --- Reinitialize old index
                else:
                    self.shuffle_indices(split, cohort)
    
    def set_training_rates(self, rates={'train': 0.8, 'valid': 0.2}):

        assert 'train' in rates
        assert 'valid' in rates

        self.batch['training'] = rates

    def set_sampling_rates(self, rates=None):

        rates = rates or self.batch['sampling']

        # --- Default, all cases without stratification
        if rates is None:
            self.db.header['all'] = True
            rates = {'all': 1.0}

        if 'all' in rates and 'all' not in self.db.header:
            self.db.header['all'] = True

        assert sum(list(rates.values())) == 1

        keys = sorted(rates.keys())
        vals = [rates[k] for k in keys]
        vals = [sum(vals[:n]) for n in range(len(vals) + 1)]

        lower = np.array(vals[:-1])
        upper = np.array(vals[1:])

        self.batch['sampling'] = rates

        self.sampling_rates = {
            'cohorts': keys,
            'lower': np.array(lower),
            'upper': np.array(upper)} 

    def init_normalization(self):
        """
        Method to initialize normalization functions as defined by self.spec

        arr = (arr.clip(min, max) - shift) / scale

        There three methods for defining parameters in *.yml file:

          (1) shift: 64      ==> use raw value if provided
          (2) shift: 'mu'    ==> use corresponding column in DataFrame
          (3) shift: '$mean' ==> use corresponding Numpy function

        """
        self.norm_lambda = {'xs': {}, 'ys': {}}
        self.norm_kwargs = {'xs': {}, 'ys': {}}

        # --- Lambda function for extracting kwargs
        extract = lambda x, row, arr : row[x] if x[0] != '@' else getattr(np, x[1:])(arr)

        # --- Set up random number generator
        rands = lambda lower, upper: np.random.rand() * (upper - lower) + lower 

        for a in ['xs', 'ys']:
            for key, specs in self.specs[a].items():
                if specs['norms'] is not None:

                    norms = specs['norms']

                    # --- Initialize random transforms
                    r = norms.pop('rands', {})
                    norms['rand_scale'] = {**{'lower': 1.0, 'upper': 1.0}, **r.get('scale', {}), **norms.get('rand_scale', {})}
                    norms['rand_shift'] = {**{'lower': 1.0, 'upper': 1.0}, **r.get('shift', {}), **norms.get('rand_shift', {})}

                    # --- Set up appropriate lambda function
                    if 'mapping' in norms:
                        l = self.map_array

                    elif 'clip' in norms and ('shift' in norms or 'scale' in norms):
                        l = lambda x, clip, rand_shift, rand_scale, shift=0, scale=1, **kwargs : \
                            (x.clip(**clip) - (shift * rands(**rand_shift))) / (scale * rands(**rand_scale))

                    elif 'clip' in norms:
                        l = lambda x, clip, **kwargs : x.clip(**clip)

                    else:
                        l = lambda x, rand_shift, rand_scale, shift=0, scale=1, **kwargs : \
                            (x - (shift * rands(**rand_shift))) / (scale * rands(**rand_scale))

                    self.norm_lambda[a][key] = l

                    # --- Set up appropriate kwargs function 
                    self.norm_kwargs[a][key] = lambda row, arr, norms : \
                        {k: extract(v, row, arr) if type(v) is str else v for k, v in norms.items()}

    def map_array(self, arr, mapping, **kwargs):
        """
        Method to map values in array

        NOTE: only values in mapping dict will be propogated

        """
        arr_ = np.zeros(arr.shape, dtype=arr.dtype)

        for k, v in mapping.items():
            arr_[arr == k] = v

        return arr_

    @check_data_is_loaded
    def print_cohorts(self):
        """
        Method to generate summary of cohorts

        ===========================
        TRAIN
        ===========================
        cohort-A: 1000
        cohort-B: 1000
        ...
        ===========================
        VALID
        ===========================
        cohort-A: 1000
        cohort-B: 1000
        ...

        """
        keys = sorted(self.indices['train'].keys())

        for split in ['train', 'valid']:
            printb(split.upper())
            for cohort in keys:
                size = self.indices[split][cohort].size
                printd('{}: {:06d}'.format(cohort, size))

    def set_specs(self, specs=None):

        self.specs.update(specs or {})

        # --- Initialize xs, ys
        for arr in ['xs', 'ys']:
            for k in self.specs[arr]:

                DEFAULTS = {
                    'dtype': None,
                    'input': True,
                    'loads': None,
                    'norms': None, 
                    'shape': None,
                    'xform': None}

                self.specs[arr][k] = {**DEFAULTS, **self.specs[arr][k]}

                # --- Initialize shape
                if type(self.specs[arr][k]['shape']) is list:
                    self.specs[arr][k]['shape'] = {
                        'saved': self.specs[arr][k]['shape'].copy(),
                        'input': self.specs[arr][k]['shape'].copy()}

                for field in ['saved', 'input']:
                    assert field in self.specs[arr][k]['shape']

    def get_specs(self):

        extract = lambda x : {
            'shape': [None if t else s for s, t in zip(x['shape']['input'], self.specs['tiles'])],
            'dtype': x['dtype']}

        specs_ = {'xs': {}, 'ys': {}} 
        for k in specs_:
            for key, spec in self.specs[k].items():
                if spec['input']:
                    specs_[k][key] = extract(spec)

        return specs_

    def get_inputs(self, Input):
        """
        Method to create dictionary of Keras-type Inputs(...) based on self.specs

        """
        specs = self.get_specs()

        return {k: Input(
            shape=specs['xs'][k]['shape'],
            dtype=specs['xs'][k]['dtype'],
            name=k) for k in specs['xs']}

    def load(self, row, **kwargs):

        arrays = {'xs': {}, 'ys': {}}
        for k in arrays:
            for key, spec in self.specs[k].items():

                # --- Load from file 
                if spec['loads'] in self.db.fnames.columns:
                    load_kwargs = self.get_load_kwargs(row, spec['shape']['saved'], **kwargs)
                    arrays[k][key] = self.load_func(row[spec['loads']], **load_kwargs)
                    if type(arrays[k][key]) is tuple:
                        arrays[k][key] = arrays[k][key][0]

                # --- Load from row
                else:
                    if spec['loads'] is None:
                        arrays[k][key] = np.ones(spec['shape']['saved'], dtype=spec['dtype'])
                    else:
                        if kwargs['indices'] is None:
                            arrays[k][key] = np.array(row[spec['loads']])
                        else:
                            arrays[k][key] = np.array(self.db.header[spec['loads']][kwargs['indices']])

        return arrays

    def get_load_kwargs(self, row=None, shape=None, full_res=False, **kwargs):
        """
        Method to load kwargs

        NOTE: the infos dict is constructed based on the following rules:

          (1) standard  : infos shape derived from self.specs
          (2) indices   : infos shape + point derived from self.specs + indices 
          (3) full_res  : infos = {}

        """
        load_kwargs = self.specs['load_kwargs'].copy()

        if 'infos' not in load_kwargs:
            load_kwargs['infos'] = {}

        if full_res:
            return load_kwargs

        if kwargs['indices'] is None:

            z = row.get('coord-z', 0.5) if 'coord-z' in row else row.get('coord', 0.5)
            y = row.get('coord-y', 0.5)
            x = row.get('coord-x', 0.5)

            load_kwargs['infos']['point'] = [z, y, x] 
            load_kwargs['infos']['shape'] = shape[:3]

        else:

            unique = lambda x, i : np.unique(self.db.header[x][kwargs['indices']]) \
                if x in self.db.header else  np.linspace(0, 1, shape[i])
            mid = lambda x : x[int(x.size / 2)]

            z = unique('coord-z', 0) if 'coord-z' in row else unique('coord', 0)
            y = unique('coord-y', 1) 
            x = unique('coord-x', 2) 

            load_kwargs['infos']['point'] = [mid(z), mid(y), mid(x)]
            load_kwargs['infos']['shape'] = [z.size, y.size, x.size] 

        return load_kwargs

    def prepare_next_epoch(self, split, cohort):

        assert cohort in self.indices[split]

        # --- Increment current
        self.current[split][cohort]['epoch'] += 1
        self.current[split][cohort]['count'] = 0 
        self.current[split][cohort]['rseed'] = np.random.randint(2 ** 32)

        # --- Random shuffle
        self.shuffle_indices(split, cohort)

    def shuffle_indices(self, split, cohort):

        # --- Seed
        np.random.seed(self.current[split][cohort]['rseed'])

        # --- Shuffle indices
        s = self.indices[split][cohort].size
        p = np.random.permutation(s)
        self.indices[split][cohort] = self.indices[split][cohort][p]

    def prepare_next_array(self, split=None, cohort=None, row=None):

        if row is not None:
            if type(row) is int:
                indices = None
                row = self.db.row(row)
            else:
                indices = np.array(row) 
                row = self.db.row(row[0])

            return {'row': row, 'split': split, 'cohort': cohort, 'indices': indices}

        if split is None:
            split = 'train' if np.random.rand() < self.batch['training']['train'] else 'valid'

        if cohort is None:
            if self.sampling_rates is not None:
                i = np.random.rand()
                i = (i < self.sampling_rates['upper']) & (i >= self.sampling_rates['lower'])
                i = int(np.nonzero(i)[0])
                cohort = self.sampling_rates['cohorts'][i]
            else:
                cohort = sorted(self.indices[split].keys())[0]

        c = self.current[split][cohort]

        if c['count'] > self.indices[split][cohort].size - 1:
            self.prepare_next_epoch(split, cohort)
            c = self.current[split][cohort]

        ind = self.indices[split][cohort][c['count']]
        row = self.db.row(index=ind)

        # --- Increment counter
        c['count'] += 1

        return {'row': row, 'split': split, 'cohort': cohort, 'indices': None} 

    def get(self, split=None, cohort=None, row=None, **kwargs):
        """
        Method to load and process data 

        NOTE: row may represent either a single index or consecutive indices to load

        """
        # --- Load data
        kwargs = self.prepare_next_array(split=split, cohort=cohort, row=row)
        arrays = self.load(**kwargs)

        # --- Process 
        arrays = self.augment(arrays, **kwargs)
        arrays = self.preprocess(arrays, **kwargs)
        arrays = self.arrs_to_numpy(arrays)
        arrays = self.normalize(arrays, **kwargs)

        # --- Ensure that spec matches
        for k in ['xs', 'ys']:
            for key in arrays[k]:
                shape = self.specs[k][key]['shape']['input']

                # --- Modify shapes for indices-type loading
                if kwargs['indices'] is not None:
                    shape = [-1 if t else s for t, s in zip(self.specs['tiles'], shape)] \
                        if any(self.specs['tiles']) else [-1] + shape

                dtype = self.specs[k][key]['dtype']
                arrays[k][key] = arrays[k][key].reshape(shape).astype(dtype)

        return arrays

    def arrs_to_numpy(self, arrays):
        """
        Method to convert arrays to Numpy (if alternate load function is provided)

        """
        for k in ['xs', 'ys']:
            for key in arrays[k]:
                if type(arrays[k][key]) is not np.ndarray:
                    if hasattr(arrays[k][key], 'to_numpy'):
                        arrays[k][key] = arrays[k][key].to_numpy()

        return arrays

    def augment(self, arrays, **kwargs):
        """
        Method to add custom data augmentation algorithms to data

        """
        if self.daug_func is not None and kwargs['indices'] is None:
            arrays = self.daug_func(arrays, self.specs, **kwargs)

        return arrays

    def preprocess(self, arrays, **kwargs): 
        """
        Method to add custom preprocessing algorithms to data

        """
        if self.prep_func is not None:
            arrays = self.prep_func(arrays, self.specs, **kwargs)

        return arrays

    def normalize(self, arrays, row, **kwargs):
        """
        Method to normalize data based on lambda defined set in self.norm_lambda

        """
        for a in ['xs', 'ys']:
            for key, func in self.norm_lambda[a].items():
                kwargs = self.norm_kwargs[a][key](row, arrays[a][key], self.specs[a][key]['norms'])
                arrays[a][key] = func(arrays[a][key], **kwargs)

        return arrays

    def test(self, n=None, split=None, cohort=None, aggregate=False):
        """
        Method to test self.get() method

        :params

          (int) n     : number of iterations; if None, then all rows
          (int) lower : lower bounds of row to load
          (int) upper : upper bounds of row to load

        """
        if aggregate:
            keys = lambda x : {k: [] for k in self.specs[x]}
            arrs = {'xs': keys('xs'), 'ys': keys('ys')} 

        # --- Iterate
        for i in range(n):

            printp('Loading iteration: {:06d}'.format(i), (i + 1) / n)
            arrays = self.get(split=split, cohort=cohort)

            if aggregate:
                for k in arrays:
                    for key in arrs[k]:
                        arrs[k][key].append(arrays[k][key][int(arrays[k][key].shape[0] / 2)])

        printd('Completed {} self.get() iterations successfully'.format(n), ljust=140)

        if aggregate:
            stack = lambda x : {k: np.stack(v) for k, v in x.items()}
            return {'xs': stack(arrs['xs']), 'ys': stack(arrs['ys'])}

    def montage(self, xs, ys=None, N=5, n=None, split=None, cohort=None, func=None, **kwargs):
        """
        Method to load montage of self.get() arrs 

        """
        n = n or N ** 2

        # --- Aggregate
        dats, lbls = [], []

        for i in range(n):

            printp('Loading iteration: {:06d}'.format(i), (i + 1) / n)
            arrays = self.get(split=split, cohort=cohort)

            dats.append(arrays['xs'][xs])

            if ys is not None:
                lbls.append(arrays['ys'][ys])

                # --- Apply label conversion and slice extraction function
                if func is not None:
                    dats[-1], lbls[-1] = func(dat=arrays['xs'][xs], lbl=arrays['ys'][ys], **kwargs)

        # --- Interleave dats
        dats = interleave(np.stack(dats), N=N)

        # --- Interleave lbls
        if ys is not None:
            lbls = interleave(np.stack(lbls), N=N)

        return dats, lbls

    def generator(self, split, batch_size=None):
        """
        Method to wrap the self.get() method in a Python generator for training input

        """
        batch_size = batch_size or self.batch['size']
        if batch_size is None:
            printd('ERROR batch size must be provided if not already set')

        while True:

            xs = []
            ys = []

            for i in range(batch_size):

                arrays = self.get(split=split) 
                xs.append(arrays['xs'])
                ys.append(arrays['ys'])

            xs = {k: np.stack([x[k] for x in xs]) for k in self.specs['xs']}
            ys = {k: np.stack([y[k] for y in ys]) for k in self.specs['ys']}

            yield xs, ys

    def generator_single_pass(self, split, cohorts=None, **kwargs):

        # --- Determine cohorts
        if type(cohorts) is str:
            cohorts = [cohorts]
        cohorts = cohorts or self.indices[split].keys()

        # --- Determine indices from cohorts
        indices = np.concatenate([self.indices[split][c] for c in cohorts])
        indices = np.sort(indices)

        # --- Create temporary new database
        db = self.db.new_db('single-pass-{}'.format(split), 
            fnames=self.db.fnames, 
            header=self.db.header)
        db.fnames.index = np.arange(db.fnames.shape[0])
        db.header.index = np.arange(db.header.shape[0])

        # --- Determine if drop_duplicates based on self.specs['tiles']
        drop_duplicates = any(self.specs['tiles'])

        if drop_duplicates:
            to_load = self.fnames_to_load()
            expanded = db.fnames_expand(cols=to_load)

        for sid, fnames, header in db.cursor(indices=indices, drop_duplicates=drop_duplicates):

            if drop_duplicates:
                indices = np.ones(db.fnames.shape[0], dtype='bool')
                for key in to_load:
                    indices = indices & (expanded[key] == fnames[key])
                row = np.nonzero(indices.to_numpy())[0]

            else:
                row = sid

            arrays = self.get(row=row)

            yield arrays['xs'], arrays['ys']

    def create_generators(self, batch_size=None, single_pass=False, **kwargs):

        if single_pass:
            gen_train = self.generator_single_pass('train', **kwargs)
            gen_valid = self.generator_single_pass('valid', **kwargs)

        else:
            gen_train = self.generator('train', batch_size)
            gen_valid = self.generator('valid', batch_size)

        return gen_train, gen_valid

# ===================================================================================
# client = Client()
# ===================================================================================
# client.make_summary(
#     query={
#         'dat': 'dat.hdf5',
#         'lbl': 'bet.hdf5'},
#     CLASSES=2)
# ===================================================================================
