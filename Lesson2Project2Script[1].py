import arcpy
import os
arcpy.env.overwriteOutput = True
print("done")
# The target folder, and target pojection will NOT be hard coded for final product
# out_dataset will be the same as target folder
target_folder = arcpy.GetParameterAsText(0)  # Parameter for the target folder
target_projection = arcpy.GetParameterAsText(1)  # Parameter for the target projection shapefile
out_dataset = target_folder  #the output data set will be the same as the target folder

try:
    desc = arcpy.Describe(target_projection)
    spatialref = desc.spatialReference
    print(spatialref.name)
    # obtains the spatial referance of the target projection

    arcpy.env.workspace = target_folder
    featureclasslist = arcpy.ListFeatureClasses()
    print(featureclasslist)
    # lists all the feature classes in the target folder

    for featureclass in featureclasslist:
        fc_desc = arcpy.Describe(featureclass)
        fc_sr = fc_desc.spatialReference
        rootname = featureclass
        # defines the spatial referance for each feature class in the list
        # set root name equal to each featureclass in list

        if fc_sr.name != spatialref.name:
            print("Reprojecting")
            # if feature class in list in NOT equal to spatial referance in
            # in target projection, continue with reproject.

            if featureclass.endswith(".shp"):
                rootname = featureclass[:-4]
                # Remove the last 4 characters ".shp" from the featureclass if
                # spatial referance is not equal to target projection

            out_prj_featureclass = os.path.join(out_dataset, f"{rootname}_projected.shp")
            print("Output path: " + out_prj_featureclass)
            # Creating our out path using the path.join method. Joining our decalared
            # out_dataset with the rootname and "_projected.shp"
            arcpy.management.Project(featureclass, out_prj_featureclass, spatialref)
            print("Output feature class: " + out_prj_featureclass )
            arcpy.AddMessage(f"Output feature class: {out_prj_featureclass}")
            # We run our projection tool, looping though each featureclass in our for loop
            # if it meets the permaeters of our if statement


    message = "Projection completed for all feature classes"
    print(message)
    arcpy.AddMessage(message)

except:

    arcpy.AddError("An error occurred")
    print(arcpy.GetMessages())