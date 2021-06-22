import time
import controller.ChargerController
import usb.core

charger = usb.core.find(idVendor=0, idProduct=1)

controller = controller.ChargerController.ChargerController(charger)

controller.start_charge_lipo(0, 4, 100)

exit()

# controller.start_storage_lipo(3, 4, 600)
while True:
    for i in range(4):
        # controller.start_charge_lipo(i, i + 1, (i + 1) * 200)
        print(f'{i}: {controller.get_channel_info(i)}')
        print(f'exception count: {controller.exception_count}')
        time.sleep(0.2)
# time.sleep(1)
# controller.stop_charge()
