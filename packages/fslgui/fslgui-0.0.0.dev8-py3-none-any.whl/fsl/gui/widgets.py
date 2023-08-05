"""
the widges module provides common widgets that are intended
to be embedded within other FSL guis.  
"""
import os
import subprocess

import wx
import fsleyes
import fsleyes.overlay as fsloverlay
import fsleyes.displaycontext as fsldc
import fsleyes.views.orthopanel as orthopanel
# from fsleyes.main import embed
import fsleyes.profiles as profiles
import fsleyes.profiles.profilemap as profilemap
import fsleyes.colourmaps as colourmaps

from fsl.utils.platform import platform as fslplatform
from fsl.utils import idle

import fsl.data.image as fslimage
import fsl.gui.icons as fslicons

def embed(parent=None, make_fsleyesframe=True, **kwargs):
    """Initialise FSLeyes and create a :class:`.FSLeyesFrame`, when
    running within another application.

    .. note:: If a ``wx.App`` does not exist, one is created.

    :arg parent: ``wx`` parent object
    :arg make_fsleyesframe: bool, default is True to make a new :class:`.FSLeyesFrame`
    :returns:    A tuple containing:
                    - The :class:`.OverlayList`
                    - The master :class:`.DisplayContext`
                    - The :class:`.FSLeyesFrame` or None if make_fsleyesframe=False

    All other arguments are passed to :meth:`.FSLeyesFrame.__init__`.
    """

    import fsleyes_props          as props
    import fsleyes.gl             as fslgl
    import fsleyes.frame          as fslframe
    import fsleyes.overlay        as fsloverlay
    import fsleyes.displaycontext as fsldc

    app    = wx.GetApp()
    ownapp = app is None
    if ownapp:
        app = FSLeyesApp()

    fsleyes.initialise()
    colourmaps.init()
    props.initGUI()

    called = [False]
    ret    = [None]

    def until():
        return called[0]

    def ready():
        frame = None
        fslgl.bootstrap()

        overlayList = fsloverlay.OverlayList()
        displayCtx  = fsldc.DisplayContext(overlayList)
        if make_fsleyesframe:
            frame       = fslframe.FSLeyesFrame(
                parent, overlayList, displayCtx, **kwargs)

        if ownapp:
            app.SetOverlayListAndDisplayContext(overlayList, displayCtx)
            # Keep a ref to prevent the app from being GC'd
            if make_fsleyesframe:
                frame._embed_app = app

        called[0] = True
        ret[0]    = (overlayList, displayCtx, frame)

    fslgl.getGLContext(parent=parent, ready=ready)
    idle.block(10, until=until)

    if ret[0] is None:
        raise RuntimeError('Failed to start FSLeyes')
    return ret[0]

def layout_from(widget):
    """
    redo layout of all widgets up the parent tree from this widget. 
    Stop when we get to a frame. This was taken from a wx wiki post
    """
    while widget.GetParent():
        widget = widget.GetParent()
        widget.Layout()
        if widget.IsTopLevel():
            break

class FileDropTextCtrl(wx.FileDropTarget):
    """
    Drop target specifically for wx.TextCtrl widgets.
    It's specific because it expects window to have a SetValue method
    """
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        # only use the first file if multiple are dropped at once
        self.window.SetValue(filenames[0])
        return True

