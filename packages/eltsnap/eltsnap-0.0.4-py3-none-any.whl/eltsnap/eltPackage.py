import pyodbc
from contextlib import contextmanager
from .create import create_html



def create_dataflow_package (server_name, database_name, connection_name_source, query, is_expression, package_qualifier, destination_connection,
                             destination_schema, destination_table, destination_truncate, keep_identity, use_bulk_copy, batch_size, command="regular"):
    if is_expression.strip() == '' or is_expression == 'is_expression(default 0)':
        is_expression = 0

    if destination_truncate.strip() == '' or destination_truncate == 'destination truncate default(0)':
        destination_truncate = 0

    if keep_identity.strip() == '' or keep_identity == 'keep identity default(0)':
        keep_identity = 0

    if use_bulk_copy.strip() == '' or use_bulk_copy == 'use bulk copy default(0)':
        use_bulk_copy = 0

    if batch_size.strip() == '' or batch_size == 'batch size default(0)':
        batch_size = 0


    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (connection_name_source, query,  is_expression, package_qualifier, destination_connection,
                    destination_schema, destination_table,
                      destination_truncate, keep_identity, use_bulk_copy, batch_size)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Data Flow Package] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val:
        p_name = 'Data Flow ' + package_qualifier + ' ' + destination_table
        if command == "regular":
            print(f"Succesfully created dataflow pacakge {p_name}!")
        elif command == "clone":
            print(f"Succesfully cloned dataflow pacakge {p_name}!")

        create_html(server_name, database_name, p_name, command_type="data_flow")

def clone_dataflow_package (server_name, database_name, package_name, new_package_name):

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_name, new_package_name)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Data Flow Package] ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val > 0:
        print(f"Succesfully cloned project with qualifier {new_package_name} !")
        create_html(server_name, database_name, new_package_name, command_type="data_flow")


def delete_package(server_name, database_name, package_name):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)


    if package_name[:9] == "Data Flow":
        try:
            with connection() as conn:
                curr = conn.cursor()
                command = f"""DECLARE @name nvarchar(336) = '{package_name}'; DELETE FROM [elt].[package_config_data_flow] WHERE [package_name] = @name;
                         DELETE FROM [elt].[project_package] WHERE [package_name] = @name; 
                         DELETE FROM [elt].[query_history] WHERE [package_name] = @name;"""
                curr.execute(command)
                print(f"succesfully deleted the package {package_name}")
                create_html(server_name, database_name, package_name, command_type="data_flow")
        except Exception as e:
            print(e)

    if package_name[:15] == "Execute Process":
        try:
            with connection() as conn:
                curr = conn.cursor()
                command = f"""DECLARE @name nvarchar(128) = '{package_name}'; DELETE FROM [elt].[package_config_execute_process] WHERE [package_name] = @name; 
                DELETE FROM [elt].[dim_table_merge_config] WHERE [package_name] = @name; 
                DELETE FROM [elt].[package_config_execute_process_variable] WHERE [package_name] = @name; 
                DELETE FROM [elt].[project_package] WHERE [package_name] = @name; 
                DELETE FROM [elt].[query_history] WHERE [package_name] = @name;"""
                curr.execute(command)
                print(f"succesfully deleted the package {package_name}")
                create_html(server_name, database_name, package_name, command_type="execute_process")


        except Exception as e:
            print(e)

    if package_name[:11] == "Execute SQL":
        try:
            with connection() as conn:
                curr = conn.cursor()
                command = f"""DECLARE @name nvarchar(128) = '{package_name}'; DELETE FROM [elt].[package_config_execute_sql] WHERE [package_name] = @name; 
                DELETE FROM [elt].[fact_table_merge_config] WHERE [package_name] = @name; DELETE FROM [elt].[dim_table_merge_config] WHERE [package_name] = @name; 
                DELETE FROM [elt].[fact_table_partition_config] WHERE [package_name] = @name; DELETE FROM [elt].[fact_table_switch_config] WHERE [package_name] = @name;
                DELETE FROM [elt].[project_package] WHERE [package_name] = @name; DELETE FROM [elt].[query_history] WHERE [package_name] = @name;"""
                curr.execute(command)
                print(f"succesfully deleted the package {package_name}")
                create_html(server_name, database_name, package_name, command_type="execute_sql")

        except Exception as e:
            print(e)

    if package_name[:19] == "Foreach Execute SQL":
        try:
            with connection() as conn:
                curr = conn.cursor()
                command = f"""DECLARE @name nvarchar(336) = '{package_name}'; DELETE FROM [elt].[package_config_foreach_execute_sql] WHERE [package_name] = @name;
                 DELETE FROM [elt].[project_package] WHERE [package_name] = @name;
                 DELETE FROM [elt].[query_history] WHERE [package_name] = @name;"""
                curr.execute(command)
                print(f"succesfully deleted the package {package_name}")
                create_html(server_name, database_name, package_name, command_type="foreach_execute_sql")

        except Exception as e:
            print(e)

    if package_name[:17] == "Foreach Data Flow":
        try:
            with connection() as conn:
                curr = conn.cursor()
                command = f"""DECLARE @name nvarchar(336) = '{package_name}'; DELETE FROM [elt].[package_config_foreach_data_flow] WHERE [package_name] = @name; 
                DELETE FROM [elt].[project_package] WHERE [package_name] = @name; 
                DELETE FROM [elt].[query_history] WHERE [package_name] = @name;"""
                curr.execute(command)
                print(f"succesfully deleted the package {package_name}")
                create_html(server_name, database_name, package_name, command_type="foreach_data_flow")

        except Exception as e:
            print(e)




