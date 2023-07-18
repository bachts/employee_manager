import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import itertools

user_name = 'bach'
password = 'password'


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/bach')

full_sql = """select * 
from
(select employees.id as id, employees.employee_code as employee_code, okr_kpis.deadline, okr_kpis.regularly as regularity,employees.full_name as full_name,okr_kpis.objective_id as okr_kpi_id, type, objective_name, key_result_name as kr_phong, unit, condition, norm, weight, ratio, result, status, departments.name as department_name
from okr_kpis, okr_kpis_employee_links, employees, employees_department_links, departments
where okr_kpis.id = okr_kpis_employee_links.okr_kpi_id
and okr_kpis_employee_links.employee_id = employees.id
and employees.id = employees_department_links.employee_id
and employees_department_links.department_id = departments.id) t1

left join

(select employees.id as t2_id, key_result_name as kr_team, teams.name as team_name
from okr_kpis, okr_kpis_employee_links, employees, employees_team_links, teams
where okr_kpis.id = okr_kpis_employee_links.okr_kpi_id
and okr_kpis_employee_links.employee_id = employees.id
and employees.id = employees_team_links.employee_id
and employees_team_links.team_id = teams.id) t2

on t1.id = t2.t2_id

left join
(select employees.id as t3_id, role_employees.name as role_name
from employees, employees_role_employee_links, role_employees
where employees.id = employees_role_employee_links.employee_id
 and employees_role_employee_links.role_employee_id = role_employees.id) t3
on t1.id = t3.t3_id

left join

(select okr_kpis.id as t4_id, proofs.name as proof_name, proofs.description proof_description, proofs.url
from okr_kpis, proofs_okr_kpi_links, proofs
where okr_kpis.id = proofs_okr_kpi_links.okr_kpi_id
and proofs_okr_kpi_links.proof_id = proofs.id) t4
on t1.okr_kpi_id = t4.t4_id
order by t1.okr_kpi_id"""

full_df = pd.read_sql(full_sql, engine)

def nhanvien() -> None:

    nhanvien_df = full_df.drop(columns=['t2_id', 't3_id', 't4_id'], axis=1)
    column_order= ['okr_kpi_id', 'employee_code', 'full_name', 'department_name', 'team_name', 'role_name', 'type', 'objective_name', 'kr_phong', 'kr_team', 'unit', 'condition', 
                  'norm', 'weight', 'ratio', 'result', 'status', 'proof_name', 'proof_description', 'url']
    nhanvien_df = nhanvien_df[column_order]
    nhanvien_df.sort_values('employee_code', inplace=True)
    nhanvien_df.fillna('No data', inplace=True)
    # index = pd.MultiIndex.from_tuples(tuples=['employee_code', 'okr_kpi_id'])
    # print(nhanvien_df.groupby(['employee_code', 'okr_kpi_id', 'type']))
    nhanvien_df.set_index(['employee_code', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
    nhanvien_df.to_excel('nhanvien.xlsx')


def department() -> None:
    department_df = full_df.drop(columns=['t2_id', 't3_id', 't4_id', 'url', 'employee_code', 'proof_name', 'proof_description', 'team_name', 'role_name'], axis=1)

    column_order = ['okr_kpi_id', 'full_name', 'department_name', 'type', 'objective_name', 'kr_phong', 'kr_team', 'unit', 'condition', 
                  'norm', 'weight', 'ratio', 'result', 'status', 'deadline']
    department_df = department_df[column_order]

    def do_nothing(x):
        return x

    # department_df.set_index(['department_name', 'type'], inplace=True)
    # print(department_df)
    department_df = department_df.fillna('No data')
    # department_df = department_df.groupby(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'weight']).agg({
    #     'full_name': do_nothing, # lambda x: ', '.join(x),
    #     'kr_phong': do_nothing,
    #     'kr_team': do_nothing,
    #     'unit': do_nothing,
    #     'condition': do_nothing,
    #     'norm': do_nothing,
    #     'weight': do_nothing,
    #     'ratio': do_nothing,
    #     'result': do_nothing,
    #     'deadline': do_nothing,
    # })
    department_df = department_df.set_index(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'kr_phong', 'kr_team'])


    department_df.to_excel('department.xlsx')

def okr_quarter() -> None:
    quarter_df = full_df.drop(columns=['t2_id', 't3_id', 't4_id'], axis=1)
    quarter_df = quarter_df.loc[quarter_df['type'] == 'okr']
    quarter_df['deadline'] = quarter_df['deadline'].astype('string')
    column_order= ['okr_kpi_id', 'employee_code', 'full_name', 'department_name', 'team_name', 'objective_name', 'kr_phong', 'regularity', 'unit', 'condition', 
                   'result', 'deadline', 'status', 'proof_name', 'proof_description',]
    quarter_df = quarter_df[column_order]
    quarter_df = quarter_df.fillna('No data')
    quarter_df = quarter_df.set_index(['department_name', 'team_name', 'employee_code', 'full_name', 'okr_kpi_id', 'objective_name'])
    quarter_df.to_excel('quarter.xlsx')


    #thieu nguon du lieu





nhanvien()
department()
okr_quarter()