import sys
import time

"""
- Position the Cursor:
  \033[<L>;<C>H
     Or
  \033[<L>;<C>f
  puts the cursor at line L and column C.
- Move the cursor up N lines:
  \033[<N>A
- Move the cursor down N lines:
  \033[<N>B
- Move the cursor forward N columns:
  \033[<N>C
- Move the cursor backward N columns:
  \033[<N>D
- Clear the screen, move to (0,0):
  \033[2J
- Erase to end of line:
  \033[K
- Save cursor position:
  \033[s
- Restore cursor position:
  \033[u
  """
if __name__ == '__main__':
    sys.stdout.write('\033[4A')
    sys.stdout.write('\033[s')
    print('\033[0;0f')
    for x in range(3):
        for y in range(3):
            z = x * 3 + y + 1
            print(f'\033[0;0f\033[K|{z:>3}|', end='\r', flush=True)
            time.sleep(0.5)
    print('jkhfjfhgvhjhgfdvhgrshgrjyt jkgkjhgkjbkjgyu ukfk fkytkf fuyfkuyf fkuy')
    time.sleep(1)
    print('\033[F ', end='')
    time.sleep(1)
    print('\033[K ', end='')
    time.sleep(1)
    print('Hello ')
    time.sleep(1)
    print('Hii')
    time.sleep(1)
    print('\033[2J')
    print('\033[0;0f')
    print('\033[0;0H')
    # \033[K - Clear to end of line
    # \033[F - One line Above
    sys.stdout.write('\033[u')
    print('Program ends,,,')