def create_foreach_dataflow_package(server_name, database_name, foreach_connection,connection_name_source, foreach_query,
    query, package_qualifier, destination_connection, destination_schema, destination_table, destination_truncate,
    keep_identity, use_bulk_copy, batch_size, command="regular"):

    if destination_truncate.strip() == '' or destination_truncate == 'destination truncate default(0)':
        destination_truncate = 0


    if keep_identity.strip() == '' or keep_identity == 'keep identity default(0)':
        keep_identity = 0

    if use_bulk_copy.strip() == '' or use_bulk_copy == 'use bulk copy default(0)':
        use_bulk_copy = 0

    if batch_size.strip() == '' or batch_size == 'batch size default(0)':
        batch_size = 0

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn
        except Exception as e:
            print(e)
    val = 0
    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (foreach_connection,connection_name_source, foreach_query, query, package_qualifier, destination_connection,
                             destination_schema, destination_table, destination_truncate, keep_identity, use_bulk_copy, batch_size)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Foreach Data Flow Package] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val:
        p_name = 'Foreach Data Flow ' + package_qualifier + ' ' + destination_table
        if command == "regular":
            print(f"Succesfully created foreach dataflow pacakge {p_name}!")
        elif command == "clone":
            print(f"Succesfully cloned foreach dataflow pacakge {p_name}!")
        create_html(server_name, database_name, p_name, command_type="foreach_data_flow")


def clone_foreach_dataflow_package(server_name, database_name, package_name, new_package_name):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_name, new_package_name)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Foreach Data Flow Package] ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val > 0:
        print(f"Succesfully cloned project with qualifier {new_package_name} !")
        create_html(server_name, database_name, new_package_name, command_type="foreach_data_flow")


def create_execute_process_package(server_name, database_name, package_qualifier, executable_expression,
                             arguments_expession, working_directory, place_values_in_ELT_Data, command="regular"):

    if place_values_in_ELT_Data.strip() == '' or place_values_in_ELT_Data.strip() == 'place values in ELT_Data default(0)':
        place_values_in_ELT_Data = 0



    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_qualifier, executable_expression,
                       arguments_expession, working_directory, place_values_in_ELT_Data)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Execute Process Package] ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val:
        p_name = 'Execute Process ' + package_qualifier
        print(f"Succesfully created Execute Process pacakge {p_name}!")
        create_html(server_name, database_name, p_name, command_type="execute_process")


def clone_execute_process_package(server_name, database_name, package_name, new_package_name):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_name, new_package_name)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Execute Process Package v2] ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val > 0:
        print(f"Succesfully cloned project with qualifier {new_package_name} !")
        create_html(server_name, database_name, new_package_name, command_type="execute_process")

def create_execute_SQL_package(server_name, database_name,connection_name_source,
                             query, package_qualifier, is_expression, return_row_count):

    if is_expression.strip() == '' or is_expression == 'is_expression(default 0)':
        is_expression = 0

    if return_row_count.strip() == '' or return_row_count == 'return row count(default 0)':
        return_row_count = 0

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)
    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (connection_name_source, query, package_qualifier,'', 0, '', is_expression, return_row_count)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Execute SQL Package] ?, ?, ?, ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val:
        p_name = 'Execute SQL ' + package_qualifier
        print(f"Succesfully created Execute SQL pacakge {p_name}!")
        create_html(server_name, database_name, p_name, command_type="execute_sql")

def clone_execute_SQL_package(server_name, database_name, package_name, new_package_qualifier):

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)
    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_name, new_package_qualifier)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Execute SQL Package v2] ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val > 0:
        print(f"Succesfully cloned project with qualifier {new_package_qualifier} !")
        create_html(server_name, database_name, new_package_qualifier, command_type="foreach_data_flow")


def create_foreach_execute_sql_package(server_name, database_name, foreach_connection, connection_name_source,
                               foreach_query, query, package_qualifier, is_expression, return_row_count, command="regular"):

    if is_expression.strip() == '' or is_expression == 'is_expression(default 0)':
        is_expression = 0

    if return_row_count.strip() == '' or return_row_count == 'return row count(default 0)':
        return_row_count = 0

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (foreach_connection, connection_name_source,
                    foreach_query, query, package_qualifier, is_expression, return_row_count)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Foreach Execute SQL Package] ?, ?, ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val:
        p_name = 'Foreach Execute SQL ' + package_qualifier
        if command == "regular":
            print(f"Succesfully created foreach execute SQL pacakge {p_name}!")
        elif command == "clone":
            print(f"Succesfully cloned foreach execute SQL pacakge {p_name}!")
        create_html(server_name, database_name, p_name, command_type="foreach_execute_sql")


def clone_foreach_execute_SQL_package(server_name, database_name, package_name, new_package_qualifier):

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    val = 0
    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (package_name, new_package_qualifier)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Foreach Execute SQL Package] ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val > 0:
        print(f"Succesfully cloned project with qualifier {new_package_qualifier} !")
        create_html(server_name, database_name, new_package_qualifier, command_type="foreach_execute_sql")
