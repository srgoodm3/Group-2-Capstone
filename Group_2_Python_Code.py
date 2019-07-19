#File name: Group_2_Python_Code
#Author: Sam Goodman
#Date created: 06/03/2019
#Date last modified: 07/18/2019

import arcpy
arcpy.env.workspace=r"D:\Capstone\Group_2_Python_2.gdb"
arcpy.env.overwriteOutput = True

#data reprojection
coordinateSystem=arcpy.SpatialReference("NAD 1983 HARN StatePlane Arizona Central FIPS 0202 (Intl Feet)")
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\US_Tracts", "US_Tracts_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\AZ_blck_grp_2017", "AZ_Block_Groups_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\Mesa", "Mesa_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\Scottsdale", "Scottsdale_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\Employers2016", "Employers_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\Valley_Metro_Bus_Stops", "Valley_Metro_Bus_Stops_Reprojected", coordinateSystem)
arcpy.Project_management(r"D:\Capstone\Group_2_Python_2.gdb\Valley_Metro_Light_Rail_Stations", "Valley_Metro_Light_Rail_Stations_Reprojected", coordinateSystem)
print("Reprojection complete")

#join census tract data to tract shapfile
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\US_Tracts_Reprojected", "US_Tracts_Layer")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Mesa_Reprojected", "Mesa_Layer")
arcpy.AddJoin_management("US_Tracts_Layer", "GISJOIN", r"D:\Capstone\Group_2_Python_2.gdb\Census_Tract_Data", "GISJOIN")
arcpy.SelectLayerByLocation_management("US_Tracts_Layer", "HAVE_THEIR_CENTER_IN", "Mesa_Layer")
arcpy.CopyFeatures_management("US_Tracts_Layer", "Mesa_Tracts")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Scottsdale_Reprojected", "Scottsdale_Layer")
arcpy.SelectLayerByLocation_management("US_Tracts_Layer", "HAVE_THEIR_CENTER_IN", "Scottsdale_Layer")
arcpy.CopyFeatures_management("US_Tracts_Layer", "Scottsdale_Tracts")
print("Join complete")

#find grocery stores
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Employers_Reprojected", "Employers_Layer")
arcpy.SelectLayerByAttribute_management("Employers_Layer","","Naics6=445110")
arcpy.CopyFeatures_management("Employers_Layer", "Grocery_Stores")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Grocery_Stores", "Grocery_Stores_Layer")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Mesa_Tracts", "Mesa_Tracts_Layer")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Scottsdale_Tracts", "Scottsdale_Tracts_Layer")
arcpy.SelectLayerByLocation_management("Grocery_Stores_Layer", "WITHIN_A_DISTANCE", "Mesa_Tracts_Layer","1 Mile","NEW_SELECTION")
arcpy.CopyFeatures_management("Grocery_Stores_Layer", "Mesa_Grocery_Stores")
arcpy.SelectLayerByLocation_management("Grocery_Stores_Layer", "WITHIN_A_DISTANCE", "Scottsdale_Tracts_Layer","1 Mile","NEW_SELECTION")
arcpy.CopyFeatures_management("Grocery_Stores_Layer", "Scottsdale_Grocery_Stores")
print("Grocery stores complete")

#find public transportation stops
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Valley_Metro_Bus_Stops_Reprojected", "Valley_Metro_Bus_Stops_Layer")
arcpy.MakeFeatureLayer_management(r"D:\Capstone\Group_2_Python_2.gdb\Valley_Metro_Light_Rail_Stations_Reprojected", "Valley_Metro_Light_Rail_Stations_Layer")
arcpy.SelectLayerByLocation_management("Valley_Metro_Bus_Stops_Layer", "WITHIN_A_DISTANCE", "Mesa_Tracts_Layer","0.25 Mile")
arcpy.CopyFeatures_management("Valley_Metro_Bus_Stops_Layer", "Mesa_Bus_Stops")
arcpy.SelectLayerByLocation_management("Valley_Metro_Bus_Stops_Layer", "WITHIN_A_DISTANCE", "Scottsdale_Tracts_Layer","0.25 Mile")
arcpy.CopyFeatures_management("Valley_Metro_Bus_Stops_Layer", "Scottsdale_Bus_Stops")
arcpy.SelectLayerByLocation_management("Valley_Metro_Light_Rail_Stations_Layer", "WITHIN_A_DISTANCE", "Mesa_Tracts_Layer","0.25 Mile")
arcpy.CopyFeatures_management("Valley_Metro_Light_Rail_Stations_Layer", "Mesa_Light_Rail_Stops")
print("Public Transportation complete")

