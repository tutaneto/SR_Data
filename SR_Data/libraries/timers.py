from threading import Timer

wtimer, wtimer_label, wtimer_cnt = 0, 0, 0

def show_working_timer(label):
    global wtimer_label
    wtimer_label = label
    wtimer_start()

def wtimer_start():
    global wtimer
    wtimer = Timer(0.5, wtimer_function)
    wtimer.start()

def wtimer_function():
    global wtimer_cnt
    wtimer_cnt += 1
    wtimer_label.value = str(wtimer_cnt)
    print(wtimer_cnt)
    wtimer_start()
