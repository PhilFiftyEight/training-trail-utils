from dataclasses import dataclass, field

import pendulum


def defaultduration():
    return pendulum.duration()


def defaultdate():
    return pendulum.datetime(1900, 1, 1)


@dataclass
class Session:
    datas: str
    date: pendulum.DateTime = field(default_factory=defaultdate)
    duration: pendulum.Duration = field(default_factory=defaultduration)
    vma: pendulum.Duration = field(default_factory=defaultduration)
    anaerobie: pendulum.Duration = field(default_factory=defaultduration)
    end_active: pendulum.Duration = field(default_factory=defaultduration)
    end_fond: pendulum.Duration = field(default_factory=defaultduration)
    recup: pendulum.Duration = field(default_factory=defaultduration)

    def __post_init__(self):
        # example of self.datas : "2022-2-10 01:51:54 08:46 27:16 03:31 01:06:31 05:45"
        def extract_datas():
            datasList = self.datas.split(" ")
            for datas in datasList:
                yield [
                    int(data)
                    for data in (datas.split(":") if ":" in datas else datas.split("-"))
                ]

        datas = extract_datas()

        self.date = pendulum.local(*next(datas))

        def make_params(datas):
            try:
                hours, minutes, seconds = datas
            except ValueError:
                minutes, seconds = datas
                hours = 0
            return dict(zip(("hours", "minutes", "seconds"), (hours, minutes, seconds)))

        for param in self.__dict__.keys():
            if param != "datas" and param != "date":
                self.__setattr__(param, pendulum.duration(**make_params(next(datas))))
