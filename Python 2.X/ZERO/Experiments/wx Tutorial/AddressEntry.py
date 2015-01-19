#Boa:Frame:AddressEntry

import wx

def create(parent):
    return AddressEntry(parent)

[wxID_ADDRESSENTRY, wxID_ADDRESSENTRYADD, wxID_ADDRESSENTRYADDRESS, 
 wxID_ADDRESSENTRYCITY, wxID_ADDRESSENTRYCLOSE, wxID_ADDRESSENTRYCOUNTRY, 
 wxID_ADDRESSENTRYDELETE, wxID_ADDRESSENTRYFIRSTNAME, 
 wxID_ADDRESSENTRYLASTNAME, wxID_ADDRESSENTRYLISTCTRL1, 
 wxID_ADDRESSENTRYPANEL1, wxID_ADDRESSENTRYPOSTALCODE, wxID_ADDRESSENTRYSAVE, 
 wxID_ADDRESSENTRYSTADDRESS, wxID_ADDRESSENTRYSTCITY, 
 wxID_ADDRESSENTRYSTCOUNTRY, wxID_ADDRESSENTRYSTFIRSTNAME, 
 wxID_ADDRESSENTRYSTLASTNAME, wxID_ADDRESSENTRYSTPOSTALCODE, 
] = [wx.NewId() for _init_ctrls in range(19)]

class AddressEntry(wx.Frame):
    def _init_coll_fgsFields_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.stFirstName, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.firstName, 0, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.stLastName, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.lastName, 0, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.stAddress, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.address, 0, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.stPostalCode, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.postalCode, 0, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.stCity, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.city, 0, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.stCountry, 0, border=2,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        parent.AddWindow(self.country, 0, border=2, flag=wx.EXPAND | wx.ALL)

    def _init_coll_fgsButtons_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.add, 0, border=2, flag=wx.ALL)
        parent.AddWindow(self.delete, 0, border=2, flag=wx.ALL)
        parent.AddWindow(self.save, 0, border=2, flag=wx.ALL)
        parent.AddWindow(self.close, 0, border=2, flag=wx.ALL)

    def _init_coll_bsMain_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.listCtrl1, 1, border=2, flag=wx.EXPAND | wx.ALL)
        parent.AddSizer(self.fgsFields, 0, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.fgsButtons, 0, border=0, flag=0)

    def _init_coll_fgsFields_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableCol(1)

    def _init_coll_listCtrl1_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'First Name', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Last Name', width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading=u'City',
              width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading=u'Country', width=-1)

    def _init_sizers(self):
        # generated method, don't edit
        self.bsMain = wx.BoxSizer(orient=wx.VERTICAL)

        self.fgsFields = wx.FlexGridSizer(cols=2, hgap=0, rows=0, vgap=0)

        self.fgsButtons = wx.FlexGridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_bsMain_Items(self.bsMain)
        self._init_coll_fgsFields_Items(self.fgsFields)
        self._init_coll_fgsFields_Growables(self.fgsFields)
        self._init_coll_fgsButtons_Items(self.fgsButtons)

        self.panel1.SetSizer(self.bsMain)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_ADDRESSENTRY, name=u'AddressEntry',
              parent=prnt, pos=wx.Point(265, 424), size=wx.Size(400, 329),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Address Entry Form')
        self.SetClientSize(wx.Size(392, 295))

        self.panel1 = wx.Panel(id=wxID_ADDRESSENTRYPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(392, 295),
              style=wx.TAB_TRAVERSAL)

        self.listCtrl1 = wx.ListCtrl(id=wxID_ADDRESSENTRYLISTCTRL1,
              name='listCtrl1', parent=self.panel1, pos=wx.Point(2, 2),
              size=wx.Size(388, 92), style=wx.LC_REPORT)
        self._init_coll_listCtrl1_Columns(self.listCtrl1)

        self.stFirstName = wx.StaticText(id=wxID_ADDRESSENTRYSTFIRSTNAME,
              label=u'First Name', name=u'stFirstName', parent=self.panel1,
              pos=wx.Point(2, 102), size=wx.Size(55, 13), style=0)

        self.firstName = wx.TextCtrl(id=wxID_ADDRESSENTRYFIRSTNAME,
              name=u'firstName', parent=self.panel1, pos=wx.Point(61, 98),
              size=wx.Size(329, 21), style=0, value=u'')

        self.stLastName = wx.StaticText(id=wxID_ADDRESSENTRYSTLASTNAME,
              label=u'Last Name', name=u'stLastName', parent=self.panel1,
              pos=wx.Point(2, 127), size=wx.Size(55, 13), style=0)

        self.lastName = wx.TextCtrl(id=wxID_ADDRESSENTRYLASTNAME,
              name=u'lastName', parent=self.panel1, pos=wx.Point(61, 123),
              size=wx.Size(329, 21), style=0, value=u'')

        self.stAddress = wx.StaticText(id=wxID_ADDRESSENTRYSTADDRESS,
              label=u'Address', name=u'stAddress', parent=self.panel1,
              pos=wx.Point(2, 165), size=wx.Size(55, 13), style=0)

        self.address = wx.TextCtrl(id=wxID_ADDRESSENTRYADDRESS, name=u'address',
              parent=self.panel1, pos=wx.Point(61, 148), size=wx.Size(329, 47),
              style=wx.TE_MULTILINE, value=u'')

        self.stPostalCode = wx.StaticText(id=wxID_ADDRESSENTRYSTPOSTALCODE,
              label=u'Postal', name=u'stPostalCode', parent=self.panel1,
              pos=wx.Point(2, 203), size=wx.Size(55, 13), style=0)

        self.postalCode = wx.TextCtrl(id=wxID_ADDRESSENTRYPOSTALCODE,
              name=u'postalCode', parent=self.panel1, pos=wx.Point(61, 199),
              size=wx.Size(329, 21), style=0, value=u'')

        self.stCity = wx.StaticText(id=wxID_ADDRESSENTRYSTCITY, label=u'City',
              name=u'stCity', parent=self.panel1, pos=wx.Point(2, 228),
              size=wx.Size(55, 13), style=0)

        self.city = wx.TextCtrl(id=wxID_ADDRESSENTRYCITY, name=u'city',
              parent=self.panel1, pos=wx.Point(61, 224), size=wx.Size(329, 21),
              style=0, value=u'')

        self.stCountry = wx.StaticText(id=wxID_ADDRESSENTRYSTCOUNTRY,
              label=u'Country', name=u'stCountry', parent=self.panel1,
              pos=wx.Point(2, 251), size=wx.Size(55, 13), style=0)

        self.country = wx.TextCtrl(id=wxID_ADDRESSENTRYCOUNTRY, name=u'country',
              parent=self.panel1, pos=wx.Point(61, 249), size=wx.Size(329, 17),
              style=0, value=u'')

        self.add = wx.Button(id=wx.ID_ADD, label=u'', name=u'add',
              parent=self.panel1, pos=wx.Point(2, 270), size=wx.Size(75, 23),
              style=0)

        self.delete = wx.Button(id=wx.ID_DELETE, label=u'', name=u'delete',
              parent=self.panel1, pos=wx.Point(81, 270), size=wx.Size(75, 23),
              style=0)

        self.save = wx.Button(id=wx.ID_SAVE, label=u'', name=u'save',
              parent=self.panel1, pos=wx.Point(160, 270), size=wx.Size(75, 23),
              style=0)

        self.close = wx.Button(id=wx.ID_CLOSE, label=u'', name=u'close',
              parent=self.panel1, pos=wx.Point(239, 270), size=wx.Size(75, 23),
              style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()

    app.MainLoop()
