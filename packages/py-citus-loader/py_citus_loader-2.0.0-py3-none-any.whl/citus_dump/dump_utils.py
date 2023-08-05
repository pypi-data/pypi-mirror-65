import os

from subprocess import STDOUT, call

from .formation_utils import *
from .coordinator_utils import (dump_schema as dump_coordinator_schema,
                                dump_sequences,
                                lock_tables_before_data_dump)
from .node_utils import *
from .configuration import *
from .utils import run_statements_in_parallel


def get_dump_statements(coordinator):
    statements = get_nodes_pg_dump_statements(coordinator)

    if coordinator.configuration.dump_coordinator_data:
        statements.append(coordinator.data_dump_statement)

    return statements


def split_schema_coordinator(coordinator):
    split_start = False
    with open(coordinator.schema_dump_path, 'r+') as schema_file:
        lines = schema_file.readlines()

    prev_line = None

    constraint_lines = []
    schema_lines = []

    for line in lines:
        if not split_start:
            split_start = split_start or 'PRIMARY KEY' in line or 'UNIQUE' in line

            if split_start:
                constraint_lines.append(prev_line)
                constraint_lines.append(line)
                del schema_lines[-1]
            else:
                schema_lines.append(line)
        else:
            constraint_lines.append(line)

        prev_line = line


    schema_file = open(coordinator.schema_dump_path, 'w')
    constraint_file = open(coordinator.schema_constraint_path, 'w')

    schema_file.writelines(schema_lines)
    constraint_file.writelines(constraint_lines)

    schema_file.close()
    constraint_file.close()

def perform_dump(coordinator):
    configuration = coordinator.configuration

    if configuration.dump_schema:
        dump_coordinator_schema(coordinator)

    # Get pg_dump statements for workers and coordinator
    statements = get_dump_statements(coordinator)

    if not os.path.exists(os.path.join(configuration.dump_folder, 'coordinator_schema.sql')):
        raise Exception('Schema dump isn\'t valid')


    split_schema_coordinator(coordinator)

    # Run pg_dump with n tasks in parallel
    if configuration.dump_data:
        # Try to lock distributed and reference tables, if can't do it, raise error
        # Add option ignore_locks option
        if not configuration.ignore_write_locks:
            print('Locking the tables to ensure no concurrent write is happening')
            lock_tables_before_data_dump(coordinator)

        run_statements_in_parallel(configuration, statements)

    # get dump for sequences
    dump_sequences(coordinator)

    print('Finished pg_dump')
