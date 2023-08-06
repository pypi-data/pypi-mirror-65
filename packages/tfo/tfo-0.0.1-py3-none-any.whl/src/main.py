class ThinFilm_model:
    def __init__(self, ambient, thinfilm, substrate, wl, angle = 0):
        self.wavelength = wl
        self.ambient = chromatic_n(ambient['a'], self.wavelength)
        self.substrate = chromatic_n(substrate['s'], self.wavelength)
        self.thinfilm = thinfilm
        self.angle = angle*pi/180