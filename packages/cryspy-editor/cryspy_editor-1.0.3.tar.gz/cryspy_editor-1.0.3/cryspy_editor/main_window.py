# -*- coding: utf-8 -*-
__author__ = 'ikibalin'
__version__ = "2020_03_05"

import os
import os.path
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from cryspy_editor.b_rcif_to_cryspy import rcif_to_cryspy
from cryspy_editor.widgets.FUNCTIONS import show_widget
from cryspy_editor.widgets.w_data_constr import w_for_data_constr
from cryspy_editor.widgets.w_global_constr import w_for_global_constr
from cryspy_editor.widgets.w_item_constr import w_for_item_constr
from cryspy_editor.widgets.w_loop_constr import w_for_loop_constr
from cryspy_editor.widgets.w_meas_inelasticl import w_for_meas_inelasticl
from cryspy_editor.widgets.w_pd2d_meas import w_for_pd2d_meas
from cryspy_editor.widgets.w_pd2d_proc import w_for_pd2d_proc
from cryspy_editor.widgets.w_pd_peak import w_for_pd_peak
from cryspy_editor.widgets.w_pd_meas import w_for_pd_meas
from cryspy_editor.widgets.w_pd_proc import w_for_pd_proc
from cryspy_editor.widgets.w_pd import w_for_pd
from cryspy_editor.widgets.w_diffrn_refln import w_for_diffrn_refln
from pycifstar import Data, Global, Item, Items, Loop, to_global

from cryspy_editor.widgets.w_item import w_for_item

try:
    FLAG_CRYSPY = True
    from cryspy_editor.widgets.FUNCTIONS import del_layout
    from cryspy.common.cl_global_constr import GlobalConstr
    from cryspy.common.cl_global_constr import DataConstr
    from cryspy.common.cl_loop_constr import LoopConstr
    from cryspy.common.cl_item_constr import ItemConstr

    from cryspy.scripts.cl_rhochi import RhoChi
    from cryspy.cif_like.cl_crystal import Crystal
    from cryspy.cif_like.cl_pd import Pd
    from cryspy.cif_like.cl_pd2d import Pd2d
    from cryspy.cif_like.cl_diffrn import Diffrn
    from cryspy.cif_like.cl_diffrn_refln import DiffrnReflnL 

    from cryspy.pd1dcif_like.cl_pd_peak import PdPeakL
    from cryspy.pd1dcif_like.cl_pd_meas import PdMeasL
    from cryspy.pd1dcif_like.cl_pd_proc import PdProcL
    from cryspy.pd2dcif_like.cl_pd2d_meas import Pd2dMeas
    from cryspy.pd2dcif_like.cl_pd2d_proc import Pd2dProc
except ImportError:
    FLAG_CRYSPY = False

try:
    FLAG_MAGREF = True
    from magref import CrystRef
    from magref.classes.cl_cryst_field import CrystField
    from magref.classes.cl_meas_inelastic import MeasInelasticL
except ImportError:
    FLAG_MAGREF = False

try:
    FLAG_MEM = True
    from lib_mem.mem.cl_density import Density
    from lib_mem.scripts.cl_mem_tensor import MemTensor
except ImportError:
    FLAG_MEM = False






class MyThread(QtCore.QThread):
    signal_start = QtCore.pyqtSignal()
    signal_end = QtCore.pyqtSignal()
    signal_refresh = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message = None
        self.function = None
        self.arguments = None
        self.output = None

    def run(self):
        l_message = []
        self.signal_start.emit()
        arg = self.arguments
        func = self.function
        out = func(*arg)
        self.output = out
        self.signal_end.emit()


