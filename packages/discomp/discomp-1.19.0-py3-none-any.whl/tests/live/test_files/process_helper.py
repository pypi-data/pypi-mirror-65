from discomp import Process
import os


def add(a, b):
    return a + b


os.environ['DISCO_LOGIN_USER'] = os.environ.get('DISCO_EMAIL')
os.environ['DISCO_LOGIN_PASSWORD'] = os.environ.get('DISCO_PASSWORD')

if __name__ == '__main__':
    args = (3, 7)
    p1 = Process(
        name='abcdjob',
        target=add,
        args=args)
    p1.start()
    p1.join()
    print(p1.job_status)
