#Boa:Dialog:Dialog1

import wx

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1STATICBITMAP1, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(5)]

class Dialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(363, 125), size=wx.Size(279, 260),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'About Notebook')
        self.SetClientSize(wx.Size(271, 226))

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=u'Notebook - Simple Text Editor', name='staticText1',
              parent=self, pos=wx.Point(8, 0), size=wx.Size(251, 23),
              style=wx.ALIGN_CENTRE)
        self.staticText1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=u'This is my first Boa Constructor application',
              name='staticText2', parent=self, pos=wx.Point(32, 24),
              size=wx.Size(204, 13), style=0)
        self.staticText2.SetBackgroundColour(wx.Colour(128, 128, 255))

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'C:/Documents and Settings/Zero/Desktop/Tutorial/Boa.jpg',
              wx.BITMAP_TYPE_JPEG), id=wxID_DIALOG1STATICBITMAP1,
              name='staticBitmap1', parent=self, pos=wx.Point(16, 40),
              size=wx.Size(236, 157), style=0)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=u'Close',
              name='button1', parent=self, pos=wx.Point(96, 200),
              size=wx.Size(75, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_DIALOG1BUTTON1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.Close()
