from . import gilbert2d

def return_curve_points_generator(num_points_x, num_points_y):
    return gilbert2d.gilbert2d(num_points_x, num_points_y)
