#!/usr/bin/env python
# coding: utf-8

# In[67]:


def arrows(frame_height,frame_width,length):
    
    '''
    Cordinates to draw indicating arrows
    frame_height : height of frame
    frame_width : width of frame
    length: length of arrow to be drawn
    return : Dictionary of arrows for various moves
    '''
    
    center_x = frame_width//2
    center_y = frame_height//2
    gap = 80
    
    u = ( center_x+length-20, center_y-gap,  center_x - length+20 , center_y-gap)
    u_h = (center_x - length+20 , center_y-gap, center_x+length-20,center_y-gap)
    d = (center_x - length +20, center_y+gap , center_x+length-20,center_y+gap)
    d_h = ( center_x+length-20,center_y+gap, center_x - length+20, center_y+gap)
    
    l = (center_x-gap , center_y-length , center_x-gap ,center_y+length)
    l_h = (center_x-gap ,center_y+length,center_x-gap , center_y-length )
    r = ( center_x+gap ,center_y+length,center_x+gap , center_y-length )
    r_h= (center_x+gap , center_y-length , center_x+gap ,center_y+length)
    
    
    
    
    arrows = {"R":[r] , "U":[u] , "L":[l],"D":[d] ,"R'":[r_h] , "U'":[u_h] , "L'":[l_h],"D'":[d_h] , "F":[u_h,d_h,l_h,r_h],
              "F'":[u,d,l,r] , "B":[u,d,l,r] , "B'":[u_h,d_h,l_h,r_h]}
    
    return arrows


# In[68]:


