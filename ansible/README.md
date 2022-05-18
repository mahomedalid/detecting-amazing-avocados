# Ansible README

This document contains information on how to set up Ansible for deploying the Amazing Avocados project.

## Prerequisites

Python 3 and Pip should already be installed on new versions of the Raspberry Pi OS.

### Install Ansible

Either install Ansible for the specific user...

```bash
$ python3 -m pip install --user ansible
```

...or install Ansible globally...

```bash
$ sudo python3 -m pip install ansible
```

## Setup Raspberry Pi(s)

In order to use Ansible, we must have distributed our SSH key to the target machine(s) and added those machines to our `inventory` file.

### SSH Key Distribution

Please use the standard `ssh-copy-id` command to distribute our SSH key Ansible will use. For instance, if we wanted to use the SSH key `~/.ssh/id_rsa` for user `spacekatt` on a machine at IP address `10.0.0.1`, then we would use the following command:

```bash
$ ssh-copy-id -i ~/.ssh/id_rsa spacekatt@10.0.0.1
```

### Inventory File

Please add a line for every machine we wish to configure, and set the `ansible_user` variable if the user is different than the default `ansible` specification. For example, we would add the following line to our inventory file after distributing the previous SSH key:

```bash
10.0.0.1 ansible_user=spacekatt
```

## Running the Playbook

To run the process, please navigate to the `detecting-amazing-avocados/ansible` directory and run the following command:

```bash
$ ansible-playbook -i inventory main.yml
```
