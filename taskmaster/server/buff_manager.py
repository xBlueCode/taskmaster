import os, time, pathlib
from select import select

from taskmaster.utils import log

from taskmaster.server.dashboard import dashboard

BUFF_SIZE = 1024
TIME_SLEEP = 1
DECODE_FORMAT = 'UTF-8'

log = log.get_logger('buff_manager')


def buff_manager():
    """\
    Buffer Manager is responsible for dispatching
    standard out/err flow of running processes by
    by selecting open fds which are ready to read from
    and transport the data to the appropriate files.
    """
    log.info('starting buff_manager')

    while 1:
        time.sleep(TIME_SLEEP)
        log.debug('checking fds')
        fds = list(dashboard.fds_buff.keys())
        if not len(fds):
            log.debug('empty fd list')
            continue
        rfds=[]
        try:  # select open fds which are ready to read from
            rfds, wfds, xfds = select(fds, [], [])
        except OSError:
            log.error('error occurred upon select fds')
            continue
        log.info('found some fds: {0}'.format(rfds))
        for fd in rfds: # transporting data from each open fd
            log.info('fd={0} ready to write in {1}'.format(fd, dashboard.fds_buff.get(fd)))
            data = None
            try:
                data = os.read(fd, BUFF_SIZE)
            except OSError as err:
                log.error('Failed to read from fd={0}'.format(fd))
            if not data:
                if fd in dashboard.fds_zombie:  # close and remove the fd if it's in zombie list
                    dashboard.fds_zombie.remove(fd)
                    os.close(fd)
                    dashboard.fds_buff.pop(fd)
                continue
            file = dashboard.fds_buff.get(fd)  # get the linked file from the dashboard
            if isinstance(file, pathlib.Path):
                if not file.exists():
                    file.touch(exist_ok=True)
                file.write_text(data.decode(DECODE_FORMAT))
