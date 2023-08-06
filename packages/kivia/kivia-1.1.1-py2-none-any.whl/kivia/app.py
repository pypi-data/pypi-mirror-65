import os
import time

import click
from colorama import Fore

from kivia.DB import DB
from kivia.utils import Utils

util = Utils()

BASE_URL = "https://wisd4.herokuapp.com"


def makeDirs():
    util.createDirs(util.getCurrentDir() + "/dbs")
    util.createDirs(util.getCurrentDir() + "/modules")
    util.createDirs(util.getCurrentDir() + "/modules/test_modules")
    util.createDirs(util.getCurrentDir() + "/modules/live_modules")


makeDirs()
db = DB(util.getCurrentDir() + "/dbs/kivia.db")
db.createTable("modules", {
    "name": "text",
    "description": "text",
    "version": "integer",
    "alias": "text",
    "filename": "text",
    "time": "text"
})


@click.group()
def run():
    """
    Kivia is a module based cli app that helps you to do everything in CLI
    \n To install a package type /kpm install [modulename]
    \n\nTo search a package type /kpm search [modulename]
    """
    pass


@run.command("list")
def request():
    """This command list the modules installed in your system """
    modules = db.getAll("modules")
    data = []
    for x in modules:
        data.append(
            {"Name": x[0], "Description": x[1], "Version": x[2], "Alias": x[3], "Installed on": time.ctime(int(x[5]))})
    util.showDatas("List of installed modules:", data)


@run.command("install")
@click.argument("link")
def add_module(link):
    """This command install a module installed in your system """
    try:
        if db.get("modules", {"alias": link}):
            util.generateError(f"{link} is already installed.")
        else:
            data = util.fetchData(util.GET, f"{BASE_URL}/api/install/{link}", prefix="Searching.").json()
            util.showDatas("Module Information", [data], exclude=["rawUrl", "unique"])
            if "error" not in data:
                if util.confirm(linebreak=False):
                    code = util.fetchData(util.GET, url=data['rawUrl'],
                                          prefix="Installing Module.").content
                    os.system(f"pip3 install {' '.join(data['dependencies'])}")
                    filename = util.getRandomCharacters(15) + "." + data['rawUrl'].split('/').pop().split('.')[1]
                    open(
                        f"{os.path.dirname(__file__)}/modules/live_modules/{filename}",
                        "w").write(
                        code.decode("utf-8"))
                    import requests
                    requests.post(f"{BASE_URL}/api/ct/{data['unique']}", data={"id": util.uniqueComputerId()})
                    db.insert("modules", (
                        data['name'], data['description'], data['version'], data['alias'],
                        filename,
                        str(round(time.time()))))
                    util.colored("\n Module Installed Successfully !", Fore.GREEN)
                else:
                    util.colored("Operation aborted.", Fore.RED)
    except Exception as e:
        # raise e
        util.generateError("Some error")


@run.command("remove")
@click.argument('id')
def delete_module(id):
    """This command uninstalls a module from a system"""
    module = db.get("modules", {"alias": id})
    if not module:
        util.generateError(f"{id} module not found.")
    else:
        if util.confirm(f"Module {module[0][0]} will be removed.Are you sure (y/n) "):
            try:
                os.remove(f"{os.path.dirname(__file__)}/modules/live_modules/{module[0][4]}")
            except:
                pass
            db.delete("modules", {"alias": id})
            print("Module removed successfully.")
        else:
            print("Operation aborted.")


@run.command("search")
@click.argument("alias")
def search_module(alias):
    """This command searches a modules in internet """
    searchData = util.fetchData(util.GET, f"{BASE_URL}/api/search/{alias}", prefix="Searching..").json()
    util.showDatas(f"Top 10 Modules with name {alias}", searchData, isError=util.isError(searchData), showNo=True,
                   onEmpty="No search result found.Make sure search key is greater than 4 character.")


@run.command("upload")
def uploadModule():
    """This command uploads your module to server for developers"""
    git_url = input("Enter github repo url : ")
    if len(git_url.split("/")) != 5:
        git_url = git_url[:-1]
    try:
        fetchInfo = util.fetchData(util.POST, f"{BASE_URL}/api/info", data={"link": git_url},
                                   prefix="Checking your repo").json()
        util.showDatas(f"Repo Details \n Author : {fetchInfo['author']}", fetchInfo['files'], showNo=True)
    except Exception as e:
        util.generateError("Module Not Found")
        return

    def check():
        try:
            no = int(input("Which file is the module? type file number : "))
            if not util.confirm(f"\nIs it {fetchInfo['files'][no - 1]['name']} ?(y/n)"):
                print("\n")
                check()
            return no
        except:
            print("Please type valid number\n")
            check()

    no = check() - 1
    code = util.fetchData(util.GET, url=fetchInfo['files'][no]['link'],
                          prefix="Fetching Module.").content
    open(f"{os.path.dirname(__file__)}/modules/test_modules/{fetchInfo['files'][no]['name']}", "w").write(
        code.decode("utf-8"))
    exec(f"import kivia.modules.test_modules.{fetchInfo['files'][no]['name'].split('.').pop(0)} as md")
    moduleInfo = locals()['md'].info()
    moduleInfo['rawUrl'] = fetchInfo['files'][no]['link']
    util.showDatas("Module Information", [moduleInfo])
    if util.confirm():
        request = util.fetchData(util.POST, f"{BASE_URL}/api/upload", data=moduleInfo,
                                 prefix="Uploading to server").json()
        if not util.isError(request):
            util.showDatas("Module sent to server.", [request])
            print("Please save this id to check your module updates.we will mail you when we verify your module. ")
        else:
            util.showDatas("Error occured.", [request])

    else:
        util.generateError("Please try again !")


@run.command("status")
@click.argument("id")
def check_module(id):
    """This command checks the status of the module using ID"""
    check = util.fetchData(util.GET, f"{BASE_URL}/api/check/{id}", prefix="Checking Id").json()
    util.showDatas("Information About Module", [check], isError=util.isError(check))


@run.command()
def bindtobash():
    """This command binds the kivia cli to bash i.e you dont need to type kivia after doing this"""
    if util.hasSudoPermission():
        print(f"----\n{Fore.RED}Please dont run this with sudo\n-----")
    else:
        if "kpm $@" in os.popen("cat ~/.bashrc").read()[:-1]:
            print("Kivia is already installed to bash.")
        else:
            os.system(f'echo "{open(util.getCurrentDir() + "/bashrc.sh").read()}">>~/.bashrc')
            print(
                f"{Fore.LIGHTGREEN_EX}Kivia is now installed to bash.\n Check it by reopening this terminal"
                f" and typing {Fore.WHITE}--help")


def moduleExists(args):
    modules = db.getAll("modules")
    for x in modules:
        if x[3] == args[0]:
            exec(f"import kivia.modules.live_modules.{x[4].split('.').pop(0)} as md")
            args.pop(0)
            moduleInfo = locals()['md'].run(args)
            return True
    return False


def showhelp():
    click.echo(util.lolcatText('''
  _  ___       _       
 | |/ (_)     (_)      
 | ' / ___   ___  __ _ 
 |  < | \ \ / / |/ _` |
 | . \| |\ V /| | (_| |
 |_|\_\_| \_/ |_|\__,_|
 
Kivia(KPM) is a package manager which helps you to install,search cli packages from internet.

For more help type kpm --help'''))


def startUp():
    import sys
    args = sys.argv
    args.pop(0)
    if not args:
        showhelp()
    else:
        if not moduleExists(args) and args:
            run(args)
