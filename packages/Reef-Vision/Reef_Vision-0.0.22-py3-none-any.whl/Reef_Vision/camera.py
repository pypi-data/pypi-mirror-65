# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import threading
from time import sleep
from .CameraManager.TPUCameraManager import CameraManager, GStreamerPipelines
import numpy as np

class Camera:
    def __init__(self, model_res, set_ai):
        #def __init__(self, render_size, inference_size, loop):
        # self._layout = gstreamer.make_layout(inference_size, render_size)
        # self._loop = loop
        self.model_res = model_res
        self._thread = None
        self.render_overlay = None
        self.set_ai = set_ai

        self.camMan = CameraManager() #Creates new camera manager object
        self.CSICam = self.camMan.newCam(0)
        
        self.H264 = self.CSICam.addPipeline(GStreamerPipelines.H264,(640,480),30,"h264sink")
        #  re-enable later
        if self.set_ai:
            
            self.AI = self.CSICam.addPipeline(GStreamerPipelines.RGB, self.model_res,30,"AI")

        self.CSICam.startPipeline() 

        if os.path.exists('/dev/video1'):
            self.USBCam = self.camMan.newCam(1) #Creates new RGB CSI-camera
            self.SB = self.USBCam.addPipeline(GStreamerPipelines.H264,(640,480),30,"usb_cam") #Creates an RGB stream at 30 fps and 640x480 for openCV
            self.USBCam.startPipeline()
        else:
            self.USBCam = None


       
            

    @property
    def resolution(self):
        return [640, 480]

    def request_key_frame(self):
        pass

    def start_recording(self, obj, format, profile, inline_headers, bitrate, intra_period):


        
        #Start gstreamer Streams
        
        objFunc = obj.write
        self.H264.addListener(objFunc)

        if self.USBCam is not None:

            objFunc = obj.write_usb
            self.SB.addListener(objFunc)


        ## re-enable later
        if self.set_ai:

            self._thread = threading.Thread(target=self.ai_stream)
            self._thread.start()


        
        
    def ai_stream(self):
            while True:
                if self.render_overlay:
                    tensor = np.frombuffer(bytes(self.AI),dtype=np.uint8)
                    layout = None
                    command = None
                    self.render_overlay(tensor, layout, command)
                sleep(.03)
    def stop_recording(self):
        print("called close")
        # self.camMan.closeAll()
        # self._thread.join()

    def make_pipeline(self, fmt, profile, inline_headers, bitrate, intra_period):
        raise NotImplemented

