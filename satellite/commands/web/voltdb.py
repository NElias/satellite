from fabric.api import run, cd

from satellite import *


def install():
    with cd('/tmp'):
        file_name = 'voltdb_3.0-1_amd64.deb'
        run('wget http://voltdb.com/downloads/technologies/server/%s' % file_name)
        sudo('dpkg -i %s' % file_name)
        run('rm %s' % file_name)

def configure():
    run('voltdb compile --classpath="./"l -o %(db)s.jar %(db)s.sql' % {'db':settings.voltdb.name})

def run():
    run("""voltdb create \
          catalog %s.jar   \
          deployment deployment.xml   \
          host localhost""" % settings.voltdb.name)