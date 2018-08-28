import numpy as np
import pandas as pd

import sys
sys.path.append("/curc/tools/x86_64/rh6/software/visit/2.10.0/2.10.0/linux-x86_64/lib/site-packages")

from visit import *
Launch() 

cwDir  = "/projects/brkr5980/anom/"
imgDir = "/projects/brkr5980/anom/imgs/"

fANM   = "anomalies_4-14.nc"
fRAW   = "CERES_SYN1.nc"
fPNG   = "land_shallow_topo_2048.tif"
fTime  = "Times.csv"

####################################################
# openDatafile()
# fName = name of dataset files
# plugin = name of plugin for the desired Reader
# Opens the dataset files
####################################################
def openDatafile(fName,plugin):
  OpenDatabase(cwDir+fName,0,plugin)

####################################################
# actvateDB()
# db = database file (fWRF or fPng)
# Activates the source
####################################################
def actvateDB(db):
  ActivateDatabase(cwDir+db)
   
####################################################
# getTimes()
# Reads the Times.csv file and returns Times var
####################################################   
def getTimes():
   time_df = pd.read_csv(cwDir+fTime, sep=",")
   tStamp = time_df["Times"]
   return tStamp

####################################################
# setViewPos()
# vNorm = Normal vector
# cUp = Camera up vector
# iPan = Pan position
# iZoom = Zoom factor
# Create the current view position
####################################################
def setViewPos(vNorm, cUp, iPan, iZoom):
  cPlane = 403.331
  pScale = 201.665
  fPt = (-0.1423, 0.017, -4.28436)
  
  vPos = View3DAttributes()
  vPos.viewNormal = vNorm
  vPos.focus = fPt
  vPos.viewUp = cUp  
  vPos.parallelScale = pScale
  vPos.nearPlane = -cPlane
  vPos.farPlane = cPlane
  vPos.imagePan = iPan 
  vPos.imageZoom = iZoom
  return vPos
  
####################################################
# createIsovolume()
# lbnd = lower bound
# ubnd = upper bound
# Creates an Isovolume plot
####################################################
def createIsovolume(lbnd=0, ubnd=1e+37, var="default"):
  AddOperator("Isovolume")
  ivAtts = IsovolumeAttributes()
  ivAtts.lbound = lbnd
  ivAtts.ubound = ubnd
  ivAtts.variable = var
  SetOperatorOptions(ivAtts)
  
####################################################
# setLights()
# Creates a 2 light, light rig env
####################################################  
def setLights():
  vDir = (0, 0, -1)
  cWhite=(255, 255, 255, 255)
  lt0 = LightAttributes()
  lt0.enabledFlag = 1
  lt0.type = lt0.Camera
  lt0.direction = vDir
  lt0.color = cWhite
  lt0.brightness = 0.2
  SetLight(0, lt0)
  
  lt1 = LightAttributes()
  lt1.enabledFlag = 1
  lt1.type = lt1.Camera
  lt1.direction = vDir
  lt1.color = cWhite
  lt1.brightness = 1
  SetLight(1, lt1)
  
  lt2 = LightAttributes()
  lt2.enabledFlag = 1
  lt2.type = lt2.Object
  lt2.direction = (0, -0.8, -0.6)
  lt2.color = cWhite
  lt2.brightness = 0.5
  SetLight(2, lt2)

####################################################
# setAnnotations()
# bkgrndClr = background color
# otitle (current time step title)
# tStamp = Current anim timestep text
# Sets the desried annotation set up including the 
#    timestep title.
####################################################
def setAnnotations(bkgrndClr):
  aAtt = AnnotationAttributes()
  aAtt.axes3D.visible = 0
  aAtt.axes3D.triadFlag = 0
  aAtt.axes3D.bboxFlag = 0
  aAtt.userInfoFlag = 0
  aAtt.databaseInfoFlag = 0
  aAtt.legendInfoFlag = 0
  aAtt.backgroundColor = bkgrndClr
  SetAnnotationAttributes(aAtt)
  