class cbuilder(QtWidgets.QMainWindow):
    def __init__(self, f_dir_data=os.path.dirname(__file__)):
        super(cbuilder, self).__init__()

        self.__f_dir_prog = os.path.dirname(__file__)
        self.__f_dir_data = f_dir_data
        self.__f_file = None
        if os.path.isfile(f_dir_data):
            self.__f_file = f_dir_data
            self.__f_dir_data = os.path.dirname(f_dir_data)
        self.__mode = "star"

        self.def_actions()
        self.init_widget()
        self.setWindowTitle(f'CrysPy editor')

        if self.__f_file is not None:
            self.to_star()
        self.show()

    def def_actions(self):
        f_dir_prog = self.__f_dir_prog
        f_dir_prog_icon = os.path.join(f_dir_prog, 'f_icon')
        self.setWindowIcon(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'icon.png')))

        open_action = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'open.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open file')
        open_action.triggered.connect(self.open)

        to_star_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'to_star.png')), 'S&TAR mode',
                                           self)
        to_star_action.setStatusTip('Switch on STAR mode')
        to_star_action.triggered.connect(self.to_star)

        if FLAG_CRYSPY:
            to_cryspy_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'to_cryspy.png')),
                                                 '&CrysPy mode', self)
            to_cryspy_action.setStatusTip('Switch on CrysPy mode')
            to_cryspy_action.triggered.connect(self.to_cryspy)

            to_rhochi_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'to_rhochi.png')),
                                                 '&RhoChi mode', self)
            to_rhochi_action.setStatusTip('Switch on RhoChi mode')
            to_rhochi_action.triggered.connect(self.to_rhochi)

        if FLAG_MEM:
            to_mem_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'to_mem.png')), '&MEM mode',
                                              self)
            to_mem_action.setStatusTip('Switch on MEM mode')
            to_mem_action.triggered.connect(self.to_mem)

        if FLAG_MAGREF:
            to_magref_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'to_magref.png')),
                                                 'M&agRef mode', self)
            to_magref_action.setStatusTip('Switch on Magref mode')
            to_magref_action.triggered.connect(self.to_magref)

        save_action = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'save.png')), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save')
        save_action.triggered.connect(self.save)

        save_as_action = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'save_as.png')), 'Save &as...',
                                           self)
        save_as_action.setStatusTip('Save as ...')
        save_as_action.triggered.connect(self.save_as)

        open_folder = QtWidgets.QAction(QtGui.QIcon(os.path.join(f_dir_prog_icon, 'open_folder.png')), 'Open folder',
                                        self)
        open_folder.setStatusTip('Open folder')
        open_folder.triggered.connect(self.open_folder)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(open_action)
        fileMenu.addAction(to_star_action)
        if FLAG_CRYSPY:
            fileMenu.addAction(to_cryspy_action)
            fileMenu.addAction(to_rhochi_action)
        if FLAG_MEM:
            fileMenu.addAction(to_mem_action)
        if FLAG_MAGREF:
            fileMenu.addAction(to_magref_action)
        fileMenu.addAction(save_action)
        fileMenu.addAction(save_as_action)

        self.toolbar = self.addToolBar("Open")
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(to_star_action)
        if FLAG_CRYSPY:
            self.toolbar.addAction(to_cryspy_action)
            self.toolbar.addAction(to_rhochi_action)
        if FLAG_MEM:
            self.toolbar.addAction(to_mem_action)
        if FLAG_MAGREF:
            self.toolbar.addAction(to_magref_action)
        self.toolbar.addAction(save_action)
        self.toolbar.addAction(save_as_action)
        self.toolbar.addAction(open_folder)

    def init_widget(self):
        """
module is reloaded for cwidget
        """
        self.location_on_the_screen()
        self.__widg_central = cwidget(self.info_width, self.info_height)
        self.setCentralWidget(self.__widg_central)

    def location_on_the_screen(self):
        """
        position and size of main window
        """
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setMinimumSize(screen.width() * 1 / 4, screen.height() * 1 / 4)
        self.info_width = screen.width() * 8. / 10.
        self.info_height = screen.height() * 14. / 16.
        self.move(screen.width() / 10, screen.height() / 20)
        self.resize(screen.width() * 8. / 10., screen.height() * 14. / 16.)

    def calc_is_finished(self):
        m_box = QtWidgets.QMessageBox()
        m_box.setIcon(QtWidgets.QMessageBox.Information)
        m_box.setText("Calculations are finished")
        m_box.setWindowTitle("Message")
        m_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        m_box.exec()
        if self.__mode == "rhochi":
            self.to_rhochi()
        elif self.__mode == "mem":
            self.to_mem()
        elif self.__mode == "magref":
            self.to_magref()

    def to_star(self):
        if self.__widg_central._star is not None:
            star_ = self.__widg_central._star
        elif self.__f_file is not None:
            star_ = to_global(self.__f_file)
        else:
            f_file_data_new, okPressed = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a cif file:',
                                                                               self.__f_dir_data, "All files (*.*)")
            if not (okPressed):
                return None
            star_ = to_global(f_file_data_new)
            self.__f_file = f_file_data_new
            self.__f_dir_data = os.path.dirname(f_file_data_new)
        self.__mode = "star"
        self.__widg_central.form_cpanel(star_)

    def to_cryspy(self):
        mode_orig = self.__mode
        flag = True
        cryspy_obj = None
        str_obj = None
        if mode_orig == "cryspy":
            cryspy_obj = self.__widg_central._object
        elif mode_orig == "star":
            obj = self.__widg_central._star
            if obj is not None:
                cryspy_obj = rcif_to_cryspy(obj)
        else:
            obj = self.__widg_central._object
            str_obj = str(obj.to_cif())
            star_obj = Global()
            star_obj.take_from_string(str_obj, f_dir=self.__f_dir_data)
            cryspy_obj = rcif_to_cryspy(star_obj)
        if cryspy_obj is None:
            cryspy_obj = GlobalConstr()
        if flag:
            self.__mode = "cryspy"
            cryspy_obj.file_input = self.__f_file
            self.__widg_central.form_cpanel(cryspy_obj)

    def to_rhochi(self):
        mode_orig = self.__mode
        flag = True
        cryspy_obj = None
        if mode_orig == "rhochi":
            cryspy_obj = self.__widg_central._object
        elif mode_orig == "star":
            obj = self.__widg_central._star
            if obj is not None:
                cryspy_obj = RhoChi.from_cif(str(obj))
        else:
            obj = self.__widg_central._object
            cryspy_obj = RhoChi.from_cif(obj.to_cif())
            if cryspy_obj is None:
                if mode_orig != "cryspy":
                    flag = False
        if cryspy_obj is None:
            cryspy_obj = RhoChi()
        if flag:
            self.__mode = "rhochi"
            cryspy_obj.file_input = self.__f_file
            self.__widg_central.form_cpanel(cryspy_obj)

    def to_mem(self):
        mode_orig = self.__mode
        flag = True
        cryspy_obj = None
        if mode_orig == "mem":
            cryspy_obj = self.__widg_central._object
        elif mode_orig == "star":
            obj = self.__widg_central._star
            if obj is not None:
                cryspy_obj = MemTensor.from_cif(str(obj))
        else:
            obj = self.__widg_central._object
            cryspy_obj = MemTensor.from_cif(obj.to_cif())
            if cryspy_obj is None:
                if mode_orig != "cryspy":
                    flag = False
        if cryspy_obj is None:
            cryspy_obj = MemTensor()
        if flag:
            self.__mode = "mem"
            cryspy_obj.file_input = self.__f_file
            self.__widg_central.form_cpanel(cryspy_obj)

    def to_magref(self):
        mode_orig = self.__mode
        flag = True
        cryspy_obj = None
        if mode_orig == "magref":
            cryspy_obj = self.__widg_central._object
        elif mode_orig == "star":
            obj = self.__widg_central._star
            if obj is not None:
                cryspy_obj = CrystRef.from_cif(str(obj))
        else:
            obj = self.__widg_central._object
            cryspy_obj = CrystRef.from_cif(obj.to_cif())
            if cryspy_obj is None:
                if mode_orig != "cryspy":
                    flag = False
        if cryspy_obj is None:
            cryspy_obj = CrystRef()
        if flag:
            self.__mode = "magref"
            cryspy_obj.file_input = self.__f_file
            self.__widg_central.form_cpanel(cryspy_obj)

    def save(self):
        f_name = self.__f_file
        if f_name is None:
            f_dir_data = self.__f_dir_data
            f_name = os.path.join(f_dir_data, "main.rcif")
        if self.__mode == "star":
            star_obj = self.__widg_central._star
            with open(f_name, "w") as fid:
                fid.write(str(star_obj))
        elif self.__mode in ["cryspy", "rhochi", "mem", "magref"]:
            cryspy_obj = self.__widg_central._object
            if cryspy_obj is None:
                return
            cryspy_obj.file_input = f_name
            if self.__mode == "cryspy":
                with open(f_name, "w") as fid:
                    fid.write(cryspy_obj.to_cif())
            else:
                cryspy_obj.save_to_file(f_name)
        return

    def save_as(self):
        f_name, okPressed = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a file:', self.__f_dir_data,
                                                                  "Rcif files (*.rcif)")
        if not (okPressed):
            return None
        self.__f_file = f_name
        self.__f_dir_data = os.path.dirname(f_name)
        os.chdir(os.path.dirname(f_name))
        self.save()

    def open_folder(self):
        os.startfile(self.__f_dir_data)

    def open(self):
        f_name, okPressed = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a cif file:', self.__f_dir_data,
                                                                  "All files (*.*)")
        if not (okPressed):
            return None
        self.__widg_central._star = None
        self.__widg_central._object = None
        self.__f_file = f_name
        self.__f_dir_data = os.path.dirname(f_name)
        os.chdir(os.path.dirname(f_name))
        mode_orig = str(self.__mode)
        self.to_star()
        if mode_orig == "cryspy":
            self.to_cryspy()
        elif mode_orig == "rhochi":
            self.to_rhochi()
        elif mode_orig == "mem":
            self.to_mem()
        elif mode_orig == "magref":
            self.to_magref()


