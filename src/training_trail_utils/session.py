import re
import pendulum
from dataclasses import dataclass, field

rdate = re.compile(r"\d{4}.\d{1,2}.\d{1,2}")
rdate_invalidseparator = re.compile(r"\d{4}[^-]\d{1,2}[^-]\d{1,2}")
rdate_invalidseparator2 = re.compile(r"\d{4}-\d{1,2}[^-]\d{1,2}")
rdate_invalidseparator3 = re.compile(r"\d{4}[^-]\d{1,2}-\d{1,2}")

datas_validation = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}(\s(\d{2})(:\d{2}){1,2}){6}$")


class InvalidStringError(Exception):
    def __init__(self, datas_string, *args):
        super().__init__(args)
        self.datas_string = re.split(" ", datas_string)

    def __str__(self):
        if self.datas_string == [""]:
            return "InvalidStringError: the datas_String is required for new Session"
        elif not re.match(rdate, self.datas_string[0]):
            return "InvalidStringError: date is required, format -> yyyy-mm-dd"
        elif (
            re.match(rdate_invalidseparator, self.datas_string[0])
            or re.match(rdate_invalidseparator2, self.datas_string[0])
            or re.match(rdate_invalidseparator3, self.datas_string[0])
        ):
            return f"InvalidStringError: invalid separator for date <{self.datas_string[0]}>, format -> yyyy-mm-dd"
        else:
            dataswithoutdate = self.datas_string[1:]
            for duration in dataswithoutdate:
                if ":" in duration or len(duration) < 3:
                    numberoftokens = len(duration.split(":"))
                    if numberoftokens < 2 or numberoftokens > 3:
                        msg = "less than 2" if numberoftokens < 2 else "more than 3"
                        return f"InvalidStringError: {msg} tokens for <{duration}>"
                else:
                    return f"InvalidStringError: invalid separator for duration <{duration}>, format -> Optionnal([0-9][0-9]:)[0-5][0-9]:[0-5][0-9]"
            duration_count = len(dataswithoutdate)
            if duration_count < 6 or duration_count > 6 :
                return (
                    f"InvalidStringError: 6 durations are required not {duration_count}"
                )
        return "InvalidStringError: Other reason, not tested"


def defaultduration():
    return pendulum.duration()


def defaultdate():
    return pendulum.datetime(1900, 1, 1)


@dataclass
class Session:
    datas: str = ""
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

        if not re.match(datas_validation, self.datas):
            raise InvalidStringError(self.datas)

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
