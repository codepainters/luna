#
# This file is part of LUNA.
#

import logging

from nmigen.vendor.lattice_ecp5 import LatticeECP5Platform

from .luna_r0_1 import LUNAPlatformRev0D1
from .luna_r0_2 import LUNAPlatformRev0D2


# Stores the latest platform; for reference / automagic.
LATEST_PLATFORM = LUNAPlatformRev0D2


# Table mapping LUNA revision numbers to their platform objects.
PLATFORM_FOR_REVISION = {
    (0, 1): LUNAPlatformRev0D1,
    (0, 2): LUNAPlatformRev0D2
}


def get_appropriate_platform() -> LatticeECP5Platform:
    """ Attempts to return the most appropriate platform for the local configuration. """

    from ... import apollo

    try:
        # Figure out what hardware revision we're going to connect to...
        debugger = apollo.ApolloDebugger()
        version = debugger.detect_connected_version()

        # ... and look up the relevant platform accordingly.
        platform = PLATFORM_FOR_REVISION[version]()

        # Finally, override the platform's device type with the FPGA we detect
        # as being present on the relevant board. (Note that this auto-detection
        # only works if we're programming a connected device; otherwise, we'll
        # need to use the custom-platform environment variables.)
        platform.device = debugger.get_fpga_type()
        return platform


    # If we don't have a connected platform, fall back to the latest platform.
    except apollo.DebuggerNotFound:
        platform = LATEST_PLATFORM()

        logging.warning(f"Couldn't auto-detect connected platform. Assuming {platform.name}.")
        return platform