def getGrid(frame_height,frame_width):
    '''
    Generating Co-ordinate to draw the grid
    frame_height : height of frame
    frame_width : width of frame
    return : Dictionary of coordinate for grid
    '''
    
    
    center_x = frame_width//2
    center_y = frame_height//2
    width = 25
    height = 25
    gap=42
    
    
    gridPos=[ 
              [center_x-(width//2)-gap-width ,center_y-(height//2)-gap-height, center_x-(width//2)-gap , center_y-(height//2)-gap],
              [center_x-width//2 , center_y-(height//2)-gap-height , center_x+width//2 , center_y-(height//2)-gap],
              [center_x+(width//2)+gap , center_y-(height//2)-gap-height , center_x+(width//2)+gap+width , center_y-(height//2)-gap],
        
              [center_x-(width//2)-gap-width , center_y-height//2 , center_x-(width//2)-gap , center_y+height//2],
              [center_x-width//2 , center_y-height//2 , center_x+width//2 , center_y+height//2],
              [center_x+(width//2)+gap , center_y-height//2 , center_x+(width//2)+gap+width , center_y+height//2],
             
             
              [center_x-(width//2)-gap-width , center_y+(height//2)+gap , center_x-(width//2)-gap ,center_y+(height//2)+gap+height],
              [center_x-width//2 , center_y+(height//2)+gap , center_x+width//2 , center_y+(height//2)+gap+height],
              [center_x+(width//2)+gap , center_y+(height//2)+gap, center_x+(width//2)+gap+width , center_y+(height//2)+gap+height]
            ]
    
    return gridPos
def visualCube(fixed=False):
    '''
    Generating Co-ordinates for visual cube 
    return: List of co-ordinates to draw grid
    '''
    
    if not fixed:
        width = 20
        height = 20
        startx,starty = 20,10
    else:
        width = 15
        height = 15
        startx,starty = 20,90
    grid=[]
    for i in range(1,10):
        grid.append( [startx,starty,startx+width,starty+height])
        startx+=width
        if i%3==0:
            starty+=height
            startx = 20
    return grid


# In[69]:


def getRoi(frame,gridPos):
    '''
    Function to return color at each of the grid
    frame: frame 
    gridPos: position of the 9 grids
    return : color in all nine grids in form of string - Example "bbwyogrgr"
    '''
    
    color = ""
    for i in range(len(gridPos)):
        roi = frame[gridPos[i][1]:gridPos[i][3] , gridPos[i][0]:gridPos[i][2]]
        roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        all_contour = []
        for key,j in COLORS.items():
            mask = cv2.inRange(roi,j[0],j[1])
            cnts,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            max_area=0
            for c in cnts:
                area = cv2.contourArea(c)
                if area>max_area:
                    max_area=area
            if max_area>300:
                all_contour.append((key,max_area))
        if len(all_contour)>0:
            color_key = max(all_contour , key = lambda x: x[1])[0]
            if color_key == 'r1' or color_key=='r2':color_key = 'r'
            if color:color += color_key
            else:color=color_key
    if len(color)==9:
        return color
    return False
    


# In[70]:


def solve(cube,actual_pattern):
    '''
    Function to solve rubiks cube using Koceimba. 
    cube: Dictionary containing colors in all the faces of cube
    actual_pattern: Actual color pattern of your cube
    return : List containing all the moves to solve the given cube
    '''
    
    pattern = "ybrgow"
    CUBE = ['' for _ in range(6)]
    for key,i in cube.items():
        c = ""
        for j in i:
            c += pattern[ actual_pattern.index(j)  ]
        CUBE[actual_pattern.index(key)] = c
    cube = ''.join(CUBE)
    for i in pattern:
        x = cube.count(i)
        if x!=9:
            return False
    try:
        x = utils.solve(cube,'Kociemba')
        y = []
        for i in x:
            i=str(i)
            #if '2' in i:
            #    i=i[:-1]
            #    y.append(i)
            y.append(i)
        return y
    except:
        return False


# In[71]:


def reset():
    '''
    Reinitialise Diffrent variables in case some error arises
    return: various temperort variables requires in main programe
    '''
    
    
    pattern = "ybrgow"
    faces = {i:'' for i in pattern}
    sub = {i:i for i in pattern}
    counter = 0
    previousColor = None
    conf = 0
    temp_pattern,actual_pattern = "",""
    got_color=False
    
    return pattern,faces,sub,counter,previousColor,conf,temp_pattern,actual_pattern,got_color


# In[72]:


#===========SOLVING STAGE=================


def stage2(cam,answer,front_face,arrow):
    '''
    Stage2 i.e the solving stage where various arrows are indicated 
    cam: reference to webcam
    answer: moves to solve the cube
    front_face: Color at the center of front face of the cube
    arrow: Dictionary containig cordinates to draw arrow for various moves
    return: None
    
    '''
    
    pause_time = 7 #time for next move to display
    previousColor = None
    conf = 0
    start = False
    counter = 0
    previousTime = None
    while True:
        _,frame = cam.read()
        frame=cv2.resize(frame,(frame_width,frame_height))
      
        if  counter<len(answer):
            color = getRoi(frame,gridPos)
            if color and not start :
                    if not previousColor:previousColor=color
                    if color == previousColor:conf+=1
                    elif color!=previousColor:
                        conf=0
                        previousColor=None
                    if conf>=15 and color[4]==front_face:
                        start=True
                        previousTime = time.time()

            if start:     
                ans = answer[counter]
                y = ans.replace('2','')
                x = arrow[y]
                if 'F' in ans:dir_text="Front Face"
                elif 'B' in ans:dir_text="Back Face"
                else:dir_text = ""
                for c,i in enumerate(x):
                    if "U2" in ans or "D2" in ans:
                        
                        cv2.arrowedLine(frame,(i[0],i[1]+17),(i[2],i[3]+17),(58,184,0),2)
                    if "R2" in ans or "L2" in ans:
                        cv2.arrowedLine(frame,(i[0]-17,i[1]),(i[2]-17,i[3]),(58,184,0),2)

                    if "F2" in ans or "B2" in ans:
                        if c<2:
                            cv2.arrowedLine(frame,(i[0],i[1]-20),(i[2],i[3]-20),(58,184,0),2)
                        else:
                            cv2.arrowedLine(frame,(i[0]-20,i[1]),(i[2]-20,i[3]),(58,184,0),2)

                    cv2.arrowedLine(frame,(i[0],i[1]),(i[2],i[3]),(58,184,0),2)

                cv2.putText(frame,dir_text , (int(frame_width//2 - 55) ,80) , cv2.FONT_HERSHEY_SIMPLEX,0.8,(58,184,0),2)
                cv2.putText(frame,ans , (30,40) , cv2.FONT_HERSHEY_SIMPLEX,1.2,(90,255,20),2)

                if time.time()-previousTime >= pause_time:
                    counter+=1
                    previousTime = time.time()
            else:
                cv2.putText(frame,"Please Keep front face towards the camera and top face upwards..." , (50,50) , cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)
            cv2.rectangle(frame,((frame_width//2)-15 , (frame_height//2)-15),((frame_width//2)+15 , (frame_height//2)+15) , (255,255,255),2)

        cv2.imshow("a",frame)
        if cv2.waitKey(5)==ord('q'):
            break


# In[76]:


def stage1():
    '''
    Color picking stage from all the faces of the cube
    return: None
    '''
    pattern,faces,sub,counter,previousColor,conf,temp_pattern,actual_pattern,got_color = reset()
    cam=cv2.VideoCapture(0)
    pt = time.time()
    tt=7
    while True:
        if got_color:
            answer = solve(faces,actual_pattern)
            #print(faces,actual_pattern)
            print(answer)
            if not answer:
                stage1()
                pattern,faces,sub,counter,previousColor,conf,temp_pattern,actual_pattern,got_color = reset()
            else:
                stage2(cam,answer,front_face,arrow)
                cam.release()
                cv2.destroyAllWindows()
                break
            #========GO TO STAGE2 HERE==========
        
        _,frame = cam.read()
        frame=cv2.resize(frame,(frame_width,frame_height))
        

        
        
        if time.time()-pt<=tt:
            cv2.putText(frame,"Keep top face towards the camera and front face towards the bottom!",(int(frame_width//2 - 270),20),cv2.FONT_HERSHEY_SIMPLEX,0.48,(0,255,255),2)
            cv2.putText(frame,"Starting in: " +str(tt - int(time.time()-pt)),(int(frame_width//2 - 150),70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
        else:
            color = getRoi(frame,gridPos)

            if color :
                if not previousColor:previousColor=color
                if color == previousColor:conf+=1
                elif color!=previousColor:
                    conf=0
                    previousColor=None

                if conf>=25:
                    center = color[4]
                    faces[center] = color
                    if center not in temp_pattern:
                        temp_pattern+=center
                    conf = 0
                    previousColor = None
                    if list(faces.values()).count('') == 0:
                        for k in seq:
                            actual_pattern+=temp_pattern[k]
                        front_face = actual_pattern[2]
                        got_color = True

            counter = len(temp_pattern)
            if not got_color:
                try:
                    cv2.putText(frame,texts[counter] , (frame_width//2 - 75,50) , cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,50,255),2)
                except:
                    pass
            else:cv2.putText(frame,"Solving,Please Wait..." , (100,50) , cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)



            for j,i in enumerate(visualGrid):
                try:
                    color_key = color[j]
                    if color_key=='r':clr=(0,0,255)
                    elif color_key=='g':clr=(0,255,0)
                    elif color_key=='b':clr=(255,0,0)
                    elif color_key=='y':clr=(0,255,255)
                    elif color_key=='o':clr=(175,55,245)
                    elif color_key=='w':clr=(255,255,255)
                    else:clr=(166, 156, 162)

                except:
                    clr = (166, 156, 162)
                cv2.rectangle(frame,(i[0],i[1]),(i[2],i[3]),clr,-1)
                cv2.rectangle(frame,(i[0]-1,i[1]-1),(i[2]+1,i[3]+1),(0,0,0) ,1)

            for i in range(6) :
                clrs = [(166, 156, 162) for _ in range(9)]
                color_key = faces[pattern[i]]
                if color_key!='':
                    clrs=[]
                    for j in color_key:
                        if j=='r':clr=(0,0,255)
                        elif j=='g':clr=(0,255,0)
                        elif j=='b':clr=(255,0,0)
                        elif j=='y':clr=(0,255,255)
                        elif j=='o':clr=(175,55,245)
                        elif j=='w':clr=(255,255,255)
                        clrs.append(clr)

                #Drawing indicator here

                for p,q in enumerate(fixedGrid):
                    cv2.rectangle(frame,(q[0],q[1]+(i*65)),(q[2],q[3]+(i*65)),clrs[p],-1)
                    cv2.rectangle(frame,(q[0],q[1]+(i*65)-1),(q[2],q[3]+(i*65)+1),(0,0,0),1)
                cv2.putText(frame,seq_text[i],(fixedGrid[0][0],(fixedGrid[0][1]-3)+(i*65)),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,165,255),1)
        
        for i in gridPos:
                cv2.rectangle(frame,(i[0],i[1]),(i[2],i[3]),(255,255,255),2)
        cv2.imshow("a",frame)
        if cv2.waitKey(5)&0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break

    return -1


# In[78]:


import cv2
import numpy as np
from rubik_solver import utils
import time
import sys
#NOTE: TRY USING GOOD LIGHTING SOURCE



#===========FEEL FREE TO CHANGE THE RANGES ACCORDING TO YOUR CUBE COLOR=========
GREEN = [np.array([50,90,30]) , np.array([85,255,255])]
BLUE = [np.array([100,90,30]) , np.array([135,255,255])]
YELLOW = [np.array([15,90,30]) , np.array([50,255,255])]
PINK = [np.array([145,90,30]) , np.array([175,255,255])]
RED1 =[np.array([0,90,30]) , np.array([12,255,255])]
RED2 = [np.array([170,90,30]) , np.array([180,255,255])]
WHITE = [np.array([0,0,35]) , np.array([255,90,255])]
#===========================================

COLORS = { 'w':WHITE,'g':GREEN,'b':BLUE,'y':YELLOW,'o':PINK , 'r1':RED1 , 'r2':RED2 } #DO NOT CAHNGE

frame_height,frame_width = 480,640
gridPos = getGrid(frame_height,frame_width)
pattern,faces,sub,counter,previousColor,conf,temp_pattern,actual_pattern,got_color = reset()
texts = ["Show Top Face" ,"Show Bottom Face" , "Show Right Face",
        "Show Back Face " , "Show Left Face" ,"Show Front Face"]    #045231
seq = [0,4,5,2,3,1] 
seq_text = ["Top","Left","Front","Right","Back","Bottom"]
#RUBIK_SOLVER ACCEPTS COLOR BE ARRANGED ACC. TO. FOLLOWING SEQUENCE - TOP,LEFT,FRONT,RIGHT,BACK,BOTTOM
visualGrid = visualCube()
fixedGrid = visualCube(fixed=True)

arrow_length = int(0.15*frame_height)
arrow = arrows(frame_height,frame_width,arrow_length)

if __name__=="__main__":
    stage1()
    sys.exit()


# In[ ]:





# In[ ]:




