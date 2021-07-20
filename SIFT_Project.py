from random import randrange
import matplotlib.pyplot as plt
import numpy as np
import cv2


figsize = (10, 10)
MIN_MATCH_COUNT = 10

def resize(img, width , height):
    return cv2.resize(img, (width,height), interpolation = cv2.INTER_AREA)

cap = cv2.VideoCapture('video_steve.mp4')
steve = cv2.imread("steve_jobs.png")# queryImage
mona_liza = cv2.imread("mona_liza.png")# cover mona liza

fr = int(cap.get(5))
print("frame rate of stored video:::",fr)

frame_size = (352, 640)
writer = cv2.VideoWriter("mona_liza_vid.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 60, frame_size)


sift = cv2.SIFT_create()
kp_steve, des_steve = sift.detectAndCompute(steve,None)

frameCounter = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:


        # find the keypoints and descriptors with SIFT
        kp_frame, des_frame = sift.detectAndCompute(frame,None)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des_steve,des_frame, k=2)

        # Apply ratio test
        good_match = []
        for m in matches:
            if m[0].distance/m[1].distance < 0.5:
                good_match.append(m)
        good_match_arr = np.asarray(good_match)

        # cv2.drawMatchesKnn expects list of lists as matches.
        im_matches = cv2.drawMatchesKnn(steve,kp_steve,frame,kp_frame,
                                        good_match[0:30],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        h,w = steve.shape[:2]
        mona_resize = cv2.resize(mona_liza, (w, h))

        if len(good_match)>MIN_MATCH_COUNT:
            src_pts = np.array([kp_steve[m.queryIdx].pt for m in good_match_arr[:, 0]]).reshape(-1, 1, 2)
            dst_pts = np.array([kp_frame[m.trainIdx].pt for m in good_match_arr[:, 0]]).reshape(-1, 1, 2)
            H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            #print(H)

            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,H)

            #frame = cv2.polylines(frame,[np.int32(dst)],True,255,3, cv2.LINE_AA)
            imgwarp = cv2.warpPerspective(mona_resize, H, (frame.shape[1], frame.shape[0]))
            maskNew = np.zeros((frame.shape[0], frame.shape[1]),np.uint8)
            maskNew = cv2.fillPoly(maskNew,[np.int32(dst)],(255,255,255))
            maskInv = cv2.bitwise_not(maskNew)
            imgAug = cv2.bitwise_and(frame, frame, mask = maskInv )
            imgAug = cv2.bitwise_or(imgwarp, imgAug)

            print("before, ", frame.shape)
            new_imgAug = resize(imgAug, frame_size[1],frame_size[0])
            print("after, ", new_imgAug.shape)
            new_imgAug = np.rot90(new_imgAug, k=3)

            # write the flipped frame
            writer.write(new_imgAug.astype('uint8'))
            frameCounter += 1

            if frameCounter > 1500:
                break

            print("wait...")
            cv2.imshow('naive warping',new_imgAug)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        else:
            break


writer.release()
cap.release()
cv2.destroyAllWindows()

