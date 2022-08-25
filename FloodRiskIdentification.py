#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      joyce
#
# Created:     29/04/2017
# Copyright:   (c) joyce 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Setting the environment of the script

import os
import arcpy
from arcpy.sa import *
from arcpy import da
path = r"C:\Users\joyce\Desktop\Finalproject"
arcpy.env.workspace = path
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# User Input shapefile which contains .dbf
dbf = arcpy.GetParameterAsText(0)

# Automatically generate field "Risk1"
FieldName = "Risk1"
# User Input: dem value field, threshold1, threshold2
FN = arcpy.GetParameterAsText(1)
FNthr1 = arcpy.GetParameterAsText(2)
FNthr2 = arcpy.GetParameterAsText(3)
FN_new = '!'+FN+'!'

expression = """Reclassdem({}, {}, {}, 3, 2, 1)""".format(FN_new,FNthr1,FNthr2)
codeblock = """def Reclassdem(inField, threshold1, threshold2, x, y, z):
    expression1 = inField < threshold1
    expression2 = threshold1 < inField < threshold2
    expression3 = inField > threshold2
    if  expression1:
        return x
    elif  expression2:
        return y
    else:
        return z
"""
arcpy.AddField_management(dbf, FieldName, "Float")
arcpy.CalculateField_management(dbf, FieldName, expression, "PYTHON", codeblock)
arcpy.AddMessage("Risk Field calculating...")

# Automatically generate field "Risk2"
FieldName2 = "Risk2"
# User Input: river buffer value field, threshold1
FN2 = arcpy.GetParameterAsText(4)
FN2thr1 = arcpy.GetParameterAsText(5)
FN2_new = '!'+FN2+'!'
expression = """Reclassbuffer({}, {}, 1, 5)""".format(FN2_new,FN2thr1)
codeblock = """def Reclassbuffer(inField, threshold1, x, y):
    expression1 = inField < threshold1
    expression2 = inField >= threshold1
    if  expression1:
        return x
    elif  expression2:
        return y
"""
arcpy.AddField_management(dbf, FieldName2, "Float")
arcpy.CalculateField_management(dbf, FieldName2, expression, "PYTHON", codeblock)
arcpy.AddMessage("Almost done...")

# Automatically generate field "Risk3"
FieldName3 = "Risk3"
# User Input: rainfall value field, threshold1, threshold2
FN3 = arcpy.GetParameterAsText(6)
FN3thr1 = arcpy.GetParameterAsText(7)
FN3thr2 = arcpy.GetParameterAsText(8)
FN3_new = '!'+FN3+'!'
expression = """Reclassrain({}, {}, {}, 3, 2, 1)""".format(FN3_new,FN3thr1,FN3thr2)
codeblock = """def Reclassrain(inField, threshold1, threshold2, x, y, z):
    expression1 = inField < threshold1
    expression2 = threshold1 < inField < threshold2
    expression3 = inField > threshold2
    if  expression1:
        return x
    elif  expression2:
        return y
    else:
        return z
"""
arcpy.AddField_management(dbf, FieldName3, "Float")
arcpy.CalculateField_management(dbf, FieldName3, expression, "PYTHON", codeblock)
arcpy.AddMessage("Please be patient...")

# Automatically generate field "RiskSUM" based on Risk1+Risk2+Risk3
FieldName4 = "RiskSUM"
expression = """SUM(!Risk1!, !Risk2!, !Risk3!)"""
codeblock = """def SUM(inField, inField2, inField3):
    return inField+inField2+inField3
"""
arcpy.AddField_management(dbf, FieldName4, "Float")
arcpy.CalculateField_management(dbf, FieldName4, expression, "PYTHON", codeblock)
arcpy.AddMessage("Risk sum calculating...")

# Automatically generate field "RiskLevel" based on "RiskSUM"
FieldName5 = "RiskLevel"
expression = """risklevel(!RiskSUM!, 4, 6, 8, "0_LOW", "1_MediumLow", "2_MediumHigh", "3_High")"""
codeblock = """def risklevel(inField, threshold1, threshold2, threshold3, a, b, c, d):
      if inField < threshold1:
        return a
      elif inField < threshold2:
        return b
      elif inField < threshold3:
        return c
      else:
        return d
"""
arcpy.AddField_management(dbf, FieldName5, "Text")
arcpy.CalculateField_management(dbf, FieldName5, expression, "PYTHON", codeblock)
arcpy.AddMessage("Risk level calculating...")
arcpy.AddMessage("Please be patient...It may take 30 seconds...")

# Symbology section

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(dbf,"Riskmap_lyr")

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management("Riskmap_lyr", "Riskmap.shp")


# Reference layer in map document
InputMapName = arcpy.GetParameterAsText(9)
MXD = arcpy.mapping.MapDocument(InputMapName)
DF = arcpy.mapping.ListDataFrames(MXD)[0]
arcpy.AddMessage("Saving .mxd...")

# Add layer into primary map document
layer = arcpy.mapping.Layer("Riskmap.shp")
arcpy.mapping.AddLayer(DF, layer, "TOP")

# Save to a new map document and clear variable references
MXD.save()
del MXD
arcpy.AddMessage("Add layer to mxd...")
mxd = arcpy.mapping.MapDocument(InputMapName)

symbology = arcpy.GetParameterAsText(10)

if symbology == "":
    pass
else:
    # Set layer that output symbology will be based on
    symbologyLayer = "RisklevelSymbology.lyr"

    # Apply the symbology from the sourcelayer to the updatelayer


    df = arcpy.mapping.ListDataFrames(mxd)[0]

    updateLayer = arcpy.mapping.ListLayers(mxd, "Riskmap", df)[0]
    sourceLayer = arcpy.mapping.Layer(symbologyLayer)
    arcpy.mapping.UpdateLayer(df,updateLayer,sourceLayer)

mxd.saveACopy("FloodMap.mxd")
arcpy.AddMessage("Map saved, Exporting to PNG...")

# Enter name for PNG, Output, String Datatype
PNGpath = arcpy.GetParameterAsText(12) + "\\" + arcpy.GetParameterAsText(11) +'.png'
arcpy.mapping.ExportToPNG (mxd, PNGpath)
del mxd
arcpy.AddMessage("Exported to PNG...")




