CHANNEL_NUM_ALL = -1

def get_system_info(channel_num: int):
    return create_packet(90, channel_num)


def get_channel_status(channel_num: int):
    return create_packet(85, channel_num)


def get_voltage(channel_num: int):
    return create_packet(88, channel_num)


def set_use_balance_leads(channel_num: int, use_balance_leads: bool):
    return create_packet(0x11, channel_num, [0x06, 0x01 if use_balance_leads else 0x00, 0x00, 0x00])


def start_charge(channel_num: int, battery_type: int, charge_type: int, cell_count: 4, charge_current_ma: int, discharge_current_ma: int, voltage_limit_lower: int, voltage_limit_upper: int):
    payload = []
    payload.append(battery_type)
    payload.append(cell_count)
    payload.append(charge_type)
    payload.append(int(charge_current_ma / 100))
    payload.append(int(discharge_current_ma / 100)) # discharge rate, should not be needed
    payload += from_short(voltage_limit_lower) # lower voltage limit
    payload += from_short(voltage_limit_upper) # uppper voltage limit
    payload += from_short(0) # dunno
    payload += from_short(0) # trickle charge
    payload.append(0x0A)
    payload.append(0x04)
    payload += [0x00, 0x00, 0x00, 0x00]
    return create_packet(0x05, channel_num, payload)


def start_charge_lipo(channel_num: int, cell_count: int, charge_current_ma: int):
    return start_charge(channel_num, 0, 1, cell_count, charge_current_ma, 100, 3200, 4200)


def start_storage_lipo(channel_num: int, cell_count: int, discharge_current_ma: int):
    return start_charge(channel_num, 0, 3, cell_count, discharge_current_ma, discharge_current_ma, 3200, 4200)


def stop_charge(channel_num: int = -1):
    if channel_num == -1:
        return create_packet(0xFE, CHANNEL_NUM_ALL)
    return create_packet(0xFE, channel_num)


def create_packet(type: int, channel_num: int, data=None):
    if data is None:
        data = []
    channel_num = 0xFF if channel_num == -1 else 1 << channel_num
    payload = [15, len(data) + 3, type, channel_num] + data
    checksum = 0
    for i in range(2, len(payload)):
        checksum += payload[i]
    payload.append(checksum & 0xFF)
    return payload + [0] * (64 - len(payload))


def from_short(value: int):
    return value.to_bytes(2, 'big')


if __name__ == '__main__':
    packet = set_use_balance_wire(3, False)
    pass