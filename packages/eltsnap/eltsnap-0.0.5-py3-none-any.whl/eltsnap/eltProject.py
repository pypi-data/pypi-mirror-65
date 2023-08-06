import pyodbc
from contextlib import contextmanager
from .create import create_html
import webbrowser

def open_webbrowser(filename):
    url = webbrowser.open(filename, new=2)

def generate_html_report(server_name, database_name):
    create_html(server_name, database_name)



def create_project(server_name, database_name, GIVE_YOUR_PROJECT_A_NAME, SELECT_A_TEMPLATE_GROUP):
    if GIVE_YOUR_PROJECT_A_NAME == 'project name':
        raise ValueError("Can't name cloned project as new project name.")

    val = 0
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
            params = (GIVE_YOUR_PROJECT_A_NAME, SELECT_A_TEMPLATE_GROUP)
    
            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Project] @project_name =?, @template_group = ?"
            curr.execute(CreateProjectCommand, params,)
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass

    if val > 0:
        print(f"Succesfully created project with id {val} !")
        create_html(server_name, database_name, GIVE_YOUR_PROJECT_A_NAME)
    else:
        print(f"The project with such name already exists Try again!")  
        return


def create_data_connection(server_name, database_name, connection_name_to_save, server_name_to_save, database_name_to_save, provider, project_name, connection_string: str):
    if connection_string.strip() == '' or connection_string == 'custom connection string (optional)':
        connection_string = None

    if project_name == 'enter project name (optional)':
        project_name = ''

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
            params = (connection_name_to_save, server_name_to_save, database_name_to_save, provider, project_name, connection_string)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Connection by Name] ?, ?, ?, ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print("Something got wrong")
        return

    if val > -1:
        print(f"Succesfully created data connection {connection_name_to_save}!")
        create_html(server_name, database_name, connection_name_to_save, command_type="connection")

def clone_data_connection(server_name, database_name, old_connection_name, connection_name_to_save, project_name):
    if project_name is 'enter project name (optional)':
        project_name = ''

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
            params = (old_connection_name, connection_name_to_save, project_name)
            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Connection By Name] ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass

    if val > 0:
        print(f"Succesfully cloned data connection with id {val} !")
        create_html(server_name, database_name, connection_name_to_save, command_type="connection")
    else:
        print(f"Error! Check your input parameters !")
        return

def delete_data_connection(server_name, database_name, connection_name_to_delete, project_name=''):
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
            connection_type = "Oledb"
            params = (connection_name_to_delete, connection_type, 0)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Delete Connection] ?, ?, ?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass

    if val > 0:
        print(f"Succesfully deleted connection with name {connection_name_to_delete} !")
        create_html(server_name, database_name, connection_name_to_delete, command_type="connection")
    else:
        print(f"Something went wrong! Check for your inputs !")
        return

def delete_project(server_name, database_name, Select_Project):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;", autocommit=True)
            yield cnxn
    
        except Exception as e:
            print(e)

    val = 0
    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (Select_Project)
    
            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Delete Project] @project_name =?"
            curr.execute(CreateProjectCommand, params,)
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass


    if val >0:
        print(f"Succesfully deleted project with id {val} !")
        create_html(server_name, database_name, Select_Project)


    else:
        print(f"Error ! Check your input parameters!")
        return

def clone_project(server_name, database_name, Select_Project, New_Project_Name):
    if New_Project_Name == 'new project name':
        raise ValueError("Can't name cloned project as new project name.")

    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",autocommit=True)
            yield cnxn
        except Exception as ex:
            print(ex)

    val = None

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (New_Project_Name, Select_Project)
            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Clone Project By Name] @project_name=?, @base_project_name =?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass

    if val is 0 or val is None:
        print(f"Error ! Check your input parameters!")
        return
    else:
        print(f"Cloned project {Select_Project} successfully to {New_Project_Name} !")
        create_html(server_name, database_name, New_Project_Name)

def rename_project(server_name, database_name, Select_Project, New_Project_Name):
    if New_Project_Name == 'new project name':
        raise ValueError("Can't name new project as 'new project name' !")
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;",
                autocommit=True)
            yield cnxn

        except Exception as e:
            raise RuntimeError("Check your inputs validity")
    val = 0
    try:
        with connection() as conn:
            curr = conn.cursor()
            CreateProjectCommand = f"SELECT [project_id],[build_template_group] FROM [elt].[project] where project_name= '{Select_Project}'"
            curr.execute(CreateProjectCommand)
            proje_id, tmp_group = curr.fetchall()[0]
    except pyodbc.Error as e:
        print("Doublecheck your database values")
    except NameError as ne:
        print("Such Project name does not exist inside our database.")
    except Exception as e:
        raise (e)

    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (New_Project_Name, tmp_group, proje_id)

            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Project] @project_name =?, @template_group =?, @project_id =?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        print(e)

    if val is None:
        print(f"Error ! Check your input parameters!")
    else:
        print(f"Renamed project successfully to {New_Project_Name} !")
        create_html(server_name, database_name, New_Project_Name)


def change_project_template(server_name, database_name, Select_Project, New_Template_Group):
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
            CreateProjectCommand = f"SELECT [project_id] FROM [elt].[project] where project_name= '{Select_Project}'"
            curr.execute(CreateProjectCommand)
            proje_id = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass
    except NameError as ne:
        print("Such Project name does not exist inside our database.")


    try:
        with connection() as conn:
            curr = conn.cursor()
            params = (Select_Project, New_Template_Group, proje_id)
            CreateProjectCommand = "SET NOCOUNT ON EXEC [elt].[Save Project] @project_name =?, @template_group =?, @project_id =?"
            curr.execute(CreateProjectCommand, params, )
            val = curr.fetchall()[0][0]
    except pyodbc.Error as e:
        pass

    if val is 0 or val is None:
        print(f"Error ! Check your input parameters!")
        return
    else:
        print(f"Renamed successfully projects  {Select_Project}  template group!")
        create_html(server_name, database_name, Select_Project)