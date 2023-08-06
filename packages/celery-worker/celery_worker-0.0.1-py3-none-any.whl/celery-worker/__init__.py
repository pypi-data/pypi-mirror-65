from celery import Celery


class CeleryWorker(object):
    def __init__(self, name, broker, backend, conf):
        self.__instance = Celery(
            name,
            broker=broker,
            backend=backend
        )
        self.__instance.conf.update(conf)

    def register(self, task):
        self.__instance.tasks.register(task)

    def start(self):
        self.__instance.start(argv=['celery', 'worker', '--beat', '--concurrency', '4', '-l', 'info'])

    def purge(self):
        self.__instance.start(argv=['celery', 'purge', '-f'])

    def publish(self, task, message):
        self.__instance.send_task(task, [message])
