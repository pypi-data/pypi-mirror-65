import pyodbc
from contextlib import contextmanager
import os
from jinja2 import Environment, FileSystemLoader
import time
import datetime
from tabulate import tabulate
from .eltSnap_Project_HTML import render

def create_html(server_name, database_name, proj_name ="", command_type ="regular"):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            print(e)

    try:
        with connection() as conn:
            curr = conn.cursor()
            #Create new Project
            if command_type == "regular":
                new_project = f"SELECT  [project_id],[project_name],[build_template_group] FROM [elt].project order by [project_name] "
            elif command_type == "connection":
                new_project = f"SELECT [connection_name],[server_name],[database_name],[provider],[custom_connect_string] FROM [elt].[oledb_connection] order by [connection_name] desc"
            elif command_type == "data_flow":
                new_project = f"SELECT TOP 10 * FROM [elt].[package_config_data_flow]"
            elif command_type == "foreach_data_flow":
                new_project = f"SELECT TOP 10 * FROM [elt].[package_config_foreach_data_flow]"
            elif command_type == "execute_process":
                new_project = f"SELECT TOP 10 * FROM [elt].[package_config_execute_process]"
            elif command_type == "execute_sql":
                new_project = f"SELECT TOP 10 * FROM [elt].[package_config_execute_sql]"
            elif command_type == "foreach_execute_sql":
                new_project = f"SELECT TOP 10 * FROM [elt].[package_config_foreach_execute_sql]"

            curr.execute(new_project)
            resultSet_ = curr.fetchall()
            columns = [col[0] for col in curr.description]
            project_parameters = resultSet_
    except Exception as e:
        print(e)

    # path = check_output(["where", "azuredatastudio"]).decode("utf-8")
    # path_to_azuredatastudio = path.split('\n')[0].strip('\r')
    # path_to_extension = os.path.join(path_to_azuredatastudio, '..', '..', 'resources', 'app', 'extensions', 'python')

    try:
        with connection() as conn:
            curr = conn.cursor()
            # Create new Project
            has_db_var = f"select setting from [elt].[application_config] where setting='path to html files location'"
            curr.execute(has_db_var)
            has_db_variable = curr.fetchall()
    except Exception as el:
        pass

    if not has_db_variable:
        with connection() as conn:
            curr = conn.cursor()
            insert_path = f"INSERT INTO [elt].[application_config] ([setting], [use_value]) VALUES ('path to html files location', '')"
            curr.execute(insert_path)

    try:
        with connection() as conn:
            curr = conn.cursor()
            new_project = f"SELECT [use_value] FROM [elt].[application_config] WHERE setting='path to html files location'"
            curr.execute(new_project)
            PATH = curr.fetchall()[0][0]
    except Exception as ex:
        pass

    try:
        PATH
    except NameError:
        PATH = ''


    while not os.path.exists(PATH):
        print(
            "There is no PATH to the directory in which eltSnap can build the html reports! Please provide absolute path for the directory")
        PATH = input()
        if not os.path.exists(PATH):
            print("The PATH does not exists")
        else:
            try:
                insert_path = f"UPDATE [elt].[application_config] SET use_value = '{PATH}' WHERE setting = 'path to html files location'"
                curr.execute(insert_path)
            except Exception as e:
                print(e)

    if os.path.exists(PATH):

        render(server_name, database_name, PATH)

    else:
        raise ("Path is wrong ! Check your azuredatastudio installaton !")


    time.sleep(0.1)
    print(tabulate(project_parameters, headers=columns))
