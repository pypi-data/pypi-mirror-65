"""
antimait is a library made of tools to ease the implementation of IoT automation systems based on devices such as
Arduino and ESP. It offers tools to connect to them through different communication protocols and means and to
analyze data collected from various sources.
"""

import serial  # type: ignore
from serial.tools import list_ports  # type: ignore

from abc import ABC, abstractmethod
from threading import Thread
from typing import List, Dict, Set, Optional
from typing_extensions import Protocol

from enum import Enum

import logging
import time
import sys


__all__ = ["com_interfaces", "Comm", "DataReceiver", "CommInterface", "SerialInterface", "Printer", "Gateway"]

DEFAULT_BAUD = 9600


def com_interfaces() -> Dict[str, str]:
    """
    Returns a dict containing information about the devices connected through the comport
    Returns:

    """
    return {ifc.device: ifc.description for ifc in list_ports.comports()}


class Comm(Enum):
    """
    Enum that ties in with the action parameter in the DataReceiver/Source
    classes.
    """
    CLOSING = 0
    DATA = 1


class DataReceiver(ABC):
    """
    An abstract class that defines the Observer part of the Observe pattern
    for data sources and objects that received data on arrival.
    """
    @abstractmethod
    def update(self, action: Comm, **update: str) -> None:
        """

        Args:
            action (Comm): an instance of the Comm enum to specify what action occurred.
            **update (str): used to customize the update mechanism. If action == Comm.DATA, the data kw must be used.

        Returns:
            None
        """
        pass


class DataSource:
    """
    Conecrete class that defines the Observable part of the Observe pattern.
    All CommInterfaces are also DataSources.
    """
    def __init__(self):
        self._receivers: List[DataReceiver] = []

    def attach(self, rec: DataReceiver) -> None:
        """
        Attaches a receiver to this DataSource and notifies it everytime an action is performed.
        Args:
            rec (DataReceiver): the new receiver.

        Returns:
            None
        """
        self._receivers.append(rec)

    def detach(self, rec: DataReceiver) -> None:
        """
        Detaches, if present, the passed receiver.
        Args:
            rec (DataReceiver): the receiver to detach.

        Returns:
            None
        """
        if rec in self._receivers:
            self._receivers.remove(rec)

    def notify(self, action: Comm, **update: str) -> None:
        """
        Notifies a receiver that either data has been received or that the source is
        closing.
        Args:
            action (Comm): an instance of the Comm enum to specify what action occurred.
            **update (str): used to customize the update mechanism. If action == Comm.DATA, the data kw must be used.

        Returns:
            None
        """
        for receiver in self._receivers:
            receiver.update(action, **update)


class CommInterface(ABC, DataSource):
    """
    An abstract class that represents a generic communication interface. A way to acquire data and to
    stop the process must be specified by any inherithing class.
    """

    @property
    @abstractmethod
    def ifc_id(self) -> str:
        """
        Returns:
            str, an identifier in the format communicationtype_interfacename.
            e.g. serial_COM5
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the Communication Interface.
        Returns:
            None
        """
        pass

    @abstractmethod
    def send(self, msg: str) -> None:
        """
        Forwards a message to the device identified by this
        interface. May not always be implemented.
        Args:
            msg (str): the message to forward to the device.

        Returns:
            None
        """
        pass

    @abstractmethod
    def listen(self) -> None:
        """
        Listens for incoming data. This method is non-blocking and spawns a
        new Thread that handles the data.
        Returns:
            None
        """
        pass

    @abstractmethod
    def listen_forever(self) -> None:
        """
        Listens for incoming data. This method is a blocking version of CommInterface.listen.
        Returns:
            None
        """
        pass


class SerialInterface(CommInterface):
    def __init__(self, port: str, baud_rate: int = None):
        """
        Constructs a new serial interface based on serial.Serial.
        When listening for serial data, this class uses the Observer pattern to notify that new
        data has been acquired. It is passed through the DataSource.notify method to any observer,
        under the data keyword.
        Args:
            port (str): the serial port from which reading the data.
            baud_rate (int): the baud rate, the default value is specified in DEFAULT_BAUD = 9600.
        """
        super().__init__()
        self._port: str = port
        self._baud_rate: int = baud_rate or DEFAULT_BAUD
        self._listening: bool = False
        try:
            self._serial: serial.Serial = serial.Serial(port=self._port, baudrate=self._baud_rate)
        except Exception as e:
            raise e

    @property
    def ifc_id(self):
        return self._port

    def _poll(self) -> None:
        """
        The method implementing the polling routine that reads from the serial port.
        Returns:
            None
        """
        if self._listening:
            return

        self._listening = True
        try:
            while self._listening:
                data = self._serial.readline()
                self.notify(action=Comm.DATA, data=data.decode())
        except serial.SerialException:
            logging.error("Serial error, closing interface")
            self.listen()
        except UnicodeDecodeError as ude:
            logging.error(ude)
            self.listen()

    def close(self) -> None:
        self._listening = False
        self.notify(action=Comm.CLOSING)

    def send(self, msg: str) -> None:
        self._serial.write(msg.encode())

    def listen(self) -> None:
        Thread(target=self._poll).start()

    def listen_forever(self) -> None:
        self._poll()


