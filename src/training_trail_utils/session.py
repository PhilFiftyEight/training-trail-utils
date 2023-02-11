from dataclasses import dataclass, field

import pendulum

def defaultduration():
    return pendulum.duration()

def defaultdate():
    return pendulum.datetime(1900,1,1)

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
        datasList = self.datas.split(' ')
        
        date = [ int(data) for data in datasList.pop(0).split('-')]
        self.date = pendulum.local(*date)