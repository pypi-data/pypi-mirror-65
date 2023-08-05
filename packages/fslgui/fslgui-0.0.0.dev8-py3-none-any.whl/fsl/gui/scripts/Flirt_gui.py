#!/usr/bin/env python

import wx
import sys
from fsl.gui.guis import FlirtGui
import argparse

parser = argparse.ArgumentParser(description="FSL's FLIRT")
parser.add_argument(
        '-input',
        default="",
        type=str,
        required=False,
        help="an input image file")

def main():
    args = parser.parse_args()

    # get an app instance
    app = wx.App()
    frame = wx.Frame(None, size=(800, 600))
    sizer = wx.BoxSizer(wx.VERTICAL)
    flirt_gui = FlirtGui(frame, "FLIRT")
    sizer.Add(flirt_gui.view, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
    frame.SetSizer(sizer)
    frame.Centre()
    frame.Show()
    app.MainLoop()
if __name__ == "__main__":
    sys.exit(main())