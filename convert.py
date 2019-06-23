import os, sys
from valve_keyvalues_python.keyvalues import KeyValues


def planeOrigin(zPos, zScaleMin):
	return str(float(zPos) + float(zScaleMin))

def planeCorners(**xyargs) -> tuple:
	#corners = ((,), (,), (,), (,))
	ret = [None, None, None, None]
	for i in xyargs:
		xyargs[i] = float(xyargs[i])

	# x is the same on p0 & p3
	ret[0] = [xyargs['x'] + xyargs['xmin'],None]
	ret[3] = [xyargs['x'] + xyargs['xmin'],None]
	# x is the sae with p1 & p2
	ret[1] = [xyargs['x'] + xyargs['xmax'], None]
	ret[2] = [xyargs['x'] + xyargs['xmax'], None]
	# y is the same with p0 & p1
	ret[0][1] = xyargs['y'] + xyargs['ymin']
	ret[1][1] = xyargs['y'] + xyargs['ymin']
	# y is the same with p2 & p3
	ret[2][1] = xyargs['y'] + xyargs['ymax']
	ret[3][1] = xyargs['y'] + xyargs['ymax']

	return ret

def boxHeight(zPos, zScaleMin, zScaleMax):
	_pos = float(zPos)
	_min = float(zScaleMin)
	_max = float(zScaleMax)
	top = _pos + _min
	bot = _pos + _max
	return str(abs(top - bot))
	
def convertFile(filename, zonename:str, zoneid:str, new:KeyValues, old:KeyValues):
	# zone title is hc'd right now test zones have weird names
	zone_title = os.path.splitext(os.path.basename(filename))[0]

	# base constrainst for each zone
	_xpos = old[zone_title][zonename]['xpos']
	_xmin = old[zone_title][zonename]['xScaleMins']
	_xmax = old[zone_title][zonename]['xScaleMaxs']

	_ypos = old[zone_title][zonename]['ypos']
	_ymin = old[zone_title][zonename]['yScaleMins']
	_ymax = old[zone_title][zonename]['yScaleMaxs']

	_zpos = old[zone_title][zonename]['zpos']
	_zmin = old[zone_title][zonename]['zScaleMins']
	_zmax = old[zone_title][zonename]['zScaleMaxs']

	# zone id
	new['tracks']['0'][zoneid] = KeyValues()
	new['tracks']['0'][zoneid]['zoneNum'] = zoneid

	 # trigger properties
	new['tracks']['0'][zoneid]['triggers'] = KeyValues()
	new['tracks']['0'][zoneid]['triggers']['1'] = KeyValues()
	new['tracks']['0'][zoneid]['triggers']['1']['zoneNum'] = zoneid
	if zoneid == '0' or zoneid == '1':
		new['tracks']['0'][zoneid]['triggers']['1']['type'] = zoneid
	# stages are type2 - checkpoints are type3
	else:
		new['tracks']['0'][zoneid]['triggers']['1']['type'] = '3'
		
	new['tracks']['0'][zoneid]['triggers']['1']['pointsZPos'] = planeOrigin(_zpos, _zmin)
	new['tracks']['0'][zoneid]['triggers']['1']['pointsHeight'] = boxHeight(_zpos, _zmin, _zmax)
	if zonename == 'start':
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps'] = KeyValues()
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps']['properties'] = KeyValues()
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps']['properties']['speed_limit'] = '350.0000' 
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps']['properties']['limiting_speed'] = '1' 
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps']['properties']['start_on_jump'] = '1' 
		new['tracks']['0'][zoneid]['triggers'][zoneid]['zoneProps']['properties']['speed_limit_type'] = '0' 




	# Corners of zon
	new['tracks']['0'][zoneid]['triggers']['1']['points'] = KeyValues()
	corners = planeCorners(
		x=_xpos, y=_ypos, z=_zpos,
		xmin=_xmin, ymin=_ymin, zmin=_zmin,
		xmax=_xmax, ymax=_ymax, zmax=_zmax
	)
	for i in range(4):
		new['tracks']['0'][zoneid]['triggers']['1']['points'][f'p{i}'] = f'{corners[i][0]} {corners[i][1]}'

def newKV():
	ret = KeyValues()
	ret['tracks'] = KeyValues()
	ret['tracks']['0'] = KeyValues()
	return ret

def walk_files(directory):
	for file_ in os.listdir(directory):
		try:
			new_kv = newKV()
			old_kv = KeyValues(filename=f'{directory}/{file_}')
			if file_.endswith(".zon"):
				convertFile(f'{directory}/{file_}', 'end', '0', new_kv, old_kv)
				convertFile(f'{directory}/{file_}', 'start', '1', new_kv, old_kv)
				new_kv.write(f'{directory}/{file_}')
				print(f"good {file_}")
		except Exception as e:
			print(f'failed {file_}\nError: {e}')

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('No target')
	else:
		walk_files(sys.argv[1])