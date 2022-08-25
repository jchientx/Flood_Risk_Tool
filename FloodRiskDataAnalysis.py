#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tasnu
#
# Created:     01/05/2017
# Copyright:   (c) tasnu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Intersection of three variables, all required inputs for the final risk map output

import arcpy
from arcpy.da import *
from arcpy.sa import *
path = r"C:\Users\tasnu\Desktop\5419_Final\01 May 2017"
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")


IntersectInput1 = arcpy.GetParameterAsText(0)                                                            # The boundary of the study area

IntersectInput2 = arcpy.GetParameterAsText(1)                                                            # The 2nd input layer (Rivers of Texas) for 1st intersect
IntersectOutput1 = arcpy.GetParameterAsText(2)                                                           # The output of the 1st intersect

IntersectInput3 = arcpy.GetParameterAsText(3)                                                            # The 2nd input layer (Precipitation of Texas) for 2nd intersect
IntersectOutput2 = arcpy.GetParameterAsText(4)                                                           # The output of the 2nd intersect

IntersectInput4 = arcpy.GetParameterAsText(5)                                                            # The 2nd input layer (Elevation data) for 3rd intersect
IntersectOutput3 = arcpy.GetParameterAsText(6)                                                           # The output of the 3rd intersect

ValueTable1 = [IntersectInput1, IntersectInput2]                                                         # The order of the 1st interseted layers input
ValueTable2 = [IntersectInput1, IntersectInput3]                                                         # The order of the 2nd interseted layers input
ValueTable3 = [IntersectInput1, IntersectInput4]                                                         # The order of the 3rd interseted layers input


arcpy.Intersect_analysis(ValueTable1, IntersectOutput1)                                                  # Executing the 1st intersection analysis
arcpy.AddMessage("The First Intersection is completed")                                                  # Adding messages for tracking the work progress

arcpy.Intersect_analysis(ValueTable2, IntersectOutput2)                                                  # Executing the 2nd intersection analysis
arcpy.AddMessage("The Second Intersection is completed")                                                 # Adding messages for tracking the work progress

arcpy.Intersect_analysis(ValueTable3, IntersectOutput3)                                                  # Executing the 3rd intersection analysis
arcpy.AddMessage("The Third Intersection is completed")                                                  # Adding messages for tracking the work progress

arcpy.AddMessage("Intersecting The Layers is Complete!!")                                                # Adding messages for tracking the work progress

# Buffering for one of the variables (rivers) intersected

BufferDistance = arcpy.GetParameterAsText(7)                                                             # Setting the buffer distance for the first intersection
BufferOutput = arcpy.GetParameterAsText(8)                                                               # Output of the buffered layer

arcpy.AddMessage("Creating the buffer........")                                                          # Adding messages for tracking the work progress

arcpy.Buffer_analysis (IntersectOutput1, BufferOutput, BufferDistance)                                   # Executing the buffer analysis tool

arcpy.AddMessage("Buffering for the Layer is Complete!!")                                                # Adding messages for tracking the work progress

# Union of all the feature classes from intersection and buffer, required and works only for polygons

UnionOutput = arcpy.GetParameterAsText(9)                                                                # Output of the union features
ValueTable = [IntersectOutput2, IntersectOutput3, BufferOutput]                                          # Order of the features to create union

arcpy.Union_analysis(ValueTable, UnionOutput)                                                            # Excecuting the union analysis tool

arcpy.AddMessage("Union of The Layers is Complete!!")                                                    # Adding messages for tracking the work progress

arcpy.CheckInExtension("3D")
arcpy.CheckInExtension("Spatial")
