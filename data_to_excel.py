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
    
    # merge các tổng đã tính ở trên vào một hàng và tìm vị trị cần điền các tổng đó trong dataframe gốc
    max_indices = df_data_sum.groupby('employeeId')['krId'].idxmax()
    merged_sum_idx_df = pd.merge(max_indices, df_time_sum, on='employeeId', how='left')
    merged_sum_idx_df.drop(columns=['employeeId'], axis=1, inplace=True)
    krId_to_idx=merged_sum_idx_df.set_index('krId') 
    merged_sum_df = pd.merge(df_data_sum, krId_to_idx, left_index=True, right_index=True, how='left')
    merged_sum_df.fillna(0, inplace=True)
    merged_sum_df[et] = merged_sum_df[et].apply(lambda x: '' if x == 0 else x)
    merged_sum_df[rt] = merged_sum_df[rt].apply(lambda x: '' if x == 0 else x)
    # print("đây là merged_sum_df: \n",merged_sum_df)

    # sắp xếp lại và lấy vị trí các đoạn cần insert các tổng vào (need_add_index_df), đồng thời dùng sorted_df cho các thao tác sau (sorted_df) 
    sorted_df=df.sort_values(by=['employeeId', 'krId'], ascending=[True, True]).reset_index()
    sorted_df.drop(columns=['index'], axis=1, inplace=True)
    # print("dataframe sorted_df: \n",sorted_df)
    index_sorted_df=sorted_df[['employeeId','krId']]
    # Tạo một cột boolean cho biết các hàng có là bản sao của hàng trước đó hay không
    is_duplicated = index_sorted_df.duplicated(subset=['employeeId', 'krId'], keep='last')
    # Chỉ giữ lại các hàng cuối cùng của mỗi cặp giá trị bằng nhau
    need_add_index_df = index_sorted_df[~is_duplicated]
    # print("đây là need_add_index_df : \n",need_add_index_df)
    # thêm các kết quả đã tính toán ở trên vào cuối của mỗi kpi
    added_row=0
    for (index, i) in zip(need_add_index_df.index,range(len(merged_sum_df))):
            df_new_record = pd.DataFrame(merged_sum_df.iloc[i, :]).T
            sorted_df=pd.concat([sorted_df.iloc[:index+added_row+1], df_new_record, sorted_df.iloc[index+added_row+1:]]).reset_index(drop=True)
            added_row+=1
    sorted_df.drop(columns=[None], axis=1, inplace=True)
    sorted_df = sorted_df.apply(lambda x: '' if x.empty else x)
    # print("đây là sorted_df mới : \n",sorted_df)


    # 1. tạo ra các dataframe chứa tên, level, tên nhóm và dataframe chưa tên các cột  (user_df)
    grouped = sorted_df.groupby(['employeeId', 'Name', 'level', 'teamName'])
    user_df = grouped.size().reset_index(name='Count')
    # print("đây là user_df : \n",user_df)

    # Create a new DataFrame to store the column names (names_df)
    columns_to_drop = ['employeeId', 'Name', 'level', 'teamName', 'krId']
    insert_header_name_df = sorted_df.drop(columns=columns_to_drop, axis=1)
    names_df = pd.DataFrame([insert_header_name_df.columns], columns=insert_header_name_df.columns)
    # print("đây là user_df : \n",names_df)

    # 2. tạo ra một list chứa các vị trí cần add các record đó vào bằng cách tìm các vị trí đầu xuất hiện của các record
    # Tạo cột mới để xác định lần xuất hiện đầu tiên của giá trị trùng nhau
    sorted_df['FirstOccurrence'] = ~sorted_df.duplicated(subset=['employeeId'])
    # lấy lần xuất hiện đầu tiên của các giá trị trùng nhau (firstOccurrence_df)
    firstOccurrence_df = sorted_df[sorted_df['FirstOccurrence']].drop(columns='FirstOccurrence')
    firstOccurrence_list = firstOccurrence_df.index
    # print("đây là firstOccurrence_df : \n",firstOccurrence_list)

    # 3. dùng openpyxl thêm các header vào các vị trí(2.) là:
    #                                      - các record(1.)
    #                                      - các record tên cột(1.)
    #                                      - Tên nhóm là header chính

    # Chuyển DataFrame thành một đối tượng Sheet bằng pandas dataframe_to_rows
    user_rows = list(dataframe_to_rows(user_df, index=False, header=True))
    column_name_rows = list(dataframe_to_rows(names_df, index=False, header=True))
    rows = dataframe_to_rows(sorted_df, index=False, header=True)

    # Ghi dữ liệu từ DataFrame vào Workbook
    level=sorted_df['level'][0].astype(int)
    # Gán tiêu đề cho sheet
    header_text = "Nhóm L"+level
    sheet.title = header_text

    for i in range(len(sorted_df)):  # 10 là số lần lặp để tạo dữ liệu mẫu, bạn có thể thay đổi số này theo yêu cầu
        df_idx = i % len(dataframes)  # Lấy index của DataFrame hiện tại (lặp lại từ 0 đến 3)
        df = dataframes[df_idx]  # Lấy DataFrame hiện tại từ danh sách dataframes
        for row in dataframe_to_rows(df, index=False, header=False):
            sheet.append(row)

    # Chuyển đổi DataFrame thành danh sách các dòng
    

    # Chèn các dòng vào vị trí xác định (từ dòng 2 trở đi)
    for r_idx, row in enumerate(rows, 2):
        for c_idx, value in enumerate(row, 1):
            sheet.cell(row=r_idx, column=c_idx, value=value)

    # Lưu Workbook
    # wb.save(file_path)




# formatKPIExcelSheet("excelSheet/nhóm L2.xlsx")


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