class Input(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.file_path = ""
        #sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, "Input image*")
        self.box = wx.StaticBox(self, label="")
        sizer = wx.StaticBoxSizer(self.box)
        self.button = wx.Button(self.box, label="Choose")
        self.file_ctrl = wx.TextCtrl(self.box, value="")
        drop_target = FileDropTextCtrl(self.file_ctrl)
        self.file_ctrl.SetDropTarget(drop_target)
        sizer.Add(self.file_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.button, 0, wx.ALL, 5)
        self.SetSizer(sizer)

        self.button.Bind(wx.EVT_LEFT_UP, self._on_choose)

    def set_label(self, text):
        self.box.SetLabel(text)
        layout_from(self.box)
        return self

    def set_text(self, text):
        self.file_ctrl.SetValue(text)
        return self

    def get_path(self):
        return self.file_ctrl.GetValue()

    def _on_choose(self, event):
        with wx.FileDialog(self, "Choose input file", style=wx.FD_OPEN) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            self.file_path = os.path.abspath(fd.GetPath())
            self.set_text(self.file_path)

class ReferencePicker(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = ""
        #sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, "Input image*")
        self.box = wx.StaticBox(self, label="Reference image")
        sizer = wx.StaticBoxSizer(self.box, orient=wx.VERTICAL)
        input_panel = wx.Panel(self.box)
        input_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choose_button = wx.Button(input_panel, label="Choose")
        self.file_ctrl = wx.TextCtrl(input_panel, value="")
        input_panel_sizer.Add(self.file_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        input_panel_sizer.Add(self.choose_button, 0, wx.ALL, 5)
        input_panel.SetSizer(input_panel_sizer)

        button_panel = wx.Panel(self.box)
        button_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_1mm_brain = wx.Button(button_panel, label="standard_1mm_brain")
        self.btn_2mm_brain = wx.Button(button_panel, label="standard_2mm_brain")
        button_panel_sizer.Add(self.btn_1mm_brain, proportion=0, flag=wx.ALL, border=5)
        button_panel_sizer.Add(self.btn_2mm_brain, proportion=0, flag=wx.ALL, border=5)
        button_panel.SetSizer(button_panel_sizer)


        sizer.Add(input_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(button_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(sizer)

        self.choose_button.Bind(wx.EVT_LEFT_UP, self._on_choose)
        self.btn_1mm_brain.Bind(wx.EVT_LEFT_UP, self._on_1mm_brain)
        self.btn_2mm_brain.Bind(wx.EVT_LEFT_UP, self._on_2mm_brain)

    def set_label(self, text):
        self.box.SetLabel(text)
        layout_from(self.box)
        return self

    def set_text(self, text):
        self.file_ctrl.SetValue(text)
        return self

    def get_path(self):
        return self.file_ctrl.GetValue()

    def _on_choose(self, event):
        with wx.FileDialog(self, "Choose input file", style=wx.FD_OPEN) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            self.file_path = os.path.abspath(fd.GetPath())
            self.set_text(self.file_path)

    def _on_1mm_brain(self, event):
        self.file_path = os.path.join(
            fslplatform.fsldir,
            "data",
            "standard",
            "MNI152_T1_1mm_brain.nii.gz"
        )
        self.set_text(self.file_path)

    def _on_2mm_brain(self, event):
        self.file_path = os.path.join(
            fslplatform.fsldir,
            "data",
            "standard",
            "MNI152_T1_2mm_brain.nii.gz"
        )
        self.set_text(self.file_path)


class Output(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = ""
        self.box = wx.StaticBox(self, label="")
        sizer = wx.StaticBoxSizer(self.box)
        self.button = wx.Button(self.box, label="Set path")
        self.file_ctrl = wx.TextCtrl(self.box, value="")
        sizer.Add(self.file_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.button, 0, wx.ALL, 5)
        self.SetSizer(sizer)

        self.button.Bind(wx.EVT_LEFT_UP, self._on_choose)

    def set_label(self, text):
        self.box.SetLabel(text)
        layout_from(self.box)
        return self

    def set_text(self, text):
        self.file_ctrl.SetValue(text)

    def get_path(self):
        return self.file_ctrl.GetValue()

    def _on_choose(self, event):
        with wx.DirDialog(None, message="Choose output directory", defaultPath=os.getcwd()) as dd:
            if dd.ShowModal() == wx.ID_CANCEL:
                return
            self.file_path = os.path.abspath(dd.GetPath())
            self.set_text(self.file_path)


class Title(wx.Panel):
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, **kwargs)
        self.SetMinSize((-1, 32))
        self.SetMaxSize((-1, 32))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.title_text = wx.StaticText(parent=self, label=title)
        self.title_text.SetFont(
                wx.Font(
                    wx.FontInfo(16).Bold()
                    )
                )
        sizer.Add(
            self.title_text,
            1,
            wx.ALIGN_CENTER | wx.ALL,
            0)
        self.SetSizer(sizer)
    def set_text(self, new_text):
        self.title_text.SetLabel(new_text)
        self.Layout()
        return self


class ToolActionPanel(wx.Panel):
    """
    A CardControlsPanel contains the action buttons related to the card.
    """
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetMinSize(wx.Size(-1, 38))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.SetBackgroundColour(wx.Colour(255, 255, 255))
        

        self.code_icon = wx.BitmapButton(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                fslicons.icon_code, wx.BITMAP_TYPE_PNG
            ),
            wx.DefaultPosition,
            wx.DefaultSize,
        )
        sizer.Add(self.code_icon, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, 4)

        self.pause_icon = wx.BitmapButton(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                fslicons.icon_pause, wx.BITMAP_TYPE_PNG
            ),
            wx.DefaultPosition,
            wx.DefaultSize,
        )
        sizer.Add(self.pause_icon, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, 4)

        self.play_icon = wx.BitmapButton(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                fslicons.icon_play, wx.BITMAP_TYPE_PNG
            ),
            wx.DefaultPosition,
            wx.DefaultSize,
        )
        sizer.Add(self.play_icon, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, 4)
        self.SetSizer(sizer)
        self.Layout()



class ViewProfile(profiles.Profile):
    def __init__(self, viewPanel, overlayList, displayCtx):
        profiles.Profile.__init__(self,
                                  viewPanel,
                                  overlayList,
                                  displayCtx,
                                  ['nav'])

    def getEventTargets(self):
        return [self.viewPanel.getXCanvas(),
                self.viewPanel.getYCanvas(),
                self.viewPanel.getZCanvas()]

    def _navModeLeftMouseDrag(self, ev, canvas, mousePos, canvasPos):
        if canvasPos is None:
            return False
        self.displayCtx.location = canvasPos
        return True


# This is the hacky bit - there is
# currently no formal way to register
# a custom profile class with a view.
# This might change in the future.

# The first profile in the profiles
# list is used as the default.
profilemap.profiles[orthopanel.OrthoPanel].insert(0, 'minview')
profilemap.profileHandlers[orthopanel.OrthoPanel, 'minview'] = ViewProfile

# def nomenu(*a):
#     pass
# FSLeyesFrame._FSLeyesFrame__makeMenuBar = nomenu


class OrthoView(wx.CollapsiblePane):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        pane = self.GetPane()
        self.overlayList, masterDisplayCtx, _ = embed(None, make_fsleyesframe=False)
        self.displayCtx = fsldc.DisplayContext(self.overlayList, parent=masterDisplayCtx)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.op = orthopanel.OrthoPanel(
                pane,
                self.overlayList,
                self.displayCtx,
                None)
        self.op.SetMinSize((-1, 300))
        self.op.Show()

        self.btn_fsleyes = wx.Button(pane, label="Open in FSLeyes")
        sizer.Add(self.btn_fsleyes, proportion=0, flag=wx.ALL, border=5)
        sizer.Add(self.op, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        pane.SetSizer(sizer)

        # bind events
        self.btn_fsleyes.Bind(wx.EVT_BUTTON, self.launch_fsleyes)
    
    def _run_fsleyes(self):
        imgs = [img.dataSource for img in self.overlayList]
        # print([img.dataSource for img in self.overlayList])
        cmd = [
            os.path.join(fslplatform.fsldir, 'bin', 'fsleyes'),
            " ".join(imgs)
        ]
        subprocess.run(
            " ".join(cmd),
            shell=True, 
            check=True
        )


    def launch_fsleyes(self, event):
        thread_id = idle.run(self._run_fsleyes)

    def reset(self):
        self.overlayList.clear()

    def add_image(self, new_img):
        img = fslimage.Image(new_img)
        self.overlayList.append(img)

    def add_mask(self, new_img):
        img = fslimage.Image(new_img)
        self.overlayList.append(img, cmap='red', alpha=30)


