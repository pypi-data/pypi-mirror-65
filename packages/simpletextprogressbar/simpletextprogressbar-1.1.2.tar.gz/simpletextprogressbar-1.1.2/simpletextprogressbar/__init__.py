# SimpleTextProgressBar by Inky V 1.1.2
#
# This code is licensed under GPL-3.0-only.
#   -You can modify this program
#   -You CANNOT distribute this as a closed-source software
#   -You NEED to redistribute this in the same license, If you
#   want to modify the code, or redistribute
# Outside this license:
#   -You DON'T need to credit me, but YOU CAN.
#   -You CANNOT delete this text!
#
#   To use this progressbar, just start it with set_progress_bar()
#   or print anything, and then change position with
#   change_position(position, size, [prefix]) function.
#
#   Unluckly, If you try to write a text and then change the
#   progress bar text, you will get the text mixed with the
#   progress bar, so... only do this after you're done changing :)
#
#   Hope It helped you :)


def set_progress_bar():
    print("", end='')


def change_position(position, size, prefix="", writeTheSameLineWhenFinished="false"):
    if position < size or position == size:
        if position / size == 0:
            print("", end="\r")
            if prefix != "":
                print(prefix+" ", end='')
            print("[0%]"+" [--------------------------------------------------]", end='')


        if position / size == 1:
            print("", end="\r")
            if prefix != "":
                 print(prefix + " ", end='')
            if writeTheSameLineWhenFinished == "true":
                print("[100%]"+" [##################################################]", end='')
            else:
                print("[100%]" + " [##################################################]")


        if 0 < position/size < 10/100:
            print("", end="\r")
            if prefix != "":
                print(prefix + " ", end='')
            print_range = ((position/size)*100)-1
            print_range_r = round(print_range/2)
            print_range_str = str(print_range)
            print("[" + print_range_str[:3] + "%]" + " [", end='')
            for x in range(print_range_r):
                print("#", end='')
            for x in range(50-print_range_r):
                print("-", end='')
            print("]", end='\r')
        if 9 / 100 < position / size < 1:
            print("", end="\r")
            if prefix != "":
                print(prefix + " ", end='')
            print_range = ((position / size) * 100) - 1
            print_range_r = round(print_range/2)
            print_range_str = str(print_range)
            print("[" + print_range_str[:2] + "%]" + "  [", end='')
            for x in range(print_range_r):
                print("#", end='')
            for x in range(50 - print_range_r):
                print("-", end='')
            print("]", end='')
    else:
        print("", end="\r")
        print("["+str(position)+"/"+str(size)+"]", end='')