#find demographic percentages
arcpy.AddField_management("Mesa_Tracts", "Age_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Tracts", "Minority_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Tracts", "Education_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Tracts", "Median_Income", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Age_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Minority_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Education_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Median_Income", "DOUBLE")
arcpy.CalculateField_management("Mesa_Tracts", "Age_Percentage", "(!Census_Tract_Data_AHYQE003!+!Census_Tract_Data_AHYQE004!+!Census_Tract_Data_AHYQE005!+!Census_Tract_Data_AHYQE006!+!Census_Tract_Data_AHYQE020!+!Census_Tract_Data_AHYQE021!+!Census_Tract_Data_AHYQE022!+!Census_Tract_Data_AHYQE023!+!Census_Tract_Data_AHYQE024!+!Census_Tract_Data_AHYQE025!+!Census_Tract_Data_AHYQE027!+!Census_Tract_Data_AHYQE028!+!Census_Tract_Data_AHYQE029!+!Census_Tract_Data_AHYQE030!+!Census_Tract_Data_AHYQE044!+!Census_Tract_Data_AHYQE045!+!Census_Tract_Data_AHYQE046!+!Census_Tract_Data_AHYQE047!+!Census_Tract_Data_AHYQE048!+!Census_Tract_Data_AHYQE049!)/!Census_Tract_Data_AHYQE001!")
arcpy.CalculateField_management("Mesa_Tracts", "Minority_Percentage", "(!Census_Tract_Data_AHZAE001!-!Census_Tract_Data_AHZAE003!)/!Census_Tract_Data_AHZAE001!")
arcpy.CalculateField_management("Mesa_Tracts", "Education_Percentage", "(!Census_Tract_Data_AH04E017!+!Census_Tract_Data_AH04E018!+!Census_Tract_Data_AH04E019!+!Census_Tract_Data_AH04E020!+!Census_Tract_Data_AH04E021!+!Census_Tract_Data_AH04E022!+!Census_Tract_Data_AH04E023!+!Census_Tract_Data_AH04E024!+!Census_Tract_Data_AH04E025!)/!Census_Tract_Data_AH04E001!")
arcpy.CalculateField_management("Mesa_Tracts", "Median_Income", "!Census_Tract_Data_AH1PE001!")
arcpy.CalculateField_management("Scottsdale_Tracts", "Age_Percentage", "(!Census_Tract_Data_AHYQE003!+!Census_Tract_Data_AHYQE004!+!Census_Tract_Data_AHYQE005!+!Census_Tract_Data_AHYQE006!+!Census_Tract_Data_AHYQE020!+!Census_Tract_Data_AHYQE021!+!Census_Tract_Data_AHYQE022!+!Census_Tract_Data_AHYQE023!+!Census_Tract_Data_AHYQE024!+!Census_Tract_Data_AHYQE025!+!Census_Tract_Data_AHYQE027!+!Census_Tract_Data_AHYQE028!+!Census_Tract_Data_AHYQE029!+!Census_Tract_Data_AHYQE030!+!Census_Tract_Data_AHYQE044!+!Census_Tract_Data_AHYQE045!+!Census_Tract_Data_AHYQE046!+!Census_Tract_Data_AHYQE047!+!Census_Tract_Data_AHYQE048!+!Census_Tract_Data_AHYQE049!)/!Census_Tract_Data_AHYQE001!")
arcpy.CalculateField_management("Scottsdale_Tracts", "Minority_Percentage", "(!Census_Tract_Data_AHZAE001!-!Census_Tract_Data_AHZAE003!)/!Census_Tract_Data_AHZAE001!")
arcpy.CalculateField_management("Scottsdale_Tracts", "Education_Percentage", "(!Census_Tract_Data_AH04E017!+!Census_Tract_Data_AH04E018!+!Census_Tract_Data_AH04E019!+!Census_Tract_Data_AH04E020!+!Census_Tract_Data_AH04E021!+!Census_Tract_Data_AH04E022!+!Census_Tract_Data_AH04E023!+!Census_Tract_Data_AH04E024!+!Census_Tract_Data_AH04E025!)/!Census_Tract_Data_AH04E001!")
arcpy.CalculateField_management("Scottsdale_Tracts", "Median_Income", "!Census_Tract_Data_AH1PE001!")
print("Demographic percentages complete")

#find buffer coverage
arcpy.Buffer_analysis("Mesa_Bus_Stops","Mesa_Bus_Stops_Buffer", "0.25 Mile")
arcpy.Buffer_analysis("Scottsdale_Bus_Stops","Scottsdale_Bus_Stops_Buffer", "0.25 Mile")
arcpy.Buffer_analysis("Mesa_Light_Rail_Stops","Mesa_Light_Rail_Stops_Buffer", "0.25 Mile")
arcpy.Buffer_analysis("Mesa_Grocery_Stores","Mesa_Grocery_Stores_Buffer", "1 Mile")
arcpy.Buffer_analysis("Scottsdale_Grocery_Stores","Scottsdale_Grocery_Stores_Buffer", "1 Mile")
arcpy.Dissolve_management("Mesa_Bus_Stops_Buffer", "Mesa_Bus_Stops_Buffer_Dissolve")
arcpy.Dissolve_management("Scottsdale_Bus_Stops_Buffer", "Scottsdale_Bus_Stops_Buffer_Dissolve")
arcpy.Dissolve_management("Mesa_Light_Rail_Stops_Buffer", "Mesa_Light_Rail_Stops_Buffer_Dissolve")
arcpy.Dissolve_management("Mesa_Grocery_Stores_Buffer", "Mesa_Grocery_Stores_Buffer_Dissolve")
arcpy.Dissolve_management("Scottsdale_Grocery_Stores_Buffer", "Scottsdale_Grocery_Stores_Buffer_Dissolve")
arcpy.Clip_analysis("Mesa_Tracts", "Mesa_Bus_Stops_Buffer_Dissolve", "Mesa_Bus_Stops_Buffer_Clip")
arcpy.Clip_analysis("Mesa_Tracts", "Mesa_Light_Rail_Stops_Buffer_Dissolve", "Mesa_Light_Rail_Stops_Buffer_Clip")
arcpy.Clip_analysis("Mesa_Tracts", "Mesa_Grocery_Stores_Buffer_Dissolve", "Mesa_Grocery_Stores_Buffer_Clip")
arcpy.Clip_analysis("Scottsdale_Tracts", "Scottsdale_Bus_Stops_Buffer_Dissolve", "Scottsdale_Bus_Stops_Buffer_Clip")
arcpy.Clip_analysis("Scottsdale_Tracts", "Scottsdale_Grocery_Stores_Buffer_Dissolve", "Scottsdale_Grocery_Stores_Buffer_Clip")
arcpy.AddGeometryAttributes_management("Mesa_Tracts", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Tracts", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Mesa_Bus_Stops_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Mesa_Light_Rail_Stops_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Bus_Stops_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Mesa_Grocery_Stores_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Grocery_Stores_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddField_management("Mesa_Tracts", "Grocery_Coverage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Grocery_Coverage", "DOUBLE")
arcpy.AddField_management("Mesa_Tracts", "Transportation_Coverage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Tracts", "Transportation_Coverage", "DOUBLE")
arcpy.MakeFeatureLayer_management("Mesa_Tracts", "Mesa_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Grocery_Stores_Buffer_Clip", "Mesa_Grocery_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Bus_Stops_Buffer_Clip", "Mesa_Bus_Layer")
arcpy.AddJoin_management("Mesa_Layer", "US_Tracts_Reprojected_GISJOIN", "Mesa_Grocery_Layer", "US_Tracts_Reprojected_GISJOIN")
arcpy.AddJoin_management("Mesa_Layer", "US_Tracts_Reprojected_GISJOIN", "Mesa_Bus_Layer", "US_Tracts_Reprojected_GISJOIN")
arcpy.CopyFeatures_management("Mesa_Layer", "Mesa_Tracts_Temp")
with arcpy.da.UpdateCursor("Mesa_Tracts_Temp", ["Mesa_Grocery_Stores_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Temp", ["Mesa_Bus_Stops_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
arcpy.CalculateField_management("Mesa_Tracts_Temp", "Mesa_Tracts_Grocery_Coverage", "!Mesa_Grocery_Stores_Buffer_Clip_POLY_AREA!/!Mesa_Tracts_POLY_AREA!")
arcpy.CalculateField_management("Mesa_Tracts_Temp", "Mesa_Tracts_Transportation_Coverage", "!Mesa_Bus_Stops_Buffer_Clip_POLY_AREA!/!Mesa_Tracts_POLY_AREA!")
arcpy.CopyFeatures_management("Mesa_Tracts_Temp", "Mesa_Tracts_Final")
arcpy.MakeFeatureLayer_management("Scottsdale_Tracts", "scottsdale_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Grocery_Stores_Buffer_Clip", "Scottsdale_Grocery_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Bus_Stops_Buffer_Clip", "Scottsdale_Bus_Layer")
arcpy.AddJoin_management("Scottsdale_Layer", "US_Tracts_Reprojected_GISJOIN", "Scottsdale_Grocery_Layer", "US_Tracts_Reprojected_GISJOIN")
arcpy.AddJoin_management("Scottsdale_Layer", "US_Tracts_Reprojected_GISJOIN", "Scottsdale_Bus_Layer", "US_Tracts_Reprojected_GISJOIN")
arcpy.CopyFeatures_management("Scottsdale_Layer", "Scottsdale_Tracts_Temp")
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Temp", ["Scottsdale_Grocery_Stores_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Temp", ["Scottsdale_Bus_Stops_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
arcpy.CalculateField_management("Scottsdale_Tracts_Temp", "Scottsdale_Tracts_Grocery_Coverage", "!Scottsdale_Grocery_Stores_Buffer_Clip_POLY_AREA!/!Scottsdale_Tracts_POLY_AREA!")
arcpy.CalculateField_management("Scottsdale_Tracts_Temp", "Scottsdale_Tracts_Transportation_Coverage", "!Scottsdale_Bus_Stops_Buffer_Clip_POLY_AREA!/!Scottsdale_Tracts_POLY_AREA!")
arcpy.CopyFeatures_management("Scottsdale_Tracts_Temp", "Scottsdale_Tracts_Final")
print("Buffer zones complete")

#assign scores
arcpy.AddField_management("Mesa_Tracts_Final", "Grocery_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Transportation_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Age_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Education_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Minority_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Income_Score", "SHORT")
arcpy.AddField_management("Mesa_Tracts_Final", "Total_Score", "SHORT")
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Age_Percentage","Age_Score"]) as cursor:
    for row in cursor:
        if row[0] <.3:
            row[1] = 4
        elif row[0] >=.3 and row[0] <.4:
            row[1] = 3
        elif row[0] >=.4 and row[0] <.5:
            row[1] = 2
        if row[0] >=.5:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Education_Percentage","Education_Score"]) as cursor:
    for row in cursor:
        if row[0] >=.9:
            row[1] = 4
        elif row[0] >=.75 and row[0] <.9:
            row[1] = 3
        elif row[0] >=.6 and row[0] <.75:
            row[1] = 2
        if row[0] <=.6:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Minority_Percentage","Minority_Score"]) as cursor:
    for row in cursor:
        if row[0] <.35:
            row[1] = 4
        elif row[0] >=.35 and row[0] <.45:
            row[1] = 3
        elif row[0] >=.45 and row[0] <.55:
            row[1] = 2
        if row[0] >=.55:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Median_Income","Income_Score"]) as cursor:
    for row in cursor:
        if row[0] >=92000:
            row[1] = 4
        elif row[0] >59000 and row[0] <92000:
            row[1] = 3
        elif row[0] >26000 and row[0] <=59000:
            row[1] = 2
        if row[0] <=26000:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Grocery_Coverage","Grocery_Score"]) as cursor:
    for row in cursor:
        if row[0] >.33:
            row[1] = 2
        elif row[0] <=.33:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Tracts_Final", ["Mesa_Tracts_Transportation_Coverage","Transportation_Score"]) as cursor:
    for row in cursor:
        if row[0] >.5:
            row[1] = 2
        elif row[0] <=.5:
            row[1] = 1
        cursor.updateRow(row)
arcpy.AddField_management("Scottsdale_Tracts_Final", "Grocery_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Transportation_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Age_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Education_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Minority_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Income_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Tracts_Final", "Total_Score", "SHORT")
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Age_Percentage","Age_Score"]) as cursor:
    for row in cursor:
        if row[0] <.3:
            row[1] = 4
        elif row[0] >=.3 and row[0] <.4:
            row[1] = 3
        elif row[0] >=.4 and row[0] <.5:
            row[1] = 2
        if row[0] >=.5:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Education_Percentage","Education_Score"]) as cursor:
    for row in cursor:
        if row[0] >=.9:
            row[1] = 4
        elif row[0] >=.75 and row[0] <.9:
            row[1] = 3
        elif row[0] >=.6 and row[0] <.75:
            row[1] = 2
        if row[0] <=.6:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Minority_Percentage","Minority_Score"]) as cursor:
    for row in cursor:
        if row[0] <.35:
            row[1] = 4
        elif row[0] >=.35 and row[0] <.45:
            row[1] = 3
        elif row[0] >=.45 and row[0] <.55:
            row[1] = 2
        if row[0] >=.55:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Median_Income","Income_Score"]) as cursor:
    for row in cursor:
        if row[0] >=92000:
            row[1] = 4
        elif row[0] >59000 and row[0] <92000:
            row[1] = 3
        elif row[0] >26000 and row[0] <=59000:
            row[1] = 2
        if row[0] <=26000:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Grocery_Coverage","Grocery_Score"]) as cursor:
    for row in cursor:
        if row[0] >.33:
            row[1] = 2
        elif row[0] <=.33:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Tracts_Final", ["Scottsdale_Tracts_Transportation_Coverage","Transportation_Score"]) as cursor:
    for row in cursor:
        if row[0] >.5:
            row[1] = 2
        elif row[0] <=.5:
            row[1] = 1
        cursor.updateRow(row)
arcpy.CalculateField_management("Mesa_Tracts_Final", "Total_Score", "!Age_Score!+!Education_Score!+!Minority_Score!+!Income_Score!+!Grocery_Score!+!Transportation_Score!")
arcpy.CalculateField_management("Scottsdale_Tracts_Final", "Total_Score", "!Age_Score!+!Education_Score!+!Minority_Score!+!Income_Score!+!Grocery_Score!+!Transportation_Score!")
print("Scores complete")

#select focus tracts
arcpy.MakeFeatureLayer_management("Mesa_Tracts_Final", "Mesa_Tracts_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Tracts_Final", "Scottsdale_Tracts_Layer")
arcpy.SelectLayerByAttribute_management("Mesa_Tracts_Layer", "NEW_SELECTION", "Total_Score<=12")
arcpy.CopyFeatures_management("Mesa_Tracts_Layer", "Mesa_Focus_Tracts")
arcpy.SelectLayerByAttribute_management("Scottsdale_Tracts_Layer", "NEW_SELECTION", "Total_Score<=15")
arcpy.CopyFeatures_management("Scottsdale_Tracts_Layer", "Scottsdale_Focus_Tracts")
print("Focus tracts complete")

#break focus tracts down to block group level
arcpy.MakeFeatureLayer_management("AZ_Block_Groups_Reprojected", "AZ_Block_Groups_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Focus_Tracts", "Mesa_Focus_Tracts_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Tracts", "Mesa_Layer")
arcpy.AddJoin_management("AZ_Block_Groups_Layer", "GISJOIN", r"D:\Capstone\Group_2_Python_2.gdb\Block_Group_Data", "GISJOIN")
arcpy.SelectLayerByLocation_management("AZ_Block_Groups_Layer", "HAVE_THEIR_CENTER_IN", "Mesa_Layer")
arcpy.CopyFeatures_management("AZ_Block_Groups_Layer", "Mesa_Block_Groups")
arcpy.SelectLayerByLocation_management("AZ_Block_Groups_Layer", "HAVE_THEIR_CENTER_IN", "Mesa_Focus_Tracts_Layer")
arcpy.CopyFeatures_management("AZ_Block_Groups_Layer", "Mesa_Focus_Block_Groups")
arcpy.MakeFeatureLayer_management("Scottsdale_Focus_Tracts", "Scottsdale_Focus_Tracts_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Tracts", "Scottsdale_Layer")
arcpy.SelectLayerByLocation_management("AZ_Block_Groups_Layer", "HAVE_THEIR_CENTER_IN", "Scottsdale_Layer")
arcpy.CopyFeatures_management("AZ_Block_Groups_Layer", "Scottsdale_Block_Groups")
arcpy.SelectLayerByLocation_management("AZ_Block_Groups_Layer", "HAVE_THEIR_CENTER_IN", "Scottsdale_Focus_Tracts_Layer")
arcpy.CopyFeatures_management("AZ_Block_Groups_Layer", "Scottsdale_Focus_Block_Groups")
print("Block groups complete")


#find demographic percentages to block groups
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Age_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Minority_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Education_Percentage", "DOUBLE")
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Median_Income", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Age_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Minority_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Education_Percentage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Median_Income", "DOUBLE")
arcpy.CalculateField_management("Mesa_Focus_Block_Groups", "Age_Percentage", "(!Block_Group_Data_AHYQE003!+!Block_Group_Data_AHYQE004!+!Block_Group_Data_AHYQE005!+!Block_Group_Data_AHYQE006!+!Block_Group_Data_AHYQE020!+!Block_Group_Data_AHYQE021!+!Block_Group_Data_AHYQE022!+!Block_Group_Data_AHYQE023!+!Block_Group_Data_AHYQE024!+!Block_Group_Data_AHYQE025!+!Block_Group_Data_AHYQE027!+!Block_Group_Data_AHYQE028!+!Block_Group_Data_AHYQE029!+!Block_Group_Data_AHYQE030!+!Block_Group_Data_AHYQE044!+!Block_Group_Data_AHYQE045!+!Block_Group_Data_AHYQE046!+!Block_Group_Data_AHYQE047!+!Block_Group_Data_AHYQE048!+!Block_Group_Data_AHYQE049!)/!Block_Group_Data_AHYQE001!")
arcpy.CalculateField_management("Mesa_Focus_Block_Groups", "Minority_Percentage", "(!Block_Group_Data_AHZAE001!-!Block_Group_Data_AHZAE003!)/!Block_Group_Data_AHZAE001!")
arcpy.CalculateField_management("Mesa_Focus_Block_Groups", "Education_Percentage", "(!Block_Group_Data_AH04E017!+!Block_Group_Data_AH04E018!+!Block_Group_Data_AH04E019!+!Block_Group_Data_AH04E020!+!Block_Group_Data_AH04E021!+!Block_Group_Data_AH04E022!+!Block_Group_Data_AH04E023!+!Block_Group_Data_AH04E024!+!Block_Group_Data_AH04E025!)/!Block_Group_Data_AH04E001!")
arcpy.CalculateField_management("Mesa_Focus_Block_Groups", "Median_Income", "!Block_Group_Data_AH1PE001!")
arcpy.CalculateField_management("Scottsdale_Focus_Block_Groups", "Age_Percentage", "(!Block_Group_Data_AHYQE003!+!Block_Group_Data_AHYQE004!+!Block_Group_Data_AHYQE005!+!Block_Group_Data_AHYQE006!+!Block_Group_Data_AHYQE020!+!Block_Group_Data_AHYQE021!+!Block_Group_Data_AHYQE022!+!Block_Group_Data_AHYQE023!+!Block_Group_Data_AHYQE024!+!Block_Group_Data_AHYQE025!+!Block_Group_Data_AHYQE027!+!Block_Group_Data_AHYQE028!+!Block_Group_Data_AHYQE029!+!Block_Group_Data_AHYQE030!+!Block_Group_Data_AHYQE044!+!Block_Group_Data_AHYQE045!+!Block_Group_Data_AHYQE046!+!Block_Group_Data_AHYQE047!+!Block_Group_Data_AHYQE048!+!Block_Group_Data_AHYQE049!)/!Block_Group_Data_AHYQE001!")
arcpy.CalculateField_management("Scottsdale_Focus_Block_Groups", "Minority_Percentage", "(!Block_Group_Data_AHZAE001!-!Block_Group_Data_AHZAE003!)/!Block_Group_Data_AHZAE001!")
arcpy.CalculateField_management("Scottsdale_Focus_Block_Groups", "Education_Percentage", "(!Block_Group_Data_AH04E017!+!Block_Group_Data_AH04E018!+!Block_Group_Data_AH04E019!+!Block_Group_Data_AH04E020!+!Block_Group_Data_AH04E021!+!Block_Group_Data_AH04E022!+!Block_Group_Data_AH04E023!+!Block_Group_Data_AH04E024!+!Block_Group_Data_AH04E025!)/!Block_Group_Data_AH04E001!")
arcpy.CalculateField_management("Scottsdale_Focus_Block_Groups", "Median_Income", "!Block_Group_Data_AH1PE001!")
print("Demographic percentages complete")

#find buffer coverage for block groups
arcpy.Clip_analysis("Mesa_Focus_Block_Groups", "Mesa_Bus_Stops_Buffer_Dissolve", "Mesa_Block_Group_Bus_Stops_Buffer_Clip")
arcpy.Clip_analysis("Mesa_Focus_Block_Groups", "Mesa_Grocery_Stores_Buffer_Dissolve", "Mesa_Block_Group_Grocery_Stores_Buffer_Clip")
arcpy.Clip_analysis("Scottsdale_Focus_Block_Groups", "Scottsdale_Bus_Stops_Buffer_Dissolve", "Scottsdale_Block_Group_Bus_Stops_Buffer_Clip")
arcpy.Clip_analysis("Scottsdale_Focus_Block_Groups", "Scottsdale_Grocery_Stores_Buffer_Dissolve", "Scottsdale_Block_Group_Grocery_Stores_Buffer_Clip")
arcpy.AddGeometryAttributes_management("Mesa_Focus_Block_Groups", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Focus_Block_Groups", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Mesa_Block_Group_Bus_Stops_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Block_Group_Bus_Stops_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Mesa_Block_Group_Grocery_Stores_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddGeometryAttributes_management("Scottsdale_Block_Group_Grocery_Stores_Buffer_Clip", "AREA", "", "SQUARE_MILES_US")
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Grocery_Coverage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Grocery_Coverage", "DOUBLE")
arcpy.AddField_management("Mesa_Focus_Block_Groups", "Transportation_Coverage", "DOUBLE")
arcpy.AddField_management("Scottsdale_Focus_Block_Groups", "Transportation_Coverage", "DOUBLE")
arcpy.MakeFeatureLayer_management("Mesa_Focus_Block_Groups", "Mesa_Block_Groups_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Block_Group_Grocery_Stores_Buffer_Clip", "Mesa_Block_Group_Grocery_Layer")
arcpy.MakeFeatureLayer_management("Mesa_Block_Group_Bus_Stops_Buffer_Clip", "Mesa_Block_Group_Bus_Layer")
arcpy.AddJoin_management("Mesa_Block_Groups_Layer", "AZ_Block_Groups_Reprojected_GISJOIN", "Mesa_Block_Group_Grocery_Layer", "AZ_Block_Groups_Reprojected_GISJOIN")
arcpy.AddJoin_management("Mesa_Block_Groups_Layer", "AZ_Block_Groups_Reprojected_GISJOIN", "Mesa_Block_Group_Bus_Layer", "AZ_Block_Groups_Reprojected_GISJOIN")
arcpy.CopyFeatures_management("Mesa_Block_Groups_Layer", "Mesa_Block_Group_Temp")
with arcpy.da.UpdateCursor("Mesa_Block_Group_Temp", ["Mesa_Block_Group_Grocery_Stores_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Group_Temp", ["Mesa_Block_Group_Bus_Stops_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
arcpy.CalculateField_management("Mesa_Block_Group_Temp", "Mesa_Focus_Block_Groups_Grocery_Coverage", "!Mesa_Block_Group_Grocery_Stores_Buffer_Clip_POLY_AREA!/!Mesa_Focus_Block_Groups_POLY_AREA!")
arcpy.CalculateField_management("Mesa_Block_Group_Temp", "Mesa_Focus_Block_Groups_Transportation_Coverage", "!Mesa_Block_Group_Bus_Stops_Buffer_Clip_POLY_AREA!/!Mesa_Focus_Block_Groups_POLY_AREA!")
arcpy.CopyFeatures_management("Mesa_Block_Group_Temp", "Mesa_Block_Groups_Final")
arcpy.MakeFeatureLayer_management("Scottsdale_Focus_Block_Groups", "Scottsdale_Block_Groups_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Block_Group_Grocery_Stores_Buffer_Clip", "Scottsdale_Block_Group_Grocery_Layer")
arcpy.MakeFeatureLayer_management("Scottsdale_Block_Group_Bus_Stops_Buffer_Clip", "Scottsdale_Block_Group_Bus_Layer")
arcpy.AddJoin_management("Scottsdale_Block_Groups_Layer", "AZ_Block_Groups_Reprojected_GISJOIN", "Scottsdale_Block_Group_Grocery_Layer", "AZ_Block_Groups_Reprojected_GISJOIN")
arcpy.AddJoin_management("Scottsdale_Block_Groups_Layer", "AZ_Block_Groups_Reprojected_GISJOIN", "Scottsdale_Block_Group_Bus_Layer", "AZ_Block_Groups_Reprojected_GISJOIN")
arcpy.CopyFeatures_management("Scottsdale_Block_Groups_Layer", "Scottsdale_Block_Group_Temp")
with arcpy.da.UpdateCursor("Scottsdale_Block_Group_Temp", ["Scottsdale_Block_Group_Grocery_Stores_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Group_Temp", ["Scottsdale_Block_Group_Bus_Stops_Buffer_Clip_POLY_AREA"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
        cursor.updateRow(row)
arcpy.CalculateField_management("Scottsdale_Block_Group_Temp", "Scottsdale_Focus_Block_Groups_Grocery_Coverage", "!Scottsdale_Block_Group_Grocery_Stores_Buffer_Clip_POLY_AREA!/!Scottsdale_Focus_Block_Groups_POLY_AREA!")
arcpy.CalculateField_management("Scottsdale_Block_Group_Temp", "Scottsdale_Focus_Block_Groups_Transportation_Coverage", "!Scottsdale_Block_Group_Bus_Stops_Buffer_Clip_POLY_AREA!/!Scottsdale_Focus_Block_Groups_POLY_AREA!")
arcpy.CopyFeatures_management("Scottsdale_Block_Group_Temp", "Scottsdale_Block_Groups_Final")
print("Buffer zones complete")

#assign scores
arcpy.AddField_management("Mesa_Block_Groups_Final", "Grocery_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Transportation_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Age_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Education_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Minority_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Income_Score", "SHORT")
arcpy.AddField_management("Mesa_Block_Groups_Final", "Total_Score", "SHORT")
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Age_Percentage","Age_Score"]) as cursor:
    for row in cursor:
        if row[0] <.3:
            row[1] = 4
        elif row[0] >=.3 and row[0] <.4:
            row[1] = 3
        elif row[0] >=.4 and row[0] <.5:
            row[1] = 2
        if row[0] >=.5:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Education_Percentage","Education_Score"]) as cursor:
    for row in cursor:
        if row[0] >=.9:
            row[1] = 4
        elif row[0] >=.75 and row[0] <.9:
            row[1] = 3
        elif row[0] >=.6 and row[0] <.75:
            row[1] = 2
        if row[0] <=.6:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Minority_Percentage","Minority_Score"]) as cursor:
    for row in cursor:
        if row[0] <.35:
            row[1] = 4
        elif row[0] >=.35 and row[0] <.45:
            row[1] = 3
        elif row[0] >=.45 and row[0] <.55:
            row[1] = 2
        if row[0] >=.55:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Median_Income","Income_Score"]) as cursor:
    for row in cursor:
        if row[0] >=92000:
            row[1] = 4
        elif row[0] >59000 and row[0] <92000:
            row[1] = 3
        elif row[0] >26000 and row[0] <=59000:
            row[1] = 2
        if row[0] <=26000:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Grocery_Coverage","Grocery_Score"]) as cursor:
    for row in cursor:
        if row[0] >.33:
            row[1] = 2
        elif row[0] <=.33:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Mesa_Block_Groups_Final", ["Mesa_Focus_Block_Groups_Transportation_Coverage","Transportation_Score"]) as cursor:
    for row in cursor:
        if row[0] >.5:
            row[1] = 2
        elif row[0] <=.5:
            row[1] = 1
        cursor.updateRow(row)
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Grocery_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Transportation_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Age_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Education_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Minority_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Income_Score", "SHORT")
arcpy.AddField_management("Scottsdale_Block_Groups_Final", "Total_Score", "SHORT")
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Age_Percentage","Age_Score"]) as cursor:
    for row in cursor:
        if row[0] <.3:
            row[1] = 4
        elif row[0] >=.3 and row[0] <.4:
            row[1] = 3
        elif row[0] >=.4 and row[0] <.5:
            row[1] = 2
        if row[0] >=.5:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Education_Percentage","Education_Score"]) as cursor:
    for row in cursor:
        if row[0] >=.9:
            row[1] = 4
        elif row[0] >=.75 and row[0] <.9:
            row[1] = 3
        elif row[0] >=.6 and row[0] <.75:
            row[1] = 2
        if row[0] <=.6:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Minority_Percentage","Minority_Score"]) as cursor:
    for row in cursor:
        if row[0] <.35:
            row[1] = 4
        elif row[0] >=.35 and row[0] <.45:
            row[1] = 3
        elif row[0] >=.45 and row[0] <.55:
            row[1] = 2
        if row[0] >=.55:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Median_Income","Income_Score"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[1] = 2
        elif row[0] >=92000:
            row[1] = 4
        elif row[0] >59000 and row[0] <92000:
            row[1] = 3
        elif row[0] >26000 and row[0] <=59000:
            row[1] = 2
        elif row[0] <=26000:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Grocery_Coverage","Grocery_Score"]) as cursor:
    for row in cursor:
        if row[0] >.33:
            row[1] = 2
        elif row[0] <=.33:
            row[1] = 1
        cursor.updateRow(row)
with arcpy.da.UpdateCursor("Scottsdale_Block_Groups_Final", ["Scottsdale_Focus_Block_Groups_Transportation_Coverage","Transportation_Score"]) as cursor:
    for row in cursor:
        if row[0] >.5:
            row[1] = 2
        elif row[0] <=.5:
            row[1] = 1
        cursor.updateRow(row)
arcpy.CalculateField_management("Mesa_Block_Groups_Final", "Total_Score", "!Age_Score!+!Education_Score!+!Minority_Score!+!Income_Score!+!Grocery_Score!+!Transportation_Score!")
arcpy.CalculateField_management("Scottsdale_Block_Groups_Final", "Total_Score", "!Age_Score!+!Education_Score!+!Minority_Score!+!Income_Score!+!Grocery_Score!+!Transportation_Score!")
print("Scores complete")
print("All functions complete")