cwDir  = "/Users/kristenbrown/Desktop/SciViz/project/"
imgDir = "/Users/kristenbrown/Desktop/SciViz/project/monthly_imgs/"

fANM   = "anomalies_4-14.nc"
fPNG   = "land_shallow_topo_2048.tif"

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
   
###################################################
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
def createTitle(tStamp):
  oTitle = CreateAnnotationObject("Text2D")
  oTitle.text = tStamp
  oTitle.position = (0.35, 0.95)
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
  attSave.width = 800
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
def createPseudocolor(var,max=0,min=0,cmap="hot",opType="ColorTable", opacity=1.0):
  AddPlot("Pseudocolor", var)
  pcAtts = PseudocolorAttributes()
  pcAtts.maxFlag = 1
  pcAtts.max = max
  pcAtts.minFlag = 1
  pcAtts.min = min
  pcAtts.colorTableName = cmap
  pcAtts.opacityType = pcAtts.ColorTable
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
plotBkgrnd()
openDatafile(fANM,"NETCDF_1.0")

attSave = setSaveImage()              #Setup the save image file options

#Create each camera view info
v1=setViewPos(vNorm=(0, 0, 1),  cUp=(0, 1, 0),  iPan=(0, 0),    iZoom=1)
v2=setViewPos(vNorm=(0, -0.8, 0.6),  cUp=(0, 0.6, 0.8),  iPan=(0, 0),  iZoom=1.2)

#Set the views for interp to work
SetView3D(v1)
SetView3D(v2)

#Create a tuple of all the camera views
vpts = (v1, v2)

wghts=[]
l_vpts = len(vpts)                                      #Get the number of camera view positions
nFrames = l_vpts*30                                     #Set total number of frames - 455 frames = 15.2 seconds at 30 fps

#Create normalized weights for each camera position 
for i in range(nFrames): 
  wghts = wghts + [float(i) / float(l_vpts-1)]  

attSave = setSaveImage()                                #Setup image save options

createPseudocolor("skin_m_loc",max=16, min=-16,cmap="YlOrRd2",opType="ColorTable", opacity=1.0)
elevate(0)
setEnv1(bkgrndClr=(0, 0, 0, 255))
DrawPlots()
  
for i in range(nFrames):                                #Loop through each frame
  t = float(i)/float(nFrames - 1)                       #Create normalized temporal weights
  p = EvalCubicSpline(t, wghts, vpts)                   #Create cubic spline for camera path for current position 
  SetView3D(p)                                          #Set the view 
  fImagename = imgDir+"increase_temp_view_%04d.png" % i #Set the image name
  attSave.fileName = fImagename                         #Save the image name
  SetSaveWindowAttributes(attSave)                      #Set the save attributes  
  SaveWindow()                                          #Save the image


nts = TimeSliderGetNStates()          #Get the total number of timesteps
for ts in range(1, nts):              #Loop thru each timestep starting at step 1 NOT 0!
  DeleteAllPlots()                    #Clear the scene to replot everything
  TimeSliderSetState(ts)              #Set the current timestep  
  plotBkgrnd()                        #Create background image plot
  actvateDB(fANM)
  createPseudocolor("skin_m_loc",max=16, min=-16,cmap="YlOrRd2",opType="ColorTable", opacity=1.0)
  elevate(0)
  setEnv1(bkgrndClr=(0, 0, 0, 255)) #Set the scene env
  DrawPlots()                         #Draw all plots
  
  attSave.fileName = imgDir+"increase_temp_anim_%04d.png" % ts #Set image file name
  SetSaveWindowAttributes(attSave)    #Save image file name
  SaveWindow()                        #Save the current image

DeleteAllPlots()


createPseudocolor("toa_m_loc",max=124, min=-124,cmap="BuPu2",opType="ColorTable", opacity=1.0)
elevate(0)
setEnv1(bkgrndClr=(0, 0, 0, 255))
DrawPlots()
for i in range(nFrames):                                #Loop through each frame
  t = float(i)/float(nFrames - 1)                       #Create normalized temporal weights
  p = EvalCubicSpline(t, wghts, vpts)                   #Create cubic spline for camera path for current position 
  SetView3D(p)                                          #Set the view 
  fImagename = imgDir+"increase_toa_view_%04d.png" % i #Set the image name
  attSave.fileName = fImagename                         #Save the image name
  SetSaveWindowAttributes(attSave)                      #Set the save attributes  
  SaveWindow()                                          #Save the image


nts = TimeSliderGetNStates()          #Get the total number of timesteps
for ts in range(1, nts):              #Loop thru each timestep starting at step 1 NOT 0!
  DeleteAllPlots()                    #Clear the scene to replot everything
  TimeSliderSetState(ts)              #Set the current timestep  
  plotBkgrnd()                        #Create background image plot
  actvateDB(fANM)
  createPseudocolor("toa_m_loc",max=124, min=-124,cmap="BuPu2",opType="ColorTable", opacity=1.0)
  elevate(0)
  setEnv1(bkgrndClr=(0, 0, 0, 255)) #Set the scene env
  DrawPlots()                         #Draw all plots
  
  attSave.fileName = imgDir+"increase_toa_anim_%04d.png" % ts #Set image file name
  SetSaveWindowAttributes(attSave)    #Save image file name
  SaveWindow()                        #Save the current image

