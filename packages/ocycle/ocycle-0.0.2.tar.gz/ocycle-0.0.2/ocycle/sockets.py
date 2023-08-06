'''

# Server:
SR = 48000
FRAME_SIZE = 4800

server = BufferServer(41955, env={'sr': SR})
for d in generate_data(FRAME_SIZE):
    sio.write(d)

# Client:
DURATION = 1 # sec

client = BufferClient(
    41955, size=lambda s, env: env['sr'] * 2 * DURATION,
    clip=True)
for d in sio:
    assert d

'''

import time
from collections import deque
import socketio
import ocycle

INIT_EVENT = 'init'
DATA_EVENT = 'data'

class BufferServer:
    def __init__(self, port, host='localhost', secure=True, env=None):
        self.env = env
        self.sio = socketio.Server()
        self.sio.on('connect')(self.__connect)
        self.sio.connect(build_url(host, port, secure))

    def __connect(self, sid, env):
        self.sio.emit(INIT_EVENT, (
            self.env(sid, env) if callable(self.env) else self.env) or {},
            room=sid)

    def __call__(self, data, t0=None):
        self.sio.emit(DATA_EVENT, {'data': data, 't0': t0})


class BufferClient:
    buffer = None

    def __init__(self, port, host='localhost', secure=True,
                 callback=None, size=None, wait_pause=0.05,
                 timeout=5, **bufferkw):
        self.callback = callback
        self.timeout = timeout
        self.wait_pause = wait_pause
        self.bufferkw = bufferkw

        self.size = size
        self.chunks = deque()
        self.sio = socketio.Client()
        self.sio.on('connect')(self.__connect)
        self.sio.on('disconnect')(self.__disconnect)
        self.sio.on(INIT_EVENT)(self.__init)
        self.sio.on(DATA_EVENT)(self.__write_buffer)
        self.sio.connect(build_url(host, port, secure))

    def __connect(self, sid, env):
        print('connect', sid, env)

    def __disconnect(self, sid):
        print('disconnect', sid)

    def __init(self, env):
        if callable(self.size):
            self.size = self.size(self, env)
        self.buffer = ocycle.BufferEmit(
            self.__append, self.size, value=True, **self.bufferkw)

    def __write_buffer(self, d):
        self.buffer.write(d['data'], d['t0'])

    def __append(self, buff, t0):
        self.chunks.append((buff, t0))

    def __next__(self):
        # return the first msg in the queue
        return (
            wait_for_item(self.chunks, self.wait_pause, self.timeout)
            and self.chunks.popleft())




def build_url(host, port, secure=False, path=None):
    return 'http{}://{}{}{}'.format(
        's'*secure, host, maybefmt(port, ':{}'), maybefmt(path, '/{}'))

def maybefmt(v, fmt, *a, default='', **kw):
    return fmt.format(v, *a, **kw) if v else default

def wait_for_item(obj, wait, timeout):
    # wait for an item to be available
    t0 = time.time()
    while not obj:
        time.sleep(wait)
        if time.time() - t0 > timeout:
            raise StopIteration
    return True
