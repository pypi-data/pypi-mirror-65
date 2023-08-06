from loguru import logger

import usb.core 
import usb.util

from pyudev import Context, Monitor, MonitorObserver

class USBEthInfo:
    port = None
    eth = None
    state = None
    manufacturer = None
    product = None

    def __repr__(self):
        return f'usb{self.port}({self.eth}) [{self.manufacturer}:{self.product}]: {self.state} '


class USBEthFinder:
    ctx = Context()
    func = None

    def __init__(self, subsystem='net'):
        self.mon = Monitor.from_netlink(self.ctx)
        self.mon.filter_by(subsystem=subsystem)
        #self.search(subsystem=subsystem)

    def search(self,subsystem='net'):
        infos = []
        for device in self.ctx.list_devices(subsystem=subsystem):
            info = self.parsingpath(device)
            logger.info(info)
            infos.append(info)
        return infos

    def parsingpath(self, device):
        path = device.device_path.split('/')
        try:
            idx = path.index('usb1')
        except ValueError:
            info = USBEthInfo()
            info.eth = path[-1]
            return info
        else:
            info = USBEthInfo()
            
            devname = path[-1]
            usbpath = path[idx+2].split('.')
            hubnum = int(usbpath[0][2])
            usbport = int(usbpath[1])
            action = device.action

            info.port = usbport
            info.eth = devname
            info.state = action

            if action != 'remove':
                port_number = (hubnum,usbport)
                if usbport == 0:
                    port_number = (hubnum,)                
                usbinfo = usb.core.find(find_all=True, bus=1, port_numbers=port_number)
                for dev in usbinfo:
                    try:
                        info.manufacturer = dev.manufacturer
                        info.product = dev.product
                    except:
                        pass
                    logger.debug(info)
            
            return info

    def observe(self, device):
        info = self.parsingpath(device)
        logger.info(info)
        if callable(self.func):
            self.func(info)

    def regster_callback(self, func=None):
        if func:
            self.func = func
        self.observer = MonitorObserver(self.mon, callback=self.observe, name='monitor-observer')

    def start(self):
        self.observer.start()

if __name__ == '__main__':
    def showdev(info):
        print(info)
    finder = USBEthFinder()
    finder.regster_callback(showdev)
    finder.start()
    finder.observer.join()

    # dev_bus = usb.core.find(find_all=True, bus=1)
    # for dev in dev_bus :
    #     if dev.bDeviceClass != 0x09:
    #         print('##################')
    #         print(f'{dev.manufacturer}:{dev.product} - port : {dev.port_numbers}, class : {dev.bDeviceClass}')
