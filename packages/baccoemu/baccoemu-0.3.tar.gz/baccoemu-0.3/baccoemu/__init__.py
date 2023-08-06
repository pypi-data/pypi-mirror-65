import numpy as np
import copy
import pickle
import progressbar
import hashlib

ebounds = np.array([[0.23, 0.4],       # omegam
                    [0.73, 0.9],       # sigma8
                    [0.04, 0.06],      # omegab
                    [0.92, 1.01],      # ns
                    [0.6, 0.8],        # h
                    [0.0, 0.4],        # Mnu
                    [-1.15, -0.85],    # w0
                    [-0.3, 0.3],       # wa
                    [0.4, 1]
                    ])

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _transform_space(x, space_rotation=False, rotation=None, bounds=None):
    """Normalize coordinates to [0,1] intervals and if necessary apply a rotation

    :param x: coordinates in parameter space
    :type x: ndarray
    :param space_rotation: whether to apply the rotation matrix defined through
                           the rotation keyword, defaults to False
    :type space_rotation: bool, optional
    :param rotation: rotation matrix, defaults to None
    :type rotation: ndarray, optional
    :param bounds: ranges within which the emulator hypervolume is defined,
                   defaults to None
    :type bounds: ndarray, optional
    :return: normalized and (if required) rotated coordinates
    :rtype: ndarray
    """
    if space_rotation:
        #Get x into the eigenbasis
        R = rotation['rotation_matrix'].T
        xR = copy.deepcopy(np.array([np.dot(R, xi)
                                     for xi in x]))
        xR = xR - rotation['rot_points_means']
        xR = xR/rotation['rot_points_stddevs']
        return xR
    else:
        return (x - bounds[:, 0])/(bounds[:, 1] - bounds[:, 0])


def _bacco_evaluate_emulator(emulator, coordinates, gp_name='gpy', values=None, sample=False):
    """
    Function evaluating the emulator at some given points.

    :param emulator: the trained gaussian process
    :type emulator: obj
    :param coordinates: points where to predict the function
    :type coordinates: array-like
    :param gp_name: type of gaussian process code to use; options are 'gpy',
                    'george' and 'sklearn', defaults to 'gpy'
    :type gp_name: str
    :param values: only for 'george', the original evaluations of the gp at the
                   coordinates used for training, defaults to None.
    :type values: array-like
    :param sample: only for 'george', whether to take only one sample of the
                   prediction or the full prediction with its variance; if
                   False, returns the full prediction, defaults to False
    :type sample: bool

    :returns: emulated values and variance of the emulation.
    :rtype: float or array_like
    """

    if gp_name == 'gpy':
        deepGP = False
        if deepGP is True:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
        else:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
    elif gp_name == 'sklearn':
        evalues, cov = emulator.predict(coordinates, return_cov=True)
    elif gp_name == 'george':
        if sample:
            evalues = emulator.predict(values, coordinates)
            cov = 0
        else:
            #import ipdb; ipdb.set_trace()
            # (coordinates,mean_only=False)
            evalues, cov = emulator.predict(
                values, coordinates, return_var=True)
    else:
        raise ValueError('emulator type {} not valid'.format(gp_name))

    return evalues, np.abs(cov)


def _compute_camb_spectrum(params, kmax=5, k_per_logint=0):
    """
    Calls camb with the current cosmological parameters and returns a
    dictionary with the following keys:
    kk, pk

    Through the species keyword the following power spectra can be obtained:
    matter, cdm, baryons, neutrinos, cold matter (cdm+baryons), photons,
    divergence of the cdm velocity field, divergence of the baryon velocity
    field, divergence of the cdm-baryon relative velocity field
    """
    import camb
    from camb import model, initialpower

    if 'tau' not in params.keys():
        params['tau'] = 0.0952
    if 'num_massive_neutrinos' not in params.keys():
        params['num_massive_neutrinos'] = 3 if params['neutrino_mass'] != 0.0 else 0
    if 'Neffective' not in params.keys():
        params['Neffective'] = 3.046
    if 'omega_k' not in params.keys():
        params['omega_k'] = 0
    if 'omega_cdm' not in params.keys():
        params['omega_cdm'] = (params['omega_matter'] - params['omega_baryon'] -
                               params['neutrino_mass'] / (93.14 * params['hubble']**2))

    assert params['omega_k'] == 0, 'Non flat geometries are not supported'

    expfactor = params['expfactor']

    # Set up a new set of parameters for CAMB
    pars = camb.CAMBparams()

    # This function sets up CosmoMC-like settings, with one massive neutrino and helium set using BBN consistency
    # Set neutrino-related parameters
    # camb.nonlinear.Halofit('takahashi')
    pars.set_cosmology(
        H0=100 * params['hubble'],
        ombh2=(params['omega_baryon'] * params['hubble']**2),
        omch2=(params['omega_cdm'] * params['hubble']**2),
        neutrino_hierarchy='degenerate',
        num_massive_neutrinos=params['num_massive_neutrinos'],
        mnu=params['neutrino_mass'],
        standard_neutrino_neff=params['Neffective'],
        tau=params['tau'])

    A_s = 2e-9

    pars.set_dark_energy(
        w=params['w0'],
        wa=params['wa'])

    pars.InitPower.set_params(ns=params['ns'], As=A_s)
    pars.YHe = 0.24
    pars.omegak = params['omega_k']
    pars.set_matter_power(
        redshifts=[
            (1 / expfactor - 1)],
        kmax=kmax,
        k_per_logint=k_per_logint)

    pars.WantCls = False
    pars.WantScalars = False
    pars.Want_CMB = False
    pars.DoLensing = False

    # calculate results for these parameters
    results = camb.get_results(pars)

    index = 7 # cdm + baryons
    kh, z, pk = results.get_linear_matter_power_spectrum(var1=(1 + index),
                                                         var2=(1 + index),
                                                         hubble_units=True,
                                                         have_power_spectra=False,
                                                         params=None)
    pk = pk[0, :]

    sigma8 = results.get_sigma8()[0]

    Normalization = (params['sigma8'] / sigma8)**2

    pk *= Normalization

    return {'k': kh, 'pk': pk}

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def load_emu():
    """Loads the emulator in memory.

    We don't automatize this step as it loads approx 5.5 G in memory,
    and we don't want the user to do so accidentaly.

    :return: a dictionary containing the emulator object
    :rtype: dict
    """
    import os
    basefold = os.path.dirname(os.path.abspath(__file__))

    emulator_name = (basefold + '/' +
                     "gpy_emulator_data_iter3_big_120.pickle_fit_PCA8_sgnr_2_rot_vec.pkl")
    emulator_checksum = 'bab4263a43fa8ccb4e3799d219ef1573'

    if (not os.path.exists(emulator_name)) or (md5(emulator_name) != emulator_checksum):
        import urllib.request
        print('Downloading Emulator data (2Gb)...')
        urllib.request.urlretrieve(
                'http://bacco.dipc.org/gpy_emulator_data_iter3_big_120.pickle_fit_PCA8_sgnr_2_rot_vec.pkl', 
                emulator_name,
                MyProgressBar())

    print('Loading emulator... (this can take up to one minute)')
    emulator = {}
    with open(emulator_name, 'rb') as f:
        n_emulator = pickle.load(f)
        emulator['emulator'] = np.empty(n_emulator, dtype=object)
        for i in range(n_emulator):
            emulator['emulator'][i] = pickle.load(f)
        emulator['scaler'] = pickle.load(f)
        emulator['pca'] = pickle.load(f)
        emulator['k'] = pickle.load(f)
    print('Emulator loaded in memory.')
    return emulator


