from pasqal.tests import Omega
import numpy as np
import matplotlib.pyplot as plt
import time 
from pulser import Pulse, Sequence, Register
from pulser_simulation import QutipEmulator
from pulser.devices import MockDevice, Chadoq2
from pulser.waveforms import InterpolatedWaveform, RampWaveform

# REGISTER

# An atom separation of 6μm gives a diagonal separation of ~8.9μm. 
# Below, we choose a Rabi frequency of Ω = 4 * 2pi rad/μs, which gives a blockade radius of ~10.5μm on Chadoq2. Hence, diagonally separated atoms are still blockaded, which we will need later on.
reg = Register({
  "q0": (-3, -3),
  "q1": (3, -3),
  "q2": (-3, 3),
  "q3": (3, 3),
  "q4": (3, 9),
  "q5": (-9, 3),
  "q6": (-3, -9),
  "q7": (9, -3),
  "q8": (3, 15),
  "q9": (-15, 3),
  "q10": (-3, -15),
  "q11": (15, -3),
})

reg.draw(blockade_radius=Chadoq2.rydberg_blockade_radius(4.0))

# BASIC PARAMETERS
# in units of rad/μs
Omega = 4
Delta = 3

# DEVICE & SEQUENCE
seq = Sequence(reg, MockDevice) # Using MockDevice since it has the rydberg_local() channel.

# CHANNELS
seq.declare_channel("ch0", "rydberg_local")
seq.declare_channel("ch1", "rydberg_local")
seq.declare_channel("ch2", "rydberg_local")
seq.declare_channel("ch3", "rydberg_local")
seq.declare_channel("ch4", "rydberg_local")
seq.declare_channel("ch5", "rydberg_local")
seq.declare_channel("ch6", "rydberg_local")
seq.declare_channel("ch7", "rydberg_local")
seq.declare_channel("ch8", "rydberg_local")
seq.declare_channel("ch9", "rydberg_local")
seq.declare_channel("ch10", "rydberg_local")
seq.declare_channel("ch11", "rydberg_local")

# PULSES
# We want to address all qubits locally, using the same Rabi frequency but different detunings. Hence, we only modify the detunings of each pulse and keep a constant Rabi amplitude, for simplicity. \
# Please note that we have not checked whether the specified time scale is sufficient for maintaining adiabaticity.

# First, we define the - in our specific example - five different detuning ramps needed. 
det1 = RampWaveform(250, 0, Delta)
pulse1 = Pulse.ConstantAmplitude(Omega, det1, 0)

det5 = RampWaveform(250, 0, 5 * Delta)
pulse5 = Pulse.ConstantAmplitude(Omega, det5, 0)

det6 = RampWaveform(250, 0, 6 * Delta)
pulse6 = Pulse.ConstantAmplitude(Omega, det6, 0)

det11 = RampWaveform(250, 0, 11 * Delta)
pulse11 = Pulse.ConstantAmplitude(Omega, det11, 0)

det13 = RampWaveform(250, 0, 13 * Delta)
pulse13 = Pulse.ConstantAmplitude(Omega, det13, 0)

# Adding pulses to channels - PLEASE SEE HANDWRITTEN EXAMPLE IN REPORT FOR EXPLANATIONS.
seq.target("q0", "ch0") 
seq.add(pulse13, "ch0")

seq.target("q1", "ch1") 
seq.add(pulse11, "ch1")

seq.target("q2", "ch2") 
seq.add(pulse11, "ch2")

seq.target("q3", "ch3") 
seq.add(pulse13, "ch3")

seq.target("q4", "ch4") 
seq.add(pulse6, "ch4")

seq.target("q5", "ch5") 
seq.add(pulse6, "ch5")

seq.target("q6", "ch6") 
seq.add(pulse6, "ch6")

seq.target("q7", "ch7") 
seq.add(pulse6, "ch7")

seq.target("q8", "ch8") 
seq.add(pulse1, "ch8")

seq.target("q9", "ch9") 
seq.add(pulse5, "ch9")

seq.target("q10", "ch10") 
seq.add(pulse5, "ch10")

seq.target("q11", "ch11") 
seq.add(pulse1, "ch11")


# Simulate & measure

simul = QutipEmulator.from_sequence(seq)
t0 = time.time()
results = simul.run()
t = t0 - time.time()
print(t)

final = results.get_final_state()
count_dict = results.sample_final_state()