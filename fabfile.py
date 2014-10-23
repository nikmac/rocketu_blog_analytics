from fabric.colors import green, yellow
from fabric.api import *
from fabric.contrib.files import upload_template

env.hosts = ['54.191.96.240']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/blog.pem'
env.shell = "/bin/bash -l -i -c"
# @task
# def ubuntu_hello():
#     run("lsb_release -a")

@task
def ubuntu_hello():
    with hide("stdout"):
        output = run("lsb_release -a")
        print(yellow(output))

# @task
# def deploy():
#     with cd("/home/ubuntu/rocketu_blog_analytics"):
#         run("git pull origin master")

def restart_app():
    sudo("service supervisor restart")
    sudo("service nginx restart")

@task
def deploy():
    with prefix("workon blog_analytics"):
        with cd("/home/ubuntu/rocketu_blog_analytics"):
            run("git pull origin master")
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")

    restart_app()


@task
def setup_postgres(database_name, password):
    sudo("adduser {}".format(database_name))
    sudo("apt-get install postgresql postgresql-contrib libpq-dev")

    with settings(sudo_user='postgres'):
        sudo("createuser {}".format(database_name))
        sudo("createdb {}".format(database_name))
        alter_user_statement = "ALTER USER {} WITH PASSWORD '{}';".format(database_name, password)
        sudo('psql -c "{}"'.format(alter_user_statement))

@task
def setup_nginx(project_name, server_name):
    upload_template("./deploy/nginx.conf",
                    "/etc/nginx/sites-enabled/{}.conf".format(project_name),
                    {'server_name': server_name},
                    use_sudo=True,
                    backup=False)

    restart_app()

@task
def hello():
    print(green("I'm alive!"))


@task
def create_file(file_name):
    local("touch ~/Desktop/{}.txt".format(file_name))


@task
def create_directory():
    local("mkdir ~/Desktop/dummy_dir")


@task
def name_dir(directory_name, path):
    local("mkdir ~/{}/{}").format(directory_name, path)