class cwidget(QtWidgets.QSplitter):
    def __init__(self, width, height):
        self.info_width = width
        self.info_height = height
        super(cwidget, self).__init__()
        self._star = None
        self._object = None
        self.additional_thread = MyThread()
        self.additional_thread.signal_end.connect(self.end_of_calc_in_thread)
        self.additional_thread.signal_refresh.connect(self.refresh_wind)
        self.additional_thread.signal_start.connect(
            self.start_of_calc_in_thread)
        self.init_widget()

    def init_widget(self):
        """
        make central layout
        """
        width_m_1 = self.info_width / 6.
        width_m_2 = (5. * self.info_width) / 6.
        width_v_1 = self.info_height * 0.75
        width_v_2 = self.info_height * 0.25

        self.w_cpanel = QtWidgets.QWidget()
        self.w_cpanel.setLayout(QtWidgets.QVBoxLayout())

        self.w_cpanel.setAutoFillBackground(True)
        self.w_cpanel.setStyleSheet("background-color:light gray;")

        self.w_output = QtWidgets.QLabel()
        self.w_output.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                          QtWidgets.QSizePolicy.Expanding))
        self.w_output.setFont(QtGui.QFont("Courier", 8, QtGui.QFont.Normal))
        self.w_output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.w_output.setAlignment(QtCore.Qt.AlignTop)
        self.w_output.setWordWrap(True)

        self.w_tab = QtWidgets.QTabWidget()

        self.w_11 = QtWidgets.QWidget()
        self.w_11.setLayout(QtWidgets.QVBoxLayout())
        self.w_12 = QtWidgets.QWidget()
        self.w_12.setLayout(QtWidgets.QVBoxLayout())
        self.w_13 = QtWidgets.QWidget()
        self.w_13.setLayout(QtWidgets.QVBoxLayout())
        self.w_2 = QtWidgets.QWidget()
        self.w_2.setLayout(QtWidgets.QVBoxLayout())
        self.w_3 = QtWidgets.QWidget()
        self.w_3.setLayout(QtWidgets.QVBoxLayout())

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.w_11)
        layout_1.addWidget(self.w_12)
        layout_1.addWidget(self.w_13)
        w_1 = QtWidgets.QWidget()
        w_1.setLayout(layout_1)

        self.w_tab.addTab(w_1, "Parameters")
        self.w_tab.addTab(self.w_2, "RCIF")
        self.w_tab.addTab(self.w_3, "Optional")

        area = QtWidgets.QScrollArea()
        area.setWidgetResizable(True)
        area.setWidget(self.w_output)

        w_0 = QtWidgets.QWidget()
        w_0.setLayout(QtWidgets.QVBoxLayout())
        w_0.layout().addWidget(self.w_tab)

        lay_setting = QtWidgets.QHBoxLayout()
        self.w_loader = QtWidgets.QRadioButton(" calculations")

        self.w_loader.setChecked(False)

        lay_setting.addWidget(self.w_loader)
        lay_setting.addStretch(1)
        cb_1 = QtWidgets.QCheckBox()
        cb_1.setCheckState(2)
        lay_setting.addWidget(cb_1)
        cb_2 = QtWidgets.QCheckBox()
        cb_2.setCheckState(2)
        lay_setting.addWidget(cb_2)
        cb_3 = QtWidgets.QCheckBox()
        cb_3.setCheckState(2)
        lay_setting.addWidget(cb_3)
        w_0.layout().addLayout(lay_setting)

        cb_1.stateChanged.connect(lambda _1: show_widget(self.w_11, _1))
        cb_2.stateChanged.connect(lambda _1: show_widget(self.w_12, _1))
        cb_3.stateChanged.connect(lambda _1: show_widget(self.w_13, _1))

        w_out = QtWidgets.QWidget()
        w_out.setLayout(QtWidgets.QHBoxLayout())
        w_out.layout().addWidget(area)

        splitter_vert = QtWidgets.QSplitter()
        splitter_vert.setOrientation(QtCore.Qt.Vertical)
        splitter_vert.addWidget(w_0)
        splitter_vert.addWidget(w_out)
        splitter_vert.setSizes([width_v_1, width_v_2])

        self.addWidget(self.w_cpanel)
        self.addWidget(splitter_vert)
        self.setSizes([width_m_1, width_m_2])
        self.form_cpanel()

    def form_cpanel(self, obj=None):
        lay_cpanel = self.w_cpanel.layout()
        del_layout(lay_cpanel)

        if obj is None:
            obj = self._object
        if obj is not None:
            self._object = obj 
            w1 = QtWidgets.QTreeWidget()
            w1.setSizePolicy(QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
            w1.setColumnCount(1)
            w1.setHeaderHidden(True)

            wi = QtWidgets.QTreeWidgetItem()
            s_name = type(obj).__name__
            wi.setText(0, f"{s_name:}")
            wi._object = obj
            w1.addTopLevelItem(wi)
            if isinstance(obj, Global):
                self._star = obj
                for _loop in obj.loops:
                    wii = QtWidgets.QTreeWidgetItem()
                    if _loop.name != "":
                        wii.setText(0, f"loop_{_loop.name:}{_loop.prefix:}")
                    else:
                        wii.setText(0, f"loop{_loop.prefix:}")
                    wii._object = _loop
                    wii.setToolTip(0, _loop.__doc__)
                    wi.addChild(wii)
                for _item in obj.items:
                    wii = QtWidgets.QTreeWidgetItem()
                    wii.setText(0, _item.name)
                    wii._object = _item
                    wii.setToolTip(0, _item.__doc__)
                    wi.addChild(wii)
                for _data in obj.datas:
                    wi = QtWidgets.QTreeWidgetItem()
                    wi.setText(0, f"data_{_data.name}")
                    wi.setToolTip(0, _data.__doc__)
                    wi._object = _data
                    for _loop in _data.loops:
                        wii = QtWidgets.QTreeWidgetItem()
                        if _loop.name != "":
                            wii.setText(
                                0, f"loop_{_loop.name:}{_loop.prefix:}")
                        else:
                            wii.setText(0, f"loop{_loop.prefix:}")
                        wii._object = _loop
                        wii.setToolTip(0, _loop.__doc__)
                        wi.addChild(wii)
                    for _item in _data.items:
                        wii = QtWidgets.QTreeWidgetItem()
                        wii.setText(0, _item.name)
                        wii._object = _item
                        wii.setToolTip(0, _item.__doc__)
                        wi.addChild(wii)

                    w1.addTopLevelItem(wi)
            else:
                self._object = obj
                l_data_obj = obj.mandatory_objs + obj.optional_objs
                for _data_obj in l_data_obj:
                    wi = QtWidgets.QTreeWidgetItem()
                    wi._object = _data_obj
                    wi.setToolTip(0, _data_obj.__doc__)
                    s_name = type(_data_obj).__name__
                    if isinstance(_data_obj, DataConstr):
                        wi.setText(0, f"{s_name:}: {_data_obj.data_name:}")
                    elif isinstance(_data_obj, LoopConstr):
                        wi.setText(0, f"{s_name:}: {_data_obj.loop_name:}")
                    elif isinstance(_data_obj, ItemConstr):
                        wi.setText(0, f"{s_name:}")

                    if isinstance(_data_obj, DataConstr):
                        l_loop_item_obj = _data_obj.mandatory_objs + \
                            _data_obj.optional_objs+_data_obj.internal_objs

                        for _li_obj in l_loop_item_obj:
                            wii = QtWidgets.QTreeWidgetItem()
                            flag_2 = False
                            if isinstance(_li_obj, ItemConstr):
                                s_li_obj = type(_li_obj).__name__
                                flag_2 = True
                            elif isinstance(_li_obj, LoopConstr):
                                s_li_obj = f"{type(_li_obj).__name__:}: {_li_obj.loop_name:}"
                                flag_2 = True
                            if flag_2:
                                wii.setText(0, s_li_obj)
                                wii._object = _li_obj
                                wii.setToolTip(0, _li_obj.__doc__)
                                wi.addChild(wii)

                                l_int_attr = _li_obj.INTERNAL_ATTRIBUTE
                                if l_int_attr is None:
                                    l_int_attr = []
                                for _int_attr in l_int_attr:
                                    _int_obj = getattr(_li_obj, _int_attr)
                                    if ((isinstance(_int_obj, ItemConstr)) | (isinstance(_int_obj, LoopConstr))):
                                        wiii = QtWidgets.QTreeWidgetItem()
                                        wiii.setText(0, f"{_int_attr:}")
                                        wiii._object = _int_obj
                                        wiii.setToolTip(0, _int_obj.__doc__)
                                        wii.addChild(wiii)
                    else:
                        l_int_attr = _data_obj.INTERNAL_ATTRIBUTE
                        if l_int_attr is None:
                            l_int_attr = []
                        for _int_attr in l_int_attr:
                            _int_obj = getattr(_data_obj, _int_attr)
                            if (isinstance(_int_obj, ItemConstr)) | (isinstance(_int_obj, LoopConstr)):
                                wii = QtWidgets.QTreeWidgetItem()
                                wii.setText(0, f"{_int_attr:}")
                                wii._object = _int_obj
                                wii.setToolTip(0, _int_obj.__doc__)
                                wi.addChild(wii)

                    w1.addTopLevelItem(wi)

            w1.itemClicked.connect(self.onItemClicked)
            w1.expandAll()
            lay_cpanel.addWidget(w1)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        self.form_tab(it._object)

    def form_tab(self, obj):
        layout_11 = self.w_11.layout()
        layout_12 = self.w_12.layout()
        layout_13 = self.w_13.layout()
        layout_2 = self.w_2.layout()
        layout_3 = self.w_3.layout()
        w_output = self.w_output
        del_layout(layout_11)
        del_layout(layout_12)
        del_layout(layout_13)
        del_layout(layout_2)
        del_layout(layout_3)

        thread = self.additional_thread

        flag_done = False
        if (FLAG_MAGREF & (not(flag_done))):
            if isinstance(obj, MeasInelasticL):
                w_for_meas_inelasticl(obj, layout_11, layout_12,
                                  layout_13, layout_2, layout_3, w_output, thread)
                flag_done = True

        if (FLAG_MEM & (not(flag_done))):
            pass

        if (FLAG_CRYSPY & (not(flag_done))):
            if isinstance(obj, PdPeakL):
                w_for_pd_peak(obj, layout_11, layout_12, layout_13,
                              layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, PdMeasL):
                w_for_pd_meas(obj, layout_11, layout_12, layout_13,
                              layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, PdProcL):
                w_for_pd_proc(obj, layout_11, layout_12, layout_13,
                              layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, DiffrnReflnL):
                w_for_diffrn_refln(obj, layout_11, layout_12, layout_13,
                                   layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, Pd2dMeas):
                w_for_pd2d_meas(obj, layout_11, layout_12, layout_13,
                                layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, Pd2dProc):
                w_for_pd2d_proc(obj, layout_11, layout_12, layout_13,
                                layout_2, layout_3, w_output, thread)
                flag_done = True
            elif isinstance(obj, Pd):
                w_for_pd(obj, layout_11, layout_12, layout_13,
                         layout_2, layout_3, w_output, thread)
                flag_done = True

        if not(flag_done):
            if isinstance(obj, GlobalConstr):
                w_for_global_constr(obj, layout_11, layout_12,
                                    layout_13, layout_2, layout_3, w_output, thread)
            elif isinstance(obj, DataConstr):
                w_for_data_constr(obj, layout_11, layout_12,
                                  layout_13, layout_2, layout_3, w_output, thread)
            elif isinstance(obj, LoopConstr):
                w_for_loop_constr(obj, layout_11, layout_12,
                                  layout_13, layout_2, layout_3, w_output, thread)
            elif isinstance(obj, ItemConstr):
                w_for_item_constr(obj, layout_11, layout_12,
                                  layout_13, layout_2, layout_3, w_output, thread)
            elif isinstance(obj, Global):
                pass
            elif isinstance(obj, Data):
                pass
            elif isinstance(obj, Loop):
                pass
            elif isinstance(obj, Item):
                w_for_item(obj, layout_11, layout_12,
                           layout_13, layout_2, layout_3, w_output, thread)

    def start_of_calc_in_thread(self):
        self.w_loader.setChecked(True)
        self.w_cpanel.setStyleSheet("background-color:white;")

        ls_out = [f"The calculations are running.\n"]
        self.w_output.setText("\n".join(ls_out))

    def end_of_calc_in_thread(self):
        self.w_loader.setChecked(False)
        self.w_cpanel.setStyleSheet("background-color:light gray;")

        thread = self.additional_thread
        function = thread.function
        function_name = function.__name__
        output = thread.output
        ls_out = []
        ls_out.append(
            f"The function '{function_name:}' is perfomed.\n\nResult is \n")
        ls_out.append(str(output))
        self.w_output.setText("\n".join(ls_out))
        self.form_cpanel()

    def refresh_wind(self):
        self.form_cpanel()


def main_w(l_arg=[]):
    app = QtWidgets.QApplication(l_arg)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    if len(l_arg) >= 2:
        f_dir_data = os.path.abspath(l_arg[1])
    else:
        f_dir_data = os.getcwd()
    main_wind_1 = cbuilder(f_dir_data)
    sys.exit(app.exec_())


if __name__ == '__main__':
    l_arg = sys.argv
    main_w(l_arg)
