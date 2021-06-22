def parse_channel_status(data: list):
    if data[0] != 15:
        raise RuntimeError(f'data[0] is not 15: {data[0]}')
    if data[2] != 85:
        raise RuntimeError(f'response type is not channel_status_info: {data[2]}')

    capacity = get_short(data, 5)
    duration = get_short(data, 7)
    voltage = get_short(data, 9)
    electricity = get_short(data, 11)
    external_temp = get_byte(data, 13)
    internal_temp = get_byte(data, 14)
    internal_resistance = get_short(data, 15)
    cells = [
        get_short(data, 17),
        get_short(data, 19),
        get_short(data, 21),
        get_short(data, 23),
        get_short(data, 25),
        get_short(data, 27),
    ]

    return {
        'duration': duration,
        'voltage': max(voltage, 100),
        'capacity': capacity,
        'current_ma': electricity,
        'external_temp': external_temp,
        'internal_temp': internal_temp,
        'internal_resistance': internal_resistance,
        'cells': cells,
    }


def get_short(data: list, index: int):
    return int.from_bytes(data[index:index + 2], 'big')


def get_byte(data: list, index: int):
    return data[index]
