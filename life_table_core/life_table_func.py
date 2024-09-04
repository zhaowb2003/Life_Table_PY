import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy import optimize
from IPython.display import display


def life_table(optionIndex: int, JudgeIndext: int, numstr: int, save_path: str = "", save_request: bool = False):
    num = 30
    num = numstr
    numSave = numstr
    LifeTableXArray = []
    LifeTableX = 0
    while LifeTableX < numSave:
        LifeTableXArray.append(LifeTableX)
        LifeTableX = LifeTableX + 1
    LifeNum = []
    NxCount = []
    numi = 0
    while num > 0:
        numi = numi + 1
        rand = np.random.randint(1, 7, [num, 1])
        randarrays = rand.tolist()
        randarray = []
        for randarrays_item in randarrays:
            randarray += randarrays_item
        judgerandarray = []

        if optionIndex == 2:
            if numi <= JudgeIndext:
                JudgeIndex = 1
            elif numi <= JudgeIndext * 2 and numi > JudgeIndext:
                JudgeIndex = 3
            else:
                JudgeIndex = 5
        elif optionIndex == 0:

            if numi <= JudgeIndext:
                JudgeIndex = 5
            elif numi <= JudgeIndext * 2 and numi > JudgeIndext:
                judgeIndex = 3
            else:

                JudgeIndex = 2

        else:
            JudgeIndex = JudgeIndext

        for randarray_item in randarray:
            if randarray_item <= JudgeIndex:
                judgerandarray += [0]
            else:
                judgerandarray += [1]

        num1 = judgerandarray.count(1)
        LifeNum.append(num1)
        NxCount.append(num1)
        num = judgerandarray.count(1)
    NxCount.pop()
    lxArray = []
    for LifeNumItem in LifeNum:
        lx = LifeNumItem / LifeNum[0]
        lxArray.append(lx)
    dxArray = []
    for dxArrayI in range(0, len(LifeNum) - 1):
        dx = LifeNum[dxArrayI] - LifeNum[dxArrayI + 1]
        dxArray.append(dx)
    qxArray = []
    for qxArrayI in range(0, len(dxArray)):
        qx = dxArray[qxArrayI] / NxCount[qxArrayI]
        qxArray.append(qx)

    LxArray = []
    LxArrayForSum = []
    for LxArrayI in range(0, len(LifeNum) - 1):
        Lx = (LifeNum[LxArrayI] + LifeNum[LxArrayI + 1]) / 2
        LxArray.append(Lx)
        LxArrayForSum.append(Lx)
    LxArray.append(0)

    TxArray = []
    TxArrayForCount = []
    TxArrayI = 0
    while TxArrayI < len(LxArray):
        Tx = sum(LxArrayForSum)
        TxArray.append(Tx)
        TxArrayForCount.append(Tx)
        TxArrayI = TxArrayI + 1
        try:
            del LxArrayForSum[0]
        except:
            pass
    TxArrayForCount.pop()
    exArray = []
    for NxCountI in range(0, len(NxCount)):
        ex = TxArrayForCount[NxCountI] / NxCount[NxCountI]
        exArray.append(ex)

    LgLifeNum = []
    xget = LifeNum.pop()
    for LogLifeNumItem in LifeNum:
        LgLifeNumItem = math.log10(LogLifeNumItem)
        LgLifeNum.append(LgLifeNumItem)

    LifeTableXArray.clear()
    for LgLifeNumItem in range(0, len(LgLifeNum)):
        LifeTableXArray.append(LgLifeNumItem)

    plt.plot(LifeTableXArray, LgLifeNum, color='r', marker='*', linestyle='')

    list_tempX = np.array(LifeTableXArray)
    list_tempY = np.array(LgLifeNum)

    if optionIndex == 0:
        def func(x, a, b, c):
            return a * np.exp(-b * x) + c

        popt, pcov = optimize.curve_fit(func, list_tempX, list_tempY, bounds=(0, [3., 1., 0.5]))
        print(popt)
        x = np.arange(0.1, len(LifeTableXArray), 0.01)
        plt.plot(x, func(x, popt[0], popt[1], popt[2]), 'r-',
                 label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    elif optionIndex == 1:
        z = np.polyfit(list_tempX, list_tempY, 1)
        p = np.poly1d(z)
        plt.plot(list_tempX, p(list_tempX))
    elif optionIndex == 2:
        z = np.polyfit(list_tempX, list_tempY, 2)
        p = np.poly1d(z)
        plt.plot(list_tempX, p(list_tempX))
    plt.show()

    LifeNum.append(xget)
    dxArray.append(np.nan)
    qxArray.append(np.nan)
    exArray.append(np.nan)
    xnew = []
    xnew += LifeTableXArray
    xnewLastItem = xnew.pop()

    LifeTableXArray.append(xnewLastItem + 1)
    mydata = {
        "x": LifeTableXArray,
        "nx": LifeNum,
        "lx": lxArray,
        "dx": dxArray,
        "qx": qxArray,
        "Lx": LxArray,
        "Tx": TxArray,
        "ex": exArray
    }
    df = pd.DataFrame(mydata)
    if save_request:
        df.to_csv("output.csv", index=True, sep=',')
    if save_path != "":
        df.to_csv(save_path, index=True, sep=',')
    return df


if __name__ == '__main__':
    df = life_table(2, 2, 1000)
    display(df)