def eval_emu(coordinates, emulator=None):
    """Evaluate the given emulator at a set of cordinates in parameter space.

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param emulator: the emulator object, defaults to None
    :type emulator: dict, optional
    :return: the emulated value of Q(k) at this point in parameter space
    :rtype: array_like
    """
    pp = [
        coordinates['omega_matter'],
        coordinates['sigma8'],
        coordinates['omega_baryon'],
        coordinates['ns'],
        coordinates['hubble'],
        coordinates['neutrino_mass'],
        coordinates['w0'],
        coordinates['wa']
    ]
    pp = np.array([np.r_[pp, coordinates['expfactor']]])

    pname = ['omega_matter', 'sigma8', 'omega_baryon', 'ns', 'h',
             'neutrino_mass', 'w0', 'wa', 'expfactor']
    for i in range(len(pp[0])):
        message = 'Param {} out of bounds [{}, {}]'.format(
            pname[i], ebounds[i, 0], ebounds[i, 1])
        assert (pp[0, i] >= ebounds[i, 0]) & (pp[0, i] <= ebounds[i, 1]), message

    _pp = _transform_space(np.array(pp), space_rotation=False, bounds=ebounds)
    npca = len(emulator['emulator'])
    cc = np.zeros(npca)
    for ii in range(npca):
        cc[ii], var = _bacco_evaluate_emulator(emulator=emulator['emulator'][ii], coordinates=_pp,
                                                       gp_name='gpy')
    yrec = emulator['pca'].inverse_transform(cc)
    return np.exp(emulator['scaler'].inverse_transform(yrec))

def linear_pk(coordinates, k=None):
    """Compute the linear prediction of the cold matter power spectrum using camb

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used by
              camb are returned, defaults to None
    :type k: array_like, optional
    :return: k and linear pk
    :rtype: tuple
    """
    _pk_dict = _compute_camb_spectrum(coordinates)
    if k is not None:
        from scipy.interpolate import interp1d
        _k = k
        _interp = interp1d(np.log(_pk_dict['k']), np.log(_pk_dict['pk']), kind='quadratic')
        _pk = np.exp(_interp(np.log(_k)))
    else:
        _k = _pk_dict['k']
        _pk = _pk_dict['pk']
    return _k, _pk

def nonlinear_pk(coordinates, k=None, emulator=None):
    """Compute the prediction of the nonlinear cold matter power spectrum

    The coordinates must be specified as a dictionary with the following
    keywords:
    #. 'omega_matter'
    #. 'omega_baryon'
    #. 'sigma8'
    #. 'hubble'
    #. 'ns'
    #. 'Mnu'
    #. 'w0'
    #. 'wa'
    #. 'expfactor'

    :param coordinates: a set of coordinates in parameter space
    :type coordinates: dict
    :param k: a vector of wavemodes in h/Mpc, if None the wavemodes used to
              build the emulator are returned, defaults to None
    :type k: array_like, optional
    :param emulator: the emulator object, defaults to None
    :type emulator: obj, optional
    :return: k and nonlinear pk
    :rtype: tuple
    """
    Q = eval_emu(coordinates, emulator=emulator)
    if k is None:
        _k = emulator['k']
        _pk_lin = linear_pk(coordinates, k=_k)
        _pk = Q * _pk_lin
    else:
        from scipy.interpolate import interp1d
        _k = k
        _k_emu, _pk_lin = linear_pk(coordinates, k=emulator['k'])
        _interp = interp1d(np.log(_k_emu), np.log(Q * _pk_lin), kind='quadratic')
        _pk = np.exp(_interp(np.log(_k)))
    return _k, _pk