####################################################
# createTitle()
# tStamp = Current anim timestep text
# Creates the title Texy2D obj and returns the obj
####################################################  
def addTitle(tStamp):
  oTitle = CreateAnnotationObject("Text2D")
  oTitle.text = tStamp
  oTitle.position = (0.47, 0.85)
  oTitle.fontBold = 1
  oTitle.useForegroundForTextColor = 0
  oTitle.textColor = (255,255,255,255)  
  return oTitle

####################################################
# setEnv1()
# bkgrndClr = background color
# otitle (current time step title)
# tStamp = Current anim timestep
# Sets up the overall env for the scene
####################################################
def setEnv1(bkgrndClr):
  setLights()
  setAnnotations(bkgrndClr)

####################################################
# setSaveImage()
# Sets up the config for saving images
####################################################
def setSaveImage():
  attSave = SaveWindowAttributes()
  attSave.outputDirectory = imgDir
  attSave.family = 0
  attSave.format = attSave.PNG
  attSave.resConstraint = attSave.NoConstraint
  attSave.width = 1200
  attSave.height = 800
  return attSave
  
####################################################
# createTruecolor()
# Creates a Truecolor plot
####################################################   
def createTruecolor():
  AddPlot("Truecolor", "color")
  
####################################################
# createPseudocolor()
# var = variable to create plot with
# cmap = color map
# opType = method to apply to opacity mapping
# opacity = opacity value
# Creates a pseudocolor  plot
####################################################     
def createPseudocolor(var,max=0,min=0,cmap="hot",opType="FullyOpaque", opacity=1.0):
  AddPlot("Pseudocolor", var)
  pcAtts = PseudocolorAttributes()
  if max > 0:
    pcAtts.maxFlag = 1
    pcAtts.max = max
    pcAtts.minFlag = 1
    pcAtts.min = min
  if opType is "Constant":
    pcAtts.opacity = opacity
    pcAtts.opacityType = pcAtts.Constant
  else:
    pcAtts.opacityType = pcAtts.ColorTable 
  pcAtts.colorTableName = cmap 
  SetPlotOptions(pcAtts)

####################################################
# elevate()
# bZero = flag to set set to zero checkbox
# Add an elevate operator
####################################################
def elevate(bZero):  
  AddOperator("Elevate")
  eAtts = ElevateAttributes()
  eAtts.zeroFlag = bZero
  SetOperatorOptions(eAtts)
  
def elevateBy(bZero,var):  
  AddOperator("Elevate")
  eAtts = ElevateAttributes()
  eAtts.zeroFlag = bZero
  eAtts.variable = var
  SetOperatorOptions(eAtts)
    
####################################################
# transform()
# bScale = flag to set Scale params
# scale = scale params
# bTrans = flag to set Translation params
# trans = translation params 
####################################################
def transform(bScale=0, scale=[0,0,0], scOr=(0,0,0), bTrans=0, trans=[0,0,0]):
  cX=0
  cY=1
  cZ=2
  AddOperator("Transform")
  tAtts = TransformAttributes()
  tAtts.doScale = bScale
  tAtts.scaleOrigin = scOr
  tAtts.scaleX = scale[cX] 
  tAtts.scaleY = scale[cY] 
  tAtts.scaleZ = scale[cZ]
  tAtts.doTranslate = bTrans
  tAtts.translateX = trans[cX]
  tAtts.translateY = trans[cY]
  tAtts.translateZ = trans[cZ]
  SetOperatorOptions(tAtts)

####################################################
# plotBkgrnd()
# Creates the background image setup
####################################################  
def plotBkgrnd():
  actvateDB(fPNG)
  createTruecolor()
  elevate(1)
  transform(bScale=1, scale=[0.1753,0.1745,1], scOr=(-218, -108, 0))
    
####################################################  
# MAIN
####################################################  

#Open the data files
openDatafile(fPNG,"Image_1.0")
openDatafile(fRAW, "NETCDF_1.0")
createPseudocolor("toa_net_all_mon",cmap="YlOrRd2",opType="Constant", opacity=0)
elevate(0)
transform(bScale=1, scale=[1,1,0.35])

openDatafile(fANM,"NETCDF_1.0")

tStamp = getTimes()                   #Get the Times.csv file
attSave = setSaveImage()                                #Setup image save options

