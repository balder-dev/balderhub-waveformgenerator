import decimal
from typing import Union

import balder

from balderhub.waveform.lib.utils.waveforms import BasePeriodicWaveform

class WaveformGeneratorFeature(balder.Feature):
    """
    Waveform Generator Feature that is independent of the device type. It  does not even need to be a
    Programmable Signal Generator, because you could use any device that can be controlled and provide the
    functionality.
    """

    def is_inverted(self) -> bool:
        """
        :return: returns True if the generator generates the inverted waveform, False otherwise.
        """
        raise NotImplementedError()

    def is_enabled(self) -> bool:
        """
        :return: returns True if the generator output is enabled, False otherwise.
        """
        raise NotImplementedError()

    def set_waveform(
            self,
            waveform: BasePeriodicWaveform,
    ) -> None:
        """
        This method sets the waveform that should be generated.
        :param waveform: the waveform to be generated
        """
        raise NotImplementedError()

    def update_waveform_parameters(
            self,
            frequency_hz: Union[decimal.Decimal, None] = None,
            amplitude_vpp: Union[decimal.Decimal, None] = None,
            offset_vdc: Union[decimal.Decimal, None] = None,
            phase: Union[decimal.Decimal, None] = None
    ) -> None:
        """
        This method updates the waveform parameters like frequency, amplitude, etc.

        :param frequency_hz: frequency
        :param amplitude_vpp: amplitude in volts (peak-peak)
        :param offset_vdc: the offset that should be applied to the waveform
        :param phase: the phase that should be applied to the waveform
        """
        raise NotImplementedError()

    def get_current_frequency_hz(self) -> decimal.Decimal:
        """
        :return: returns the current applied frequency in Hz
        """
        raise NotImplementedError()

    def get_current_amplitude_vpp(self) -> decimal.Decimal:
        """
        :return: returns the current applied amplitude in volts (peak-peak)
        """
        raise NotImplementedError()

    def get_current_offset_vdc(self) -> decimal.Decimal:
        """
        :return: returns the current applied offset in volts
        """
        raise NotImplementedError()

    def get_current_phase(self) -> decimal.Decimal:
        """
        :return: returns the current applied phase [0;2*pi]
        """
        raise NotImplementedError()

    def enable_signal(self) -> None:
        """
        Enables the waveform generator output
        """
        raise NotImplementedError()

    def disable_signal(self) -> None:
        """
        Disables the waveform generator output
        """
        raise NotImplementedError()

    def invert_signal(self, state: bool) -> None:
        """
        Changes the invert state of the waveform generator
        :param state: True if the signal should be inverted, False otherwise
        """
        raise NotImplementedError()
