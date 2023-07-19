import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import itertools

user_name = 'bach'
password = 'password'


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/okr')

full_sql = """select *
from
(select key_result_department as kr_phong, key_result_team as kr_team, key_result_personal as kr_personal, 
type, "OKR_okr".id as okr_kpi_id, unit, deadline, norm, weight, ratio, condition, result, status, objective_name, files,
user_id, regularity
from "OKR_okr", "OKR_objective"
where "OKR_okr".id = "OKR_objective".id) t1

left join 
(select id, full_name, level
 from "users_myuser") t2
on t1.user_id = t2.id

left join
(select employee_id, name as employee_code, position, team_id, department_id
from "Employee_employee") t3
on t2.id = t3.employee_id

left join
(select team_id, name as team_name
from "Employee_team") t4
on t3.team_id = t4.team_id

left join
(select department_id, name as department_name
from "Employee_department") t5
on t3.department_id = t5.department_id
"""

full_df = pd.read_sql(full_sql, engine)


columns = ['kr_phong', 'kr_team', 'kr_personal', 'type', 'okr_kpi_id', 'unit',
       'deadline', 'norm', 'weight', 'ratio', 'condition', 'result', 'status',
       'objective_name', 'files', 'user_id', 'id', 'full_name', 'level',
       'employee_id', 'employee_code', 'position', 'team_id', 'department_id',
       'team_id', 'team_name', 'department_id', 'department_name']
def nhanvien() -> None:
    # NO_LEVEL = -1, 'No Level'
    #     SVCNTS = 0, 'SVCNTS'
    #     L1 = 1, 'L1'
    #     L2 = 2, 'L2'
    #     L3 = 3, 'L3' 

    column_order = ['okr_kpi_id', 'employee_id', 'full_name', 'department_name', 'team_name',
                    'position', 'type', 'objective_name', 'kr_phong', 'kr_team', 'kr_personal', 
                    'unit', 'condition', 'norm', 'weight', 'ratio', 'result', 'status', 'files', 'level']
                    

    nhanvien_df = full_df[column_order]
    print(nhanvien_df.dtypes)
    nhanvien_df.sort_values('employee_id', inplace=True)
    nhanvien_df.fillna('No data', inplace=True)
    nhanvien_df.set_index(['employee_id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
    
    levels = {
        -1: 'NoLevel',
        0: 'SVCNTS',
        1: 'L1',
        2: 'L2',
        3: 'L3'
    }
    for value, str in levels.items():
        temp_df = nhanvien_df.loc[nhanvien_df['level']==value]
        temp_df.drop(columns=['level'], axis=1)
        temp_df.to_excel(f'nhanvien{str}.xlsx')

def department() -> None:
    column_order = ['okr_kpi_id', 'full_name', 'department_name', 'type',
                    'objective_name', 'kr_phong', 'kr_team', 'kr_personal', 'unit',
                    'condition', 'norm', 'weight', 'ratio',  'result', 'status', 'deadline'] 

    department_df = full_df[column_order]
    department_df['deadline'] = department_df['deadline'].dt.tz_localize(None)

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

    

    quarter_df = full_df.loc[full_df['type'] == 'okr']
    quarter_df['deadline'] = quarter_df['deadline'].dt.tz_localize(None)
    column_order = ['okr_kpi_id', 'employee_code', 'full_name', 'department_name', 'team_name',
                    'objective_name', 'kr_phong', 'regularity', 'unit', 'condition',
                    'result', 'deadline', 'status', 'files']
    quarter_df = quarter_df[column_order]
    quarter_df = quarter_df.fillna('No data')
    quarter_df = quarter_df.set_index(['department_name', 'team_name', 'employee_code', 'full_name', 'okr_kpi_id', 'objective_name'])
    quarter_df.to_excel('quarter.xlsx')


    #thieu nguon du lieu





nhanvien()
department()
okr_quarter()