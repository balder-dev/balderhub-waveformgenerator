import balder
from balderhub.waveform.lib.utils.waveforms import BasePeriodicWaveform


class TestConfig(balder.Feature):
    """
    Test configuration feature that is used for applying different test conditions to waveform generators
    """

    @property
    def waveforms_to_test(self) -> list[BasePeriodicWaveform]:
        """
        :return: a list of waveforms that should be tested
        """
        return []
