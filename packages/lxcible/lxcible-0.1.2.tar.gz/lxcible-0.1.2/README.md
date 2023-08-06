[![pypy badge](https://img.shields.io/pypi/v/lxcible.svg)](https://pypi.python.org/pypi/lxcible)

# lxcible
A dynamic Ansible inventory based on running linuxcontainers

![logo](https://gitlab.science.ru.nl/uploads/-/system/project/avatar/4060/lxcible.png)


## Installation
``` console
$ pip install lxcible
```

Or from source:
``` console
$ mkdir src
$ cd src
$ git clone git@gitlab.science.ru.nl:bram/lxcible.git
$ cd lxcible
$ sudo pip install .
```

## Introduction
A dynamic ansible inventory based on running linuxcontainers.

When invoked with `--list`, `lxcible` will output a json inventory based on 
currently running containers.

## Usage Example
Create some containers from an image that has your public key in
`/home/ubuntu/.ssh/authorize_keys`:
``` console
$ lxc launch bionic-with-pubkey foo
Creating foo
Starting foo
$ lxc launch bionic-with-pubkey bar
Creating bar
Starting bar
$ lxc launch bionic-with-pubkey baz
Creating baz
Starting baz
```

```
$ lxc list
+------+---------+----------------------+----------------------------------------------+-----------+-----------+
| NAME |  STATE  |         IPV4         |                     IPV6                     |   TYPE    | SNAPSHOTS |
+------+---------+----------------------+----------------------------------------------+-----------+-----------+
| bar  | RUNNING | 10.153.75.179 (eth0) | fd42:9f54:f06:b4a5:216:3eff:fe0a:a7d4 (eth0) | CONTAINER | 0         |
+------+---------+----------------------+----------------------------------------------+-----------+-----------+
| baz  | RUNNING | 10.153.75.163 (eth0) | fd42:9f54:f06:b4a5:216:3eff:fe30:3194 (eth0) | CONTAINER | 0         |
+------+---------+----------------------+----------------------------------------------+-----------+-----------+
| foo  | RUNNING | 10.153.75.98 (eth0)  | fd42:9f54:f06:b4a5:216:3eff:fed6:ca26 (eth0) | CONTAINER | 0         |
+------+---------+----------------------+----------------------------------------------+-----------+-----------+
```

With these three running containers, `lxcible --list` produces the following output:
``` json
{
    "_meta": {
        "hostvars": {
            "bar": {
                "ansible_host": "10.153.75.179"
            },
            "baz": {
                "ansible_host": "10.153.75.163"
            },
            "foo": {
                "ansible_host": "10.153.75.98"
            }
        }
    },
    "all": [
        "bar",
        "baz",
        "foo"
    ]
}
```

Minimal test playbook:
``` yaml
---
- hosts: all
  serial: 1
  gather_facts: False
  tasks: 
    - name: Fetch ssh host keys
      delegate_to: localhost
      lineinfile:
        path: ~/.ssh/known_hosts
        create: yes
        state: present
        line: "{{ lookup('pipe', 'ssh-keyscan -t rsa ' + ansible_host) }}"

- hosts: all
  gather_facts: False
  tasks: 
    - name: "Test connectivity"
      ping:
```

This will gather the ssh host keys using ssh-keyscan. This part will be done serially because 
`lineinfile` doesn't handle concurrent writes not so well (see: <https://github.com/ansible/ansible/issues/31712>).
The second part pings the hosts to test ssh-connectivity.

Lets run the playbook:
``` console
$ ansible-playbook -u ubuntu -i /usr/local/bin/lxcible main.yml 

PLAY [all] ****************************************************************************************************************************

TASK [Fetch ssh host keys] ************************************************************************************************************
# 10.153.75.179:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
changed: [bar -> localhost]

PLAY [all] ****************************************************************************************************************************

TASK [Fetch ssh host keys] ************************************************************************************************************
# 10.153.75.163:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
changed: [baz -> localhost]

PLAY [all] ****************************************************************************************************************************

TASK [Fetch ssh host keys] ************************************************************************************************************
# 10.153.75.98:22 SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
changed: [foo -> localhost]

PLAY [all] ****************************************************************************************************************************

TASK [Test connectivity] **************************************************************************************************************
ok: [baz]
ok: [bar]
ok: [foo]

PLAY RECAP ****************************************************************************************************************************
bar                        : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
baz                        : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
foo                        : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Groups
Now, lets add the machines to ansible groups:
```
$ lxc config set bar user.ansible.groups lemp
$ lxc config set foo user.ansible.groups django,node_exporter
$ lxc config set baz user.ansible.groups node_exporter
```

```
$ lxcible --list
{
    "_meta": {
        "hostvars": {
            "bar": {
                "ansible_host": "10.153.75.179"
            },
            "baz": {
                "ansible_host": "10.153.75.163"
            },
            "foo": {
                "ansible_host": "10.153.75.98"
            }
        }
    },
    "all": [
        "bar",
        "baz",
        "foo"
    ],
    "django": [
        "foo"
    ],
    "lemp": [
        "bar"
    ],
    "node_exporter": [
        "baz",
        "foo"
    ]
}
```
