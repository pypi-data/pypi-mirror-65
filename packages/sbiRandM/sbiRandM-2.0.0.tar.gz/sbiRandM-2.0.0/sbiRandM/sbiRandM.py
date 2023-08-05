#!/usr/bin/env python
import click
import mainWindow as mw

def showWindow():

    mw.exe()

@click.group()
@click.version_option(version="2.0.0", prog_name='sbiRandM')
def dokecs():  # pragma: no cover
    pass

@click.command()
@click.option('--window', help='Use the program with the GUI')

def sbiRandM():
    if mw.window != None:
        showWindow()

dokecs.add_command(sbiRandM)

if __name__ == '__main__':
    sbiRandM()
