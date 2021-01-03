"""
Monte-Carlo method based gear's contact strength reliability analysis
"""
import numpy as np
import matplotlib.pyplot as plt
import math


def calculate_C_S():
    """
    计算接触应力
    :return:按概率分布生成的接触应力值
    """
    Z_E = 190
    T_1 = np.random.normal(283.92, 5, 1)
    b = np.random.normal(35, 0.05, 1)
    d_e1 = 14 * np.random.normal(5.4, 0.05, 1)
    Z_I = np.random.normal(0.106803, 0.00019771, 1)
    K_A = np.random.uniform(1.25, 1.5, 1)
    K_V = np.random.normal(1.05, 0.01, 1)
    K_Hbeta = 1 + 5.6 * 10 ** (-6) * b ** 2
    Z_X = 0.00492 * b + 0.4375
    Z_XC = 1.5
    sigma_H = Z_E * math.sqrt(2000 * T_1 / (b * d_e1 ** 2 * Z_I) * K_A * K_V * K_Hbeta * Z_X * Z_XC)
    return sigma_H


def calculate_A_C_S():
    """
    计算许用接触应力
    :return:按概率分布生成的许用接触应力
    """
    sigma_Hlim = np.random.lognormal(7.1694, 0.0386, 1)
    Z_NT = np.random.normal(1.20445, 0.1, 1)
    Z_W = 1
    S_H = 1.1
    K_theta = 1
    Z_Z = 1
    sigma_HP = sigma_Hlim * Z_NT * Z_W / (S_H * K_theta * Z_Z)
    return sigma_HP


def XY_count():
    """
    Monte_Carlo采样计数
    :return:应力区间，接触应力计数值，许用接触应力计数值，可靠性计数值
    """
    count_size = 100000
    R_count = 0
    x = np.linspace(1000, 1700, 100)
    y_sigma_H = np.zeros(100)
    y_sigma_HP = np.zeros(100)
    for i in range(count_size):
        sigma_H = calculate_C_S()
        sigma_HP = calculate_A_C_S()
        if sigma_HP - sigma_H >= 0:
            R_count += 1
        for j in range(100):
            if (sigma_H >= 1000) and (sigma_H <= 1700) and (j + 1 <= 99):
                if (sigma_H >= x[j]) and (sigma_H <= x[j + 1]):
                    y_sigma_H[j] += 1
            if (sigma_HP >= 1000) and (sigma_HP <= 1700) and (j + 1 <= 99):
                if (sigma_HP >= x[j]) and (sigma_HP <= x[j + 1]):
                    y_sigma_HP[j] += 1
    return x, y_sigma_H, y_sigma_HP, R_count


def draw_fig():
    """
    绘制图像
    :return:
    """
    x, y_sigma_H, y_sigma_HP, R_count = XY_count()
    R = R_count / 100000
    print(R)
    y_p_sigma_H = np.zeros(100)
    y_p_sigma_HP = np.zeros(100)
    for i in range(100):
        y_p_sigma_H[i] = y_sigma_H[i] / 100000
        y_p_sigma_HP[i] = y_sigma_HP[i] / 100000
    fig = plt.figure(1, figsize=(10, 8))
    ax = fig.add_subplot(111)
    #ax.bar(x, height=y_sigma_H,width=0.1, color='blue', edgecolor='white', label='MC PDF')
    ax.plot(x, y_p_sigma_H, color="red", linewidth=1, marker="o", label='Contact Stress')
    ax.plot(x, y_p_sigma_HP, color="green", linewidth=1, marker="v", label="Allowable Contact Stress")
    ax.legend(loc='best', frameon=True)
    ax.set_xlabel("Stress Value / Mpa")
    ax.set_ylabel("Probability")
    ax.set_title("Monte Carlo Simulation")
    ax.grid(True)
    plt.show()

def main():
    # data_file = open("data.txt", "w")
    draw_fig()


if __name__ == '__main__':
    main()
