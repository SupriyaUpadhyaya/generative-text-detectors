import numpy as np
import re
import string
from statistics import stdev, mean

# Sample data (replace with your actual data)
Mat = [
    ["This is a sample sentence.", "Another sentence here."],
    ["A third sentence.", "Yet another sentence."]
]

# Final Features
FractTO = np.arange(1, len(Mat)+1)
SPP = np.arange(1, len(Mat)+1)
for i in range(len(Mat)):
    SPP[i] = sum([1 for cell in Mat[i] for char in cell if char != ' '])

for i in range(len(Mat)):
    if SPP[i] == 0:
        SPP[i] = 1
V1 = SPP

ParLength = np.arange(1, len(Mat)+1)
for i in range(len(Mat)):
    ParLength[i] = sum([1 for cell in Mat[i] if cell != ''])
V2 = ParLength

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == ')'])
VPar = np.array([1 if val > 0 else 0 for val in FractTO])

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == '-'])
Vdash = np.array([1 if val > 0 else 0 for val in FractTO])
V4 = Vdash

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == ';'])
VSem = np.array([1 if val > 0 else 0 for val in FractTO])

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == ':'])
VCol = np.array([1 if val > 0 else 0 for val in FractTO])

VSemCol = np.array([1 if (VCol[i] + VSem[i]) > 0 else 0 for i in range(len(Mat))])
V5 = VSemCol

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == '?'])
VQuest = np.array([1 if val > 0 else 0 for val in FractTO])
V6 = VQuest

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char == "'"])
Vapos = np.array([1 if val > 0 else 0 for val in FractTO])
V7 = Vapos

SPP2 = np.arange(1, len(Mat)+1)
for i in range(len(Mat)):
    SPP2[i] = sum([1 for cell in Mat[i] for char in cell if char != ' '])

Sentence = [idx for idx, row in enumerate(Mat) if any(re.findall(r'\w', cell) for cell in row)]
for i in range(len(Mat)-2, -1, -1):
    for j in range(sum(SPP2)):
        if j < len(Sentence) and Sentence[j] > 300*i:
            Sentence[j] -= 300*i
Sentence2 = Sentence.copy()
for i in range(len(SPP2)-1, 0, -1):
    if i+1 < len(Sentence2) and Sentence[i+1] > Sentence[i]:
        Sentence2[i] = Sentence[i+1] - Sentence[i]
    else:
        Sentence2[i] = Sentence[i]

V8 = np.zeros(len(V5))
start_idx = 0
for i, val in enumerate(SPP2):
    end_idx = start_idx + val
    vals = Sentence2[start_idx:end_idx]
    std_dev = stdev(vals) if len(vals) > 1 else 0
    V8[i] = std_dev
    start_idx = end_idx

Sentence3 = Sentence2.copy()
for i in range(len(SPP2)-1):
    Sentence3[i] = Sentence2[i+1] - Sentence2[i]
Sentence3[-1] = Sentence2[-1] - Sentence2[-2]

V9 = np.zeros(len(V5))
start_idx = 0
for i, val in enumerate(SPP2):
    end_idx = start_idx + val
    vals = Sentence3[start_idx:end_idx]
    std_dev = mean([abs(val) for val in vals]) if len(vals) > 1 else 0
    V9[i] = std_dev
    start_idx = end_idx

V10 = V7.copy()
start_idx = 0
for i, val in enumerate(SPP2):
    end_idx = start_idx + val
    vals = Sentence2[start_idx:end_idx]
    result = 0 if any(val < 11 for val in vals) else 1
    V10[i] = result
    start_idx = end_idx

V11 = V7.copy()
start_idx = 0
for i, val in enumerate(SPP2):
    end_idx = start_idx + val
    vals = Sentence2[start_idx:end_idx]
    result = 0 if any(val > 34 for val in vals) else 1
    V11[i] = result
    start_idx = end_idx

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = len(re.findall(r'(?i)although', ''.join(Mat[i])))
VAlth = np.array([1 if val > 0 else 0 for val in FractTO])
V12 = VAlth

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] for char in cell if char.lower() == 'h' and cell.lower()[:7] == 'however'])
VHow = np.array([1 if val > 0 else 0 for val in FractTO])
V13 = VHow

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = len(re.findall(r'(?i)but', ''.join(Mat[i])))
VBut = np.array([1 if val > 0 else 0 for val in FractTO])
V14 = VBut

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = len(re.findall(r'(?i)because', ''.join(Mat[i])))
VBec = np.array([1 if val > 0 else 0 for val in FractTO])
V15 = VBec

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = len(re.findall(r'(?i)this', ''.join(Mat[i])))
Vthis = np.array([1 if val > 0 else 0 for val in FractTO])
V16 = Vthis

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = 1 if any(re.findall(r'(?i)hers', cell) for cell in Mat[i]) else 0
Vhers = FractTO
V17 = Vhers

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = 1 if any(char.isdigit() for cell in Mat[i] for char in cell) else 0
VNums = FractTO
V18 = VNums

for i in range(len(Mat)):
    FractTO[i] = sum([1 for cell in Mat[i] if any(char.isupper() for char in cell)])
    FractTO[i] /= SPP[i]
V19 = np.array([1 if val > 2 else 0 for val in FractTO])

FractTO = np.zeros(len(Mat))
for i in range(len(Mat)):
    FractTO[i] = len(re.findall(r'\b(et)\b', ''.join(Mat[i]), re.IGNORECASE))
Vet = np.array([1 if val > 0 else 0 for val in FractTO])
V20 = Vet

# Example usage
print("V1:", V1)
print("V2:", V2)
print("V3:", VPar)
print("V4:", V4)
print("V5:", V5)
print("V6:", V6)
print("V7:", V7)
print("V8:", V8)
print("V9:", V9)
print("V10:", V10)
print("V11:", V11)
print("V12:", V12)
print("V13:", V13)
print("V14:", V14)
print("V15:", V15)
print("V16:", V16)
print("V17:", V17)
print("V18:", V18)
print("V19:", V19)
print("V20:", V20)
