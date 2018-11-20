#!usr/bin/python
# -*- coding: utf-8 -*- 


import numpy as np 
import cv2 
# initialize the known distance from the camera to the object, 
# which in this case is 24 inches 
KNOWN_DISTANCE = 27.0 
# initialize the known object width, which in this case, 
# the piece of paper is 11 inches wide 
KNOWN_WIDTH = 11.69 
KNOWN_HEIGHT = 8.27
WARNING_DISTANCE = 1.0

cap = cv2.VideoCapture(0)
img_path="DC1002.jpg"
firstimg=cv2.imread("DC1002.jpg")

last_photo = firstimg
new_photo = firstimg
c=1
# initialize the list of images that we'll be using 
IMAGE_PATHS = ["DC10002.jpg", "DC10003.jpg","DC10008.jpg","DC10011.jpg","DC10012.jpg","DC1002.jpg", "DC1003.jpg","DC1004.jpg","DC10013.jpg","DC10014.jpg","DC10015.jpg","DC10016.jpg","DC10019.jpg","DC10021.jpg",
"DC10024.jpg","DC10025.jpg","DC10026.jpg","DC10028.jpg","DC10031.jpg","DC10032.jpg","DC10033.jpg","DC10034.jpg","DC10035.jpg","DC10036.jpg",
"DC10037.jpg","DC10038.jpg","DC10039.jpg","DC10040.jpg","DC10041.jpg","DC10042.jpg","DC10043.jpg","DC10044.jpg","DC10045.jpg"]
def find_marker(image): 
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # 将彩色图转化为灰度图 
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0) 
    #cv2.imshow("gray_img",gray_img)
    # 高斯平滑去噪 
    #thresh_img=cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY_INV)
    
    #cv2.imshow("thresh_img",gray_img)

    edged_img = cv2.Canny(gray_img, 50, 125)
    # Canny算子阈值化 
    #cv2.imshow("edged_img",edged_img) 
    img, countours, hierarchy = cv2.findContours(edged_img.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # 注意，findcontours函数会“原地”修改输入的图像。opencv3会返回三个值,分别是img, countours, hierarchy 
    # 第二个参数表示轮廓的检索模式,cv2.RETR_EXTERNAL表示只检测外轮廓；v2.RETR_LIST检测的轮廓不建立等级关系 
    # cv2.RETR_CCOMP建立两个等级的轮廓；cv2.RETR_TREE建立一个等级树结构的轮廓。 
    # 第三个参数method为轮廓的近似办法,cv2.CHAIN_APPROX_NONE存储所有的轮廓点， 
    # 相邻的两个点的像素位置差不超过1，即max（abs（x1 - x2），abs（y2 - y1）） == 1 
    # cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标， 
    # 例如一个矩形轮廓只需4个点来保存轮廓信息 
    #cv2.drawContours(image,countours,-1,(0,0,255),2,8) 
    # # 第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。 
    # 
    #cv2.imshow('image', image) 
    #print(len(countours))
    # 输出如下：15，即该图检测出15个轮廓 
    c = max(countours, key = cv2.contourArea) 
   
    # 提取最大面积矩形对应的点集 
    rect = cv2.minAreaRect(c) 
    #print(rect)
    # cv2.minAreaRect()函数返回矩形的中心点坐标，长宽，旋转角度[-90,0)，当矩形水平或竖直时均返回-90 
    # c代表点集，返回rect[0]是最小外接矩形中心点坐标， 
    # rect[1][0]是width，rect[1][1]是height，rect[2]是角度 

    # box = cv2.boxPoints(rect) # # 但是要绘制这个矩形，我们需要矩形的4个顶点坐标box, 通过函数cv2.boxPoints()获得， 
    # # 即得到box：[[x0, y0], [x1, y1], [x2, y2], [x3, y3]] 
    # # print(box)，输出如下： 
    # # [[508.09482 382.58597] 
    # # [101.76947 371.29916] 
    # # [109.783356 82.79956] 
    # # [516.1087 94.086365]] 
    # # # 根据检测到的矩形的顶点坐标box，我们可以将这个矩形绘制出来，如下所示： 
    # for i in range(len(box)): 
    #   cv2.line(image, (box[i][0],box[i][1]),(box[(i+1)%4][0],box[(i+1)%4][1]),(0,0,255),2,8) 
    # cv2.imshow('image', image) 
    return rect 
# def Location(img_path,)
def distance_to_camera(knownWidth, focalLength, perWidth): 
    return (knownWidth * focalLength) / perWidth 

def calculate_focalDistance(img_path): 
    first_image = cv2.imread(img_path) 
    # cv2.imshow('first image',first_image) 
    marker = find_marker(first_image) 
    # 得到最小外接矩形的中心点坐标，长宽，旋转角度 
    
    # 其中marker[1][0]是该矩形的宽度，单位为像素 
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH 
    # 获取摄像头的焦距 
    #print('焦距（focalLength ）= ',focalLength) 
    # 将计算得到的焦距打印出来 
    return focalLength

def calculate_Distance(image_path,focalLength_value,dis_x,dis_y,dis_z): 
    # 加载每一个图像的路径，读取照片，找到A4纸的轮廓 
    # 然后计算A4纸到摄像头的距离 
    image = image_path 
    cv2.imshow("image", image) 
#    cv2.waitKey(300) 

    marker = find_marker(image) 
    center_x=np.int0(marker[0][0])
    center_y=np.int0(marker[0][1])
    distance_inches = distance_to_camera(KNOWN_WIDTH,focalLength_value, marker[1][0]) 
    # 计算得到目标物体到摄像头的距离，单位为英寸， 
    # 注意，英寸与cm之间的单位换算为： 1英寸=2.54cm 

    box = cv2.boxPoints(marker) 
    # print( box )，输出类似如下： 
    # [[508.09482 382.58597] 
    # [101.76947 371.29916] 
    # [109.783356 82.79956] 
    # [516.1087 94.086365]] 
    box =np.int0( box) 
    # 将box数组中的每个坐标值都从浮点型转换为整形 
    # print( box )，输出类似如下： 
    # [[508 382] 
    # [101 371] 
    # [109 82] 
    # [516 94]] 
    cv2.drawContours(image, [box], -1, (0, 0, 255), 2) 
    # 在原图上绘制出目标物体的轮廓 

    cv2.line(image,(center_x,center_y),(center_x,center_y),(0,255,0),2)

    rdis_x=dis_x
    rdis_y=dis_y
    rdis_z=dis_z
    
    if abs(rdis_x) <= WARNING_DISTANCE and abs(rdis_y) <= WARNING_DISTANCE and abs(rdis_z) <= WARNING_DISTANCE:
        cv2.putText(image,"System is normal",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    else:
        if abs(rdis_x) > WARNING_DISTANCE:
             cv2.putText(image,"Warning : distance X exceeds threshold",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
        else:
            if abs(rdis_y) > WARNING_DISTANCE:
                cv2.putText(image,"Warning : distance Y exceeds threshold",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
            else:
                if abs(rdis_z) > WARNING_DISTANCE:
                    cv2.putText(image,"Warning : distance Z exceeds threshold",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1) 
    

    #cv2.putText(image,image_path,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.putText(image,"ActurlX=%2f"%center_x,(image.shape[1] - 600, image.shape[0] - 50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)

    cv2.putText(image,"ActurlY=%2f"%center_y,(image.shape[1] - 600, image.shape[0] - 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)

    cv2.putText(image, "The distance from camera %.2fcm" % (distance_inches * 2.54), (image.shape[1] - 600, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1) 
    # cv2.putText()函数可以在照片上添加文字 
    # cv2.putText(img, txt, (int(x),int(y)), fontFace, fontSize, fontColor, fontThickness) 
    # 各参即为：照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细 
    cv2.imshow("image", image)
 
def get_dis(image_path):
    image = image_path
 #   cv2.imshow("image", image) 
 #   cv2.waitKey(300) 
    marker = find_marker(image)
    return marker

if __name__ == "__main__": 
    while(1):
        print("the num %2f"%c)
        ret,frame = cap.read()
        last_photo=new_photo
        new_photo= frame

        img_path1 = "DC1002.jpg"
        img_path2 = "DC1003.jpg"
        img_path = "DC1002.jpg"
        focalLength = calculate_focalDistance(img_path)
        print(focalLength)

#        for i in range(0,30) :
#           img_path1 = IMAGE_PATHS[i]
#           img_path2 = IMAGE_PATHS[i+1]

#           print(IMAGE_PATHS[i])
#           print(IMAGE_PATHS[i+1])

   
 
        marker1=get_dis(last_photo)
        marker2=get_dis(new_photo)

        center_X1=marker1[0][0]
        center_Y1=marker1[0][1]

        center_X2=marker2[0][0]
        center_Y2=marker2[0][1]

        print(center_X1,center_Y1)
        print(center_X2,center_Y2)
        perWidth=marker1[1][0]

        dis_x=center_X1-center_X2
        dis_y=center_Y1-center_Y2

        rdis_x=dis_x*(KNOWN_WIDTH/perWidth)*2.54
        rdis_y=dis_y*(KNOWN_WIDTH/perWidth)*2.54

        center_Z1=distance_to_camera(KNOWN_WIDTH, focalLength, marker1[1][0])
        center_Z2=distance_to_camera(KNOWN_WIDTH, focalLength, marker2[1][0])

        rdis_z=(center_Z1-center_Z2)*2.54

        print("dis_x:%2fcm"%abs(rdis_x))
        print("dis_y:%2fcm"%abs(rdis_y))
        print("dis_z:%2fcm"%abs(rdis_z))

        calculate_Distance(new_photo,focalLength,rdis_x,rdis_y,rdis_z)
#        cv2.waitKey(1000)
 
        if abs(rdis_x) <= WARNING_DISTANCE and abs(rdis_y) <= WARNING_DISTANCE and abs(rdis_z) <= WARNING_DISTANCE:
            print("System is normal")
        else: 
            if abs(rdis_x) > WARNING_DISTANCE:
                print("Warning : distance X exceeds threshold")
            else:
                if abs(rdis_y) > WARNING_DISTANCE:
                    print("Warning : distance y exceeds threshold")
                else:
                    if abs(rdis_z) > WARNING_DISTANCE:
                        print("Warning : distance z exceeds threshold")
        c=c+1
        if cv2.waitKey(1000) & 0xFF == ord('q'):
           break  
    # 获得摄像头焦距 
    # for image_path in IMAGE_PATHS: 
    #    calculate_Distance(image_path,focalLength) 
    #    cv2.waitKey(1000000)
cv2.destroyAllWindows() 

