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
