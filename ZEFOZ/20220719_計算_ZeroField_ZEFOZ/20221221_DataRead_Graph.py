import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
from PhysicalConstant_DB import PhysicalConstant_DB

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['xtick.major.size'] = 7
plt.rcParams['ytick.major.size'] = 7
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.style.use(["science", "nature"])

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

# for i in range(30):
#     text = "Magnetic Field:" + "\n" + str(MagneticField[i]) + "\n" + \
#            "Frequency:" + "\n" + str(Frequency[i]) + "\n" + \
#            "Levels:" + "\n" + str(Levels[i]) + "\n" + \
#            "Gradient:" + "\n" + str(Gradient[i]) + "\n" + \
#            "Gradient_INT:" + "\n" + str(Gradient_INT[i]) + "\n" + \
#            "Curvature:" + "\n" + str(Curvature[i]) + "\n" + \
#            "Curvature_INT:" + "\n" + str(Curvature_INT[i]) + "\n" + \
#            "f:" + "\n" + str(f[i]) + "\n" + \
#            "\n\n"
#     with open("magneticField_Result.txt", "a", encoding="utf_8") as file:
#         file.write(text)

MagneticField = MagneticField[:100]
Frequency = Frequency[:100]
Levels = Levels[:100]
Gradient = Gradient[:100]
Gradient_INT = Gradient_INT[:100]
Curvature = Curvature[:100]
Curvature_INT = Curvature_INT[:100]
f = f[:100]

MagneticField_INT = []
for m in MagneticField:
    MagneticField_INT.append(np.linalg.norm(m))
MagneticField_INT = np.array(MagneticField_INT)

# 図示
fig = plt.figure()
fig.patch.set_alpha(0)
# 1つ目の図
ax1 = fig.add_subplot(1, 1, 1)
ax1.patch.set_alpha(0)
ax1.set_xlabel(r'$\rm{Magnetic \, Field \, (mT)}$')
ax1.set_ylabel(r'$\rm{S_2 \, (GHz/mT^2)}$')
# ax1.set_xlabel(r'$\rm{Frequency (GHz)}$')
# ax1.set_ylabel(r'$\rm{Transition \, Strength (GHz/mT)}$')
ax1.set_xscale('linear')
ax1.set_yscale('log')
# プロット処理
ax1.scatter(MagneticField_INT * 1e+03, Curvature_INT * 1e-15)
# ax1.scatter(Frequency * 1e-09, f * 1e-12)
plt.show()
fig.savefig('test.png', bbox_inches="tight", pad_inches=0.05, dpi=300)

print("finished.")
