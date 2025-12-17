from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True, frozen=True)
class Person:
    name: str
    gender: Literal['M', 'F', 'O']
    age: float
    email: str | None


user_details: list[tuple[str, Literal['M', 'F', 'O'], int, str]] = [
    ('Blake Quinn', 'F', 18, 'ebi@icotew.me'),
    ('Lenora Baker', 'F', 26, 'ep@zigceun.kz'),
    ('Hattie Garner', 'F', 14, 'dejegve@es.is'),
    ('Isabella Morales', 'F', 18, 'dema@rad.rw'),
    ('Corey Maxwell', 'F', 28, 'hupaksag@tuepi.mm'),
    ('Gregory Clayton', 'M', 27, 'wekaj@im.ki'),
    ('Brett Barrett', 'F', 22, 'enibos@lidmifgoj.la'),
    ('Rosie Hunt', 'F', 26, 'osbuflel@bi.zm'),
    ('Marian Klein', 'M', 25, 'tituf@zal.al'),
    ('Patrick Parsons', 'M', 22, 'fesak@ebsukel.eg'),
    ('Ophelia Briggs', 'F', 22, 'hilimpun@hulowi.sy'),
    ('Devin Gray', 'M', 19, 'dufrepec@azuosuzu.zw'),
    ('Elva Sherman', 'M', 28, 'ugpan@aveet.mm'),
    ('Jesse Welch', 'F', 16, 'dup@cupowu.sc'),
    ('Lillian Ryan', 'F', 22, 'kuape@mezjur.jm'),
    ('Ernest Daniel', 'M', 15, 'amieki@kifzem.net'),
    ('Willie Allison', 'M', 19, 'bilrotco@agipuv.ax'),
    ('Evelyn Cain', 'F', 27, 'upo@ulehew.se'),
    ('Mina Sutton', 'F', 14, 'en@lu.me'),
    ('Clara Potter', 'F', 25, 'gasid@mo.sj'),
    ('Nancy Greer', 'F', 26, 'lum@in.cx'),
    ('Jose Tran', 'M', 23, 'sehwinwam@ecu.kp'),
    ('Hulda Rowe', 'M', 19, 'wi@aki.mz'),
    ('Effie Francis', 'F', 28, 'zet@zolbu.rw'),
    ('Anne Phillips', 'F', 14, 'evi@deh.pm'),
    ('Chase Foster', 'M', 18, 'nif@gaud.lv'),
    ('Garrett Adkins', 'M', 17, 'geflede@ged.an'),
    ('Alexander Becker', 'M', 29, 'neig@nulasib.hm'),
    ('Lucas Erickson', 'M', 14, 'dektazutu@tibir.bm'),
    ('Lawrence Butler', 'M', 28, 'azmazrek@moukowa.hn'),
    ('Mabel Perkins', 'F', 18, 'fa@omakake.ss'),
    ('Lizzie Logan', 'F', 19, 'ahazasa@cof.kp'),
    ('Garrett Lucas', 'M', 19, 'balopwis@rusilim.iq'),
    ('Verna Wheeler', 'F', 20, 'tenonaz@oloir.bd'),
    ('Logan Hansen', 'M', 22, 'wif@feg.lb'),
    ('Ola Walsh', 'F', 24, 'naw@reac.zm'),
    ('Cory Green', 'F', 19, 'fa@amsoju.me'),
    ('Oscar Walker', 'M', 24, 'acizi@pazi.cg'),
    ('Ronald Boone', 'M', 17, 'leh@bir.gu'),
]


users = [Person(*x) for x in user_details]
