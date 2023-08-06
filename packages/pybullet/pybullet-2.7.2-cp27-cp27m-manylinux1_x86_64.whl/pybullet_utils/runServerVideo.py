#add parent dir to find package. Only needed for source code build, pip install doesn't need it.
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)

import pybullet_data
import pybullet as p
import time

p.connect(p.GUI_SERVER, options="--mp4=\"test.mp4\" --mp4fps=30")
p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING,1)


p.setAdditionalSearchPath(pybullet_data.getDataPath())
while (1):
  #this is a no-op command, to allow GUI updates on Mac OSX (main thread)
  p.setPhysicsEngineParameter()
  time.sleep(0.01)
