# -*- encoding: utf-8 -*-
"""
@File    : state_machine.py
@Time    : 2020/4/4 10:23
@Author  : Fantuan
@Software: PyCharm
"""
from transitions import Machine
class TankMachine(object):
    pass

model=TankMachine()
states=['shot','move','garrison']
transitions=[
    {'trigger':'defense','source':'garrison','dest':'shot'},
    {'trigger':'security','source':'garrison','dest':'move'},
    {'trigger':'defense','source':'move','dest':'shot'},
    # {'trigger':'','source':'','dest':''},
    # {'trigger':'','source':'','dest':''},
]
machine = Machine(model=model, states=states, transitions=transitions, initial='garrison')

if __name__ == "__main__":
    pass
    # print model.state
    # model.security()
    # print model.state
    # print model.is_move()
    # model.to_garrison()
    # print model.state
