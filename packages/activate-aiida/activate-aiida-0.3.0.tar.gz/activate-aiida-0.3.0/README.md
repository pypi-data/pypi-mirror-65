[![Anaconda-Server Badge](https://anaconda.org/cjs14/activate-aiida/badges/version.svg)](https://anaconda.org/cjs14/activate-aiida)

# activate-aiida

This is a small package to build around the internal [aiida-core](https://github.com/aiidateam/aiida-core) tools (v1.2), to quickly create and launch **isolated**
AiiDA environments from scratch. Its focussed on development, but can also be used more generally.

The basic steps are:

1. Buy a new computer
2. Install Conda
   - On linux:
     - `wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh`
     - `bash miniconda.sh`
     - `conda update conda`
3. Create the development environment:
   - `conda env create -n aiida-dev -f aiida-dev-env.yml`
   - `conda activate aiida-dev`
   - This is a copy of `environment.yaml` in aiida-core,
     but with all the extra development packages, and other goodies like jupyter lab
4. Install aiida-core in development mode
   - `pip install --no-deps -e .`
5. Run `source aiida-activate --help` to see the options
   - This needs to be called with `source`, so that it can set-up some environmental variables
   - Running `source aiida-activate setup.yaml -c -w 4` will:
     - Initialise a database at `store_path`/pgsql, if it doesn't already exist
     - Kill any currently running postgres server
     - Start up a postgres server with the desired settings
     - Ensure RabbitMQ is running
     - Set the aiida repository path to `store_path`/.aiida
     - Run `verdi quicksetup --config=setup.yaml`, if the profile does not already exist
     - Set the profile as the default profile
     - Stop any current daemon and start one with 4 workers
     - Activate verdi tab completion
6. When your done, `aiida-deactivate` will stop the daemon and the postgres server

## Example Config File

```yaml
store_path: /home/csewell/Documents/aiida-core/test_repo

su_db_username: chrisjsewell
# su_db_password:  # not yet supported

db_engine: postgresql_psycopg2
db_backend: django

db_host: localhost
db_port: 5432
db_name: basic_db
db_username: chrisjsewell
db_password: niceday

profile: basic
email: christopher.sewell@epfl.ch
first_name: Chris
last_name: Sewell
institution: EPFL

non_interactive: true
```

## Example CLI

```console
$ source aiida-activate setup.yaml -c -w 4
  parsed args: -c true -w 4 setup.yaml
- Reading variables from setup.yaml
- Setting Up SQL Database
  PGDATA='/home/csewell/Documents/aiida-core/test_repo/pgsql'
- Activating Postgres server: /home/csewell/Documents/aiida-core/test_repo/pgsql on port 5432
waiting for server to start.... done
server started
  Logging Postgres server to: /home/csewell/Documents/aiida-core/test_repo/pgsql/postgres_env_.log
- Ensure RabbitMQ Running
- Setting Up AiiDa Database
  AIIDA_PATH='/home/csewell/Documents/aiida-core/test_repo'
Info: Database user "chrisjsewell" already exists!
Use it?  [y/N]: y
Success: created new profile `basic`.
Info: migrating the database.
Operations to perform:
  Apply all migrations: auth, contenttypes, db
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying db.0001_initial... OK
  Applying db.0002_db_state_change... OK
  Applying db.0003_add_link_type... OK
  Applying db.0004_add_daemon_and_uuid_indices... OK
  Applying db.0005_add_cmtime_indices... OK
  Applying db.0006_delete_dbpath... OK
  Applying db.0007_update_linktypes... OK
  Applying db.0008_code_hidden_to_extra... OK
  Applying db.0009_base_data_plugin_type_string... OK
  Applying db.0010_process_type... OK
  Applying db.0011_delete_kombu_tables... OK
  Applying db.0012_drop_dblock... OK
  Applying db.0013_django_1_8... OK
  Applying db.0014_add_node_uuid_unique_constraint... OK
  Applying db.0015_invalidating_node_hash... OK
  Applying db.0016_code_sub_class_of_data... OK
  Applying db.0017_drop_dbcalcstate... OK
  Applying db.0018_django_1_11... OK
  Applying db.0019_migrate_builtin_calculations... OK
  Applying db.0020_provenance_redesign... OK
  Applying db.0021_dbgroup_name_to_label_type_to_type_string... OK
  Applying db.0022_dbgroup_type_string_change_content... OK
  Applying db.0023_calc_job_option_attribute_keys... OK
  Applying db.0024_dblog_update... OK
  Applying db.0025_move_data_within_node_module... OK
  Applying db.0026_trajectory_symbols_to_attribute... OK
  Applying db.0027_delete_trajectory_symbols_array... OK
  Applying db.0028_remove_node_prefix... OK
  Applying db.0029_rename_parameter_data_to_dict... OK
  Applying db.0030_dbnode_type_to_dbnode_node_type... OK
  Applying db.0031_remove_dbcomputer_enabled... OK
  Applying db.0032_remove_legacy_workflows... OK
  Applying db.0033_replace_text_field_with_json_field... OK
  Applying db.0034_drop_node_columns_nodeversion_public... OK
  Applying db.0035_simplify_user_model... OK
  Applying db.0036_drop_computer_transport_params... OK
  Applying db.0037_attributes_extras_settings_json... OK
  Applying db.0038_data_migration_legacy_job_calculations... OK
  Applying db.0039_reset_hash... OK
  Applying db.0040_data_migration_legacy_process_attributes... OK
  Applying db.0041_seal_unsealed_processes... OK
  Applying db.0042_prepare_schema_reset... OK
  Applying db.0043_default_link_label... OK
  Applying db.0044_dbgroup_type_string... OK
Success: database migration completed.
- Starting AiiDA
  Rescanning aiida plugins
  Setting default profile: basic
Success: basic set as default profile
  Stopping any current daemon
Profile: basic
Daemon was not running
  Activating daemon for profile: basic with 4 workers
  Activating verdi tab completion
- Finishing Status:
 ✓ config dir:  /home/csewell/Documents/aiida-core/test_repo/.aiida
 ✓ profile:     On profile basic
 ✓ repository:  /home/csewell/Documents/aiida-core/test_repo/.aiida/repository/basic
 ✓ postgres:    Connected as chrisjsewell@localhost:5432
 ✓ rabbitmq:    Connected to amqp://127.0.0.1?heartbeat=600
 ✓ daemon:      Daemon is running as PID 22227 since 2020-04-10 00:55:10
```

```console
$ deactivate-aiida 
Stopping Daemon:
Profile: basic
Waiting for the daemon to shut down... OK
Stopping Postgres:
waiting for server to shut down.... done
server stopped
Done!
```

## Troubleshooting

If postgres is not stopped correctly you may get this error:

    psql: could not connect to server: No such file or directory

In this case you may have to manually delete the
`path/to/database/postmaster.pid` file (see [here](https://stackoverflow.com/a/13573207/5033292))

If a port has been left open (from [here](https://stackoverflow.com/a/17703016/5033292)):

    >> sudo lsof -i :PORTNUM
    >> sudo kill -9 PID

