import datetime


class Time:
    def __init__(self, t1, t2=datetime.datetime.now()):
        self.moment = abs(round((t2 - t1).total_seconds()))
        self.result = None
        self.count()

    def count(self):
        if self.moment < 60:
            s = self.moment
            if int(str(s)[-1]) == 1:
                s = "1 секунду"
            elif int(str(s)[-1]) in [2, 3, 4]:
                s = f"{s} секунды"
            else:
                s = f"{s} секунд"
            self.result = f"{s}"
        elif 3600 > self.moment >= 60:
            m = round(self.moment / 60)
            if int(str(m)[-1]) == 1:
                m = "1 минуту"
            elif int(str(m)[-1]) in [2, 3, 4]:
                m = f"{m} минуты"
            else:
                m = f"{m} минут"
            self.result = f"{m}"
        elif 86400 > self.moment >= 3600:
            h = round(self.moment / (60 * 60))
            if int(str(h)[-1]) == 1:
                h = "1 час"
            elif int(str(h)[-1]) in [2, 3, 4]:
                h = f"{h} часа"
            else:
                h = f"{h} часов"
            self.result = f"{h}"
        else:
            d = round(self.moment / (60 * 60 * 24))
            if int(str(d)[-1]) == 1:
                d = "1 день"
            elif int(str(d)[-1]) in [2, 3, 4]:
                d = f"{d} дня"
            else:
                d = f"{d} дней"
            self.result = f"{d}"

    def __str__(self):
        return self.result