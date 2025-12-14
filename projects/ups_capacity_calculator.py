from dataclasses import dataclass
from typing import Any, Self


@dataclass(slots=True, frozen=True, kw_only=True)
class Appliance:
    name: str
    rating: int

    def __call__(self: Self, count: int, *args: Any, **kwds: Any) -> int:
        return count * self.rating


if __name__ == '__main__':
    MOBILE_CHARGER = Appliance(name='Mobile Charger', rating=7)
    WIFI_ROUTER = Appliance(name='Wifi Router', rating=10)
    SET_TOP_BOX = Appliance(name='Set top box', rating=30)
    TUBE_LIGHT = Appliance(name='Tube Light', rating=25)
    NIGHT_LIGHT = Appliance(name='Night Lamp', rating=1)
    FRIDGE = Appliance(name='Refridgerator', rating=400)
    MIXER = Appliance(name='Blender', rating=750)
    LED_TV = Appliance(name='LED TV', rating=90)
    TV = Appliance(name='TV', rating=100)
    MONITER = Appliance(name='Computer Moniter', rating=45)
    COMPUTER_LAPTOP = Appliance(name='Laptop Computer', rating=120)
    COMPUTER_DESKTOP = Appliance(name='Desktop Computer', rating=750)
    WALL_FAN = Appliance(name='Wall Fan', rating=60)
    TABLE_FAN = Appliance(name='Table Fan', rating=25)
    CEILING_FAN = Appliance(name='Ceiling Fan', rating=70)
    power_load: int = sum(
        (
            MOBILE_CHARGER(4),
            WIFI_ROUTER(1),
            WALL_FAN(2),
            TUBE_LIGHT(2),
            NIGHT_LIGHT(2),
            COMPUTER_LAPTOP(2),
            TABLE_FAN(2),
            # MIXER(1),
        )
    )
    power_factor: float = 0.7
    battery_backup_needed: float = 3  # in Hours
    inverter_capacity_needed: float = power_load / power_factor
    print(f'MAX LOAD Voltage : {power_load} Watts.')
    # print(inverter_capacity_needed)
    print(
        f'Inverter Needed : {((inverter_capacity_needed // 100) + 1) * 100} VA'
    )
    """
    backup_time = (battery_ah * battery_voltage * battery_efficiency) / ( power_load )
    """
    battery_ah = 150 + 150
    battery_voltage = 12
    battery_efficiency = 0.95
    backup_time = battery_ah * battery_voltage * battery_efficiency / power_load
    print(f'Backup Time : {backup_time} Hrs.')
