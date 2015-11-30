import os, sys, yaml
import maya.cmds as mc
import maya.mel as mm

from ptAlembic import abcUtils
reload(abcUtils)

from ptAlembic import fileUtils
from ptAlembic import importShade
reload(importShade)

from utils import customLog 

logger = customLog.customLog()

exportGrp = 'Geo_Grp'
exportDept = 'anim'

# import data 
def doImport(dataPath) : 
	data = loadData(dataPath)
	importCache(data)


# read data 
def loadData(dataPath) : 
	config = open(dataPath, 'r')
	data = yaml.load(config)

	return data


# import cache cmd 
def importCache(data) : 
	# input data
	if data : 
		# loop through each namespace dictionary
		for each in data : 
			# namespace
			namespace = each 

			# alembic abc cache file
			path = data[each]['cachePath']

			# shader file 
			shadeFile = data[each]['shadeFile']

			# shader data file 
			shadeDateFile = data[each]['shadeDataFile']

			# if no asset in the scene, import new 
			if not mc.objExists('%s:Rig_Grp' % namespace) : 

				# check namespace exists. If not, create one 
				if not mc.namespace(exists = namespace) : 
					mc.namespace(add = namespace)

				# set to asset namespace 
				mc.namespace(set = namespace)

				# import new alembic for this asset 
				obj = '/'
				abcResult = abcUtils.importABC(obj, path, 'new')
				logger.info('import cache %s success' % namespace)

				# import shader for this asset 
				shadeResult = importShade.applyShade(namespace, shadeFile, shadeDateFile)

				# clean unused node 
				mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

				# set namespace back to root 
				mc.namespace(set = ':')
				logger.info('apply shader')

				# set Rig_Grp to existing geo_grp
				if mc.objExists('%s:%s' % (namespace, exportGrp)) : 
					mc.group('%s:%s' % (namespace, exportGrp), n = 'Rig_Grp')
					logger.info('set Rig_Grp')



			# if asset already exists, update animation
			else : 
				# geo group 
				obj = '%s:%s' % (namespace, exportGrp)

				# merge alembic to geo_grp 
				abcResult = abcUtils.importABC(obj, path, 'add')