"""
This progam creates an interactive number of stars
"""
#your code here
def draw_stars(rows, increasing=True):
    for i in range(1, rows+1):
        print('*' * i)

if __name__ == '__main__':
    str = input('How many rows of stars should I print? ')
    draw_stars(int(str))
