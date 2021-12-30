import time

import usb.core

import controller.data.commands as commands
import controller.data.parser as parser
import controller.exception.CommunicationException
import controller.exception.DeviceNotConnectedException


class ChargerController:
    def __init__(self, usb_device):
        self.get_channel_info = self.wrap_function(self.get_channel_info)
        self.start_charge_lipo = self.wrap_function(self.start_charge_lipo)
        self.start_storage_lipo = self.wrap_function(self.start_storage_lipo)
        self.stop_charge = self.wrap_function(self.stop_charge)
        self.usb_device_serial = usb_device.iSerialNumber
        self.usb_device = None
        self.exception_count = 0
        self.init_device()

    def init_device(self):
        for attempt in range(1, 4):
            self.usb_device = usb.core.find(iSerialNumber=self.usb_device_serial)
            if self.usb_device is not None: break
            time.sleep(attempt * 0.1)
        if self.usb_device is None:
            raise controller.exception.DeviceNotConnectedException.DeviceNotConnectedException('device not found')
        if self.usb_device.is_kernel_driver_active(0):
            print('detaching kernel driver')
            self.usb_device.detach_kernel_driver(0)
        self.usb_device.set_configuration()

    def wrap_function(self, function):
        def call_with_retries(*args, **kwargs):
            last_exception = None
            for retry in range(1, 4):
                try:
                    if self.usb_device is None:
                        raise usb.core.USBError('device not connected', 5, 19)
                    return function(*args, **kwargs)
                except usb.core.USBError as e:
                    self.exception_count += 1
                    print(f'call exception, sleeping for {retry * 100}ms before retry')
                    if e.errno == 19: # device disconnected
                        print('restarting device')
                        self.init_device()
                    last_exception = e
                    time.sleep(retry * 0.1)
            raise last_exception
        return call_with_retries

    def set_use_balance_leads(self, channel_num: int, use_balance_leads: bool):
        payload = commands.set_use_balance_leads(channel_num, use_balance_leads)
        self.usb_device.write(0x01, payload)
        response = self.usb_device.read(0x81, 64)

    def get_channel_info(self, channel_num: int):
        payload = commands.get_channel_status(channel_num)
        self.usb_device.write(0x01, payload)
        response = self.usb_device.read(0x81, 64)
        return parser.parse_channel_status(response)

    def start_charge_lipo(self, channel_num: int, cell_count: 4, charge_current_ma: int):
        payload = commands.start_charge_lipo(channel_num, cell_count, charge_current_ma)
        self.usb_device.write(0x01, payload)
        response = self.usb_device.read(0x81, 64)

    def start_storage_lipo(self, channel_num: int, cell_count: 4, discharge_current_ma: int):
        payload = commands.start_storage_lipo(channel_num, cell_count, discharge_current_ma)
        self.usb_device.write(0x01, payload)
        response = self.usb_device.read(0x81, 64)

    def stop_charge(self, channel_num: int = -1):
        payload = commands.stop_charge(channel_num)
        self.usb_device.write(0x01, payload)
        response = self.usb_device.read(0x81, 64)
