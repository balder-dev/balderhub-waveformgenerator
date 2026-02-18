import decimal
import enum
import re
import time
from typing import Union

import numpy as np

from balderhub.scpi.lib.scenario_features.scpi_transmission_feature import ScpiTransmissionFeature
from balderhub.waveform.lib.utils.waveforms.base_periodic_waveform import BasePeriodicWaveform

from ...scenario_features.waveform_generator_instrument import WaveformGeneratorInstrument


class BaseSiglentSDGSeriesAWGInstrument(WaveformGeneratorInstrument):
    """
    Feature implementation for the Siglent SDG Series Arbitrary waveform generators
    """
    scpi = ScpiTransmissionFeature()

    class Channel(enum.Enum):
        """available channel for this instrument"""
        CH1 = 1
        CH2 = 2

    @property
    def resolution_bits(self):
        """
        :return: returns the vertical resolution of the device in bits
        """
        return 16

    def _get_waveform_identifier(self, for_waveform: BasePeriodicWaveform) -> str:
        if self.prefer_stored_waveforms and for_waveform.__class__ in self.stored_waveform_mapping.keys():
            return self.stored_waveform_mapping[for_waveform.__class__]

        name = self._convert_custom_waveform_name(for_waveform)
        return f"NAME,{name}"

    def is_inverted(self, channel: Channel) -> bool:
        result = self.scpi.query_values(f'C{channel.value}:INVERT?'.encode(self.scpi.ENCODING))
        response = result.decode(self.scpi.ENCODING)

        if response == f"C{channel.value}:INVT ON":
            return True
        if response == f"C{channel.value}:INVT OFF":
            return False
        raise ValueError(f'unexpected response: `{result}`')

    def is_enabled(self, channel: Channel) -> bool:
        # TODO improve: use regular expression
        result = self.scpi.query_values(f'C{channel.value}:OUTP?'.encode(self.scpi.ENCODING))
        relevant_result = result[8:result.find(b',')]
        if relevant_result == b'OFF':
            return False
        if relevant_result == b'ON':
            return True
        raise ValueError(f'received unexpected answer: {result}')

    def enable_signal(self, at_channel: Channel) -> None:
        self.scpi.write_values(f'C{at_channel.value}:OUTP ON'.encode(self.scpi.ENCODING))
        time.sleep(1)

    def disable_signal(self, at_channel: Channel) -> None:
        self.scpi.write_values(f'C{at_channel.value}:OUTP OFF'.encode(self.scpi.ENCODING))
        time.sleep(1)

    def invert_signal(self, at_channel: Channel, state: bool):
        value = 'ON' if state else 'OFF'
        self.scpi.write_values(f'C{at_channel.value}:INVERT {value}'.encode(self.scpi.ENCODING))

    def save_waveform(
            self,
            waveform: BasePeriodicWaveform,
    ) -> None:
        name = self._convert_custom_waveform_name(waveform)
        min_val = - (1 << self.resolution_bits - 1)
        max_val = (1 << self.resolution_bits - 1) - 1
        wvfm_data = np.round(waveform.data * max_val).clip(min_val, max_val).astype(np.int16)

        command = f"C1:WVDT WVNM,{name},WAVEDATA,".encode(self.scpi.ENCODING)  # TODO what is with channel???
        command += wvfm_data
        self.scpi.write_values(command)
        time.sleep(1)

    def get_stored_waveform_identifiers(self) -> list[str]:
        result = self.scpi.query_values(b'STL? USER')
        response = result.decode(self.scpi.ENCODING).strip()
        expected_response_beginning = 'STL WVNM'
        if response == expected_response_beginning:
            return []
        if not response.startswith(expected_response_beginning + ','):
            raise ValueError(f'received unexpected response: {response}')
        result = []
        for raw_name in response[len(expected_response_beginning) + 1:].strip().split(','):
            result.append(f'NAME,{raw_name}')
        return result

    def _get_cmd_parameter_for(
            self,
            frequency_hz: Union[decimal.Decimal, None] = None,
            amplitude_vpp: Union[decimal.Decimal, None] = None,
            offset_vdc: Union[decimal.Decimal, None] = None,
            phase: Union[decimal.Decimal, None] = None
    ) -> list[str]:
        result = []
        if frequency_hz is not None:
            result.append(f"FRQ,{frequency_hz}")
        if amplitude_vpp is not None:
            result.append(f"AMP,{amplitude_vpp}")
        if offset_vdc is not None:
            result.append(f"OFST,{offset_vdc}")
        if phase is not None:
            result.append(f"PHSE,{phase}")
        return result

    def select_waveform(
            self,
            at_channel: Channel,
            waveform: BasePeriodicWaveform,
    ) -> None:

        # already gets correct name, even if it is a build-in that should be used
        identifier = self._get_waveform_identifier(waveform)
        command = f'C{at_channel.value}:BSWV WVTP,ARB'
        additional_params = self._get_cmd_parameter_for(
            decimal.Decimal(waveform.frequency_hz),
            decimal.Decimal(waveform.amplitude_vpp),
            decimal.Decimal(waveform.offset_vdc),
            decimal.Decimal(waveform.phase)
        )
        if additional_params:
            command += ' ,' +','.join(additional_params)

        self.scpi.write_values(command.encode(self.scpi.ENCODING))
        self.scpi.write_values(f"C{at_channel.value}:ARWV {identifier}".encode(self.scpi.ENCODING))
        time.sleep(1)

    def update_waveform_parameters(
            self,
            of_channel: Channel,
            frequency_hz: Union[decimal.Decimal, None] = None,
            amplitude_vpp: Union[decimal.Decimal, None] = None,
            offset_vdc: Union[decimal.Decimal, None] = None,
            phase: Union[decimal.Decimal, None] = None
    ) -> None:
        command = f"C{of_channel.value}:BSWV "
        additional_params = self._get_cmd_parameter_for(frequency_hz, amplitude_vpp, offset_vdc, phase)
        if not additional_params:
            raise ValueError('please provide at least one parameter: ')
        command += ',' +','.join(additional_params)

        self.scpi.write_values(command.encode(self.scpi.ENCODING))
        time.sleep(1)

    def get_waveform_parameters(
            self,
            of_channel: Channel
    ) -> tuple[decimal.Decimal, decimal.Decimal, decimal.Decimal, decimal.Decimal]:
        """
        Method to request all important waveform parameters (frequency, amplitude, offset, phase) from the instrument
        :param of_channel: the channel the parameters should be requested for
        :return: a tuple with frequency, amplitude, offset, phase
        """
        response = self.scpi.query_values(
            f'C{of_channel.value}:BSWV?'.encode(self.scpi.ENCODING)
        ).decode('utf-8').strip()
        # TODO improve
        expected_response_beginning = f'C{of_channel.value}:BSWV WVTP,'

        if not response.startswith(expected_response_beginning):
            raise ValueError(f'received unexpected response: {response}')
        data = response[len(expected_response_beginning):].split(',')
        data_pairs = {}
        for idx in range(1, len(data), 2):
            new_key = data[idx]
            if new_key in data_pairs:
                raise ValueError(
                    f'received unexpected response, because key {new_key} was mentioned more than once: {response}'
                )
            data_pairs[new_key] = data[idx + 1]

        freq_match = re.match(r'(\d+\.?\d*)HZ', data_pairs['FRQ'])
        if not freq_match:
            raise ValueError(f'was unable to extract frequency from response: {response}')

        ampl_match = re.match(r'(\d+\.?\d*)V', data_pairs['AMP'])
        if not ampl_match:
            raise ValueError(f'was unable to extract amplitude from response: {response}')

        offset_match = re.match(r'(-?\d+\.?\d*)V', data_pairs['OFST'])
        if not offset_match:
            raise ValueError(f'was unable to extract offset from response: {response}')

        phase_match = re.match(r'(-?\d+\.?\d*)', data_pairs['PHSE'])
        if not phase_match:
            raise ValueError(f'was unable to extract phase from response: {response}')

        return (
            decimal.Decimal(freq_match[1]),
            decimal.Decimal(ampl_match[1]),
            decimal.Decimal(offset_match[1]),
            decimal.Decimal(phase_match[1])
        )

    def get_current_frequency_hz(self, of_channel: Channel) -> decimal.Decimal:
        return self.get_waveform_parameters(of_channel=of_channel)[0]

    def get_current_amplitude_vpp(self, of_channel: Channel) -> decimal.Decimal:
        return self.get_waveform_parameters(of_channel=of_channel)[1]

    def get_current_offset_vdc(self, of_channel: Channel) -> decimal.Decimal:
        return self.get_waveform_parameters(of_channel=of_channel)[2]

    def get_current_phase(self, of_channel: Channel) -> decimal.Decimal:
        return self.get_waveform_parameters(of_channel=of_channel)[3]
