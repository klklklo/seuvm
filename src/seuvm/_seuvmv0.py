import numpy as np
import xarray as xr
import seuvm._misc as _m


class Seuvmv0:
    '''
    Seuvm ver.0 ("average") model class.
    '''
    def __init__(self):
        self.dataset = _m.get_seuvm_ver0()

    def _get_spectrum(self, _f107):
        spectra = np.empty((190, 0))
        for f107 in _f107:
            if f107 > 60 and f107 <= 80:
                i = 0
            elif f107 > 80 and f107 <= 100:
                i = 1
            elif f107 > 100 and f107 <= 120:
                i = 2
            elif f107 > 120 and f107 < 140:
                i = 3
            elif f107 > 140 and f107 < 160:
                i = 4
            elif f107 > 160 and f107 < 180:
                i = 5
            elif f107 > 180 and f107 < 200:
                i = 6
            elif f107 > 200 and f107 < 220:
                i = 7
            elif f107 > 220 and f107 < 240:
                i = 8
            elif f107 > 240 and f107 < 260:
                i = 9
            elif f107 > 260 and f107 < 280:
                i = 10

            spectrum = np.array(self.dataset.to_pandas().iloc[i, 3:]).reshape((190,1))
            # print(spectrum.shape)
            spectra = np.hstack([spectra, spectrum])
            print(spectra)

        return spectra


    def predict(self, f107):
        f107 = np.array([f107], dtype=np.float64) if isinstance(f107, (int, float)) \
            else np.array(f107, dtype=np.float64)

        res = self._get_spectrum(f107)
        return xr.Dataset(data_vars={'euv_flux_spectra': (('band_center', 'f107'), res),
                                     'lband': ('band_number', np.arange(0,190)),
                                     'uband': ('band_number', np.arange(1,191))},
                          coords={'f107': f107,
                                  'band_center': [i+0.5 for i in range(190)],
                                  'band_number': np.arange(190)})