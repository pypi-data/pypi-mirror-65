import os

from discomp import Pool

os.environ['DISCO_LOGIN_USER'] = os.environ.get('DISCO_EMAIL')
os.environ['DISCO_LOGIN_PASSWORD'] = os.environ.get('DISCO_PASSWORD')


def ten_cube(x):
    theCube = (x*10)**3
    print (theCube)
    return theCube


def run_the_job():
    # execute only if run as a script
    p = Pool()
    results = p.map(ten_cube, range(10))
    return results


if __name__ == "__main__":
    # execute only if run as a script
    print(run_the_job())
