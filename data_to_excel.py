import pandas as pd
import os
import openpyxl
from django.db import connection
from openpyxl import Workbook
from openpyxl.styles import Font

def GenerateExcelSheet(basedir,levels) -> None:
    cursor= connection.cursor()
    cursor.execute(
            '''select   ee.id as employeecode,
                        full_name as fullName,
                        level,
                        ee.team_id as teamId,
                        name as teamName,
                        type,
                        oo.kr_id as krId,
                        oo.key_result_department as krDep,
                        oo.key_result_team as krTeam,
                        oo.key_result_personal as krPer,
                        ofo.formula_name as formulaName,
                        ofo.formula_value as formulaValue,
                        os.source_name as sourceName,
                        oo.regularity,
                        oo.unit,
                        oo.condition,
                        oo.norm,
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
    dataframe= pd.DataFrame(result)
    # for column in dataframe:  
    #     print("các column: ", dataframe)

    dataframe.columns= ['employeeId', 'fullName', 'level', 'teamId', 'teamName',
                    'Loại', 'krId', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 'Giá trị tính',
                    'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
                    '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
                        'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']    
   
    # pandas sẽ group lại các KPI ở đây theo employeeid và kr_id từ đó lấy được các pair kr của các kpi
    # tính toán tổng "trọng số chỉ tiêu", "kết quả", "tỷ lệ", "tổng thời gian dự kiến" lưu vào thành 1 hashmap theo key là (employee_id, kr_id) và value là một list các tổng đã tính
    

    dataframe.sort_values('employeeId', inplace=True)
    dataframe.drop(columns=['employeeId'], axis=1, inplace=True)
    dataframe.drop(columns=['teamId'], axis=1, inplace=True)   
    dataframe.drop(columns=['Giá trị tính'], axis=1, inplace=True)    

    dataframe.fillna('No data', inplace=True)
    # dataframe.set_index(['id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
    for value, str in levels.items():
        temp_df = dataframe.loc[dataframe['level']==value]
        temp_df.drop(columns=['level'], axis=1)
        if os.path.exists(basedir+f"\nhóm {str}.xlsx"):
            os.remove(basedir+f"\nhóm {str}.xlsx")
        temp_df.to_excel(f'nhóm {str}.xlsx')
    # loop qua từng sheet do mỗi sheet đều có format giống nhau
    workbook = Workbook()


# def department() -> None:
#     column_order = ['okr_kpi_id', 'full_name', 'department_name', 'type',
#                     'objective_name', 'kr_phong', 'kr_team', 'kr_personal', 'unit',
#                     'condition', 'norm', 'weight', 'ratio',  'result', 'status', 'deadline'] 

#     department_df = full_df[column_order]
#     department_df['deadline'] = department_df['deadline'].dt.tz_localize(None)

#     def do_nothing(x):
#         return x

#     # department_df.set_index(['department_name', 'type'], inplace=True)
#     # print(department_df)
#     department_df = department_df.fillna('No data')
#     # department_df = department_df.groupby(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'weight']).agg({
#     #     'full_name': do_nothing, # lambda x: ', '.join(x),
#     #     'kr_phong': do_nothing,
#     #     'kr_team': do_nothing,
#     #     'unit': do_nothing,
#     #     'condition': do_nothing,
#     #     'norm': do_nothing,
#     #     'weight': do_nothing,
#     #     'ratio': do_nothing,
#     #     'result': do_nothing,
#     #     'deadline': do_nothing,
#     # })
#     department_df = department_df.set_index(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'kr_phong', 'kr_team'])
        # dataframe.rename(columns={"0": "employeeId"}, inplace=True)
        # dataframe.rename(columns={"1": "fullName"}, inplace=True)
        # dataframe.rename(columns={"2": "level"}, inplace=True)
        # dataframe.rename(columns={"3": "teamId"}, inplace=True)
        # dataframe.rename(columns={"4": "teamName"}, inplace=True)
        # dataframe.rename(columns={"5": "Loại"}, inplace=True)
        # dataframe.rename(columns={"6": "KR phòng"}, inplace=True)
        # dataframe.rename(columns={"7": "KR team"}, inplace=True)
        # dataframe.rename(columns={"8": "KR cá nhân"}, inplace=True)
        # dataframe.rename(columns={"9": "Công thức tính"}, inplace=True)
        # dataframe.rename(columns={"10": "Nguồn dữ liệu"}, inplace=True)
        # dataframe.rename(columns={"11": "Định kỳ tính"}, inplace=True)
        # dataframe.rename(columns={"12": "Đơn vị tính"}, inplace=True)
        # dataframe.rename(columns={"13": "Điều kiện"}, inplace=True)
        # dataframe.rename(columns={"14": "Norm"}, inplace=True)
        # dataframe.rename(columns={"15": "% Trọng số chỉ tiêu"}, inplace=True)
        # dataframe.rename(columns={"16": "Kết quả"}, inplace=True)
        # dataframe.rename(columns={"17": "Tỷ lệ"}, inplace=True)
        # dataframe.rename(columns={"18": "Tổng thời gian dự kiến/ ước tính công việc (giờ)"}, inplace=True)
        # dataframe.rename(columns={"19": "Tổng thời gian thực hiện công việc thực tế (giờ)"}, inplace=True)
        # dataframe.rename(columns={"20": "Note"}, inplace=True)

#     department_df.to_excel('department.xlsx')

# def okr_quarter() -> None:

    

#     quarter_df = full_df.loc[full_df['type'] == 'okr']
#     quarter_df['deadline'] = quarter_df['deadline'].dt.tz_localize(None)
#     column_order = ['okr_kpi_id', 'id', 'full_name', 'department_name', 'team_name',
#                     'objective_name', 'kr_phong', 'regularity', 'unit', 'condition',
#                     'result', 'deadline', 'status', 'files']
#     quarter_df = quarter_df[column_order]
#     quarter_df = quarter_df.fillna('No data')
#     quarter_df = quarter_df.set_index(['department_name', 'team_name', 'id', 'full_name', 'okr_kpi_id', 'objective_name'])
#     quarter_df.to_excel('quarter.xlsx')


