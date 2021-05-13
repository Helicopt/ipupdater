import os.path as osp
import pygsheets
import socket
import uuid
import time


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def update():

    # authorization
    gc = pygsheets.authorize(service_file=osp.join(
        '/etc', 'upip', 'configs', 'auth.json'))

    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('ipaddr')

    # select the first sheet
    wks = sh[0]

    # get name, ip, mac
    name = socket.gethostname()
    ip = get_ip_address()
    mac = hex(uuid.getnode())

    # get record from cloud
    names = wks.get_col(1, include_tailing_empty=False)
    macs = wks.get_col(2, include_tailing_empty=False)
    ips = wks.get_col(3, include_tailing_empty=False)
    alias = wks.get_col(4, include_tailing_empty=False)

    # update: if mac in record, then update name and ip
    found = False
    for i in range(1, len(macs)):
        if macs[i] == mac:
            found = True
            if i >= len(ips) or ips[i] != ip:
                wks.update_value('C%d' % (i + 1), ip)
            if i >= len(names) or names[i] != name:
                wks.update_value('A%d' % (i + 1), name)
            break

    # update: if mac not in record but empty alias in record, then update name, mac and ip
    if not found:
        for i in range(1, len(alias)):
            if alias[i] == name and (i >= len(macs) or macs[i] == ''):
                found = True
                wks.update_value('A%d' % (i + 1), name)
                wks.update_value('B%d' % (i + 1), mac)
                wks.update_value('C%d' % (i + 1), ip)
                break

    # update: if nothing related in record, then append name, mac and ip
    if not found:
        i = max([len(o) for o in [names, macs, ips, alias]])
        wks.update_value('A%d' % (i + 1), name)
        wks.update_value('B%d' % (i + 1), mac)
        wks.update_value('C%d' % (i + 1), ip)

    return ip


if __name__ == '__main__':
    previous_ip = update()
    cnt = 0
    regular_cnt = 5

    while True:
        time.sleep(120)
        try:
            current_ip = get_ip_address()
            if current_ip != previous_ip or cnt + 1 == regular_cnt:
                previous_ip = update()
        except:
            cnt = regular_cnt - 2
        cnt = (cnt + 1) % regular_cnt
