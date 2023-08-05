import asyncio, logging
from . import inotify

log = logging.getLogger(__name__)


def watch_inotify(fd: inotify.Inotify) -> asyncio.Queue:
    """Asynchronously watch the given Inotify pushing events to returned queue
    
    notify = inotify.Inotify()
    notify.add_watch(...)
    queue = watch_inotify(notify)
    while True:
        evt = await queue.get()
        if process(evt):
            notify.close()
            break
    """
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def on_ready():
        if fd.closed:
            loop.remove_reader(fd)
            return
        for evt in fd.get_events(block=False):
            queue.put_nowait(evt)

    asyncio.get_event_loop().add_reader(fd, on_ready)
    return queue
