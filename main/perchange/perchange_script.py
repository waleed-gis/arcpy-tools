# importing modules
import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy.ia import *
from arcpy.sa import *
from arcpy.sa import *
from sys import argv
from pyrsistent import s

def timestamp(message): # This is meant to replace print() or arcpy.AddMessage() in the script when I want to add messages.  It timestamps the messages so I can monitor performance of different stages in script.
    now = datetime.datetime.now()
    print(now.strftime("%H:%M:%S") + " - " + message)

timestamp("Modules loaded. Starting geoprocessing")
# inputs

country = 'BLZ'
variable = 'NDVI'
pre_year = '2000'
post_year = '2020'
r_ext = '.tif'

# -----------------------------------------------------------
pre_r = country + '_' + variable + '_' + pre_year + r_ext
post_r = country + '_' + variable + '_' + post_year + r_ext

# Locations 
pre_raster_loc = "D:\\Work\\Fiverr\\Fieverr_IncomePoverty\\change_detection\\pre\\"
post_raster_loc = "D:\\Work\\Fiverr\\Fieverr_IncomePoverty\\change_detection\\post\\"

pre_raster = pre_raster_loc + pre_r
post_raster = post_raster_loc + post_r

# Export Output
export_loc = "D:\\Work\\Fiverr\\Fieverr_IncomePoverty\\change_detection\\final_export\\"
temp_loc = "D:\\Work\\Fiverr\\Fieverr_IncomePoverty\\change_detection\\final_export\\temp\\"
# workspace loc
ws_loc = "D:\Work\Fiverr\Fieverr_IncomePoverty\change_detection\ChangeDet_EnvVar\ChangeDet_EnvVar.gdb"

# Workspace declare
env.workspace = ws_loc  
arcpy.env.overwriteOutput = False

# Check out any necessary licenses.
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("ImageAnalyst")
timestamp('Input output initialized successfully...')
"""
PRE RASTER Normalization
"""
pre_stat_raster = arcpy.management.CalculateStatistics(in_raster_dataset=pre_raster)
pre_stat_raster = arcpy.Raster(pre_stat_raster)
pre_normalized_name = pre_r[0:8] + '_nor_pre'
pre_normalized_loc = temp_loc + pre_normalized_name + '.tif'
# Post Normalization Analysis
pre_normalized = (pre_stat_raster - pre_stat_raster.minimum) / (pre_stat_raster.maximum - pre_stat_raster.minimum)
pre_normalized.save(pre_normalized_loc)

"""
POST Raster Normalization
"""
post_stat_raster = arcpy.management.CalculateStatistics(in_raster_dataset=post_raster)
post_stat_raster = arcpy.Raster(post_stat_raster)
post_normalized_name = post_r[0:8] + '_nor_post'
post_normalized_loc = temp_loc + post_normalized_name + r_ext
# Post Normalization Analysis
post_normalized = (post_stat_raster - post_stat_raster.minimum) / (post_stat_raster.maximum - post_stat_raster.minimum)
post_normalized.save(post_normalized_loc)
timestamp('Pre and post normalization done...')
"""
Percentage Change Analysis
"""
perchange_loc = export_loc + post_r[0:8] + '_cd' + r_ext
perchange = ((post_normalized -  pre_normalized ) / ( pre_normalized )) * 100
perchange.save(perchange_loc)
timestamp('percent change done...')
timestamp('---COMPLETED---')
