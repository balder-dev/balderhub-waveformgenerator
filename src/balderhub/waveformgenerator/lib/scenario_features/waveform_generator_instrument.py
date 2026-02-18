import decimal
from typing import Union
import enum
import hashlib

import balder

from balderhub.waveform.lib.utils.waveforms.base_periodic_waveform import BasePeriodicWaveform


class WaveformGeneratorInstrument(balder.Feature):
    """raw implementation of a programmable signal generator instrument"""

    class Channel(enum.Enum):
        """enum holding all available channels of this instrument"""

    def _get_waveform_identifier(self, for_waveform: BasePeriodicWaveform) -> str:
        """
        Returns the identifier for the given waveform.

        If :meth:`WaveformGeneratorInstrumentWithStored.prefer_stored_waveforms` is True and the given waveform is
        within the dictionary :meth:`WaveformGeneratorInstrumentWithStored.stored_waveform_mapping` this method
        returns the build in identifier instead of the theoretically name this waveform would be stored on the device
        """
        raise NotImplementedError()

    @property
    def stored_waveform_mapping(self) -> dict[type[BasePeriodicWaveform], str]:
        """
        Allows to map waveforms to stored waveforms on the device. If
        :meth:`WaveformGeneratorInstrument.prefer_stored_waveforms` is True, the feature prefers to use these stored
        waveforms instead of uploading custom ones.
        :return: a dictionary with the waveform type as key and the waveform identifier (instrument specific) as value
        """
        return {}

    @property
    def prefer_stored_waveforms(self) -> bool:
        """
        :return: returns True if the feature should try to use stored waveforms (defined in
                 :meth:`WaveformGeneratorInstrument.prefer_stored_waveforms`) instead of uploading custom ones
        """
        return True

    def _convert_custom_waveform_name(self, waveform: BasePeriodicWaveform):
        return f"Balder_{hashlib.md5(waveform.data.tobytes()).hexdigest()}"

    def is_inverted(self, channel: Channel) -> bool:
        """

        :param channel: the channel that should be checked
        :return: returns True if the generator generates the inverted waveform at the given channel, False otherwise.

        """
        raise NotImplementedError()

    def is_enabled(self, channel: Channel) -> bool:
        """
        :param channel: the channel to check
        :return: returns True if the generator output at the given channel is enabled, False otherwise.
        """
        raise NotImplementedError()

    def get_stored_waveform_identifiers(self) -> list[str]:
        """
        :return: returns a list of all stored waveform identifiers (instrument specific)
        """
        raise NotImplementedError()

    def is_waveform_on_instrument(self, waveform: BasePeriodicWaveform) -> bool:
        """
        This method returns True if the given waveform is already saved at the instrument, False otherwise.
        :param waveform: the waveform to check
        :return: True if the waveform is already saved at the instrument, False otherwise
        """
        wvfm_identifier = self._get_waveform_identifier(waveform)
        if wvfm_identifier in self.stored_waveform_mapping.values():
            return True
        return wvfm_identifier in self.get_stored_waveform_identifiers()

    def save_waveform(
            self,
            waveform: BasePeriodicWaveform,
    ) -> None:
        """
        This method transfers the provided waveform to the instrument. In other words, this method does everything
        necessary to set up the configured waveform.

        :param waveform: the waveform that should be saved
        """
        raise NotImplementedError()

    def select_waveform(
            self,
            at_channel: Channel,
            waveform: BasePeriodicWaveform,
    ) -> None:
        """
        This method selects a waveform and applies it to the given channel. Please make sure, that the waveform was
        transferred to device first (see :meth:`WaveformGeneratorInstrument.save_waveform`)

        :param at_channel: the channel, the waveform should be applied to
        :param waveform: the waveform to apply
        """
        raise NotImplementedError()

    def update_waveform_parameters(
            self,
            of_channel: Channel,
            frequency_hz: Union[decimal.Decimal, None] = None,
            amplitude_vpp: Union[decimal.Decimal, None] = None,
            offset_vdc: Union[decimal.Decimal, None] = None,
            phase: Union[decimal.Decimal, None] = None
    ) -> None:
        """
        This method updates the waveform parameters like frequency, amplitude, etc. for the given channel.

        :param of_channel: The channel to apply the waveform to.
        :param frequency_hz: frequency
        :param amplitude_vpp: amplitude in volts (peak-peak)
        :param offset_vdc: the offset that should be applied to the waveform
        :param phase: the phase that should be applied to the waveform
        """
        raise NotImplementedError()

    def update_frequency(self, of_channel: Channel, frequency_hz: decimal.Decimal) -> None:
        """
        Updates the frequency at the given channel

        :param of_channel: the channel to apply the new frequency to
        :param frequency_hz: the new frequency that should be applied
        """
        self.update_waveform_parameters(of_channel=of_channel, frequency_hz=frequency_hz)

    def update_amplitude(self, of_channel: Channel, amplitude_vpp: decimal.Decimal) -> None:
        """
        Updates the amplitude in volts (peak-peak) at the given channel

        :param of_channel: the channel to apply the new amplitude in volts (peak-peak) to
        :param amplitude_vpp: the new amplitude in volts (peak-peak) that should be applied
        """
        self.update_waveform_parameters(of_channel=of_channel, amplitude_vpp=amplitude_vpp)

    def update_offset(self, of_channel: Channel, offset_vdc: decimal.Decimal) -> None:
        """
        Updates the offset at the given channel

        :param of_channel: the channel to apply the new offset to
        :param offset_vdc: the new offset that should be applied
        """
        self.update_waveform_parameters(of_channel=of_channel, offset_vdc=offset_vdc)

    def update_phase(self, of_channel: Channel, phase: decimal.Decimal) -> None:
        """
        Updates the phase at the given channel

        :param of_channel: the channel to apply the new phase to
        :param phase: the new phase that should be applied
        """
        self.update_waveform_parameters(of_channel=of_channel, phase=phase)

    def get_current_frequency_hz(self, of_channel: Channel) -> decimal.Decimal:
        """
        :param of_channel: the channel to check
        :return: returns the current applied frequency in Hz at the requested channel
        """
        raise NotImplementedError()

    def get_current_amplitude_vpp(self, of_channel: Channel) -> decimal.Decimal:
        """
        :param of_channel: the channel to check
        :return: returns the current applied amplitude in volts (peak-peak) at the requested channel
        """
        raise NotImplementedError()

    def get_current_offset_vdc(self, of_channel: Channel) -> decimal.Decimal:
        """
        :param of_channel: the channel to check
        :return: returns the current applied offset in volts at the requested channel
        """
        raise NotImplementedError()

    def get_current_phase(self, of_channel: Channel) -> decimal.Decimal:
        """
        :param of_channel: the channel to check
        :return: returns the current applied phase [0;2*pi] at the requested channel
        """
        raise NotImplementedError()

    def enable_signal(self, at_channel: Channel) -> None:
        """
        Enables the waveform generator output at the given channel

        :param at_channel: the channel to enable the signal at
        """
        raise NotImplementedError()

    def disable_signal(self, at_channel: Channel) -> None:
        """
        Disables the waveform generator output at the given channel

        :param at_channel: the channel to disable the signal at
        """
        raise NotImplementedError()

    def invert_signal(self, at_channel: Channel, state: bool):
        """
        Changes the invert state of the waveform generator at the given channel

        :param at_channel: the channel to apply the inverted signal state to
        :param state: True if the signal should be inverted, False otherwise
        """
        raise NotImplementedError()
