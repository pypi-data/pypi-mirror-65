import sys
import os


def pyprogress(iteration, total, prefix='', suffix='', decimals=0, length=100, fill='#'):

    """
    TODO: Simplify the progress bar and add:
        * eta waiting time
        * clearing screen
    """

    percent = f"{100 * (iteration / float(total))}"
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '>' + '-' * (length - filledLength)
    print(f"""{prefix} ||{bar}|| {percent}% {suffix}""")
