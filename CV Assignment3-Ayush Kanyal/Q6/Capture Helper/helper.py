import cv2
import depthai as dai


def getMonoCamera(pipeline, isLeft):
    mono = pipeline.createMonoCamera()

 #configure camera resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono

def getFrame(queue):
    frame = queue.get()
    return frame.getCvFrame()


#create a pipeline
pipeline = dai.Pipeline()

monoLeft = getMonoCamera(pipeline, isLeft = True)
monoRight = getMonoCamera(pipeline, isLeft = False)

xoutLeft = pipeline.createXLinkOut()
xoutLeft.setStreamName("left")
xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName("right")

#Attach cameras to output XLink 
monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)
count = 0
#pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:

    #get the output queues.
    leftQueue = device.getOutputQueue(name = 'left', maxSize=1)
    rightQueue = device.getOutputQueue(name = 'right', maxSize = 1)
    while True:
        leftFrame = getFrame(leftQueue)
        rightFrame = getFrame(rightQueue)

        cv2.imshow('left', leftFrame)
        cv2.imshow('right', rightFrame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break 
        elif key == ord('p'):
            cv2.imwrite("picture_left"+str(count)+".png", leftFrame)
            cv2.imwrite("picture_right"+str(count)+".png", rightFrame)
            print("saved")
            count+=1