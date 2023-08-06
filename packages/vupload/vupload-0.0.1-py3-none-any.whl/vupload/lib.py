# -*- coding: UTF-8 -*-
"""Decouple business logic from the CLI script"""
import os

import requests
from vlab_inf_common.vmware import vCenter, vim




def get_upload_url(vcenter, vcenter_user, vcenter_password, the_vm, vm_user, vm_password, local_file, upload_dir):
    creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=password)
    upload_path = '{}/{}'.format(upload_dir, os.path.basename(local_file))
    file_size = os.stat(local_file).st_size

    with vCenter(host=vcenter, user=vcenter_user, password=vcenter_password) as vcenter:
        vm = vcenter.find_by_name(name=the_vm, vimtype=vim.VirtualMachine)
        url = _get_url(vcenter, vm, creds, upload_path, file_size)


def _get_url(vcenter, vm, creds, upload_path, file_size):
    """Mostly to deal with race between a VM powering on, and all of VMwareTools being ready.

    :Returns: String

    :param vcenter: **Required** The instantiated connection to vCenter
    :type vcenter: vlab_inf_common.vmware.vCenter

    :param vm: **Required** The new DataIQ machine
    :type vm: vim.VirtualMachine

    :param creds: **Required** The username & password to use when logging into the new VM
    :type creds: vim.vm.guest.NamePasswordAuthentication

    :param file_size: **Required** How many bytes are going to be uploaded
    :type file_size: Integer
    """
    # If the VM just booted the service can take some time to be ready
    for retry_sleep in range(10):
        try:
            url = vcenter.content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(vm=the_vm,
                                                                                                 auth=creds,
                                                                                                 guestFilePath=upload_path,
                                                                                                 fileAttributes=vim.vm.guest.FileManager.FileAttributes(),
                                                                                                 fileSize=file_size,
                                                                                                 overwrite=True)
        except vim.fault.GuestOperationsUnavailable:
            time.sleep(retry_sleep)
        else:
            return url
    else:
        error = 'Unable to upload file. Timed out waiting on VMware Tools to become available.'
        raise ValueError(error)
