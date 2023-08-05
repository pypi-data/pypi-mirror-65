#!/usr/bin/env python
#
# bet_view.py
#
# Author: Taylor Hanayik <hanayik@gmail.com>

import wx
import wx.lib.scrolledpanel as scrolled
from fsleyes_widgets.floatslider import SliderSpinPanel

import fsl.gui.widgets as fslwidgets


class BetOptions(wx.CollapsiblePane):
    """
    BetOptions is a collapsible pane containing widgets that control
    bet's operation. 

    add the Options pane to a parent's sizer with a proportion value of 0.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pane = self.GetPane()
        sizer = wx.BoxSizer(wx.VERTICAL)

        # the dropdown choices for the bet mode
        self.bet_choice_panel = wx.Panel(pane)
        self.bet_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bet_choice_label = wx.StaticText(self.bet_choice_panel, label="BET mode")
        self.choice_btype = wx.Choice(self.bet_choice_panel, choices=[])
        self.choice_btype.SetSelection(0)
        self.bet_choice_sizer.Add(self.bet_choice_label, 0, wx.ALL, 5)
        self.bet_choice_sizer.Add(self.choice_btype, 0, wx.ALL, 5)
        self.bet_choice_panel.SetSizer(self.bet_choice_sizer)

        # the checkboxes for configuring bet
        self.cb_save_bet = wx.CheckBox(pane, label="Save brain-extracted image")
        self.cb_save_bet.SetValue(True) # default to always saving the Betted image
        self.cb_save_mask = wx.CheckBox(pane, label="Save brain mask image")
        self.cb_apply_thr = wx.CheckBox(pane, label="Apply thresholding to brain and mask image")
        self.cb_save_skull = wx.CheckBox(pane, label="Save exterior skull surface image")
        self.cb_save_overlay = wx.CheckBox(pane, label="Save brain overlay image")
        self.cb_verbose = wx.CheckBox(pane, label="Verbose")
        self.cb_verbose.Hide()

        # the fractional intensity slider (contained in a panel with a label)
        self.fval_panel = wx.Panel(pane)
        self.fval_panel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fval_control = SliderSpinPanel(self.fval_panel, value=0.5, minValue=0, maxValue=1, style=0)
        self.fval_label = wx.StaticText(self.fval_panel, label="Fractional intensity")
        self.fval_panel.sizer.Add(self.fval_label, 0, wx.ALL, 5)
        self.fval_panel.sizer.Add(self.fval_control, 0, wx.ALL, 5)
        self.fval_panel.SetSizer(self.fval_panel.sizer)

        # the gradient intensity slider
        self.gval_panel = wx.Panel(pane)
        self.gval_panel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gval_control = SliderSpinPanel(self.gval_panel, value=0, minValue=-1, maxValue=1, style=16)
        self.gval_label = wx.StaticText(self.gval_panel, label="Gradient intensity")
        self.gval_panel.sizer.Add(self.gval_label, 0, wx.ALL, 5)
        self.gval_panel.sizer.Add(self.gval_control, 0, wx.ALL, 5)
        self.gval_panel.SetSizer(self.gval_panel.sizer)

        # the bet center coordinates
        self.coord_panel = wx.Panel(pane)
        self.coord_panel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.coordx = wx.SpinCtrlDouble(self.coord_panel, min=0, max=10000, initial=0, inc=1)
        self.coordy = wx.SpinCtrlDouble(self.coord_panel, min=0, max=10000, initial=0, inc=1)
        self.coordz = wx.SpinCtrlDouble(self.coord_panel, min=0, max=10000, initial=0, inc=1)
        self.label_coordstr = wx.StaticText(self.coord_panel, label="Center point: ")
        self.labelx = wx.StaticText(self.coord_panel, label="X ")
        self.labely = wx.StaticText(self.coord_panel, label="Y ")
        self.labelz = wx.StaticText(self.coord_panel, label="Z ")
        self.coord_panel.sizer.Add(self.label_coordstr, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.labelx, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.coordx, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.labely, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.coordy, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.labelz, 0, wx.ALL, 5)
        self.coord_panel.sizer.Add(self.coordz, 0, wx.ALL, 5)
        self.coord_panel.SetSizer(self.coord_panel.sizer)

        # now add all of the options widgets to the sizer
        sizer.Add(self.fval_panel, 0, wx.ALL, 0) # 0 pixel border since the fval_panel already applied a 5 pix border
        sizer.Add(self.bet_choice_panel, 0, wx.ALL, 0)
        sizer.Add(self.cb_save_bet, 0, wx.ALL, 5)
        sizer.Add(self.cb_save_mask, 0, wx.ALL, 5)
        sizer.Add(self.cb_apply_thr, 0, wx.ALL, 5)
        sizer.Add(self.cb_save_skull, 0, wx.ALL, 5)
        sizer.Add(self.cb_save_overlay, 0, wx.ALL, 5)
        sizer.Add(self.cb_verbose, 0, wx.ALL, 5)
        sizer.Add(self.gval_panel, 0, wx.ALL, 0)
        sizer.Add(self.coord_panel, 0, wx.ALL, 0)


        # now layout the widgets so they can be sized appropriately (automatically done by wx)
        pane.SetSizer(sizer)

class BetView(wx.Panel):
    """
    Bet view defines the graphical layout of widgets for using BET
    """
    def __init__(self, parent, title="BET", **kwargs):
        super().__init__(parent, **kwargs)
        self.parent     = parent
        self.title      = title

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.title_panel = fslwidgets.Title(self, self.title)
        sizer.Add(self.title_panel, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        self.input = fslwidgets.Input(self).set_label("Input image*")
        sizer.Add(self.input, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.t2_input = fslwidgets.Input(self).set_label("Additional T2w image")
        sizer.Add(self.t2_input, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.t2_input.Hide()  # hide by default unless a special bet mode is chosen

        self.output = fslwidgets.Output(self).set_label("Output Image*")
        sizer.Add(self.output, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.action_panel = fslwidgets.ToolActionPanel(self)
        self.action_panel.pause_icon.Hide() # hide the pause icon since it is not needed
        sizer.Add(self.action_panel, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        self._scroll_panel = scrolled.ScrolledPanel(self)
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        self.options = BetOptions(self._scroll_panel, label="Options", style=wx.CP_NO_TLW_RESIZE)
        scroll_sizer.Add(self.options, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.orthoview = fslwidgets.OrthoView(self._scroll_panel, label="Image Display", style=wx.CP_NO_TLW_RESIZE)
        scroll_sizer.Add(self.orthoview, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        self._scroll_panel.SetSizer(scroll_sizer)
        self._scroll_panel.SetupScrolling()
        sizer.Add(self._scroll_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(sizer)


class FlirtView(wx.Panel):
    """
    FlirtView defines the graphical layout of widgets used in Flirt
    """
    def __init__(self, parent, title="FLIRT", **kwargs):
        super().__init__(parent, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # title panel
        #------------
        self.title_panel = fslwidgets.Title(self, title)
        sizer.Add(self.title_panel, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=5)


        # mode selection panel
        #---------------------
        mode_panel = wx.Panel(self)
        mode_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mode_st = wx.StaticText(mode_panel, label="Mode")
        # make mode_choice an attribute to be updated by the controller
        self.mode_choice = wx.Choice(mode_panel, choices=[])
        mode_sizer.Add(mode_st, proportion=0, flag=wx.ALL, border=5)
        mode_sizer.Add(self.mode_choice, proportion=0, flag=wx.ALL, border=5)
        mode_panel.SetSizer(mode_sizer)
        sizer.Add(mode_panel, proportion=0, flag=wx.ALL, border=5)

        # low res input panel (hidden when mode is highres to standard)
        self.input_lowres = fslwidgets.Input(self).set_label("Lowres image*")
        sizer.Add(self.input_lowres, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.input_lowres.Hide()
        
        # high res input panel
        self.input_highres = fslwidgets.Input(self).set_label("Highres image*")
        sizer.Add(self.input_highres, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # reference image picker panel
        self.input_reference = fslwidgets.ReferencePicker(self).set_label("Reference image*")
        sizer.Add(self.input_reference, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(sizer)

    

class FslView():
    """
    FslView is the main FSL start window. not to be 
    confused with the deprecated image viewer fslview (RIP)
    """
    

