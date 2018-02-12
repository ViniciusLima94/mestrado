# Neuron cell (FS)
from neuron import h
import matplotlib.pyplot as plt
import numpy as np

h.celsius = 36
h.load_file('stdrun.hoc')
	
def simulate(I = 0.8, curr = True, noise = False):

	soma = h.Section(name = 'soma')
	soma.L = soma.diam = 67
	soma.nseg = 1
	soma.Ra = 100
	soma.cm = 1

	soma.insert('pas')
	soma.e_pas = -70
	soma.g_pas = 0.00015

	soma.insert('hh2')
	soma.ek  = -100
	soma.ena = 50
	soma.gnabar_hh2 = 0.05
	soma.gkbar_hh2 = 0.01
	soma.vtraub_hh2 = -55

	apc = h.APCount(soma(0.5))

	if noise == True:
		fl = h.Gfluct2(soma(0.5))
		fl.std_e = 0.012
		fl.std_i = 0.0264	

	h.v_init = -70

	if curr == True:
		stim = h.IClamp(soma(0.5))
		stim.delay = 300
		stim.dur = 400
		stim.amp = I

	t_vec = h.Vector()
	v_vec = h.Vector()
	t_vec.record(h._ref_t)
	v_vec.record(soma(0.5)._ref_v)


	h.tstop = 1000
	h.run()

	return apc.n, t_vec, v_vec
	

count, t_vec, v_vec = simulate()
plt.figure('FStrace')
plt.plot(t_vec, v_vec)
plt.ylabel('Potencial de Membrana [mV]')
plt.xlabel('Tempo [ms]')
#plt.savefig('FStrace.pdf', dpi = 600)


import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

I = np.linspace(0, 2, 30)
count = []
for amp in I:
	c, _, _  = simulate(I = amp)
	count.append(c / 100e-3)

plt.figure('FSfi')
plt.plot(I, count)
plt.ylabel('Frequência de disparos [Hz]')
plt.xlabel('Corrente injetada [nA]')
#plt.savefig('FSfi.pdf', dpi = 600)

_, t_vec, v_vec = simulate(I = 0.8, curr = False, noise = True)
plt.figure('FStracenoise')
plt.plot(t_vec, v_vec)
plt.ylabel('Potencial de Membrana [mV]')
plt.xlabel('Tempo [ms]')
#plt.savefig('FStracenoise.pdf', dpi = 600)