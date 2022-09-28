from ast import arg
from pickle import TRUE
from xml.dom.minidom import TypeInfo
from depthai_sdk import Previews
from depthai_sdk.managers import PipelineManager, PreviewManager
import depthai as dai
import cv2
from depthai_sdk.fps import FPSHandler


pm = PipelineManager()
pm.createColorCam(xout=True, fps=60, res= dai.ColorCameraProperties.SensorResolution.THE_4_K)
pm.createLeftCam(xout=True, fps=120, res= dai.MonoCameraProperties.SensorResolution.THE_400_P)
pm.createRightCam(xout=True, fps=120, res= dai.MonoCameraProperties.SensorResolution.THE_400_P)
pm.createDepth(useDisparity=True)
handler = FPSHandler()


with dai.Device(pm.pipeline) as device:
    pv = PreviewManager(display=[Previews.color.name, Previews.disparityColor.name])
    pv.createQueues(device)
    
    while True:
        frame = pv.prepareFrames()
        handler.nextIter()
        fps = round(handler.fps())
        
        pv.showFrames(callback=print("FPS : "+ str(fps)))

        if cv2.waitKey(1) == ord('q'):
            break
