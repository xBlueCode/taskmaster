import os, time, pathlib
from select import select

from taskmaster.utils import log

from taskmaster.server.dashboard import dashboard

BUFF_SIZE = 1024
TIME_SLEEP = 1

log = log.get_logger('buff_manager')


def buff_manager():
    log.info('starting buff_manager')

    while 1:
        time.sleep(TIME_SLEEP)
        log.debug('checking fds')
        fds = list(dashboard.fds_buff.keys())
        if not len(fds):
            log.debug('empty fd list')
            continue
        rfds=[]
        try:
            rfds, wfds, xfds = select(fds, [], [])
        except OSError:
            log.error('error occurred upon select fds')
            continue
        log.info('found some fds: {0}'.format(rfds))
        for fd in rfds:
            log.info('fd={0} ready to write in {1}'.format(fd, dashboard.fds_buff.get(fd)))
            data = None
            try:
                data = os.read(fd, BUFF_SIZE)
            except OSError as err:
                log.error('Failed to read from fd={0}'.format(fd))
            if not data:
                if fd in dashboard.fds_zombie:
                    dashboard.fds_zombie.remove(fd)
                    os.close(fd)
                    dashboard.fds_buff.pop(fd)
                continue
            file = dashboard.fds_buff.get(fd)
            if isinstance(file, pathlib.Path):
                if not file.exists():
                    file.touch(exist_ok=True)
                file.write_text(data.decode('UTF-8'))


        # with open(file, os.O_CREAT | os.O_WRONLY | os.O_APPEND) as file:
        # 	file.write(data)
