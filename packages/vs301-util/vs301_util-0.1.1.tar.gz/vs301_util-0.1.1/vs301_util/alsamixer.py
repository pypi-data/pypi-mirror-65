from alsaaudio import Mixer

class Alsamixersetup:
    def __init__(self, dev='I2S4', subname='codec master mode', cardindex=1):
        self.mixer = Mixer(control=f'{dev} {subname}', cardindex=1)
    
    def getcurrentenum(self):
        return self.mixer.getenum()[0]
    
    def getenumlist(self):
        return self.mixer.getenum()[1]

    def setenum(self, name):
        idx = self.getenumlist().index(name)
        self.mixer.setenum(idx)



if __name__ == '__main__':
    mux = Alsamixersetup(subname='Mux')
    print(f'mux list : {mux.getenumlist()}')
    print(f'current enum : {mux.getcurrentenum()}')
    mux.setenum('ADMAIF1')
    print(f'current enum : {mux.getcurrentenum()}')

    codec = Alsamixersetup(subname='codec master mode')
    print(f'codec list : {codec.getenumlist()}')
    print(f'current enum : {codec.getcurrentenum()}')
    codec.setenum('cbs-cfs')
    print(f'current enum : {codec.getcurrentenum()}')
