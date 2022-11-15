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

        for side in ['upper', 'lower']:
            for i in range(1, 7):
                self.__setattr__(f't_{side[0]}{i}', np.array(self.IN[f'thickness_{side}_{i}']))

    
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

    @property
    def t_u1(self):
        return np.array(self.IN['thickness_upper_1'])
    @t_u1.setter
    def t_u1(self, value):
        self.IN['thickness_upper_1'], self._t_u1 = value.tolist(), value
    
    @property
    def t_u2(self):
        return np.array(self.IN['thickness_upper_2'])
    @t_u2.setter
    def t_u2(self, value):
        self.IN['thickness_upper_2'], self._t_u2 = value.tolist(), value
    
    @property
    def t_u3(self):
        return np.array(self.IN['thickness_upper_3'])
    @t_u3.setter
    def t_u3(self, value):
        self.IN['thickness_upper_3'], self._t_u3 = value.tolist(), value
    
    @property
    def t_u4(self):
        return np.array(self.IN['thickness_upper_4'])
    @t_u4.setter
    def t_u4(self, value):
        self.IN['thickness_upper_4'], self._t_u4 = value.tolist(), value
    
    @property
    def t_u5(self):
        return np.array(self.IN['thickness_upper_5'])
    @t_u5.setter
    def t_u5(self, value):
        self.IN['thickness_upper_5'], self._t_u5 = value.tolist(), value

    @property
    def t_u6(self):
        return np.array(self.IN['thickness_upper_6'])
    @t_u6.setter
    def t_u6(self, value):
        self.IN['thickness_upper_6'], self._t_u6 = value.tolist(), value
    
    @property
    def t_l1(self):
        return np.array(self.IN['thickness_lower_1'])
    @t_l1.setter
    def t_l1(self, value):
        self.IN['thickness_lower_1'], self._t_l1 = value.tolist(), value
    
    @property
    def t_l2(self):
        return np.array(self.IN['thickness_lower_2'])
    @t_l2.setter
    def t_l2(self, value):
        self.IN['thickness_lower_2'], self._t_l2 = value.tolist(), value
    
    @property
    def t_l3(self):
        return np.array(self.IN['thickness_lower_3'])
    @t_l3.setter
    def t_l3(self, value):
        self.IN['thickness_lower_3'], self._t_l3 = value.tolist(), value
    
    @property
    def t_l4(self):
        return np.array(self.IN['thickness_lower_4'])
    @t_l4.setter
    def t_l4(self, value):
        self.IN['thickness_lower_4'], self._t_l4 = value.tolist(), value
    
    @property
    def t_l5(self):
        return np.array(self.IN['thickness_lower_5'])
    @t_l5.setter
    def t_l5(self, value):
        self.IN['thickness_lower_5'], self._t_l5 = value.tolist(), value
    
    @property
    def t_l6(self):
        return np.array(self.IN['thickness_lower_6'])
    @t_l6.setter
    def t_l6(self, value):
        self.IN['thickness_lower_6'], self._t_l6 = value.tolist(), value
    