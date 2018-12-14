import json

def check_status(status):
    if len(status) > 4 or \
       status[3:4] == ' ':
        try:
            num = int(status[:4])
        except:
            return False
        else:
            return True
    return False
