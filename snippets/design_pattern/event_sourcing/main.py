import shutil

from events import EventStore
from inventory import Inventory


def main():
    COLS, ROWS = shutil.get_terminal_size()
    #
    store: EventStore = EventStore()
    inventory: Inventory = Inventory(store)
    #
    inventory.add_item('sword')
    inventory.add_item('banana')
    inventory.add_item('shield')
    inventory.add_item('bow')
    inventory.add_item('arrow')
    inventory.remove_item('bow')
    inventory.add_item('arrow')
    #
    print(' Items in Inventory '.center(COLS, '='))
    for item, count in inventory.get_items():
        print(item, count)
    print('=' * COLS)
    #
    print('Arrows in Inventory', inventory.get_count('arrow'))
    print(' Event '.center(COLS, '='))
    for x in store.get_all_events():
        print(x.timestamp, x.data, x.event_type)
        # print(event_type, data, timestamp)
    print('=' * COLS)


if __name__ == '__main__':
    main()
