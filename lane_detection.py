import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

while True:
    ret,lanes = cap.read()

    ###REGION OF INTEREST THROUGH MASKINg
    mask1 = np.zeros((1080,1920),dtype=np.uint8)
    print(mask1.shape)
    trapezoid_points = np.array([[0,1079],[1919,1079], [1034,580],[784,580]],dtype=np.int32)
    trapezoid_points = trapezoid_points.reshape(-1,1,2)
    cv2.fillPoly(mask1, [trapezoid_points] ,255)

    lane_withmask = cv2.bitwise_and(lanes,lanes,mask=mask1)


    ###CLAHE TO TURN UP THE CONTRAST lanes be more visible
    lane_withmask = cv2.cvtColor(lane_withmask, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lane_withmask)

    clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(6, 6))

    new_l_channel = clahe.apply(l_channel)
    merged = cv2.merge([new_l_channel, a_channel, b_channel])
    lane_withmask = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)



    ##PREPROCESSING STUFF(THRESHOLDING based off of the hue saturation value 
    lane_withmask = cv2.cvtColor(lane_withmask, cv2.COLOR_BGR2HSV)
    lower_HSV = np.array([0,0,205])
    upper_HSV = np.array([179,110,255])
    lane_withmask = cv2.inRange(lane_withmask, lower_HSV, upper_HSV )



    #EDGE DETECTION usin the Canny Function built into opencv
    med_val = np.median(lane_withmask)
    threshold1 = int(max(0,.9*med_val))
    threshold2 = int(min(255,1.8*med_val))

    lanes_edge = cv2.Canny(lane_withmask, threshold1, threshold2)


    ##Gettin lnies from the edge detection hough line transformation
    lines = cv2.HoughLinesP(lanes_edge, rho=1, theta=np.pi / 180, threshold=25,         # votes needed to be a line  
                            minLineLength=40,      # minimum line lengthmaxLineGap=25          # allowed gap between segments
    )

    if lines is None:
        cv2.imshow('lane_detector', lanes)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        continue


    left_lane_slopes = []
    right_lane_slopes = []
    left_lane_intercepts = []
    right_lane_intercepts = []

    for line in lines:
        x1,y1,x2,y2 = line[0]

        if x1!=x2:
            line_slope = (y2-y1)/(x2-x1)
            line_midpoint_x = (x1+x2)/2
            line_midpoint_y = (y1+y2)/2
            line_intercept = line_midpoint_y - (line_slope*line_midpoint_x)

            if abs(line_slope) >= .65 and abs(line_slope)<=.9:
                # cv2.line(lanes,(x1,y1),(x2,y2),(0,0,255),5)
                if max(x1,x2) < 960 and line_slope < 0:
                    left_lane_slopes.append(line_slope) 
                    left_lane_intercepts.append(line_intercept)
                
                if min(x1,x2) > 960 and line_slope > 0:
                    right_lane_slopes.append(line_slope)
                    right_lane_intercepts.append(line_intercept)

    ##trimming in case of outliers        
    trimming_value_leftslopes = math.floor(.1 * len(left_lane_slopes))
    trimming_value_rightslopes = math.floor(.1 * len(right_lane_slopes))
    trimming_values_leftintercepts = math.floor(.1*len(left_lane_intercepts))
    trimming_values_rightintercepts = math.floor(.1*len(right_lane_intercepts))

    left_lane_slopes.sort()
    right_lane_slopes.sort()
    left_lane_intercepts.sort()
    right_lane_intercepts.sort()

    if trimming_value_leftslopes>0:
        left_lane_slopes = left_lane_slopes[trimming_value_leftslopes:-1*trimming_value_leftslopes]
    if trimming_value_rightslopes>0:
        right_lane_slopes = right_lane_slopes[trimming_value_rightslopes:-1*trimming_value_rightslopes]

    if trimming_values_leftintercepts>0:
        left_lane_intercepts = left_lane_intercepts[trimming_values_leftintercepts:-1*trimming_values_leftintercepts]
    if trimming_values_rightintercepts>0:
        right_lane_intercepts = right_lane_intercepts[trimming_values_rightintercepts:-1*trimming_values_rightintercepts]

    print("Left Lane Intercepts: ", left_lane_intercepts)
    print("Left Lane Slopes: ", left_lane_slopes)
    print("Right Lane Intercepts: ", right_lane_intercepts)
    print("Right Lane Slopes: ", right_lane_slopes)

    if len(left_lane_slopes) == 0 or len(right_lane_slopes) == 0:
        cv2.imshow('lane_detector', lanes)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        continue

    left_lane_intercept_average = sum(left_lane_intercepts)/len(left_lane_intercepts)
    right_lane_intercept_average = sum(right_lane_intercepts)/len(right_lane_intercepts)
    left_lane_slopes_average = sum(left_lane_slopes)/len(left_lane_slopes)
    right_lane_slopes_average = sum(right_lane_slopes)/len(right_lane_slopes)

    y_bottom = 1079
    y_top = 700

    #extrapolating lines from one given y to another given y on the screen to generate lane lines
    left_bottom_point = int((y_bottom - left_lane_intercept_average) / left_lane_slopes_average)
    right_bottom_point = int((y_bottom - right_lane_intercept_average) / right_lane_slopes_average)

    left_top_point = int((y_top - left_lane_intercept_average) / left_lane_slopes_average)
    right_top_point = int((y_top - right_lane_intercept_average) / right_lane_slopes_average)


    cv2.line(lanes,(left_bottom_point,y_bottom),(left_top_point,y_top),(0,0,255),10)
    cv2.line(lanes,(right_bottom_point,y_bottom),(right_top_point,y_top),(0,0,255),10)









    
    cv2.imshow('lane_detector',lanes)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break