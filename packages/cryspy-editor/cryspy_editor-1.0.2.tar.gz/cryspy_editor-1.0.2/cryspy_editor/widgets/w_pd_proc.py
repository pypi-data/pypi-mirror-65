import numpy
from PyQt5 import QtWidgets
from . import interactive_matrix
from . import interactive_graph_mod_mono
from . import interactive_graph_mod_pwd

from .interactive_graph_mod_pwd import cwidg_central as cwidg_pwd
from .FUNCTIONS import get_layout_rciftab_obj, del_layout
from .w_loop_constr import w_for_loop_constr

def w_for_pd_proc(obj, layout_11, layout_12, layout_13, layout_2, layout_3, w_output, thread):
    w_for_loop_constr(obj, layout_11, layout_12, layout_13, layout_2, layout_3, w_output, thread)
    del_layout(layout_3)

    stack_widg = QtWidgets.QStackedWidget()
    
    lay_grid = QtWidgets.QGridLayout()
    lay_grid.addWidget(QtWidgets.QLabel("sum"), 0, 1)
    lay_grid.addWidget(QtWidgets.QLabel("diff."), 0, 2)
    lay_grid.addWidget(QtWidgets.QLabel("up"), 0, 3)
    lay_grid.addWidget(QtWidgets.QLabel("down"), 0, 4)


    _rb_1 = QtWidgets.QRadioButton()
    _rb_1.toggled.connect(lambda: stack_widg.setCurrentIndex(0))
    lay_grid.addWidget(_rb_1, 1, 1)
    _rb_1.setChecked(True)

    _rb_2 = QtWidgets.QRadioButton()
    _rb_2.toggled.connect(lambda: stack_widg.setCurrentIndex(1))
    lay_grid.addWidget(_rb_2, 1, 2)

    _rb_3 = QtWidgets.QRadioButton()
    _rb_3.toggled.connect(lambda: stack_widg.setCurrentIndex(2))
    lay_grid.addWidget(_rb_3, 1, 3)

    _rb_4 = QtWidgets.QRadioButton()
    _rb_4.toggled.connect(lambda: stack_widg.setCurrentIndex(3))
    lay_grid.addWidget(_rb_4, 1, 4)


    _lay_1 = QtWidgets.QHBoxLayout()
    _lay_1.addLayout(lay_grid)
    _lay_1.addStretch(1)
    layout_3.addLayout(_lay_1)


    ttheta = obj.ttheta

    intensity_up = numpy.array(obj.intensity_up, dtype=float)
    intensity_up_sigma = numpy.array(obj.intensity_up_sigma, dtype=float)
    intensity_down = numpy.array(obj.intensity_down, dtype=float)
    intensity_down_sigma = numpy.array(obj.intensity_down_sigma, dtype=float)
    intensity_up_total = numpy.array(obj.intensity_up_total, dtype=float)
    intensity_down_total = numpy.array(obj.intensity_down_total, dtype=float)

    intensity_sum_total = intensity_up_total + intensity_down_total
    intensity_diff_total = intensity_up_total - intensity_down_total

    flag = all([_ is None for _ in obj.intensity_up])
    if flag:
        intensity_sum = numpy.array(obj.intensity, dtype=float)
        intensity_sum_sigma = numpy.array(obj.intensity_sum_sigma, dtype=float)
        intensity_diff = numpy.zeros(shape=intensity_sum.shape, dtype=float)
    else:
        intensity_sum = intensity_up + intensity_down
        intensity_diff = intensity_up - intensity_down
        intensity_sum_sigma = numpy.sqrt(intensity_up_sigma**2 + intensity_down_sigma**2)

    
    x = numpy.array(ttheta, dtype=float)

    widg_proj_u = cwidg_pwd()
    widg_proj_u.plot_file(x, [intensity_up_total], [intensity_up], [intensity_up_sigma])

    widg_proj_d = cwidg_pwd()
    widg_proj_d.plot_file(x, [intensity_down_total], [intensity_down], [intensity_down_sigma])

    widg_proj_sum = cwidg_pwd()
    widg_proj_sum.plot_file(x, [intensity_sum_total], [intensity_sum], [intensity_sum_sigma])

    widg_proj_diff = cwidg_pwd()
    widg_proj_diff.plot_file(x, [intensity_diff_total], [intensity_diff], [intensity_sum_sigma])


    stack_widg.addWidget(widg_proj_sum)
    stack_widg.addWidget(widg_proj_diff)
    stack_widg.addWidget(widg_proj_u)
    stack_widg.addWidget(widg_proj_d)

    stack_widg.setCurrentIndex(0)

    layout_3.addWidget(stack_widg)

    return 

