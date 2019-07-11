#Developped By Hesam Eskandari
#https://www.instagram.com/eskandarihesam
#https://github.com/Hesam-Eskandari
#https://www.facebook.com/EskandariHesam
#keyboard keys: 1,2,3,4,5,6,7,8,9 for size of the pen or eraser and 'r' as reverse mode for the eraser
#go to line 90 to change the photo's name to load (default name is 'photo.jpg')

from cv2 import EVENT_LBUTTONUP, imshow, imread, waitKey, destroyAllWindows, COLOR_BGR2GRAY
from cv2 import cvtColor, namedWindow, setMouseCallback, COLOR_GRAY2BGR, COLOR_BGR2HSV
from cv2 import COLOR_HSV2BGR, EVENT_LBUTTONDOWN, EVENT_MOUSEMOVE, imwrite, resize
from numpy import shape, append, array, sum

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
def color(ground,gr_pop,x_c,y_c,original,reverse):
    """
    Input:(original_image,under_live_process_image,cursor_x,cursor_y)
    Output: processed_gr_pop
    """
    if reverse == 1:
        gray_subs =  cvtColor(ground.copy(),COLOR_BGR2GRAY)
        ground_c = cvtColor(gray_subs,COLOR_GRAY2BGR)
    else:
        ground_c = ground.copy()
    gr_hsv = cvtColor(ground_c,COLOR_BGR2HSV)
    global coords
    coords = [[x_c,y_c]]
    gr_pop_hsv = cvtColor(gr_pop,COLOR_BGR2HSV)

        
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
            if allow == 1:

                if abs(item[1])<shape(gr_hsv)[0] and abs(item[0])<shape(gr_hsv)[1]:
                    if gr_pop_hsv[item[1],item[0],0] == 0:
                        if abs(gr_hsv[item[1],item[0],0]-gr_hsv[y,x,0]) < thresh1:
                            if abs(gr_hsv[item[1],item[0],1]-gr_hsv[y,x,1]) < thresh2:
                                if abs(gr_hsv[item[1],item[0],2]-gr_hsv[y,x,2]) < thresh3:
                                    coords.append([item[0],item[1]])
                                    if i >= 1000:
                                        break
                                    else:
                                        tail(gr_hsv,item[0],item[1],a,i+1)


                                
        click(0,0,0,0,0)
        return coords
    if not reverse:
        coords = tail(gr_hsv,x_c,y_c,a,0)
    else:
        coords = [[x_c,y_c]]                  
    
    for item in coords:
        x,y = item[0],item[1]
        m_y,M_y = max(y-a+1,0),min(y+a,shape(ground_c)[0])
        m_x,M_x = max(x-a+1,0),min(x+a,shape(ground_c)[1])
        gr_pop[m_y:M_y,m_x:M_x,:] = ground_c[m_y:M_y,m_x:M_x,:].copy()
        original = append(original,[[m_y,M_y,m_x,M_x,reverse]],axis=0)
    return gr_pop, original
global continum, a
original = array([[0,0,0,0,0]])
a,mode = 4,1
continum = 0
x_c,y_c = 0,0
namedWindow('desk')
setMouseCallback('desk',click)
ground2 = imread('photo.jpg')
coeff = 1000
ground = resize(ground2,(int(coeff*shape(ground2)[1]/float(shape(ground2)[0])+0.5),int(coeff+0.5)))
gr_pop = cvtColor(ground,COLOR_BGR2GRAY)
gr_pop = cvtColor(gr_pop,COLOR_GRAY2BGR)
reverse = 0
while True:
    imshow('desk',gr_pop)
    key = waitKey(1*mode) & 0xFF
    if key == 27:
        break
    elif key == 49:
        a,mode = 2,1
    elif key == 50:
        a,mode = 3,1
    elif key == 51:
        a,mode = 4,1
    elif key == 52:
        a,mode = 6,2
    elif key == 53:
        a,mode = 9,3
    elif key == 54:
        a,mode = 12,4
    elif key == 55:
        a,mode = 15,5
    elif key == 56:
        a,mode = 18,6
    elif key == 57:
        a,mode = 22,7
    elif key == ord('r'):
        reverse = 1-reverse
        a = 4
        key = 255
    if x_c != 0:
        gr_pop, original = color(ground.copy(),gr_pop,x_c,y_c,original,reverse)
        click(0,0,0,0,0)
destroyAllWindows()
original = original[1:,:]*shape(ground2)[0]/float(shape(ground)[0])+0.5
original = original.astype('uint16')
gray_final = cvtColor(ground2,COLOR_BGR2GRAY)
color_pop_final = cvtColor(gray_final,COLOR_GRAY2BGR)
gray = color_pop_final.copy()
for row in original:
    if not row[-1]:
        color_pop_final[row[0]:row[1],row[2]:row[3],:]=ground2[row[0]:row[1],row[2]:row[3],:]
    else:
        color_pop_final[row[0]:row[1],row[2]:row[3],:]=gray[row[0]:row[1],row[2]:row[3],:]
imwrite('color_pop.jpg',color_pop_final)


# In[31]:


x = np.array([[1,2]])
x = np.append(x,[[2,3]],axis=0)
x = np.append(x,[[2,4]],axis=0)
print(x)
sum(np.isin(x,[1,2]),0)


# In[34]:




