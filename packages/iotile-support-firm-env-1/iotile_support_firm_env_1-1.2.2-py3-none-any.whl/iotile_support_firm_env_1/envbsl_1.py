"""An emulator for firm_env v1.X.Y."""

from collections import namedtuple
from random import normalvariate
from iotile.emulate import EmulatedPeripheralTile
from iotile.core.hw.virtual import tile_rpc


EnvData = namedtuple("EnvData", ['temp', 'humidity', 'pressure'])


class EmulatedEnvironmentalTile(EmulatedPeripheralTile):
    """RPC based emulator for environmental tile.
    
    Supported Test Scenarios:
        - set_environment: Loads in a fixed value for the temperature, pressure
          and humidity that is returned.
        - random_environment: Sets the standard deviation of the temperature,
          pressure and humidity values returned.

    Notes:
        - Calibration is not yet supported.  The RPCs related to calibration
          are not yet implemented.

    Args:
        address (int): The address of this tile in the VirtualIOTIleDevice
            that contains it
        args (dict): The arguments to use to create this tile.  There are no currently
            supported arguments.
        device (TileBasedVirtualDevice) : optional, device on which this tile is running
    """

    STATE_NAME = "environmental_tile"
    STATE_VERSION = "0.0.1"
    name = b'envbsl'

    def __init__(self, address, _args, device=None):
        EmulatedPeripheralTile.__init__(self, address, device)

        self.register_scenario('set_environment', self.set_environment)
        self.register_scenario('random_environment', self.random_environment)

        self._last_value = EnvData(0, 0, 0)
        self._base_value = EnvData(25., 50., 1013.)
        self._variability = 0.0

    def _next_value(self):
        if self._variability == 0.0:
            return self._base_value

        temp = normalvariate(self._base_value.temp, abs(self._base_value.temp * self._variability))
        humidity = normalvariate(self._base_value.humidity, abs(self._base_value.humidity * self._variability))
        press = normalvariate(self._base_value.pressure, abs(self._base_value.pressure * self._variability))

        return EnvData(temp, humidity, press)

    def dump_state(self):
        """Dump the current state of this emulated tile as a dictionary.

        Returns:
            dict: The current state of the object that could be passed to load_state.
        """

        state = super(EmulatedPeripheralTile, self).dump_state()

        state['base_value'] = list(self._base_value)
        state['last_value'] = list(self._last_value)
        state['variability'] = self._variability

        return state

    def restore_state(self, state):
        """Restore the current state of this emulated object.

        Args:
            state (dict): A previously dumped state produced by dump_state.
        """

        super(EmulatedPeripheralTile, self).restore_state(state)

        self._base_value = EnvData(*state.get('base_value', (25., 50., 1013.)))
        self._last_value = EnvData(*state.get('last_value', (0, 0, 0)))
        self._variability = state.get('variability', 0.0)

    @tile_rpc(0x8000, "", "L")
    def poll_data(self):
        """Get a new data set from the BMD-300."""

        self._last_value = EnvData(*self._next_value())
        return [0]

    @tile_rpc(0x8001, "", "l")
    def get_temperature(self):
        """Get the last polled temperature value."""

        return [int(self._last_value.temp * 100)]

    @tile_rpc(0x8002, "", "L")
    def get_pressure(self):
        """Get the last polled pressure value."""

        return [int(self._last_value.pressure * 100)]

    @tile_rpc(0x8003, "", "L")
    def get_humidity(self):
        """Get the last polled humidity value."""

        return [int(self._last_value.humidity * 1024)]

    def set_environment(self, temperature=None, humidity=None, pressure=None):
        """Manually set the environmental data.

        Args:
            temperature (float): The temperature to set in Celsius.  If not passed
                the old value is used.
            humidity (float): The humidity to set in %RH.  If not passed, the old
                value is used.
            pressure (float): The pressure to set in hPa.  If not passed the old
                value is used.
        """

        old_data = list(self._base_value)
        if temperature is not None:
            old_data[0] = float(temperature)

        if humidity is not None:
            old_data[1] = float(humidity)

        if pressure is not None:
            old_data[2] = float(pressure)

        self._base_value = EnvData(*old_data)

    def random_environment(self, variability=0.05):
        """Randomly fluctuate the environment by a certain percentage.

        Args:
            variability (float): The fractional percentage that each env
                value should be modified by before returning.  This is 
                used as the standard deviation parameter in a normal
                distribution around the current value set as the mean.
        """

        self._variability = variability
