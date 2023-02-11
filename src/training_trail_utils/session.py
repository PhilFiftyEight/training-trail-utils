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
        # example of self.datas : "2022-2-10 51:54 08:46 27:16 03:31 06:31 05:45"
        def extract_datas():
            datasList = self.datas.split(" ")
            for datas in datasList:
                yield [
                    int(data)
                    for data in (datas.split(":") if ":" in datas else datas.split("-"))
                ]

        datas = extract_datas()

        date = next(datas)
        self.date = pendulum.local(*date)

        duration = next(datas)
        try:
            hours, minutes, seconds = duration
        except ValueError:
            minutes, seconds = duration
            hours = 0
        self.duration = pendulum.duration(seconds=seconds, minutes=minutes, hours=hours)

        vma = next(datas)
        try:
            hours, minutes, seconds = vma
        except ValueError:
            minutes, seconds = vma
            hours = 0
        self.vma = pendulum.duration(seconds=seconds, minutes=minutes, hours=hours)

        anaerobie = next(datas)
        try:
            hours, minutes, seconds = anaerobie
        except ValueError:
            minutes, seconds = anaerobie
            hours = 0
        self.anaerobie = pendulum.duration(
            seconds=seconds, minutes=minutes, hours=hours
        )

        end_active = next(datas)
        try:
            hours, minutes, seconds = end_active
        except ValueError:
            minutes, seconds = end_active
            hours = 0
        self.end_active = pendulum.duration(
            seconds=seconds, minutes=minutes, hours=hours
        )

        end_fond = next(datas)
        try:
            hours, minutes, seconds = end_fond
        except ValueError:
            minutes, seconds = end_fond
            hours = 0
        self.end_fond = pendulum.duration(seconds=seconds, minutes=minutes, hours=hours)

        recup = next(datas)
        try:
            hours, minutes, seconds = recup
        except ValueError:
            minutes, seconds = recup
            hours = 0
        self.recup = pendulum.duration(seconds=seconds, minutes=minutes, hours=hours)
