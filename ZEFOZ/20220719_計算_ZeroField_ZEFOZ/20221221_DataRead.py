import numpy as np
from scipy.constants import pi
from PhysicalConstant_DB import PhysicalConstant_DB

loaded_array = np.load('test.npz')

MagneticField = loaded_array['MagneticField']
Frequency = loaded_array['Frequency']
Levels = loaded_array['Levels']
Gradient = loaded_array['Gradient']
Gradient_INT = loaded_array['Gradient_INT']
Curvature = loaded_array['Curvature']
Curvature_INT = loaded_array['Curvature_INT']
f = loaded_array['f']

# T2 = 1 / (26e-06 * Curvature_INT * PhysicalConstant_DB.hbar * 26e-06 * pi)

for i in range(100):
    text = "Magnetic Field:" + "\n" + str(MagneticField[i]) + "\n" + \
           "Frequency:" + "\n" + str(Frequency[i]) + "\n" + \
           "Levels:" + "\n" + str(Levels[i]) + "\n" + \
           "Gradient:" + "\n" + str(Gradient[i]) + "\n" + \
           "Gradient_INT:" + "\n" + str(Gradient_INT[i]) + "\n" + \
           "Curvature:" + "\n" + str(Curvature[i]) + "\n" + \
           "Curvature_INT:" + "\n" + str(Curvature_INT[i]) + "\n" + \
           "f:" + "\n" + str(f[i]) + "\n" + \
           "\n\n"
    with open("magneticField_Result.txt", "a", encoding="utf_8") as file:
        file.write(text)
