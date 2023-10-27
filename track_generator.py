from . import curve_options

import pcbnew
import numpy as np
import sys
from scipy.interpolate import interp1d

class TracksGenerator(object):

    def __init__(self, trace_clearance, trace_width, pcb_size_x, pcb_size_y, copper_to_edge_clearance, net_name):
        self.board = pcbnew.GetBoard()
        # self.netList = self.board.GetNetsByName()
        # self.net = self.netList.items()[1][1]
        self.net = pcbnew.NETINFO_ITEM(self.board, net_name)
        self.board.Add(self.net)

        self.trace_clearance = trace_clearance
        self.trace_width = trace_width
        self.pcb_size_x = pcb_size_x 
        self.pcb_size_y = pcb_size_y
        self.copper_to_edge_clearance = copper_to_edge_clearance

        self.points_generator_grix_x = int(np.floor((pcb_size_x-2*(trace_width+copper_to_edge_clearance))/(trace_clearance + trace_width)))
        self.points_generator_grix_y = int(np.floor((pcb_size_y-2*(trace_width+copper_to_edge_clearance))/(trace_clearance + trace_width)))

        self.number_of_points = self.points_generator_grix_x*self.points_generator_grix_y

        self.pcb_grid_mapping_x = interp1d([0, self.points_generator_grix_x-1],[0+(self.trace_width/2.0+self.copper_to_edge_clearance), self.pcb_size_x-(self.trace_width/2.0+self.copper_to_edge_clearance)])
        self.pcb_grid_mapping_y = interp1d([0, self.points_generator_grix_y-1],[0+(self.trace_width/2.0+self.copper_to_edge_clearance), self.pcb_size_y-(self.trace_width/2.0+self.copper_to_edge_clearance)])

    def euclidean_distance(self, point1, point2) :
        return np.sqrt(np.square(point1[0] - point2[0]) + np.square(point1[1] - point2[1]))

    def check_trace_clearance(self, point_start, point_end):

        if self.euclidean_distance(point_start, point_end) < (self.trace_clearance + self.trace_width):
            print(point_start)
            print(point_end)
            print(self.euclidean_distance(point_start, point_end))
            sys.exit("Clearance violoation")

    def get_curve_generator(self):
        return curve_options.return_curve_points_generator(self.points_generator_grix_x, self.points_generator_grix_y)
    
    def map_point_to_pcb_grid(self, point):
        return float(self.pcb_grid_mapping_x(point[0])), float(self.pcb_grid_mapping_y(point[1]))
    
    def draw_track(self, point_start, point_end):
        p_start = self.map_point_to_pcb_grid(point_start)
        p_end = self.map_point_to_pcb_grid(point_end)

        self.check_trace_clearance(p_start, p_end)  

        track = pcbnew.PCB_TRACK(self.board) # PCB_TRACK FP_SHAPE

        # Size here is specified as integer nanometers, so multiply mm by 1e6
        track.SetWidth(int(self.trace_width * 1e6))
        track.SetLayer(pcbnew.F_Cu)

        track.SetNet(self.net)
        
        track.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(float(p_start[0]), float(p_start[1]))))
        track.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(float(p_end[0]), float(p_end[1]))))

        self.board.Add(track)
        # self.group.AddItem(track)

    def drawEdgeCutLine(self, start, end):
        board = pcbnew.GetBoard()
        segment = pcbnew.PCB_SHAPE(board)
        segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
        segment.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(float(start[0]), float(start[1]))))
        segment.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(float(end[0]), float(end[1]))))
        segment.SetLayer(pcbnew.Edge_Cuts)
        segment.SetWidth(int(0.1 * 1e6))
        board.Add(segment)
    
    def drawEdgeCuts(self):
        self.drawEdgeCutLine((0, 0), (0, self.pcb_size_y))
        self.drawEdgeCutLine((0, 0), (self.pcb_size_x, 0))
        self.drawEdgeCutLine((self.pcb_size_x, 0), (self.pcb_size_x, self.pcb_size_y))
        self.drawEdgeCutLine((0, self.pcb_size_y), (self.pcb_size_x, self.pcb_size_y))
        return
    
    def draw_heater(self):
        curve_generator = self.get_curve_generator()

        self.drawEdgeCuts()

        point_start = next(curve_generator)
        for _ in range(self.number_of_points-1): # we don't want to route a track starting from the last point
            point_end = next(curve_generator)
            self.draw_track(point_start, point_end)

            point_start = point_end
        
        pcbnew.Refresh()
