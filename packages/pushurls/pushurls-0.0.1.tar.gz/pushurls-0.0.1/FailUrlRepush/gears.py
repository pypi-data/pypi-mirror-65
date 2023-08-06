import os

import redis


def printer(msg, length_ctrl=True, fill_with='-', alignment='l', msg_head_tail=None, print_out=True, reflash=False):
    try:
        length = os.get_terminal_size().columns
    except:
        length = 150
    al = {'l': '<', 'r': '>', 'm': '^'}.get(alignment)
    if not msg_head_tail:
        msg_head_tail = [' >>> ', '']
    if isinstance(msg_head_tail, str):
        msg_head_tail = [msg_head_tail, '']
    elif not isinstance(msg_head_tail, list):
        try:
            msg_head_tail = list(msg_head_tail)
        except:
            pass
    msg_head_tail = [' {} '.format(x) if x else '' for x in msg_head_tail]
    if not isinstance(msg, str):
        msg = str(msg)
    if length_ctrl:
        if isinstance(length_ctrl, int) and length_ctrl > 1:
            length = length_ctrl
        if len(msg) > length:
            msg = f" {msg[:(length - 10)]} ..."
        else:
            msg = f" {msg} "
    msg = msg_head_tail[0] + msg + msg_head_tail[1]
    msg = ("{:%s%s%s}" % (fill_with, al, length)).format(msg)
    if print_out:
        if not reflash:
            print(msg)
        else:
            print(f"{msg}\r", end='')
    else:
        return msg


def redis_cli(host, port, db):
    redis_client = redis.Redis(host=host,
                               port=port,
                               # password=123,
                               db=db)
    return redis_client
