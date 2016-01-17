from invoke import run, task
import platform
import getpass
import ssh_client

def dest_root(os):
    if os == 'Darwin':
        return '~'
    else:
        return '/var/lib/plexmediaserver'

def get_password(username, hostname):
    return getpass.getpass('Password for %s@%s: ' % (username, hostname))

def execute_remote_command(command, hostname, username, password):
    client = None

    try:
        client = ssh_client.SshClient(host=hostname, port=22, username=username, password=password)

        ret = client.execute(command, sudo=True)

        print "  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"]
    finally:
        if client:
            client.close()

src = 'src/lib'
bundle_name = 'Etvnet.bundle'

plex_home = dest_root(platform.system()) + "/Library/Application\ Support/Plex\ Media\ Server"
plugins_dir = plex_home + '/Plug-ins'
plugin_dir = plugins_dir + '/' + bundle_name

unix_plex_home = dest_root('Unix') + "/Library/Application\ Support/Plex\ Media\ Server"
unix_plugins_dir = unix_plex_home + '/Plug-ins'
unix_plugin_dir = unix_plugins_dir + '/' + bundle_name

username = 'alex'
hostname = "10.0.1.37"
archive = bundle_name + '.zip'

@task
def test(script):
    run("python " + script)

@task
def reset():
    run("rm -rf " + plex_home + "/Plug-in\ Support/Caches/com.plexapp.plugins.etvnet")
    run("rm -rf " + plex_home + "/Plug-in\ Support/Data/com.plexapp.plugins.etvnet")
    run("rm -rf " + plex_home + "/Plug-in\ Support/Preferences/com.plexapp.plugins.etvnet.xml")
    # run("rm -rf " + plugin_dir)

    print("Plugin was reset.")

@task
def copy(plugin_dir):
    run("mkdir -p " + plugin_dir + "/Contents/Code")
    run("mkdir -p " + plugin_dir + "/Contents/Services/Shared\ Code")

    run("cp -R " + src + "/etvnet/*.py " + plugin_dir + "/Contents/Code")
    run("cp -R " + src + "/common/*.py " + plugin_dir + "/Contents/Code")
    run("cp -R " + src + "/plex_plugin/Contents " + plugin_dir)
    #run("cp " + "etvnet.config " + plugin_dir + "/Contents")

    print("Files were copied.")

@task
def reload():
    import urllib2

    url = "http://127.0.0.1:32400/:/plugins/com.plexapp.system/restart"
    urllib2.urlopen(url).read()

    print("Server was restarted.")

    run("tail -f ~/Library/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log")

@task
def deploy():
    copy(plugin_dir)
    reset()
    reload()

@task
def pip():
    import pip

    installed_packages = pip.get_installed_distributions()

    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])

    print(installed_packages_list)

@task
def reset_remote(password):
    command = """
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Caches/com.plexapp.plugins.etvnet
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Data/com.plexapp.plugins.etvnet
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Preferences/com.plexapp.plugins.etvnet.xml
        sudo -S rm -rf {plex_home}/Plug-ins\{bundle_name}/Contents/Code
        # sudo -S rm -rf {plex_home}/Plug-ins\{bundle_name}/Contents/Resources
        # sudo -S rm -rf {plex_home}/Plug-ins\{bundle_name}/Contents/Services
        # sudo -S rm -rf {plex_home}/Plug-ins\{bundle_name}/Contents/Strings
        # sudo -S rm -f {plex_home}/Plug-ins\{bundle_name}/Contents/DefaultPrefs.json
        # sudo -S rm -f {plex_home}/Plug-ins\{bundle_name}/Contents/Info.plist

        echo "Plugin was reset.".
    """.format(plex_home=unix_plex_home, plugin_dir=unix_plugin_dir, bundle_name=bundle_name)

    execute_remote_command(command, hostname, username, password)

@task
def zip(archive):
    run("cd build && zip -r " + archive + " .")

@task
def scp(archive):
    run("scp build/" + archive + " " + username + "@" + hostname + ":" + archive)

@task
def unzip_remote(password):
    command = "sudo -S unzip -o " + bundle_name + ".zip -d " + unix_plugins_dir

    execute_remote_command(command, hostname, username, password)

@task
def restart_remote(password):
    command = """
        sudo -S service plexmediaserver restart

        echo "Server was restarted."
    """.format(plugin_dir=unix_plugin_dir, src=src)

    execute_remote_command(command, hostname, username, password)

@task
def chown_remote(password):
    command = "sudo -S chown -R plex " + unix_plugin_dir

    execute_remote_command(command, hostname, username, password)

@task
def ls_remote(password):
    execute_remote_command('ls', hostname, username, password)

@task
def clean():
    run("rm -rf build")

@task
def build():
    clean()

    run("mkdir -p build/" + bundle_name)

    copy('build/' + bundle_name)
    zip(archive)

@task
def rdeploy():
    password = get_password(hostname, username)

    build()

    # command = "sudo -S rm -rf " + unix_plugin_dir + "/Contents/Code"
    #
    # execute_remote_command(command, hostname, username, password)
    #
    # command = "sudo -S rm -f " + "~/" bundle_name + ".zip"
    #
    # execute_remote_command(command, hostname, username, password)

    scp(archive)

    reset_remote(password)
    unzip_remote(password)
    restart_remote(password)
    chown_remote(password)

