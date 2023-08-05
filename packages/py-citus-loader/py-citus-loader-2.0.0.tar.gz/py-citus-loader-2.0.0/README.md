# Citus loader

Citus loader is a tool that will allow you to do dump and restore on citus formations.

Here is how it works:

## citus-dump

The command citus-dump will:

- Do a schema dump of your formation
- Create a file with the distribute statements
- Take a pg_dump of each of your nodes and coordinator.

Here are the options you can configure:


- host: should the the host of your initial formation
- db: database you want to dump
- port: default 5432
- pwd: password
- pg_dump: if necessary, the path to the pg_dump you want to use
- pg_dump_jobs: value of the --jobs argument in pg_dump
- parallel_tasks: number of pg_dump tasks running in parallel
- dump_schema: default True, take a pg_dump of the schema
- dump_data: default True, take a pg_dump of the data
- ignore_write_locks: by default, citus-dump will try to lock the tables to ensure that before running pg_dump, no insert/update/delete statement is running on the workers.
- config_file: path to your yaml file with the configuration for the citus-dump command


We strongly recommend using a yaml configurattion file. You can find an example in tests/configuration.yml

## citus-restore

On your destination formation, citus-restore will:

- Restore the schema
- Distribute the tables
- Restore the shards to their appropriate worker.


- host: should the the host of your destination formation
- db: database you want to reestore
- port: default 5432
- pwd: password
- pg_restore: if necessary, the path to the pg_dump you want to use
- pg_restore_jobs: value of the --jobs argument in pg_restore
- parallel_tasks: number of pg_dump tasks running in parallel
- restore_schema: default True, restores the schema and distribute the tables
- restore_data: default True, does a pg_restore of the shards data
- config_file: path to your yaml file with the configuration for the citus-restore command


We strongly recommend using a yaml configurattion file. You can find an example in tests/configuration.yml
