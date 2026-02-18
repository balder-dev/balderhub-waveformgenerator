from balderhub.waveform.lib.utils import waveforms
from .base_siglent_sdg_series_awg_instrument import BaseSiglentSDGSeriesAWGInstrument

class SiglentSDG2000XAWGInstrument(BaseSiglentSDGSeriesAWGInstrument):
    """
    NOTE: This feature is experimental and subject to change. It was not fully validated yet.
          If you are a owner of this device and if you are interested in contribution, please open a issue with the
          validation results of the BalderHub package test results.
    """

    @property
    def stored_waveform_mapping(self):
        result = super().stored_waveform_mapping
        result[waveforms.common.CardiacWaveform] = "INDEX,26"
        return result
