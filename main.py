import pandas
import matplotlib.pyplot as plt
import numpy as np

def read_file():
    file_name = "wig20_d.csv"
    input_file = pandas.read_csv(file_name)
    return input_file['Najwyzszy'], input_file['Data']

def chart(macd, signal, samples, dates):
    plt.figure(figsize=(12, 8))
    ax1 = plt.subplot(212)
    plt.plot(dates, macd, label='MACD')
    plt.plot(dates, signal, label='SIGNAL', color='red')
    plt.xlabel('Dates', fontsize=12)
    plt.text(-120, 60, 'Values', va='center', rotation='vertical', fontsize=12)
    plt.xticks(np.arange(0, 1000, step=50), rotation=20)
    plt.yticks(list(range(-int(max(macd)) - 8, int(max(macd)) + 11, int(max(macd) / 5))))
    plt.legend(loc=4)

    ax2 = plt.subplot(211, sharex=ax1)
    plt.plot(dates, samples, label='WIG_20', color='green')
    plt.title('Trading indicator MACD', fontsize=14)
    plt.xticks(np.arange(0, 1000, step=50), rotation=20)
    plt.yticks(np.arange(1800, 2700, 100))
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=.07, right=.99, hspace=0.001)

    plt.legend(loc=1)
    plt.show()

def calculate_ema(samples, current_day, N):
    alfa = 2/(N+1)
    denominator = 0
    numerator = 0
    for i in range(N+1):
        denominator += (1-alfa)**i
        if current_day-1-i > 0:
            numerator += samples[current_day-1-i]*(1-alfa)**i
        else:
            numerator += samples[0]*(1-alfa)**i
    result = numerator/denominator
    return result

def calculate_macd(samples, current_day):
    ema_12 = calculate_ema(samples, current_day, 12)
    ema_26 = calculate_ema(samples, current_day, 26)
    macd = ema_12-ema_26
    return macd

def calculate_signal(samples, current_day):
    signal = calculate_ema(samples, current_day, 9)
    return signal

def trading_stocks(user_profile, samples, macd_array, signal_array):
    samples = list(samples)
    for i in range(len(samples)):
        if 0 < i <= len(samples):
            if (((macd_array[i-1] < signal_array[i-1] and macd_array[i] > signal_array[i])
                    or (i > 2 and macd_array[i-2] < signal_array[i-2] and macd_array[i-1] == signal_array[i-1] and macd_array[i] > signal_array[i]))
                    and user_profile['money'] > 0):
                buy = int(user_profile['money']/samples[i])
                user_profile['stock'] += buy
                user_profile['money'] -= buy*samples[i]
            elif (((macd_array[i-1] > signal_array[i-1] and macd_array[i] < signal_array[i])
                   or (i > 1 and macd_array[i-2] > signal_array[i-2] and macd_array[i-1] == signal_array[i-1] and macd_array[i] < signal_array[i]))
                   and user_profile['stock'] > 0):
                sell = user_profile['stock']*samples[i]
                user_profile['money'] += sell
                user_profile['stock'] = 0
    benefit = (user_profile['stock']*samples[-1]+user_profile['money'])/(1000*samples[0])
    return benefit


def main(N):
    samples, dates = read_file()
    macd_array = [calculate_macd(samples, i) for i in range(1, N+1)]
    signal_array = [calculate_signal(macd_array, i) for i in range(1, N+1)]
    user_account = {
        'money': 0,
        'stock': 1000,
    }
    print("Starting budget at first day: {}".format(user_account['stock'] * samples[0]))
    benefit = trading_stocks(user_account, samples, macd_array, signal_array)
    print("Final budget at last day: {}".format(user_account['stock'] * samples[N-1] + user_account['money']))
    print("Benefit: {}".format(benefit))
    chart(macd_array, signal_array, samples, dates)

if __name__ == '__main__':
    main(1000)

