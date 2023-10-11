class Predictor:
    def __init__(self):
        pass

    def extrapolate_currency_rate(self, currency_data):  # На вход массив значений курса
        if len(currency_data)<2:
            raise ValueError("Lists of values cannot be less than 2 elements")
        for i in range(1, 7):
            length = len(currency_data)
            rate = currency_data[length - 1] / currency_data[length - 2]
            currency_data.append(currency_data[length - 1] * rate)
        return currency_data  # На выход массив с семью дополнительными значениями

    def exchange_rate(self, currency_data1, currency_data2,
                      date):  # На вход массивы курсов двух валют и номер требуемого дня в виде целого числа
        value1 = self.extrapolate_currency_rate(currency_data1)
        value2 = self.extrapolate_currency_rate(currency_data2)
        rate = value2[date - 1] / value1[date - 1]
        return rate  # На выход отношение второй валюты к первой в заданной дате

    # Пример использования
    # currency_data = [10.0, 20.0, 30.0, 40.0]  Курс первой валюты
    # currency_data2 = [20.0, 30.0, 40.0, 50.0]  Курс второй валюты
    # print(exchange_rate(currency_data, currency_data2, 5))  Курс обмена на условный пятый день
