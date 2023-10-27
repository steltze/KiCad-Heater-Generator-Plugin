import wx

class HeaterPluginSettingsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(HeaterPluginSettingsDialog, self).__init__(parent, title=title, size=(300, 200))

        self.trace_width = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.trace_clearance = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.pcb_size_x = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.pcb_size_y = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.copper_to_edge_clearance = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.net_name = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        
        self.ok_button = wx.Button(self, wx.ID_OK, label="Generate")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        self.create_layout()
        
    def create_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer.Add(wx.StaticText(self, label="Trace Width (mm):"), 0, wx.ALL, 10)
        sizer.Add(self.trace_width, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(wx.StaticText(self, label="Trace Clearance (mm):"), 0, wx.ALL, 10)
        sizer.Add(self.trace_clearance, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(wx.StaticText(self, label="PCB Size X (mm):"), 0, wx.ALL, 10)
        sizer.Add(self.pcb_size_x, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(wx.StaticText(self, label="PCB Size Y (mm):"), 0, wx.ALL, 10)
        sizer.Add(self.pcb_size_y, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(wx.StaticText(self, label="Copper to Edge Clearance (mm):"), 0, wx.ALL, 10)
        sizer.Add(self.copper_to_edge_clearance, 0, wx.EXPAND | wx.ALL, 10)

        sizer.Add(wx.StaticText(self, label="Net Name:"), 0, wx.ALL, 10)
        sizer.Add(self.net_name, 0, wx.EXPAND | wx.ALL, 10)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.ok_button, 0, wx.ALL, 10)
        button_sizer.Add(self.cancel_button, 0, wx.ALL, 10)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)
        
        self.SetSizerAndFit(sizer)
        
    def on_ok(self, event):
        try:
            self.trace_width = float(self.trace_width.GetValue())
            self.trace_clearance = float(self.trace_clearance.GetValue())
            self.pcb_size_x = float(self.pcb_size_x.GetValue())
            self.pcb_size_y = float(self.pcb_size_y.GetValue())
            self.copper_to_edge_clearance = float(self.copper_to_edge_clearance.GetValue())
            self.net_name = str(self.net_name.GetValue())
                        
            self.EndModal(wx.ID_OK)
        except ValueError:
            wx.MessageBox("Invalid input. Please enter valid float values.", "Error", wx.OK | wx.ICON_ERROR)
        
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)
