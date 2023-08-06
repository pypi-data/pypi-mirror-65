import cv2
import  numpy
import  sys



#读取一张图片
class READ_ONE_IMAGE:
    def __init__(self,filename):
        self.filename = filename
        self.read_image()
    def read_image(self):
        image = cv2.imread(self.filename)
        cv2.imshow("image",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#滤波器
class PF:
    def __init__(self,filename,ksize):#ksize it's a tuple and %2 ==1
        self.filename = filename
        self.ksize = ksize
        self.pf()
    def pf(self):
        image = cv2.imread(self.filename)
        blurred = cv2.GaussianBlur(image,ksize=self.ksize,sigmaX=0)
        g_hpf   = image - blurred
        cv2.imshow("g_hpf",g_hpf)
        cv2.waitKey()
        cv2.destroyAllWindows()


#静态人脸检测
class DETECT_IMAGE:
    def __init__(self,filename):
        self.filename =filename
        self.detect()
    def detect(self):
        face_cascade = cv2.CascadeClassifier(
            r"C:\Users\meng\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")
        image = cv2.imread(self.filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.namedWindow("deteced")
        cv2.imshow("deteced", image)
        cv2.imwrite("../../西瓜书机器学习/人脸检测/deteded.jpeg", image)
        cv2.waitKey(0)


#角点监测
class DETECT_CAMERA:
    def __init__(self):
        self.camera()
    def camera(self):
        camera = cv2.VideoCapture(0)
        face = cv2.CascadeClassifier(
            ".//haarcascades//haarcascade_frontalface_default.xml"
        )
        cv2.namedWindow('camera')
        while True:
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face.detectMultiScale(gray, 1.1, 3, 0, (100, 100))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('camera', frame)
            if cv2.waitKey(1000 // 12) & 0xFF == ord('q'):
                break
        camera.release()
        cv2.destroyAllWindows()


class DETECT_VIDEO:
    def __init__(self):
        self.video()
    def video(self):
        video = cv2.VideoCapture("c://data//meinv.mp4")
        face = cv2.CascadeClassifier(r"C:\Users\meng\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")
        cv2.namedWindow('video')
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face.detectMultiScale(gray, 1.1, 3, 0, (100, 100))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("video", frame)
            if cv2.waitKey(1000//10) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()


class DETECT_CORNER:
    def __init__(self,filename):
        self.filename = filename
        self.corner()
    def corner(self):
        image = cv2.imread(self.filename)
        gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray  = numpy.float32(gray)
        dst   = cv2.cornerHarris(gray,2,23,0.04)
        image[dst>0.01 * dst.max()] = [0,0,255]
        while True:
            cv2.imshow("corners",image)
            if cv2.waitKey(1000//12) & 0xff == ord("q"):
                break
        cv2.destroyAllWindows()

#特征提取
class NEW_SIFT:
    def __init__(self,filname):
        self.filename = filename
        self.sift()
    def sift(self):
        image  = cv2.imread(self.filename)
        gray   = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        keypoints,descriptor = sift.detectAndCompute(gray,None)
        image =cv2.drawKeypoints(image = image,outImage=image,keypoints=keypoints,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                 color=(51,163,236))
        cv2.imshow("sift_points",image)
        while True:
            if cv2.waitKey(1000 // 12)  & 0xff ==ord("q"):
                break
        cv2.destroyAllWindows()

#边缘检测
class DETECT_EDGES:
    def __init__(self,filename):
        self.filename = filename
        self.canny()
    def canny(self):
        image = cv2.imread(self.filename)
        cv2.imshow("canny.jpg",cv2.Canny(image,200,200))
        cv2.waitKey()
        cv2.destroyAllWindows()

#圆检测
class DETECT_LINE:
    def __init__(self,filename):
        self.filename = filename
        self.line()
    def line(self):
        image = cv2.imread(self.filename)
        gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,80)
        minlength = 20
        maxlinegap = 5
        lines = cv2.HoughLinesP(edges,1,numpy.pi/180,100,minlength,maxlinegap)
        for var1,var2,var3,var4 in lines[0]:
            cv2.line(image,(var1,var2),(var3,var4),(0,0,255),2)
        cv2.imshow("edges",edges)
        cv2.imshow("line",image)
        cv2.waitKey()
        cv2.destroyAllWindows()
#圆检测
class DETECT_CIECLE:
    def __init__(self,filename):
        self.filename = filename
        self.circle()
    def circle(self):
        image = cv2.imread(self.filename)
        gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        new_image = cv2.medianBlur(gray,5)
        color_image = cv2.cvtColor(new_image,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(new_image,cv2.HOUGH_GRADIENT,1,120,param1=100,param2=30,minRadius=0,maxRadius=0)

        for var in circles[0,:]:
            cv2.circle(image,(var[0],var[1]),var[2],(0,255,0),2)
            cv2.circle(image,(var[0],var[1]),2,(0,0,255),3)
        cv2.imwrite("../../西瓜书机器学习/人脸检测/planets_circle.jpeg", image)
        cv2.imshow("houghcircle",image)
        cv2.waitKey()

#轮廓检测
class EDGES_AND_MINRECTANGULAR_AND_MINCIRCLE:
    def __init__(self,filename):
        self.filename = filename
        self.func()
    def func(self):
        img = cv2.imread(self.filename, cv2.IMREAD_UNCHANGED)
        grayImage = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
        ret, thread = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        image, contours, hier = cv2.findContours(thread, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return  img,grayImage,ret,thread,image,contours,hier
    def minretangle(self):#矩形检测
        img,grayImage,ret,thread,image,contours,hier=self.func()
        for var in contours:
            x,y,w,h = cv2.boundingRect(var)
            cv2.rectangle(img,(x, y), (x + w, y + h), (0, 255, 0))
            rect = cv2.minAreaRect(var)
            box = cv2.boxPoints(rect)
            box = numpy.int0(box)
            cv2.drawContours(img, [box], 0, (0, 0, 255), 1)
        cv2.drawContours(img, contours, -1, (255, 255, 0))
        cv2.imshow('retangle_find_edges', img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    def mincircle(self):#圆检测
        img, grayImage, ret, thread, image, contours, hier = self.func()
        for var in contours:
            x, y, w, h = cv2.boundingRect(var)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255))
            (x, y), radius = cv2.minEnclosingCircle(var)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(img, center, radius, (255, 0, 0), 1)
        cv2.drawContours(img, contours, -1, (255, 255, 0))
        cv2.imshow('circle_find_edges', img)
        cv2.waitKey()
        cv2.destroyAllWindows()



#凸轮廓检测
class DP:
    def __init__(self,filename):
        self.filename = filename
        self.dp()
    def dp(self):
        img = cv2.pyrDown(cv2.imread(filename, cv2.IMREAD_UNCHANGED))
        ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
        black = cv2.cvtColor(numpy.zeros((img.shape[1], img.shape[0]), dtype=numpy.uint8), cv2.COLOR_GRAY2BGR)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            hull = cv2.convexHull(cnt)
            cv2.drawContours(black, [cnt], -1, (0, 255, 0), 2)
            cv2.drawContours(black, [approx], -1, (255, 255, 0), 2)
            cv2.drawContours(black, [hull], -1, (0, 0, 255), 2)

        cv2.imshow("hull", black)
        cv2.waitKey()
        cv2.destroyAllWindows()


import  matplotlib.pyplot as plt
class GradCut:#图像分割
    def __init__(self,filename):
        self.filename = filename
        self.gradcut()
    def gradcut(self):
        image = cv2.imread(self.filename)
        mask  = numpy.zeros(image.shape[:2],numpy.uint8)
        bgdmodel = numpy.zeros((1,65),numpy.float64)
        fgdmodel = numpy.zeros((1,65),numpy.float64)
        rect = (100,50,421,378)
        cv2.grabCut(image,mask,rect,bgdmodel,fgdmodel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = numpy.where((mask==0) | (mask==2),0,1).astype("uint8")
        image = image *mask2[:,:,numpy.newaxis]
        plt.subplot(121)
        plt.imshow(image)
        plt.title("gradcut")
        plt.xticks([]),plt.yticks([])
        plt.subplot(122)
        plt.imshow(cv2.cvtColor(cv2.imread(self.filename),cv2.COLOR_BGR2RGB))
        plt.title("Original")
        plt.xticks([]),plt.yticks([])
        plt.show()


#分水岭分割
class WATERSHED:
    def __init__(self,filename):
        self.filename = filename
        self.watershed()
    def watershed(self):
        image = cv2.imread(filename)
        gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        kernel    = numpy.ones((3,3),numpy.uint8)
        opening   =cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret,sure_fg=cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_fg=numpy.uint8(sure_fg)
        unknow =cv2.subtract(sure_bg,sure_fg)
        ret,markers=cv2.connectedComponents(sure_fg)
        markers+=1
        markers[unknow==255] = 0
        markers = cv2.watershed(image,markers)
        image[markers==-1] = [255,0,0]
        plt.imshow(image)
        plt.show()

#特征提取
class Hessian_AND_SURF:
    def __init__(self,filname):
        self.filename = filename
        self.sift()
    def sift(self):
        image = cv2.imread(self.filename)
        gray   = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SURF_create()
        keypoints,descriptor = sift.detectAndCompute(gray,None)
        image =cv2.drawKeypoints(image = image,outImage=image,keypoints=keypoints,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                 color=(51,163,236))
        cv2.imshow("surf_points",image)
        while True:
            if cv2.waitKey(1000 // 12)  & 0xff ==ord("q"):
                break
        cv2.destroyAllWindows()

#特征匹配
# #input feature Image and train image
class ORB:
    def __init__(self,filename1,filename2):
        self.filename1 = filename1
        self.filename2 = filename2
        self.orb()
    def orb(self):
        image1 = cv2.imread(self.filename1,cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(self.filename2,cv2.IMREAD_GRAYSCALE)
        orb = cv2.ORB_create()
        kp1,des1=orb.detectAndCompute(image1,None)
        kp2,des2=orb.detectAndCompute(image2,None)
        bf =cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
        matches=bf.match(des1,des2)
        matches=sorted(matches,key=lambda x:x.distance)
        image3=cv2.drawMatches(image1,kp1,image2,kp2,matches[:40],image2,flags=2)
        cv2.imshow("image3",image3)
        cv2.waitKey()
        cv2.destroyAllWindows()





#特征匹配
#input feature Image and train image
class KNN:
    def __init__(self,filename1,filename2):
        self.filename1 = filename1
        self.filename2 = filename2
        self.knn()
    def knn(self):
        img1 = cv2.imread(self.filename2)
        img2 = cv2.imread(self.filename1)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.knnMatch(des1, des2, k=1)
        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, img2, flags=2)
        cv2.imshow("image3",img3)
        cv2.waitKey()
        cv2.destroyAllWindows()


class FLANN:
    def __init__(self,query_filename1,train_filename2):
        self.filename1 = query_filename1
        self.filename2 = train_filename2
        self.flann()
    def flann(self):
        queryImage = cv2.imread(self.filename1, 0)
        trainingImage = cv2.imread(self.filename2, 0)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(queryImage, None)
        kp2, des2 = sift.detectAndCompute(trainingImage, None)
        FLANN_INDEX_KDTREE = 0
        indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        searchParams = dict(checks=50)
        flann = cv2.FlannBasedMatcher(indexParams, searchParams)
        matches = flann.knnMatch(des1, des2, k=2)
        matchesMask = [[0, 0] for i in range(len(matches))]
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                matchesMask[i] = [1, 0]
        drawParams = dict(matchColor=(0, 255, 0),
                          singlePointColor=(255, 0, 0),
                          matchesMask=matchesMask,
                          flags=0
                          )
        resultImage = cv2.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams)

        cv2.imshow("result_image",resultImage)
        cv2.waitKey()
        cv2.destroyAllWindows()


class Simple_Adjustment_FNN:
    def __init__(self,min_match_count,query_filename,train_filename):
        self.filename1 = query_filename
        self.filename2 = train_filename
        self.min_match_count = min_match_count
        self.simple_adjustment_FNN()
    def simple_adjustment_FNN(self):
        img1 = cv2.imread(self.filename1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(self.filename2, cv2.IMREAD_GRAYSCALE)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # checks指定索引树要被遍历的次数
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
# 寻找距离近的放入good列表
        good = []

        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > self.min_match_count:
            src_pts = numpy.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = numpy.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h, w = img1.shape
            pts = numpy.float32([[0, 0], [0, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [numpy.int32(dst)], True, 255, 3, cv2.LINE_AA)
        else:
            matchesMask = None

        draw_params = dict(
        matchColor=(0, 255, 0),
        singlePointColor=None,
        matchesMask=matchesMask,
        flags=2)
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img3)
        plt.show()






#行人检测
class Target_Detection_And_Recognition_People:
    def __init__(self,filename):
        self.filename = filename
        self.strat()
    def svmdetectperson(self,img):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        person, w = hog.detectMultiScale(img)
        return person

    def is_inside(self,a, b):
        x1, y1, w1, h1 = a
        x2, y2, w2, h2 = b  # judge b  is not include a
        return x1 > x2 and y1 > y2 and x1 + w1 < x2 + w2 and y1 + h1 < y2 + h2

    def draw(self,img, a):
        x, y, w, h = a
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)

    def strat(self):
        img = cv2.imread(self.filename)
        person = self.svmdetectperson(img)
        filtered = []
        for i, p in enumerate(person):
            for j, p1 in enumerate(person):
                if i != j and self.is_inside(p, p1):
                    break
            filtered.append(p)
        for p in filtered:
            self.draw(img,p)
        cv2.imshow("people detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


#动作检测
class ACT_DETECT:
    def __init__(self,filename):
        self.filename=filename
        self.act_detect()
    def act_detect(self):
        bs=cv2.createBackgroundSubtractorKNN(detectShadows=True)
        video=cv2.VideoCapture(self.filename)
        while True:
            ret,frame = video.read()
            fgmask=bs.apply(frame)
            th=cv2.threshold(fgmask.copy(),244,255,cv2.THRESH_BINARY)[1]
            dilated=cv2.dilate(th,
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),
                               iterations=2)
            image, contours, hier = cv2.findContours(
            dilated,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
            for var in contours:
                if cv2.contourArea(var)>1600:
                    parm1,parm2,parm3,parm4 =cv2.boundingRect(var)
                    cv2.rectangle(frame,(parm1,parm2),(parm1+parm3,parm2+parm4),(255,255,0),2)
            cv2.imshow("mog",fgmask)
            cv2.imshow("thresh",th)
            cv2.imshow("detection",frame)
            if cv2.waitKey(1000//12) & 0xff==27:
                break
        video.release()
        cv2.destroyAllWindows()


#均值漂移
class Mean_Shift:
    def __init__(self,filename):
        self.filename = filename
        self.mean_shift()
    def mean_shift(self):
        cap = cv.VideoCapture(self.filename)
        # take first frame of the video
        ret, frame = cap.read()
        # setup initial location of window
        r, h, c, w = 250, 90, 400, 125  # simply hardcoded the values
        track_window = (c, r, w, h)
        # set up the ROI for tracking
        roi = frame[r:r + h, c:c + w]
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, numpy.array((0., 60., 32.)), numpy.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        while (1):
            ret, frame = cap.read()
            if ret == True:
                hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
                # apply meanshift to get the new location
                ret, track_window = cv.meanShift(dst, track_window, term_crit)
                # Draw it on image
                x, y, w, h = track_window
                img2 = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
                cv.imshow('img2', img2)
                k = cv.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv.imwrite(chr(k) + ".jpg", img2)
            else:
                break
        cv.destroyAllWindows()
        cap.release()

class CAM_Shift:
    def __init__(self,filename):
        self.filename =filename
        self.cam_shift()
    def cam_shift(self):
        cap = cv.VideoCapture(self.filename)
        # take first frame of the video
        ret, frame = cap.read()
        # setup initial location of window
        r, h, c, w = 250, 90, 400, 125  # simply hardcoded the values
        track_window = (c, r, w, h)
        # set up the ROI for tracking
        roi = frame[r:r + h, c:c + w]
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, numpy.array((0., 60., 32.)), numpy.array((180., 255., 255.)))
        roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        while (1):
            ret, frame = cap.read()
            if ret == True:
                hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
                # apply meanshift to get the new location
                ret, track_window = cv.CamShift(dst, track_window, term_crit)
                # Draw it on image
                pts = cv.boxPoints(ret)
                pts = numpy.int0(pts)
                img2 = cv.polylines(frame, [pts], True, 255, 2)
                cv.imshow('img2', img2)
                k=cv.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv.imwrite(chr(k) + ".jpg", img2)
            else:
                break
        cv.destroyAllWindows()
        cap.release()

if __name__ == '__main__':
    pass




















