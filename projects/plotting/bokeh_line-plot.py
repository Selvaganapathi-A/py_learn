from bokeh import command, layouts, plotting, resources


def main():
    x = (1, 2, 3, 4, 5, 6, 7, 8)
    y = (1, 2, 3, 4, 5, 3, 0, 7)
    p = plotting.figure(title='hello', x_axis_label='x', y_axis_label='y')
    p.line(x, y)
    plotting.save(p, 'output.html', resources.INLINE, 'Hello')


if __name__ == '__main__':
    main()