class Printer(DataReceiver):
    """
    A simple receiver class that serves as an example for other receiver implementations.
    This just prints whatever it receives.
    """
    def update(self, action: Comm, **update: str) -> None:
        if action == Comm.DATA:
            if "data" in update:
                print("Printing data: {}".format(update["data"]))
            else:
                logging.error("data keyword not passed!")
        elif action == Comm.CLOSING:
            logging.info("Printer closing")


class SerialPort:
    """
    This class is used internally in the Gateway class to have an hashable
    container for serial ports informations.
    """
    def __init__(self, port: str, description: str):
        self._port: str = port
        self._description: str = description

    @property
    def port(self):
        return self._port

    @property
    def description(self):
        return self._description

    def __repr__(self) -> str:
        return "SerialPort({}, {})".format(self._port, self._description)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SerialPort):
            return False
        if self is other:
            return True
        return self._port == other._port and self._description == other._description

    def __hash__(self) -> int:
        return hash(str(hash(self._port)) + str(hash(self._description)))


class OnConnect(Protocol):
    def __call__(self, interface: CommInterface, description: str) -> None:
        pass


class Gateway:
    """
    A gateway class that handles serial connections.
    """
    _MONITOR_DELAY: int = 1  # seconds

    def __init__(self):
        self._interfaces: Dict[str, CommInterface] = {}
        self._serial_ports: Set[SerialPort] = set()
        self._started: bool = True

    on_connect: Optional[OnConnect] = None
    """
    on_connect callable that defaults to None. Redefine to give a custom on_connect 
    behaviour to the gateway object.
    """

    @property
    def interfaces(self) -> List[CommInterface]:
        """
        Returns:
           List[CommInterface], a list of the interfaces connected at this time
        """
        return list(self._interfaces.values())

    def _on_connect(self, interface: CommInterface, description: str) -> None:
        """
        Do not touch this method. This checks for the user defined on_connect to call as
        a callback when a new device goes up.
        Args:
            interface (CommInterface): the interface that is connecting.
            description (str): a string containing information about the interface.

        Returns:
            None
        """
        try:
            if self.on_connect is not None:
                self.on_connect(interface, description)
        except TypeError:
            logging.error("Wrong parameters for the custom on_connect method.")
            sys.exit(1)

    def _serial_monitor(self) -> None:
        """
        The serial devices loop.
        Every time interval (defined in _MONITOR_DELAY) a read of the serial devices connected to the
        machine is performed; new devices are attached and devices that are no longer connected get killed.
        Returns:
            None
        """
        while self._started:
            devices = {SerialPort(portinfo.device, portinfo.description) for portinfo in list_ports.comports()}
            to_remove: Set[SerialPort] = self._serial_ports.difference(devices)
            to_add: Set[SerialPort] = devices.difference(self._serial_ports)

            if to_remove:
                for elem_rem in to_remove:
                    self._interfaces[elem_rem.port].close()
                    self._interfaces.pop(elem_rem.port, None)
                    self._serial_ports.discard(elem_rem)
                    logging.info("Serial interface {} ({}) disconnected.".format(elem_rem.port, elem_rem.description))

            if to_add:
                for elem_add in to_add:
                    self._serial_ports.add(elem_add)
                    new_interface = SerialInterface(elem_add.port)
                    self._on_connect(new_interface, elem_add.description)
                    new_interface.listen()
                    self._interfaces[elem_add.port] = new_interface
                    logging.info("Serial interface {} ({}) connected.".format(elem_add.port, elem_add.description))

            time.sleep(self._MONITOR_DELAY)

    def close(self):
        """
        Closes the gateway, ending the serial loop.
        Returns:
            None
        """
        self._started = False
        for interface in self._interfaces:
            self._interfaces[interface].close()

    def forward(self, dest: str, msg: str) -> None:
        """
        Forwards a string message to the device connected through the interface identified by dest.
        Args:
            dest: the id of the interface to which you're forwarding data.
            msg: the message being sent.

        Returns:
            None
        """
        try:
            self._interfaces[dest].send(msg)
        except KeyError:
            raise KeyError("No such interface!")

    def broadcast(self, msg: str) -> None:
        """
        Broadcasts a string message to each interface connected.
        Args:
            msg: the message being broadcasted.

        Returns:
            None
        """

        for interface_id in self._interfaces:
            self._interfaces[interface_id].send(msg)

    def listen(self):
        """
        Non blocking listen method for the gateway.
        Returns:
            None
        """
        Thread(target=self._serial_monitor).start()

    def listen_forever(self):
        """
        Blocking listen method for the gateway.
        Returns:
            None
        """
        self._serial_monitor()
