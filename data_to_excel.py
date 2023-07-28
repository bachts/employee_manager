import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import itertools
from django.db import connection

user_name = 'postgres'
password = 'password'


# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/okr')


# tên nhân viên - create_by_id 
# cấp bậc - create_by_id
# tên team - create_by_id
# Loại - type (okr_kpis)
# KR phòng - chưa có 
# KR team - chưa có
# KR cá nhân - title (okr_kpis)
# công thức tính - chưa có 
# nguồn dữ liệu - chưa có 
# định kỳ tính - regularly (okr_kpis)
# đơn vị tính - unit (okr_kpis)
# điều kiện - condition (okr_kpis)
# norm - norm (okr_kpis)
# % Trọng số chỉ tiêu - weight (okr_kpis)
# Kết quả - result (okr_kpis)
# Tỷ lệ % - result*weight
# Tổng thời gian dự kiến/ ước tính công việc (giờ) - 
# Tổng thời gian thực hiện công việc thực tế (giờ) - 
# Note dự kiến -   


full_sql = """select *
from
(select 
key_result_department as kr_phong,
key_result_team as kr_team, 
key_result_personal as kr_personal, 
type, 
"OKR_okr".id as okr_kpi_id, 
unit, 
deadline, 
norm, 
weight, 
ratio, 
condition, 
result, 
status, 
objective_name, 
files,
user_id, 
regularity

from "OKR_okr", "OKR_objective"
where "OKR_okr".id = "OKR_objective".id) t1

left join 
(select id, full_name, level, position, team_id, department_id
from "Employee_employee") t2
on t1.user_id = t2.id

left join
(select team_id, name as team_name
from "Employee_team") t3
on t2.team_id = t3.team_id

left join
(select department_id, name as department_name
from "Employee_department") t4
on t2.department_id = t4.department_id
"""

# full_df = pd.read_sql(full_sql, engine)


# columns = ['kr_phong', 'kr_team', 'kr_personal', 'type', 'okr_kpi_id', 'unit',
#        'deadline', 'norm', 'weight', 'ratio', 'condition', 'result', 'status',
#        'objective_name', 'files', 'user_id', 'id', 'full_name', 'level',
#        'id', 'employee_code', 'position', 'team_id', 'department_id',
#        'team_id', 'team_name', 'department_id', 'department_name']

def nhanvien() -> None:
    # NO_LEVEL = -1, 'No Level'
    #     SVCNTS = 0, 'SVCNTS'
    #     L1 = 1, 'L1'
    #     L2 = 2, 'L2'
    #     L3 = 3, 'L3' 
    cursor= connection.cursor()
    cursor.execute(
            '''select   ee.id as employeecode,
                        full_name as fullName,
                        level,
                        ee.team_id as teamId,
                        name as teamName,
                        type,
                        oo.key_result_department as krDep,
                        oo.key_result_team as krTeam,
                        oo.key_result_personal as krPer,
                        ofo.formula_name as formulaName,
                        ofo.formula_value as formulaValue,
                        os.source_name as sourceName,
                        oo.regularity,
                        oo.unit,
                        oo.condition,
                        oo.weight,
                        oo.result,
                        oo.weight*oo.result as ratio,
                        oo.estimated,
                        oo.actual,
                        oo.note
                        FROM "Employee_employee" as ee,
                            "Employee_team" as et,
                            "OKR_okr" as oo,
                            "OKR_formula" as ofo,
                            "OKR_source" as os
                        where ee.team_id=et.team_id 
                            and ee.id=oo.user_id 
                            and oo.formula_id=ofo.id 
                            and oo.source_id=os.id'''

            )
    result = cursor.fetchall()
    df_result= pd.DataFrame(result)
    column_order = ['employeeId', 'fullName', 'level', 'teamId', 'teamName',
                    'Loại', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 
                    'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
                    '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
                        'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']
                    

    nhanvien_df = df_result[column_order]
    # print(nhanvien_df.dtypes)
    nhanvien_df.sort_values('id', inplace=True)
    nhanvien_df.fillna('No data', inplace=True)
    # nhanvien_df.set_index(['id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
    
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
    column_order = ['okr_kpi_id', 'id', 'full_name', 'department_name', 'team_name',
                    'objective_name', 'kr_phong', 'regularity', 'unit', 'condition',
                    'result', 'deadline', 'status', 'files']
    quarter_df = quarter_df[column_order]
    quarter_df = quarter_df.fillna('No data')
    quarter_df = quarter_df.set_index(['department_name', 'team_name', 'id', 'full_name', 'okr_kpi_id', 'objective_name'])
    quarter_df.to_excel('quarter.xlsx')


    #thieu nguon du lieu





nhanvien()



