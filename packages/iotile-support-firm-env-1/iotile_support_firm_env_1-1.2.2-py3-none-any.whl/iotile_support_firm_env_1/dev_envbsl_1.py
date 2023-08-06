"""A basic reference device emulator containing just this one tile."""

from iotile.emulate.reference import ReferenceDevice
from iotile.emulate import EmulatedPeripheralTile
from iotile.core.dev import ComponentRegistry


class EnvironmentTileReferenceDevice(ReferenceDevice):
    """Reference implementation of an IOTile device with a single environmental tile.

    This device is produced as part of the firm_env component and contains a
    reference emulated device with a single environemtal tile at address 11
    and a reference controller implementation.

    Args:
        args (dict): A dictionary of optional creation arguments.  Currently
            supported are:
                iotile_id (int or hex string): The id of this device. This
                    defaults to 1 if not specified.
    """

    STATE_NAME = "envbsl_1_ref_device"
    STATE_VERSION = "0.1.0"

    def __init__(self, args):
        super(EnvironmentTileReferenceDevice, self).__init__(args)

        reg = ComponentRegistry()
        _name, tile_factory = reg.load_extensions(group="iotile.virtual_tile", product_name="virtual_tile", name_filter='envbsl_1',
                                              class_filter=EmulatedPeripheralTile, unique=True)

        tile = tile_factory(11, {}, self)
        self.add_tile(11, tile)
