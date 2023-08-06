import os
import shutil
import sys
from os import getcwd
from pathlib import Path
from time import sleep

import click

from ofxcloudsync import dirs, load_sync_ofx, write_sync_ofx, SYNC_OFX
from ofxcloudsync.ofx_sync import run_local_sync


@click.group(chain=True)
@click.version_option()
@click.pass_context
def ofxcs(ctx):
    """Command line interface to ofx-cloudsync."""
    ctx.ensure_object(dict)
    sys.path.append(getcwd())


@ofxcs.command("configure")
@click.pass_context
def configure(ctx):
    """
    configures ofx-cloudsync
    """

    aws_cred = os.path.join(os.path.expanduser("~"), '.aws', 'credentials')
    if not os.path.exists(aws_cred):
        if click.confirm('Do you want to enter access key details?'):
            key_id = click.prompt("Enter key ID", type=str)
            secret_key = click.prompt("Enter secret key", type=str)
            region = click.prompt("Enter region code", type=str)
            with open(aws_cred, 'w') as wf:
                s = f"""[default]
aws_access_key_id = {key_id}
aws_secret_access_key = {secret_key}
region = {region}"""
                wf.write(s)

        elif click.confirm('Do you want to enter request some access key details?'):
            click.launch("mailto:ofxcs@agiledat.co.uk?subject=Request for ofx-cloudsync keys&body="
                         "Hi. I'd like to be able to use this cool OrcaFlex cloud sync tool.")
    bucket = click.prompt("Enter bucket name", type=str)
    try:
        os.mkdir(dirs.user_data_dir)
    except:
        pass
    pca_new = click.prompt('Where do you want to install the post-calculation action script?',
                           default=os.path.join(dirs.user_data_dir, "pca_ofx2cloud.py"))
    pca = Path(__file__).parent.parent.joinpath("ofxcloudsync", "pca_ofx2cloud.py")
    shutil.copy(pca, pca_new)
    root_default = os.path.join(dirs.user_data_dir, "ofxsync")
    root_folder = click.prompt('Where do you want to save the simulations?',
                               default=root_default)
    sync_ofx = {
        "bucket": bucket,
        "root_folder": root_folder,
        "sync": []
    }
    write_sync_ofx(sync_ofx)


@ofxcs.command("add")
@click.pass_context
@click.option("--folder",
              '-f',
              help="Add a folder to keep in sync.",
              type=str
              )
def add(ctx, folder):
    """add a folder to sync"""
    sync_ofx = load_sync_ofx()
    sync_ofx['sync'].append(folder)
    write_sync_ofx(sync_ofx)


@ofxcs.command("remove")
@click.pass_context
@click.option("--folder",
              '-f',
              help="Folder to stop syncing.",
              type=str
              )
@click.option("--delete",
              help="The folder will be deleted on the local drive.",
              default=False,
              is_flag=True
              )
def remove(ctx, folder, delete):
    """stop syncing a folder"""
    sync_ofx = load_sync_ofx()
    sync_ofx['sync'].remove(folder)
    write_sync_ofx(sync_ofx)
    if delete:
        folder_path = os.path.join(sync_ofx['root_folder'], folder)
        shutil.rmtree(folder_path)


@ofxcs.command("sync")
@click.pass_context
@click.option("--once",
              help="The sync will run once and exit. The default is for the sync to keep running until the user exits.",
              default=False,
              is_flag=True
              )
def sync(ctx, once):
    """sync files from cloud to local drive"""
    click.echo("Starting sync.")
    if once:
        run_local_sync()
        click.echo("Sync complete.")
    else:
        while True:
            try:
                run_local_sync()
                sleep(2)
            except KeyboardInterrupt:
                click.echo("exiting. Bye.")