#Create each camera view info
v1=setViewPos(vNorm=(0, 0, 1),  cUp=(0, 1, 0),  iPan=(0, 0),    iZoom=1)
v2=setViewPos(vNorm=(0, -0.8, 0.6),  cUp=(0, 0.6, 0.8),  iPan=(0, 0),  iZoom=1.5)
v3=setViewPos(vNorm=(-0.8, -0.4, 0.4),  cUp=(0, 0, 1.5),  iPan=(0, 0),  iZoom=1.5)

#Set the views for interp to work
SetView3D(v1)
SetView3D(v2)
SetView3D(v3)

#Create a tuple of all the camera views
vpts = (v1, v2)

wghts=[]
l_vpts = len(vpts)                                      #Get the number of camera view positions
nFrames = l_vpts*30                                     #Set total number of frames - 455 frames = 15.2 seconds at 30 fps

#Create normalized weights for each camera position 
for i in range(nFrames): 
  wghts = wghts + [float(i) / float(l_vpts-1)]  


createPseudocolor("skin_m_loc",max=16, min=-16,cmap="YlOrRd3",opType="ColorTable", opacity=1.0)
elevateBy(0,"toa_m_loc")
createIsovolume(lbnd=0, ubnd=125, var="toa_m_loc")
transform(bScale=1, scale=[1,1,0.25])


setEnv1(bkgrndClr=(0, 0, 0, 255))
plotBkgrnd()
title = addTitle(tStamp[0])
DrawPlots()
SetActiveTimeSlider(cwDir+fANM)

for i in range(nFrames):                                #Loop through each frame
  t = float(i)/float(nFrames - 1)                       #Create normalized temporal weights
  p = EvalCubicSpline(t, wghts, vpts)                   #Create cubic spline for camera path for current position 
  SetView3D(p)                                          #Set the view 
  fImagename = imgDir+"increase_bothM_view_%04d.png" % i #Set the image name
  attSave.fileName = fImagename                         #Save the image name
  SetSaveWindowAttributes(attSave)                      #Set the save attributes  
  SaveWindow()                                          #Save the image


for ts in range(1, 84):              #Loop thru each timestep starting at step 1 NOT 0!
  title.Delete()
  TimeSliderSetState(ts-1)              #Set the current timestep  
  title = addTitle(tStamp[ts-1])
  
  attSave.fileName = imgDir+"increase_bothM_anim_%04d.png" % ts #Set image file name
  SetSaveWindowAttributes(attSave)    #Save image file name
  SaveWindow()                        #Save the current image

#Create a tuple of all the camera views
vpts = (v2, v3)

wghts=[]
l_vpts = len(vpts)                                      #Get the number of camera view positions
nFrames = l_vpts*30                                     #Set total number of frames - 455 frames = 15.2 seconds at 30 fps

#Create normalized weights for each camera position 
for i in range(nFrames): 
  wghts = wghts + [float(i) / float(l_vpts-1)]  
SetActiveTimeSlider(cwDir+fANM)

for i in range(nFrames):                                #Loop through each frame
  t = float(i)/float(nFrames - 1)                       #Create normalized temporal weights
  p = EvalCubicSpline(t, wghts, vpts)                   #Create cubic spline for camera path for current position 
  SetView3D(p)                                          #Set the view 
  fImagename = imgDir+"increase_bothM_view_mid_%04d.png" % i #Set the image name
  title.Delete()
  TimeSliderSetState(i+84)             #Set the current timestep  
  title = addTitle(tStamp[i+84])
  attSave.fileName = fImagename                         #Save the image name
  SetSaveWindowAttributes(attSave)                      #Set the save attributes  
  SaveWindow()                                          #Save the image


SetActiveTimeSlider(cwDir+fANM)
for ts in range(nFrames, 180):              #Loop thru each timestep starting at step 1 NOT 0!
  title.Delete()
  TimeSliderSetState(ts-1)              #Set the current timestep  
  title = addTitle(tStamp[ts-1])  
  attSave.fileName = imgDir+"increase_bothM_anim_mid_%04d.png" % ts #Set image file name
  SetSaveWindowAttributes(attSave)    #Save image file name
  SaveWindow()                        #Save the current image
