import os.path
from CameraManager.TPUCameraManager import CameraManager, GStreamerPipelines
camMan = CameraManager() #Creates new camera manager object
streamStarted = False
cameras = {"USB":1,"CSI":0}

streamingCamera = "USB" #Change this for a differnt camera

while True:
    try:
        if os.path.exists('/dev/video{0}'.format(cameras[streamingCamera])):
            if(streamStarted == False):
                USBCam = camMan.newCam(cameras[streamingCamera]) #Creates new USB-camera
                CV = USBCam.addPipeline(GStreamerPipelines.RGB,(640,480),30,"CV") #Creates an RGB stream at 30 fps and 640x480 for openCV Change RGB for H264 or MJPEG
                USBCam.startPipeline()
                streamStarted = True
            else:
                pass
            if(CV):
                print("Camera Streaming")
                print(bytes(CV)) #RGB Byte Stream that can be converted to a numpy array
        else:
            print("Camera Disconnected")
            if(streamStarted == True):
                try:
                    print("Closing Camera")
                    camMan.close(USBCam)
                    streamStarted = False
                except:
                    pass
            else:
                pass
    except:
        pass