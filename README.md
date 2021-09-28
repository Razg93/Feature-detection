# Feature detection

[![Feature detection](https://user-images.githubusercontent.com/50642442/134975500-c4aec6d5-d16c-4467-ab0c-e877c0f25f1d.png)](https://www.youtube.com/watch?v=2Z2LyaOJzBc "Feature detection")

In this project I used SIFT, a feature detection algorithm in computer vision to detect and describe local features in images, and camera calibration to determine the location of the camera in the scene.
Using these techniques I was able to replace the Steve Jobs book with Mona Liza image.
After finding the camera parameters with chessboard images processing I implemented the following steps:

1.Dividing the image to frames and finding the same tamplate as the replacement object in the frame.

![image](https://user-images.githubusercontent.com/50642442/126384387-80805c42-43e2-4541-a94e-88cb38f8ee8e.png)   ![image](https://user-images.githubusercontent.com/50642442/126384719-74526a52-7671-4196-9a02-1ad0abb820e9.png)

2.Finding the similar features in the template image and original image using SIFT function and draw the matches.

![image](https://user-images.githubusercontent.com/50642442/126383165-42f9b902-721b-4001-a4fc-b53c2edb264f.png)

3.Using perspective projection matrix to transforms from the camera coordinate
system to the normalized image coordinate system and warping the replacement image so that the features in the two images line up perfectly.

![image](https://user-images.githubusercontent.com/50642442/126386437-24a09900-414b-44d1-a8f0-75f5d3f13ffa.png)

4.Build binary inverted mask from the original image.

![image](https://user-images.githubusercontent.com/50642442/126389210-06237775-e813-4c60-901b-afac3c0da2c4.png) ![image](https://user-images.githubusercontent.com/50642442/126389244-ca7880a0-9fbf-4c8e-925d-64d3b076835c.png)

5.Finally merge the two images.

![image](https://user-images.githubusercontent.com/50642442/126389379-9f107c49-802f-4611-acfb-122304528bbb.png)






