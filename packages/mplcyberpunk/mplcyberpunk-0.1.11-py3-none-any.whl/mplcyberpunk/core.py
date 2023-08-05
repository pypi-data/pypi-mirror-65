# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def add_glow_effects(ax=None):
    """Add a glow effect to the lines in an axis object and an 'underglow' effect below the line."""
    make_lines_glow(ax=ax)
    add_underglow(ax=ax)


def make_lines_glow(ax=None, n_glow_lines=10, diff_linewidth=1.05, alpha_line=0.3):
    """Add a glow effect to the lines in an axis object.

    Each existing line is redrawn several times with increasing width and low alpha to create the glow effect.
    """
    if not ax:
        ax = plt.gca()

    lines = ax.get_lines()

    alpha_value = alpha_line / n_glow_lines

    for line in lines:

        data = line.get_data()
        linewidth = line.get_linewidth()

        for n in range(1, n_glow_lines + 1):
            glow_line, = ax.plot(*data)
            glow_line.update_from(line)  # line properties are copied as seen in this solution: https://stackoverflow.com/a/54688412/3240855

            glow_line.set_alpha(alpha_value)
            glow_line.set_linewidth(linewidth + (diff_linewidth * n))
            glow_line.is_glow_line = True  # mark the glow lines, to disregard them in the underglow function.


def add_underglow(ax=None, alpha_underglow=0.1):
    """Add an 'underglow' effect, i.e. faintly color the area below the line."""
    if not ax:
        ax = plt.gca()

    # because ax.fill_between changes axis limits, save current xy-limits to restore them later:
    xlims, ylims = ax.get_xlim(), ax.get_ylim()

    lines = ax.get_lines()

    for line in lines:

        # don't add underglow for glow effect lines:
        if hasattr(line, 'is_glow_line') and line.is_glow_line:
            continue

        x, y = line.get_data()
        color = line.get_c()

        ax.fill_between(x=x,
                        y1=y,
                        y2=[0] * len(y),
                        color=color,
                        alpha=alpha_underglow)

    ax.set(xlim=xlims, ylim=ylims)
