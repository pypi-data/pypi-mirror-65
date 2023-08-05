#
# Copyright (c) 2019 UAVCAN Development Team
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import typing
import pyuavcan


class SerialSession:
    def __init__(self, finalizer: typing.Callable[[], None]):
        self._close_finalizer: typing.Optional[typing.Callable[[], None]] = finalizer
        if not callable(self._close_finalizer):  # pragma: no cover
            raise TypeError(f'Invalid finalizer: {type(self._close_finalizer).__name__}')

    def close(self) -> None:
        fin = self._close_finalizer
        if fin is not None:
            self._close_finalizer = None
            fin()

    def _raise_if_closed(self) -> None:
        if self._close_finalizer is None:
            raise pyuavcan.transport.ResourceClosedError(f'Session is closed: {self}')
