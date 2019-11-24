import os, time, pathlib
from select import select

from taskmaster.utils import log

from taskmaster.server.dashboard import dashboard

logger = log.get_logger('buff_manager')


def buff_manager():
    logger.info('starting buff_manager')

    while 1:
        fds = list(dashboard.fds_buff.keys())
        if not len(fds):
            time.sleep(1)
            continue
        rfds=[]
        try:
            rfds, wfds, xfds = select(fds, [], [], 1)
        except OSError:
            logger.error('error occurred upon select fds')
            continue
        logger.info('found some fds: {0}'.format(rfds))
        for fd in rfds:
            logger.info('fd={0} ready to write in {1}'.format(fd, dashboard.fds_buff.get(fd)))
            data = os.read(fd, 1024)
            if not data:
                continue
            file = dashboard.fds_buff.get(fd)
            if isinstance(file, pathlib.Path):
                if not file.exists():
                    file.touch(exist_ok=True)
                file.write_text(data.decode('UTF-8'))
        time.sleep(1)


        # with open(file, os.O_CREAT | os.O_WRONLY | os.O_APPEND) as file:
        # 	file.write(data)
