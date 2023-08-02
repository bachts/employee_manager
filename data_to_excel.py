import pandas as pd
import os
import openpyxl
from django.db import connection
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def GenerateExcelSheet(basedir,levels) -> None:
        cursor= connection.cursor()
        cursor.execute(
                '''select   ee.id as employeecode,
                            full_name as name,
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

        dataframe.columns= ['employeeId', 'Name', 'level', 'teamId', 'teamName',
                        'Loại', 'krId', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 'Giá trị tính',
                        'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
                        '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
                            'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']    
    
        dataframe.sort_values('employeeId', inplace=True)
        # dataframe.drop(columns=['employeeId'], axis=1, inplace=True)
        dataframe.drop(columns=['teamId'], axis=1, inplace=True)   
        dataframe.drop(columns=['Giá trị tính'], axis=1, inplace=True)    
        dataframe.replace("NUM","%", inplace=True)
        dataframe.replace("CAT","Đạt/Không đạt", inplace=True)
        dataframe.replace("MO","Tháng", inplace=True)
        dataframe.replace("QUAR","Quý", inplace=True)
        dataframe.replace("EQUAL","=", inplace=True)
        dataframe.fillna(0, inplace=True)
        # dataframe.set_index(['id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
        for value, str in levels.items():
            temp_df = dataframe.loc[dataframe['level']==value]
            temp_df.drop(columns=['level'], axis=1)
            if os.path.exists(basedir+f"\\nhóm {str}.xlsx"):
                os.remove(basedir+f"\\nhóm {str}.xlsx")
            temp_df.to_excel(basedir+f'\\nhóm {str}.xlsx')
    

def formatKPIExcelSheet(file_path) -> None:
    wb = load_workbook(file_path)
    sheet = wb.active
    data = sheet.values
    columns = next(data)  # Lấy tên cột từ hàng đầu tiên
    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame(data, columns=columns)
    tsct = '% Trọng số chỉ tiêu'
    kq = 'Kết quả'
    tl = 'Tỷ lệ'
    et = 'Tổng thời gian dự kiến/ ước tính công việc (giờ)'
    rt = 'Tổng thời gian thực hiện công việc thực tế (giờ)'
    df[tsct]=df[tsct].astype(int)
    df[kq]=df[kq].astype(float)
    df[tl]=df[tl].astype(float)
    df[et]=df[et].astype(float)
    df[rt]=df[rt].astype(float)
    # tính tổng các trường cần tính
    tsct_sum=df.groupby(['employeeId', 'krId'])[tsct].sum().reset_index()
    kq_sum=df.groupby(['employeeId', 'krId'])[kq].sum().reset_index()
    tl_sum=df.groupby(['employeeId', 'krId'])[tl].sum().reset_index()
    et_sum=df.groupby(['employeeId'])[et].sum().reset_index()
    rt_sum=df.groupby(['employeeId'])[rt].sum().reset_index()
    # Tạo DataFrame chứa các tổng
    df_data_sum = pd.DataFrame({'employeeId': tsct_sum['employeeId'],
                           'krId': tsct_sum['krId'],
                           tsct: tsct_sum[tsct],
                           kq: kq_sum[kq],
                           tl: tl_sum[tl]})
    df_time_sum = pd.DataFrame({'employeeId': et_sum['employeeId'],
                           et: et_sum[et],
                           rt: rt_sum[rt]}) 

    # Tìm các KrId lớn nhất(hay kr phía sau) để lưu kết quả giờ làm vào hàng đó (merged_sum_df)
    max_indices = df_data_sum.groupby('employeeId')['krId'].idxmax()
    merged_sum_idx_df = pd.merge(max_indices, df_time_sum, on='employeeId', how='left')
    merged_sum_idx_df.drop(columns=['employeeId'], axis=1, inplace=True)
    krId_to_idx=merged_sum_idx_df.set_index('krId') 
    merged_sum_df = pd.merge(df_data_sum, krId_to_idx, left_index=True, right_index=True, how='left')
    merged_sum_df.fillna(0, inplace=True)

    # sắp xếp lại và lấy vị trí các đoạn cần insert các tổng vào (need_add_index_df), đồng thời dùng các dataframe đã được sắp xếp cho các insert row sau
    print("đây là sheet: \n",merged_sum_df)
    sorted_df=df.sort_values(by=['employeeId', 'krId'], ascending=[True, True]).reset_index()
    sorted_df.drop(columns=['index'], axis=1, inplace=True)
    print("dataframe mới: \n",sorted_df)
    index_sorted_df=sorted_df[['employeeId','krId']]
    # Tạo một cột boolean cho biết các hàng có là bản sao của hàng trước đó hay không
    is_duplicated = index_sorted_df.duplicated(subset=['employeeId', 'krId'], keep='last')
    # Chỉ giữ lại các hàng cuối cùng của mỗi cặp giá trị bằng nhau
    need_add_index_df = index_sorted_df[~is_duplicated]
    # print("đây là index max -1 : \n",need_add_index_df)

    # thêm các tổng đã tính bên trên vào các index mới tìm ở trên
    for row in dataframe_to_rows(merged_sum_df, index=False, header=False):
        print("gia trị index:", index)
        sheet.insert_rows(index, amount=1)
        for col, value in enumerate(row, start=1):
            sheet.cell(row=index, column=col, value=value)
    new_data = sheet.values
    new_columns = next(new_data) 
    new_df = pd.DataFrame(new_data, columns=new_columns)
    # print("dataframe mới: \n",new_df)
    # # Thêm một hàng trống sau mỗi nhóm của DataFrame chứa các tổng
    # df_sum[tsct] = df_sum[tsct].astype(str).str.cat(sep=' ')
    # df_sum[kq] = df_sum[kq].astype(str).str.cat(sep=' ')
    # df_sum[tl] = df_sum[tl].astype(str).str.cat(sep=' ')
    # df_sum = df_sum.replace(r'\s+', ' ', regex=True)
    # df_sum = df_sum.replace({tsct: {' ': '  '}, kq: {' ': '  '}, tl: {' ': '  '}}, regex=True)
    # # Thêm các tổng vào DataFrame
    # df = pd.concat([df, df_sum])



formatKPIExcelSheet("excelSheet/nhóm L2.xlsx")


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


