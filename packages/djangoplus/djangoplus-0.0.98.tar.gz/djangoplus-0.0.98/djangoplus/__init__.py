

count = 0


def next_number():
    global count
    if count > 1000:
        count = 0
    count=count + 1
    return count