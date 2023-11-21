def do_segments_intersect(seg1_start, seg1_end, seg2_start, seg2_end):
    def orientation(p, q, r):
        # Calculate the orientation of three points (p, q, r)
        # Returns 0 if they are collinear, 1 if clockwise, and 2 if counterclockwise
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
    
    def on_segment(p, q, r):
        # Check if point q lies on line segment pr
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False
    
    # Calculate orientations for each combination of points
    o1 = orientation(seg1_start, seg1_end, seg2_start)
    o2 = orientation(seg1_start, seg1_end, seg2_end)
    o3 = orientation(seg2_start, seg2_end, seg1_start)
    o4 = orientation(seg2_start, seg2_end, seg1_end)
    
    # General case: segments intersect if orientations are different
    if o1 != o2 and o3 != o4:
        return True
    
    # Special cases where segments share endpoints
    if o1 == 0 and on_segment(seg1_start, seg2_start, seg1_end):
        return True
    if o2 == 0 and on_segment(seg1_start, seg2_end, seg1_end):
        return True
    if o3 == 0 and on_segment(seg2_start, seg1_start, seg2_end):
        return True
    if o4 == 0 and on_segment(seg2_start, seg1_end, seg2_end):
        return True
    
    return False

# Example usage
segment1_start = (1, 1)
segment1_end = (10, 10)
segment2_start = (8, 1)
segment2_end = (4, 2)

# Draw the graphs using matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Plot the segments
plt.plot([segment1_start[0], segment1_end[0]], [segment1_start[1], segment1_end[1]], color='red')
plt.plot([segment2_start[0], segment2_end[0]], [segment2_start[1], segment2_end[1]], color='blue')

plt.show()

if do_segments_intersect(segment1_start, segment1_end, segment2_start, segment2_end):
    print("Segments intersect!")
else:
    print("Segments do not intersect.")
