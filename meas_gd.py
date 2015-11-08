#!/usr/bin/env python

import visa
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_pdf import PdfPages

def main():
	
	waves = np.array(sys.argv[1:len(sys.argv)],dtype='|S4')
	wave_params = waves.astype(np.float)
	start, stop, steps = wave_params
	# start, stop, steps = float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])

	recman = visa.ResourceManager()
	SRS = recman.open_resource('GPIB1::08::INSTR') #lock-in amplifier
	LSR = recman.open_resource('GPIB1::29::INSTR') #Santec laser

	#initialize stuff
	LSR.write('SOUR:POW:UNIT mW')
	LSR.write('SOUR:POW %f' % 0.01)
	
	Ws = np.linspace(start,stop,steps)
	Ts,Rs = [],[]
	for w in Ws:
		LSR.write('SOUR:WAV %f' % w)
		Rs.append(SRS.query_ascii_values('OUTP?3'))
		Ts.append(SRS.query_ascii_values('OUTP?5'))

	f, axarr = plt.subplots(2, sharex=True)
	axarr[0].plot(Ws, Rs,color="blue",linewidth=2.5)
	axarr[0].set_title('Transmission')
	axarr[1].plot(Ws, Ts,color="red",linewidth=2.5)
	axarr[1].set_title('Phase')
	plt.ylabel('Phase (Degrees)')
	plt.xlabel('Wavelength (um)')

	filename='ave_10'
	pp = PdfPages(filename+'.pdf')
	pp.savefig(f)
	pp.close()
	Rs = [Rsf[0] for Rsf in Rs]
	Ts = [Tsf[0] for Tsf in Ts]
	data = np.array([Ws.tolist(), Rs, Ts])
	np.savetxt(filename+'.csv', data.T, delimiter=",")

	plt.show()

if __name__ == '__main__':
	main()

