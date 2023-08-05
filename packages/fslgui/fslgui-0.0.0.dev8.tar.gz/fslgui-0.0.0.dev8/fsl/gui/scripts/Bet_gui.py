#!/usr/bin/env python

import wx
import sys
from fsl.gui.guis import BetGui
import argparse

parser = argparse.ArgumentParser(description="FSL's brain extraction tool")
parser.add_argument(
        '-input',
        default="",
        type=str,
        required=False,
        help="an input image file"
        )
parser.add_argument(
        "-output",
        default="",
        required=False,
        type=str,
        help="the output name for the brain extracted image(s)"
        )
parser.add_argument(
        "-o",
        action='store_false',
        required=False,
        help="generate brain surface outline overlaid onto original image"
        )
parser.add_argument(
        "-m",
        action='store_false',
        required=False,
        help="generate binary brain mask"
        )
parser.add_argument(
        "-s",
        action='store_false',
        required=False,
        help="generate approximate skull image"
        )
parser.add_argument(
        "-n",
        action='store_false',
        required=False,
        help="do not save segmented brain image"
        )
parser.add_argument(
        "-f",
        default=0.5,
        type=float,
        required=False,
        help="do not save segmented brain image"
        )

def main():
    args = parser.parse_args()

    # get an app instance
    app = wx.App()
    # get our wx.Frame (this bet window will not be embedded in a panel)
    # betview = BetView(
    #         parent=None,
    #         in_img=args.input,
    #         out_img=args.output,
    #         o_opt=args.o,
    #         m_opt=args.m,
    #         s_opt=args.s,
    #         n_opt=args.n,
    #         f_opt=args.f) # parent=None will return a wx.Frame
    # betview.window.Show()
    frame = wx.Frame(None, size=(800, 600))
    sizer = wx.BoxSizer(wx.VERTICAL)
    controller = BetGui(frame, "BET")
    sizer.Add(controller.view, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
    frame.SetSizer(sizer)
    frame.Centre()
    frame.Show()
    app.MainLoop()
if __name__ == "__main__":
    sys.exit(main())
