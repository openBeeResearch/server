#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import subprocess
from subprocess import check_output
import json
import datetime
from dateutil.relativedelta import relativedelta

import time

# Lectura del fitxer "lastminute" que indica quin va ser l'últim minut llegit, si no el troba
# o considera que està corrupte crea una referencia nova amb el minut actual.
while True:

	last = 'http://161.116.80.31:5984/urbanbees_source/_design/alldata/_view/alldata?limit=1&descending=true'
	output = check_output(['curl', '-X', 'GET', last])
	lastdata = json.loads(output)
	lasttime = lastdata['rows'][0]['value']['time']
	lastday = (lasttime.split(' ')[0]).split('-')
	lastminute = ((lasttime.split(' ')[1]).split('.')[0]).split(':')
	last_datetime = datetime.datetime(int(lastday[0]), int(lastday[1]), int(lastday[2]), int(lastminute[0]), int(lastminute[1]), int(lastminute[2]) )
	aux_last_datetime = last_datetime - relativedelta(minutes=5)
	datetime_isoformat = aux_last_datetime.isoformat()
	day = datetime_isoformat.split('T')[0]
	minute = (datetime_isoformat.split('T')[1]).split('.')[0]
	lastkey = day + '%20' + minute 

	if os.path.isfile("lastminute"):
	
		aux = open("lastminute", "rb")
		lastminute = aux.readline()
	
		#print lastminute
	
		aux.close()
	
		d = lastminute.split('%20')

		if  (len(d) == 2) & (len(d[0]) == 10):
			startkey = lastminute
		else: 
			actual_minute = datetime.datetime.now().isoformat()
			day = actual_minute.split('T')[0]
			minute = (actual_minute.split('T')[1]).split('.')[0]
			startkey = day + '%20' + minute 
		
	else: 
		actual_minute = datetime.datetime.now().isoformat()
	
		day = actual_minute.split('T')[0]
		minute = (actual_minute.split('T')[1]).split('.')[0]
	
		startkey = day + '%20' + minute 

	print startkey
	print lastkey
	print (startkey < lastkey)
	if (startkey < lastkey):
		#Iteració pel següent minut: 
		day = (startkey.split('%20')[0]).split('-')
		minute = (startkey.split('%20')[1]).split(':')

		startkey_datetime = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(minute[0]), int(minute[1]), int(minute[2]) )

		# Amb el format datetime es pot sumar facilment els dos minuts:
		endkey_datetime = startkey_datetime + relativedelta(minutes=2)
		endkey_isoformat = endkey_datetime.isoformat()
		day = endkey_isoformat.split('T')[0]
		minute = (endkey_isoformat.split('T')[1]).split('.')[0]
		endkey = day + '%20' + minute 


		#Extracció de dos dominuts sencers: 
		extract_dir = 'http://161.116.80.31:5984/urbanbees_source/_design/alldata/_view/alldata?startkey="'

		#print startkey, endkey

		#Treure salt de linia
		startkey_f = startkey.split('\n')[0]
		extract_dir += startkey_f + '"&endkey="' + endkey + '"'

		print extract_dir

		#extract_dir = 'http://161.116.80.31:5984/urbanbees_source/_design/alldata/_view/alldata?startkey="2014-10-24%2013:21:00"&endkey="2014-10-24%2013:22:00"&limit=5'

		output = check_output(['curl', '-X', 'GET', extract_dir])

		#print output

		decoded_data = json.loads(output)
		print len(decoded_data['rows'])
		if (len(decoded_data['rows']) > 0):
			#print decoded_data

			humidity_ext = 0
			humidity_int = 0
			temperature_ext = 0
			temperature_int = 0
			weight = 0

			gates_in = []
			for i in range(25):
			  gates_in.append(0)

			gates_out = []
			for i in range(25):
			  gates_out.append(0)

			i = 0
			for i in range(len(decoded_data['rows'])): 
				humidity_ext += decoded_data['rows'][i]['value']['humidity_ext']
				humidity_int += decoded_data['rows'][i]['value']['humidity_int']
				temperature_ext += decoded_data['rows'][i]['value']['temperature_ext']
				temperature_int += decoded_data['rows'][i]['value']['temperature_int']
				weight += decoded_data['rows'][i]['value']['weight']
				j = 0
				for j in range(25): 
					gates_in[j] += float(decoded_data['rows'][i]['value']['gates'][str(j)]['in'])
				j = 0
				for j in range(25): 
					gates_out[j] += float(decoded_data['rows'][i]['value']['gates'][str(j)]['out'])	

			N = len(decoded_data['rows'])

			dt = startkey_f
			auxd = (dt.split('%20')[0])
			auxt = (dt.split('%20')[1])
			dt = auxd + ' ' + auxt
			#gates
			num_gate = 0
			colnum = 0
			g='{"time": "'+dt+'", "gates": {'
			for numgate in range(25):

				if (numgate < (25-1)):
					g+='"'+str(numgate)+'": {'+' "in": "'+str(float(gates_in[numgate])/ N)+'", "out": "'+str(float(gates_out[numgate])/ N)+'"}, '
				if (numgate == (25-1)):
					g+='"'+str(numgate)+'": {'+' "in": "'+str(float(gates_in[numgate])/ N)+'", "out": "'+str(float(gates_out[numgate])/ N)+'"} '
				numgate += 1

			#Otro parche porque cuando no entra en el if de si el fichero esta vacio se 		    #queja de que num_rows es 0
			g+='},'

			g_mean_in = 0
			g_mean_out = 0
			for i in range(25):
				if (i!=16 and i!=17 and i!=18 and i!=19 and i!=23):
					g_mean_in += float(gates_in[i])/N
					g_mean_out += float(gates_out[i])/N

			g+='"gate_mean_in":'+ str(g_mean_in/20) +','
			g+='"gate_mean_out":'+ str(g_mean_out/20) +','


			#Otro parche porque cuando no entra en el if de si el fichero esta vacio se 		    #queja de que num_rows es 0
			#weight 822 punto de la noche de 26 julio
			g+='"weight": '
			g+=str(weight/N)
			g+=', '
			#exterior humidity
			g+='"humidity_ext": '
			g+=str(humidity_ext/N)
			g+=', '
			#interior humidity
			g+='"humidity_int": '
			g+=str(humidity_int/N)
			g+=', '
			#exterior temperature 
			g+='"temperature_ext": '
			g+=str(temperature_ext/N)
			g+=', '
			#interior temperature
			g+='"temperature_int": '
			g+=str(temperature_int/N)
			g+='}'

			#Se pide una id para el objeto json que se va a introducir
			output = check_output(['curl', '-X', 'GET', 'http://161.116.80.31:5984/_uuids'])
			decoded_data = json.loads(output)
			data = decoded_data['uuids']
			string = 'http://161.116.80.31:5984/urbanbees_source_cache/' + data[0]
			output = check_output(['curl', '-X', 'PUT', string,'-d',g])

			print(g)

		#Guardant l'ultim minut, (només sumem 1 ja que hem d'assegurar solapament)

		endkey_datetime = startkey_datetime + relativedelta(minutes=1)
		endkey_isoformat = endkey_datetime.isoformat()
		day = endkey_isoformat.split('T')[0]
		minute = (endkey_isoformat.split('T')[1]).split('.')[0]
		endkey = day + '%20' + minute 

		f = open("lastminute", "w")
		f.write(endkey)
		f.close()

	#time.sleep(600)

