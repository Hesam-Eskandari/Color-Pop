#Developped By Hesam Eskandari
#https://www.instagram.com/eskandarihesam
#https://github.com/Hesam-Eskandari
#https://www.facebook.com/EskandariHesam


from cv2 import EVENT_LBUTTONUP, imshow, imread, waitKey, destroyAllWindows, COLOR_BGR2GRAY
from cv2 import cvtColor, namedWindow, setMouseCallback, COLOR_GRAY2BGR, COLOR_BGR2HSV
from cv2 import COLOR_HSV2BGR, EVENT_LBUTTONDOWN, EVENT_MOUSEMOVE, imwrite, resize
from numpy import shape

def click(event,x,y,flags,param):
    """
    Input: (mouse_type_event,x_event_position,y_event_position,flags,parameters)
    Output: global defined variables
    """
    global x_c,y_c, continum 
    if event == EVENT_LBUTTONUP:
        x_c,y_c = x,y
        continum = 1 - continum
        
    elif event == EVENT_MOUSEMOVE and continum == 1:
        x_c,y_c,continum = x,y,1
    else:
        x_c,y_c = 0,0
def color(ground,gr_pop,x_c,y_c):
    """
    Input:(original_image,under_live_process_image,cursor_x,cursor_y)
    Output: processed_gr_pop
    """
    gr_hsv = cvtColor(ground,COLOR_BGR2HSV)
    global coords
    #coords = np.aray([[x_c,y_c]])
    coords = [[x_c,y_c]]
    #a = 15
    gr_pop_hsv = cvtColor(gr_pop,COLOR_BGR2HSV)
    #def tail(ground,x,y,a,i=0):
    def tail(gr_hsv,x,y,a,i=0):
        """
        Input: (original_image,examin_x,examin_y,step_size)
        Output: chosen_coords
        """
        thresh1, thresh2, thresh3 = 4, 205, 250
        for item in [(x-a+1,y),(x,y-a+1),(x+a-1,y),(x,y+a-1)]:
            allow = 1
            for element in coords:
                if element == [item[0],item[1]]:
                    allow = 0
                    #print('here_allow')
            if allow == 1:
                if item[1]<shape(gr_hsv)[0] and item[0]<shape(gr_hsv)[1]:
                #if item[1]<shape(ground)[0] and item[0]<shape(ground)[1]:
                    if gr_pop_hsv[item[1],item[0],0] == 0:
                        #if abs(ground[item[1],item[0],0]-ground[y,x,0]) < thresh1:
                        if abs(gr_hsv[item[1],item[0],0]-gr_hsv[y,x,0]) < thresh1:
                            #if abs(ground[item[1],item[0],1]-ground[y,x,1]) < thresh2:
                            if abs(gr_hsv[item[1],item[0],1]-gr_hsv[y,x,1]) < thresh2:
                                #if abs(ground[item[1],item[0],2]-ground[y,x,2]) < thresh3:
                                if abs(gr_hsv[item[1],item[0],2]-gr_hsv[y,x,2]) < thresh3:
                                    #coords = np.append(coords,[[item[0],item[1]]],axis=0)
                                    coords.append([item[0],item[1]])
                                    #print(i)
                                    if i >= 1000:
                                        break
                                    else:
                                        #tail(ground,item[0],item[1],a,i+1)
                                        tail(gr_hsv,item[0],item[1],a,i+1)
        click(0,0,0,0,0)
        #print('i=',i)
        return coords
    
    #coords = tail(ground,x_c,y_c,a,0)
    coords = tail(gr_hsv,x_c,y_c,a,0)
    #print(coords)                   
        
    #h,s,v = gr_hsv[y_c,x_c,:]
    
    for item in coords:
        x,y = item[0],item[1]
        m_y,M_y = max(y-a+1,0),min(y+a,shape(ground)[0])
        m_x,M_x = max(x-a+1,0),min(x+a,shape(ground)[1])
        #gr_pop_hsv[m_y:M_y,m_x:M_x,:] = gr_hsv[m_y:M_y,m_x:M_x,:].copy()
        #gr_pop = cvtColor(gr_pop_hsv,COLOR_HSV2BGR)
        gr_pop[m_y:M_y,m_x:M_x,:] = ground[m_y:M_y,m_x:M_x,:].copy()
    return gr_pop
global continum, a
a,mode = 4,1
continum = 0
x_c,y_c = 0,0
namedWindow('desk')
setMouseCallback('desk',click)
#ground = np.ones((300,600,3),'uint8')
ground = imread('photo5.jpg')
ground = resize(ground,(int(650*shape(ground)[1]/shape(ground)[0]),650))
gr_pop = cvtColor(ground,COLOR_BGR2GRAY)
gr_pop = cvtColor(gr_pop,COLOR_GRAY2BGR)
#gr_pop = 255*np.ones((300,600,3),'uint8')
while True:
    imshow('desk',gr_pop)
    key = waitKey(40*mode) & 0xFF
    if key == 27:
        break
    elif key == 49:
        a,mode = 3,1
    elif key == 50:
        a,mode = 4,1
    elif key == 51:
        a,mode = 6,2
    elif key == 52:
        a,mode = 8,3
    elif key == 53:
        a,mode = 12,5
    elif key == 54:
        a,mode = 15,5
    if x_c != 0:
        gr_pop = color(ground,gr_pop,x_c,y_c)
        #print(np.shape(gr_pop))
        click(0,0,0,0,0)
destroyAllWindows()
imwrite('color_pop.jpg',gr_pop)