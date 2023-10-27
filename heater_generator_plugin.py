import pcbnew
import os
import wx
from . import track_generator

from .heater_settings_dialog import HeaterPluginSettingsDialog

class HeaterGeneratorPluginAction(pcbnew.ActionPlugin):
    def defaults(self) -> None:
        self.name = "Heater PCB Generator"
        self.category = "Modify PCB"
        self.description = "Create a PCB"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")
        self.show_toolbar_button = True

    def Run(self) -> None:
        pcb_frame = next(
            x for x in wx.GetTopLevelWindows() if x.GetName() == "PcbFrame"
        )

        dlg = HeaterPluginSettingsDialog(pcb_frame, "KiCad Plugin Settings")
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            trace_width = dlg.trace_width
            trace_clearance = dlg.trace_clearance
            pcb_size_x = dlg.pcb_size_x
            pcb_size_y = dlg.pcb_size_y
            copper_to_edge_clearance = dlg.copper_to_edge_clearance
            net_name = dlg.net_name

            heater_generator = track_generator.TracksGenerator(trace_clearance, trace_width, pcb_size_x, pcb_size_y, copper_to_edge_clearance, net_name)
            heater_generator.draw_heater()
    
        dlg.Destroy()
