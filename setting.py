import sys, os 
import maya.cmds as mc

from tool.utils import pipelineTools, sceneInfo, fileUtils 
reload(pipelineTools)
reload(sceneInfo)
reload(fileUtils)

exportDept = 'anim'

def getSceneInfo(project = '', episode = '', sequence = '', shot = '', dept = '') : 
	drive = ''
	fileName = ''

	if not project and not episode and not sequence and not shot and not dept : 
		shotInfo = pipelineTools.info()

		if shotInfo : 
			project = shotInfo['projectName']
			episode = shotInfo['episodeName']
			sequence = shotInfo['sequenceName']
			shot = shotInfo['shotName']
			dept = shotInfo['step']
			drive = shotInfo['drive']
			fileName = shotInfo['basename']

	if project and episode and sequence and shot and dept : 
		if not drive : 
			drive = 'P:'

		projectCode = sceneInfo.getCode('project', project)
		episodeCode = sceneInfo.getCode('episode', episode)

		info = {'drive': drive, 'fileName': fileName, 'project': project, 
				'episode': episode, 'sequence': sequence, 'shot': shot, 
				'department': dept, 'projectCode': projectCode, 'episodeCode': episodeCode
				}

		return info


def cachePathInfo(increment = True, project = '', episode = '', sequence = '', shot = '', dept = '') : 

	info = getSceneInfo(project , episode, sequence, shot, dept)

	if info : 
		drive = info['drive']
		project = info['project']
		episode = info['episode']
		sequence = info['sequence']
		shot = info['shot']
		dept = info['department']
		basename = info['fileName']
		projectCode = info['projectCode']
		episodeCode = info['episodeCode']
		dataName = '%s_%s_%s_%s_list' % (projectCode, episodeCode, sequence, shot)
		nonCacheFile = '%s_%s_%s_%s_nonCache' % (projectCode, episodeCode, sequence, shot)
		cameraName = '%s_%s_%s_%s_cam' % (projectCode, episodeCode, sequence, shot)
		cameraInfo = '%s_%s_%s_%s_camInfo.yml' % (projectCode, episodeCode, sequence, shot)
		fileName = '%s_%s_%s_%s_cacheInfo.yml' % (projectCode, episodeCode, sequence, shot)
		timeLog = '%s_%s_timelog.yml' % (projectCode, episodeCode)
		assetLog = '%s_%s_assetlog.yml' % (projectCode, episodeCode)
		shotCameraName = '%s_cam' % (shot)
		dept = exportDept

		if exportDept == dept : 
			cachePath = '%s/%s/film/%s/%s/%s/%s/cache/alembic' % (drive, project, episode, sequence, shot, dept)
			cacheInfoPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s' % (drive, project, episode, sequence, shot, dept, fileName)
			cacheDir = '%s/%s/film/%s/%s/%s/%s/cache' % (drive, project, episode, sequence, shot, dept)
			animCurvePath = '%s/%s/film/%s/%s/%s/%s/cache/animCurve' % (drive, project, episode, sequence, shot, dept)
			dataPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s.yml' % (drive, project, episode, sequence, shot, dept, dataName)
			nonCacheDataPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s.yml' % (drive, project, episode, sequence, shot, dept, nonCacheFile)
			nonCachePath = '%s/%s/film/%s/%s/%s/%s/cache/nonCache' % (drive, project, episode, sequence, shot, dept)
			cameraPath = '%s/%s/film/%s/%s/%s/%s/cache/camera/%s.ma' % (drive, project, episode, sequence, shot, dept, cameraName)
			cameraInfoPath = '%s/%s/film/%s/%s/%s/%s/cache/data/%s' % (drive, project, episode, sequence, shot, dept, cameraInfo)
			timeLogPath = '%s/%s/film/%s/edl/cache/timeLog/%s' % (drive, project, episode, timeLog)
			assetLogPath = '%s/%s/film/%s/edl/cache/assetLog/%s' % (drive, project, episode, assetLog)
			assetDataPath = '%s/%s/film/%s/%s/%s/%s/cache/assetData' % (drive, project, episode, sequence, shot, dept)

			# list version 
			version = findVersion(cachePath, increment)
			exportPath = '%s/%s' % (cachePath, version)
			exportAnimCurvePath = '%s/%s' % (animCurvePath, version)
			
			return {'cachePath': cachePath, 'exportPath': exportPath, 'cacheInfoPath': cacheInfoPath, 'dataPath': dataPath, 
					'nonCachePath': nonCachePath, 'nonCacheDataPath': nonCacheDataPath, 'cacheDir': cacheDir, 
					'cameraPath': cameraPath, 'cameraInfoPath': cameraInfoPath, 'cameraName': cameraName, 'shotCameraName': shotCameraName,
					'timeLogPath': timeLogPath, 'assetLogPath': assetLogPath, 'exportAnimCurvePath': exportAnimCurvePath, 
					'assetDataPath': assetDataPath}


def findVersion(cachePath, increment) : 
	dirs = fileUtils.listFolder(cachePath)
	versions = []

	for eachDir in dirs : 
		if eachDir[0] == 'v' and eachDir[1:].isdigit() : 
			intVersion = int(eachDir.replace('v', ''))
			versions.append(intVersion)


	if versions : 
		maxVersion = sorted(versions)[-1]
		nextVersion = maxVersion 

		if increment : 
			nextVersion = maxVersion + 1 
			
		strVersion = 'v%03d' % nextVersion

	else : 
		strVersion = 'v001'

	return strVersion