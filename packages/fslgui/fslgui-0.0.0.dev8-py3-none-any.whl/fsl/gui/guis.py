#!/usr/bin/env python
#
# bet_gui.py
#
# Author: Taylor Hanayik <hanayik@gmail.com>

import os

import wx
from fsl.data import image

import fsl.gui.views as fslviews
import fsl.gui.tools as fsltools


class BaseGui(object):
    """
    BaseGui is the parent class for all FSL GUIs.
    Common functionality and attributes are implemented here.
    """
    def __init__(self):
        # maybe add some other common funcionality here
        pass

    @staticmethod
    def _layout_from(widget):
        """
        redo layout of all widgets up the parent tree from this widget.
        Stop when we get to a frame. This was taken from a wx wiki post
        """
        while widget.GetParent():
            widget = widget.GetParent()
            widget.Layout()
            if widget.IsTopLevel():
                break

    def layout_from(self, event):
        self._layout_from(event.GetEventObject())

class BetGui(BaseGui):
    """
    Bet GUI is the controller of the BetView that can interact with the BetModel
    """
    def __init__(self, parent, title="BET", model=None):
        super().__init__()
        
        if model is None:
            # set the model
            self.model = fsltools.Bet()

        # set the view
        self.view = fslviews.BetView(parent, title)

        # update the view with some model data
        self.view.options.choice_btype.AppendItems(list(self.model.bet_type_choices.keys()))

        # bind events and their handlers
        self.view.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.layout_from)
        self.view.options.choice_btype.Bind(wx.EVT_CHOICE, self._on_bet_choice)
        self.view.options.cb_save_bet.Bind(wx.EVT_CHECKBOX, self._on_save_bet)
        self.view.options.cb_apply_thr.Bind(wx.EVT_CHECKBOX, self._on_apply_thr)
        self.view.options.cb_save_mask.Bind(wx.EVT_CHECKBOX, self._on_save_mask)
        self.view.options.cb_save_overlay.Bind(wx.EVT_CHECKBOX, self._on_save_overlay)
        self.view.options.cb_save_skull.Bind(wx.EVT_CHECKBOX, self._on_save_skull)
        self.view.options.coordx.Bind(wx.EVT_SPINCTRLDOUBLE, self._on_coord_update)
        self.view.options.coordy.Bind(wx.EVT_SPINCTRLDOUBLE, self._on_coord_update)
        self.view.options.coordz.Bind(wx.EVT_SPINCTRLDOUBLE, self._on_coord_update)
        self.view.action_panel.play_icon.Bind(wx.EVT_LEFT_UP, self._on_run)
        self.view.action_panel.code_icon.Bind(wx.EVT_LEFT_UP, self._on_code)
        self.view.input.file_ctrl.Bind(wx.EVT_TEXT, self._on_input_edit)
        self.view.output.file_ctrl.Bind(wx.EVT_TEXT, self._on_output_edit)
        self.view.t2_input.file_ctrl.Bind(wx.EVT_TEXT, self._on_t2_input_edit)

    def _on_coord_update(self, event):
        x = self.view.options.coordx.GetValue()
        y = self.view.options.coordy.GetValue()
        z = self.view.options.coordz.GetValue()

        self.model.center_coord = (x, y, z)
        print(self.model.center_coord)

    def _on_input_edit(self, event):
        widget = event.GetEventObject()
        val = widget.GetValue()
        if not os.path.isfile(val):
            return
        else:
            self.model.image_in = val
            self.view.orthoview.reset()
            self.view.orthoview.add_image(val)
            ext = image.getExt(val)
            self.view.output.file_ctrl.SetValue(
                image.removeExt(val) + self.model.suffix + ext
            )

    def _on_output_edit(self, event):
        widget = event.GetEventObject()
        val = widget.GetValue()
        if not os.path.isfile(val):
            return
        else:
            self.model.image_out = val

    def _on_t2_input_edit(self, event):
        widget = event.GetEventObject()
        val = widget.GetValue()
        if not os.path.isfile(val):
            return
        else:
            self.model.image_t2 = val


    def _on_bet_choice(self, event):
        widget = event.GetEventObject()
        idx = widget.GetSelection()
        choice_str = widget.GetString(idx)
        self._update_bet_type(choice_str)
        if 'T2w' in choice_str:
            self.view.t2_input.Show()
            self._layout_from(self.view.t2_input)
        else:
            self.view.t2_input.Hide()
            self._layout_from(self.view.t2_input)

    def _on_save_bet(self, event):
        widget = event.GetEventObject()
        val = widget.GetValue()
        if val:
            val = False
        else:
            val = True
        self.model.discard_bet = val

    def _on_apply_thr(self, event):
        widget = event.GetEventObject()
        self.model.applythresh = widget.GetValue()

    def _on_save_mask(self, event):
        widget = event.GetEventObject()
        self.model.save_mask = widget.GetValue()

    def _on_save_overlay(self, event):
        widget = event.GetEventObject()
        self.model.save_overlay = widget.GetValue()

    def _on_save_skull(self, event):
        widget = event.GetEventObject()
        self.model.save_skull = widget.GetValue()

    def _update_bet_type(self, btype):
        self.model.bet_type = self.model.bet_type_choices[btype]

    def _on_code(self, event):
        self.model.fval = self.view.options.fval_control.GetValue()
        self.model.gval = self.view.options.gval_control.GetValue()
        self.model.image_out = self.view.output.file_ctrl.GetValue()
        print(self.model.command())

    def _load_result(self):
        self.view.orthoview.reset()
        self.view.orthoview.add_image(self.model.image_in)
        self.view.orthoview.add_mask(self.model.image_out)

    def _on_run(self, event):
        self._on_code(None)
        self.model.run(self._load_result)


class FlirtGui(BaseGui):
    """
    The FlirtGui is the controller for the FlirtView that
    can interact with the flirt model
    """
    def __init__(self, parent, title="FLIRT", model=None):
        super().__init__()

        if model is None:
            self.model = fsltools.Flirt()

        self.view = fslviews.FlirtView(parent, title)
        self.view.mode_choice.AppendItems(self.model.flirt_type_choices)

        # bind events
        self.view.mode_choice.Bind(wx.EVT_CHOICE, self._on_mode_choice)

    def _on_mode_choice(self, event):
        widget = event.GetEventObject()
        idx = widget.GetSelection()
        choice_str = widget.GetString(idx)
        if 'lowres' in choice_str:
            self.view.input_lowres.Show()
            self._layout_from(self.view.input_lowres)
        else:
            self.view.input_lowres.Hide()
            self._layout_from(self.view.input_lowres)