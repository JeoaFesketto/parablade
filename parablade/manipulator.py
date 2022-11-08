import numpy as np

class BladeManipulator:
    def __init__(self, IN):
        self.IN = IN
        self.x_l = np.array(self.IN["x_leading"])
        self.y_l = np.array(self.IN["y_leading"])
        self.z_l = np.array(self.IN["z_leading"])

        self.x_t = np.array(self.IN["x_trailing"])
        self.z_t = np.array(self.IN["z_trailing"])

        self.t_i = np.array(self.IN["theta_in"])
        self.t_o = np.array(self.IN["theta_out"])
        self.stgr = np.array(self.IN["stagger"])

        self.chord = np.array(self.IN["CHORD"])
    
    def __setitem__(self):
        raise NotImplementedError(
            'This won\'t work, setting a value to a slice wont call the setter method and might cause errors down the '
            'line. Find another way to set the value. A possibility would be to create copy and modify that to '
            'finally set the copied and modified list directly.'
        )
    

    @property
    def x_l(self):
        return np.array(self.IN["x_leading"])
    @x_l.setter
    def x_l(self, value):
        self.IN["x_leading"], self._x_l = value.tolist(), value

    @property
    def y_l(self):
        return np.array(self.IN["y_leading"])
    @y_l.setter
    def y_l(self, value):
        self.IN["y_leading"], self._y_l = value.tolist(), value

    @property
    def z_l(self):
        return np.array(self.IN["z_leading"])
    @z_l.setter
    def z_l(self, value):
        self.IN["z_leading"], self._z_l = value.tolist(), value

    @property
    def x_t(self):
        return np.array(self.IN["x_trailing"])
    @x_t.setter
    def x_t(self, value):
        self.IN["x_trailing"], self._x_t = value.tolist(), value

    @property
    def z_t(self):
        return np.array(self.IN["z_trailing"])
    @z_t.setter
    def z_t(self, value):
        self.IN["z_trailing"], self._z_t = value.tolist(), value

    @property
    def t_i(self):
        return np.array(self.IN["theta_in"])
    @t_i.setter
    def t_i(self, value):
        self.IN["theta_in"], self._t_i = value.tolist(), value

    @property
    def t_o(self):
        return np.array(self.IN["theta_out"])
    @t_o.setter
    def t_o(self, value):
        self.IN["theta_out"], self._t_o = value.tolist(), value

    @property
    def stgr(self):
        return np.array(self.IN["stagger"])
    @stgr.setter
    def stgr(self, value):
        self.IN["stagger"], self._stgr = value.tolist(), value

    @property
    def chord(self):
        return np.array(self.IN["CHORD"])
    @chord.setter
    def chord(self, value):
        self.IN["CHORD"], self._chord = value.tolist(), value