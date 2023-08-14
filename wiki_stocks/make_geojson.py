import json
#input
all_properties = json.load(open('/home/shawnmonk/monk/qgis/volusia-addresses/parcel.geojson'))
shell = json.load(open('/home/shawnmonk/monk/qgis/volusia-addresses/shell.geojson'))
parcel_ids = open('/home/shawnmonk/monk/qgis/volusia-addresses/vacant_parcelids.txt').read().split('\n')


for v in all_properties['features']:
    # print(v['properties']['ALTKEY'])
    # break
    if(str(v['properties']['ALTKEY']) in parcel_ids):
        shell['features'].append(v)

#output
heavy = open('/home/shawnmonk/monk/qgis/volusia-addresses/vacant.geojson', 'w')
json.dump(shell, heavy)
