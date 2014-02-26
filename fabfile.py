from fabric.api import *
# Default release is 'current'
env.release = 'current'

def production():
  """Production server settings"""
  env.settings = 'production'
  env.user = 'politicando'
  env.path = '/home/%(user)s/sites/politicando' % env
  env.hosts = ['politicando.org']

def setup():
  """
  Setup a fresh virtualenv and install everything we need so it's ready to deploy to
  """
  run('mkdir -p %(path)s; cd %(path)s; /usr/local/bin/virtualenv --no-site-packages .; mkdir releases; mkdir shared;' % env)
  clone_repo()
  checkout_latest()
  install_requirements()

def deploy():
  """Deploy the latest version of the site to the server and restart nginx"""
  checkout_latest()
  install_requirements()
  collect_static()
  symlink_current_release()
#  migrate()
  restart_server()

def collect_static():
  run('cd %(path)s/releases/%(release)s; ../../bin/python manage.py collectstatic --noinput' % env)

def clone_repo():
  """Do initial clone of the git repo"""
  run('cd %(path)s; git clone /home/%(user)s/git/repositories/politicando.git repository' % env)

def checkout_latest():
  """Pull the latest code into the git repo and copy to a timestamped release directory"""
  import time
  env.release = time.strftime('%Y%m%d%H%M%S')
  run("cd %(path)s/repository; git pull origin master" % env)
  run('cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*' % env)

def install_requirements():
  """Install the required packages using pip"""
  run('cd %(path)s; %(path)s/bin/pip install -r ./releases/%(release)s/requirements.txt' % env)

def symlink_current_release():
  """Symlink our current release, uploads and settings file"""
  with settings(warn_only=True):
    run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)
  run('cd %(path)s; ln -s %(release)s releases/current' % env)
  """ production settings"""
  #run('cd %(path)s/releases/current/; cp settings_%(settings)s.py politicando/settings.py' % env)
  with settings(warn_only=True):
    run('rm %(path)s/shared/static' % env)
    run('cd %(path)s/releases/current/static/; ln -s %(path)s/releases/%(release)s/static %(path)s/shared/static ' %env)

def migrate():
  """Run our migrations"""
  run('cd %(path)s/releases/current; ../../bin/python manage.py syncdb --noinput --migrate' % env)

def rollback():
  """
  Limited rollback capability. Simple loads the previously current
  version of the code. Rolling back again will swap between the two.
  """
  run('cd %(path)s; mv releases/current releases/_previous;' % env)
  run('cd %(path)s; mv releases/previous releases/current;' % env)
  run('cd %(path)s; mv releases/_previous releases/previous;' %env)
  restart_server()

def restart_server():
  """Restart the web server"""
  with settings(warn_only=True):
    sudo('kill -9 `cat /tmp/project-master_politicando.pid`')
    sudo('rm /tmp/project-master_politicando.pid /tmp/uwsgi_politicando.sock')
  run('cd %(path)s/releases/current; %(path)s/bin/uwsgi --ini %(path)s/releases/current/uwsgi.ini' % env)
  sudo('/etc/init.d/nginx restart')
