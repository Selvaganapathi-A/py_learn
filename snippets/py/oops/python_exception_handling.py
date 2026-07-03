import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s')
    try:
        print(input(67))
        print(1 / 0)
    except KeyboardInterrupt as ke:
        raise ZeroDivisionError('Cannot Divde zero wuth zero') from ke
    except Exception as e:
        logging.exception(e)
    else:
        print('- else block -')
    finally:
        print('Any ways')
    print('-' * 80)
