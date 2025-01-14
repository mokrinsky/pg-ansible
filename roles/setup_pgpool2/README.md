# setup_pgpool2

This role is for installing and configuring PgpoolII. PgpoolII is a
connection pooler for PostgreSQL.

## Requirements

Following are the requirements of this role.

1. Ansible
2. `tmax_opensql.postgres` -> `setup_repo` - for repository installation
3. `tmax_opensql.postgres` -> `install_dbserver` - for installation of
   PostgreSQL binaries.
4. `tmax_opensql.postgres` -> `setup_extension` - for installation of
   PostgreSQL binaries.
5. `tmax_opensql.postgres` -> `init_dbserver` - for the initialization of
   primary server

## Role Variables

When executing the role via ansible these are the required variables:

- **_pg_version_**

  Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`, `14.7`, `14.8`, `15.0`, `15.1`, `15.2`, `15.3`

- **_pg_type_**

  Database Engine supported are: `PG`

These and other variables can be assigned in the `pre_tasks` definition of the
section: _How to include the `setup_pgpool2` role in your Playbook_

The rest of the variables can be configured and are available in the:

  * [roles/setup_pgpool2/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgpool2/vars/PG.yml](./vars/PG.yml)

Below is the documentation of the rest of the main variables:

### `pgpool2_watchdog`

Enable PgpoolII High Availability capability when deploying a PgpoolII multi
nodes cluster (3, 5 etc..). Default: `false`

Example:

```yaml
pgpool2_watchdog: true
```

### `pgpool2_vip`

Thie is the virtual IP address to put on the Pgpool2 primary node when
deploying a PgpoolII multi node cluster. Watchdog feature must be enabled.
Default: empty.

Example:

```yaml
pgpool2_vip: "10.0.0.123"
```

### `pgpool2_vip_dev`

System's network device to attach the virtual IP address. Default: empty.

Example:

```yaml
pgpool2_vip_dev: "eth0"
```

### `pgpool2_load_balancing`

Enable read only queries load balancing across all the Postgres nodes.
Default: `true`.

Example:

```yaml
pgpool_load_balancing: true
```

### `pgpool2_failover`

Enable failover command, follow primary command.
Default: `false`

Example:

```yaml
pgpool2_failover: true
```


### failover_script_local_path
Set failover script local path.
Default: `./templates/failover.sh.template`
```yaml
failover_script_local_path: "/opensql/failover.sh"
```

### follow_primary_script_local_path
Set follow_primary script local path.
Default: `./templates/follow_primary.sh.template`

```yaml
follow_primary_script_local_path: "/opensql/follow_prrimary.sh"
```

### `pgpool2_ssl`

Enable SSL support. Default: `true`.

Example:

```yaml
pgpool2_ssl: true
```

### `pgpool2_port`

Pgpool2 listening TCP port. Default: `9999`.

Example:

```yaml
pgpool2_port: 5433
```

### `pgpool2_pg_port`

PostgreSQL(backend) TCP port to connect to from pgpool. Default: `5432`.

Example:

```yaml
pgpool2_port: 5434
```

### `if_up_command`, `if_down_command`, `arping_command`

Set commands when initially setting watchdog.

Example:
```yaml
if_up_command: "/bin/sudo /sbin/ip addr add $_IP_$/24 dev eth0 label eth0:0"
if_down_command: "/bin/sudo /sbin/ip addr del $_IP_$/24 dev eth0"
arping_command: "/bin/sudo /sbin/arping -U $_IP_$ -w 1 -I eth0"
```

### `use_system_user`

Start pgpool-II systemd unit using this parameter.
If set to false, systemd unit is not used and it operates in the form of process through command.
Default: true

Example:

```yaml
use_system_user: false
```

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pgpool2:
      hosts:
        pool1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
        pool2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
        pool3:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### How to include the `setup_pgpool2` role in your Playbook

Below is an example of how to include the `setup_pgpool2` role:

```yaml
---
- hosts: pgpool2
  name: Deploy PgpoolII instances
  become: true
  gather_facts: true

  collections:
    - tmax_opensql.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

        pgpool2_load_balancing: true
        pgpool2_watchdog: true
        pgpool2_vip: "10.0.0.123"
        pgpool2_vip_dev: "eth0"
        pgpool2_port: 5433

  roles:
    - setup_pgpool2
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_pgpool2/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgpool2/vars/PG.yml](./vars/PG.yml)

## Database engines supported
### Supported OS
- CentOS7
- CentOS8
- Rocky8
- Rocky9

### Supported PostgreSQL Version
- 14.0 - 14.8
- 15.0 - 15.3

## pgpool-II supported

- RedHat
  * pgpool-II : 4.3

## License

BSD

## Author information

Author:
  * [Sang Myeung Lee](https://github.com/sungmu1)

Original Author:
  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
