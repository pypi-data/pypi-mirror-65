#!/usr/bin/python
# -*- coding: <utf-8> -*-
import pyodbc
from contextlib import contextmanager
from pprint import pprint
import os
import webbrowser
from jinja2 import Environment,FileSystemLoader
import time
import shutil


def render(server_name, database_name, PATH):
    @contextmanager
    def connection():
        try:
            cnxn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};Server=" + server_name + ";Database=" + database_name + ";Trusted_Connection=yes;MARS_Connection=Yes;")
            yield cnxn

        except Exception as e:
            print(e)

    with connection() as conn:
        curr = conn.cursor()
        get_projects = "SELECT TOP(1000)[project_name] FROM [elt].[project]"
        curr.execute(get_projects)
        c = curr.fetchall()
        project_set = [proj[0] for proj in c]

    from collections import defaultdict

    project_package_set = defaultdict(list)
    # projects with packages
    with connection() as conn:
        curr = conn.cursor()
        for i in project_set:
            get_project_package = "select p.project_name, pp.sequence_number, pp.package_name from elt.project as p right join [elt].[project_package] as pp on p.project_id=pp.project_id where p.project_name='{0}' order by  pp.sequence_number;".format(
                i)
            curr.execute(get_project_package)
            c = curr.fetchall()
            project_package_set[i].append(c)
            project_package_columns = [col[0] for col in curr.description][1:]

    with connection() as conn:
        # DF ppackage
        curr = conn.cursor()
        DataFlowPackage_ = "SELECT [src_connection],[src_query],[is_expression],[dst_connection] ,[dst_schema] ,[dst_table] ,[dst_truncate] ,[keep_identity] ,[package_name],[use_bulk_copy], [batch_size]" \
                           "  FROM [elt].[package_config_data_flow]"
        curr.execute(DataFlowPackage_)
        c = curr.fetchall()
        DF_table = c

    with connection() as conn:
        # FEDF package

        curr = conn.cursor()
        ForEachDF_ = "SELECT [foreach_connection] ,[foreach_query_expr],[src_connection],[src_query_expr],[dst_connection],[dst_schema],[dst_table],[dst_truncate],[keep_identity],[package_name]" \
                     ",[use_bulk_copy],[batch_size] FROM [elt].[package_config_foreach_data_flow]"
        curr.execute(ForEachDF_)
        c = curr.fetchall()
        ForEachDF = c

    with connection() as conn:
        # EXSQL package

        curr = conn.cursor()
        ExecSql_ = "SELECT [connection_manager],[query] ,[is_expression]   ,[return_row_count] ,[package_name] FROM [elt].[package_config_execute_sql]"
        curr.execute(ExecSql_)
        c = curr.fetchall()
        ExecSql = c

    with connection() as conn:
        # EXProc package

        curr = conn.cursor()
        ExecProc_ = "SELECT [executable_expr],[arguments_expr],[working_directory],[place_values_in_ELT_Data],[package_name] FROM [elt].[package_config_execute_process]"
        curr.execute(ExecProc_)
        c = curr.fetchall()
        ExecProc = c

    with connection() as conn:
        # JSONTT package

        curr = conn.cursor()
        JSONtt_ = "SELECT [src_connection] ,[table_selection_option],[table_list],[flat_file_connection],[dst_connection],[package_name] FROM [elt].[package_config_json_table_transfer]"
        curr.execute(JSONtt_)
        c = curr.fetchall()
        JSONtt = c

    with connection() as conn:
        # SS data package

        curr = conn.cursor()
        SemiS_ = "SELECT [src_connection],[dst_connection],[dst_schema],[dst_tables_init_option],[package_name] FROM [elt].[package_config_semi_struct_load]"
        curr.execute(SemiS_)
        c = curr.fetchall()
        SemiS = c

    with connection() as conn:
        # FEXSQL package
        curr = conn.cursor()
        ForEachSQL_ = "SELECT [foreach_connection],[foreach_query_expr],[query_connection],[query],[return_row_count],[package_name] FROM [elt].[package_config_foreach_execute_sql]"
        curr.execute(ForEachSQL_)
        c = curr.fetchall()
        ForEachSQL = c

    # project_enviroments
    enviroment_project = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        enviroment_project_st = "  select p.project_name, e.[environment_name] from [elt].[project] as p inner join [elt].[project_environment] as e on p.project_id=e.project_id;"
        curr.execute(enviroment_project_st)
        c = curr.fetchall()
        for e in c:
            enviroment_project[e[0]].append(e[1])
    # print(env_side)
    # exit()
    # pprint(enviroment_project)
    # exit()
    # for i,j in enviroment_project.items():
    #     # print(i,j)
    #     for m in j:
    #         print(m)
    # exit()

    # enviroments data details
    enviroments = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        env_side_ = "SELECT [environment_name],[build_template_group] FROM [elt].[environment]"
        curr.execute(env_side_)
        envs_build = curr.fetchall()
        env_side = [c[0] for c in envs_build]
        for i in env_side:
            enviroments_ = "SELECT ep.[parameter_name], e.[build_template_group], ep.[key_vault_name] FROM [elt].[environment_parameter] as ep inner join [elt].[environment] as e on ep.environment_name=e.environment_name where ep.environment_name='{0}'".format(
                i)
            curr.execute(enviroments_)
            c = curr.fetchall()
            enviroments[i].append(c)
            environ_package_columns = [col[0] for i, col in enumerate(curr.description) if i != 1]

    # projects_per enviroment
    proj_per_env = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        env_s_ = "SELECT distinct [environment_name] FROM [elt].[environment]"
        curr.execute(env_s_)
        ens = curr.fetchall()
        en = [c[0] for c in envs_build]
        for i in en:

            proj_per_env_query = "SELECT  p.[project_name] from elt.project as p right join" \
                                 " elt.project_environment as pe on pe.project_id=p.project_id where pe.environment_name = {0!r}".format(
                i)
            curr.execute(proj_per_env_query)
            c = curr.fetchall()
            c = [c[0] for c in c]
            for pair in c:
                proj_per_env[i].append(pair)

    # projects per pakackage
    proj_per_package_DF = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_DF_ = "SELECT pp.package_name,p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Data Flow%';"
        curr.execute(projs_per_package_DF_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_DF[pair[0]].append(pair[1])

    proj_per_package_FEDF = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_FEDF_ = "SELECT pp.package_name, p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Foreach Data%';"
        curr.execute(projs_per_package_FEDF_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_FEDF[pair[0]].append(pair[1])

    proj_per_package_EXSQL = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_EXSQL_ = "SELECT pp.package_name, p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Execute SQL%';"
        curr.execute(projs_per_package_EXSQL_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_EXSQL[pair[0]].append(pair[1])

    proj_per_package_FEEXSQL = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_FEEXSQL_ = "SELECT pp.package_name, p.project_name FROM .[elt].[project_package] as pp left join elt.project as p on p.project_id=pp.project_id where pp.package_name like '%Foreach Execute SQL%';"
        curr.execute(projs_per_package_FEEXSQL_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_FEEXSQL[pair[0]].append(pair[1])

    proj_per_package_EXPro = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_EXPro_ = "SELECT pp.package_name, p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Execute Process%';"
        curr.execute(projs_per_package_EXPro_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_EXPro[pair[0]].append(pair[1])

    proj_per_package_JJTS = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_JJTS_ = "SELECT pp.package_name, p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Json%';"
        curr.execute(projs_per_package_JJTS_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_JJTS[pair[0]].append(pair[1])

    proj_per_package_SSDT = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        projs_per_package_SSDT_ = "SELECT pp.package_name, p.project_name  FROM .[elt].[project_package] as pp  left join elt.project as p	on p.project_id=pp.project_id   where pp.package_name like '%Semi-Structured%';"
        curr.execute(projs_per_package_SSDT_)
        ppp = curr.fetchall()
        for pair in ppp:
            if pair[1] != None:
                proj_per_package_SSDT[pair[0]].append(pair[1])

    with connection() as conn:
        curr = conn.cursor()
        connections_query = "SELECT  [connection_name] FROM [elt].[oledb_connection]"
        curr.execute(connections_query)
        c = curr.fetchall()
        connections = [m[0] for m in c]

    with connection() as conn:
        curr = conn.cursor()
        connection_details_ = "SELECT [connection_name],[server_name],[database_name],[provider],[connection_expression] FROM [elt].[oledb_connection]"
        curr.execute(connection_details_)
        c = curr.fetchall()
        connection_details = c

    conns_projects = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        get_conections_by_projects = "SELECT *FROM [elt].[show projects using connection] (?)"
        for k in connections:
            curr.execute(get_conections_by_projects, k)
            c = curr.fetchall()
            c1 = [p[0] for p in c]
            conns_projects[k].append(c1)

    conns_packages = defaultdict(list)
    with connection() as conn:
        curr = conn.cursor()
        get_conections_by_packages = "SELECT * FROM [elt].[show packages using connection] (?)"
        for k in connections:
            curr.execute(get_conections_by_packages, k)
            c = curr.fetchall()
            c1 = [p[0] for p in c]
            conns_packages[k].append(c1)

    import datetime
    filename = os.path.join(PATH, 'eltSnap_Project_HTML.html')
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'html')

    shutil.copy2(os.path.join(templates_dir, 'eltstyle.css'), PATH)
    shutil.copy2(os.path.join(templates_dir, 'images', 'eltSnap_whiteTransparent.png'), PATH)

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('HTML_template.html')

    with open(filename, 'w') as writer:
        writer.write(template.render(
            h1="eltSnap Projects",
            published=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            project_name="Project Name",
            project_set=project_set,
            project_package_set=project_package_set,
            project_package_columns=project_package_columns,
            proj_per_package_DF=proj_per_package_DF,
            proj_per_package_FEDF=proj_per_package_FEDF,
            proj_per_package_EXSQL=proj_per_package_EXSQL,
            proj_per_package_FEEXSQL=proj_per_package_FEEXSQL,
            proj_per_package_EXPro=proj_per_package_EXPro,
            proj_per_package_JJTS=proj_per_package_JJTS,
            proj_per_package_SSDT=proj_per_package_SSDT,
            DF_table=DF_table,
            ExecSql=ExecSql,
            ForEachDF=ForEachDF,
            ExecProc=ExecProc,
            ForEachSQL=ForEachSQL,
            connections=connections,
            connection_details=connection_details,
            conns_projects=conns_projects,
            conns_packages=conns_packages,
            enviroment_project=enviroment_project,
            enviroments=enviroments,
            environ_package_columns=environ_package_columns,
            env_side=env_side,
            envs_build=envs_build,
            proj_per_env=proj_per_env,
            JSONtt=JSONtt,
            SemiS=SemiS
        ))

    # time.sleep(0.1)
    print(f'The HTML file destination is on the location : {filename}')