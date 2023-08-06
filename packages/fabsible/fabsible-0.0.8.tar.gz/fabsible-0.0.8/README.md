Fabsible
========

Fabsible is ansible framework which is object-oriented.

Getting started
---------------

Installation
############

Create python virtual env

```
python3 -m venv venv
. venv/bin/activate
```

Install fabsible

```
pip install fabsible
```


Configuration
-------------

TODO: creating inventory file

Init new project

```
fabsible-init -i libvirt-inventory.py
```

Create provisioning tasks and place them in `files/providers/<name>.yml`. Ex.

```
cat files/providers/libvirt.yml
- name: libvirt
  debug:
    msg: "Jeste provisione libvirte"

- include_role:
    name: exphost.create_user
  vars:
    ansible_user: root
    ansible_password: super_password
  loop: "{{ users }}"
  loop_control:
    loop_var: user
```

Create users

```
cat group_vars/all/users_admins.yml
users_admins:
  - user: torgiren
    group: wheel
    password: "XXX" #Password hash
    home: "/home/torgiren"
```

and add ssh-keys to `files/ssh-keys/<username>/<keyname>.pub`

add become password (TODO: this should be per user not per project)

```
cat become.yml
ansible_become_pass: anotherpassword
```

Run
---

`fabsible-play`
