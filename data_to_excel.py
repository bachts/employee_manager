import pandas as pd
import os
import openpyxl
from django.db import connection
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill, Border, Side

def GenerateExcelSheet(basedir, levels) -> None:
        cursor = connection.cursor()
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
        dataframe = pd.DataFrame(result)
        # for column in dataframe:
        #     print("các column: ", dataframe)

        dataframe.columns = ['employeeId', 'Name', 'level', 'teamId', 'teamName',
                        'Loại', 'krId', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 'Giá trị tính',
                        'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
                        '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
                            'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']

        dataframe.sort_values('employeeId', inplace=True)
        # dataframe.drop(columns=['employeeId'], axis=1, inplace=True)
        dataframe.drop(columns=['teamId'], axis=1, inplace=True)
        dataframe.drop(columns=['Giá trị tính'], axis=1, inplace=True)
        dataframe.replace("NUM", "%", inplace=True)
        dataframe.replace("CAT", "Đạt/Không đạt", inplace=True)
        dataframe.replace("MO", "Tháng", inplace=True)
        dataframe.replace("QUAR", "Quý", inplace=True)
        dataframe.replace("EQUAL", "=", inplace=True)
        dataframe.fillna(0, inplace=True)
        # dataframe.set_index(['id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
        for value, str in levels.items():
            temp_df = dataframe.loc[dataframe['level'] == value]
            temp_df.drop(columns=['level'], axis=1)
            if os.path.exists(basedir+f"\\nhóm {str}.xlsx"):
                os.remove(basedir+f"\\nhóm {str}.xlsx")
            temp_df.to_excel(basedir+f'\\nhóm {str}.xlsx')


def excelToDataframe(file_path):
    wb = load_workbook(file_path)
    sheet = wb.active
    data = sheet.values
    columns = next(data)  # Lấy tên cột từ hàng đầu tiên
    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame(data, columns=columns)
    wb.close()
    return df


def formatKPIExcelSheet(file_path) -> None:

    # Tạo DataFrame từ dữ liệu
    df = excelToDataframe(file_path)
    tsct = '% Trọng số chỉ tiêu'
    kq = 'Kết quả'
    tl = 'Tỷ lệ'
    et = 'Tổng thời gian dự kiến/ ước tính công việc (giờ)'
    rt = 'Tổng thời gian thực hiện công việc thực tế (giờ)'
    df[tsct] = df[tsct].astype(int)
    df[kq] = df[kq].astype(float)
    df[tl] = df[tl].astype(float)
    df[et] = df[et].astype(float)
    df[rt] = df[rt].astype(float)
    # tính tổng các trường cần tính
    tsct_sum = df.groupby(['employeeId', 'krId'])[tsct].sum().reset_index()
    kq_sum = df.groupby(['employeeId', 'krId'])[kq].sum().reset_index()
    tl_sum = df.groupby(['employeeId', 'krId'])[tl].sum().reset_index()
    et_sum = df.groupby(['employeeId'])[et].sum().reset_index()
    rt_sum = df.groupby(['employeeId'])[rt].sum().reset_index()
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
    merged_sum_idx_df = pd.merge(
        max_indices, df_time_sum, on='employeeId', how='left')
    merged_sum_idx_df.drop(columns=['employeeId'], axis=1, inplace=True)
    krId_to_idx = merged_sum_idx_df.set_index('krId')
    merged_sum_df = pd.merge(df_data_sum, krId_to_idx,
                             left_index=True, right_index=True, how='left')
    merged_sum_df.fillna(0, inplace=True)
    merged_sum_df[et] = merged_sum_df[et].apply(lambda x: '' if x == 0 else x)
    merged_sum_df[rt] = merged_sum_df[rt].apply(lambda x: '' if x == 0 else x)
    # print("đây là merged_sum_df: \n",merged_sum_df)

    # sắp xếp lại và lấy vị trí các đoạn cần insert các tổng vào (need_add_index_df), đồng thời dùng sorted_df cho các thao tác sau (sorted_df)
    sorted_df = df.sort_values(by=['employeeId', 'krId'], ascending=[
                               True, True]).reset_index()
    sorted_df.drop(columns=['index'], axis=1, inplace=True)
    # print("dataframe sorted_df: \n",sorted_df)
    index_sorted_df = sorted_df[['employeeId', 'krId']]
    # Tạo một cột boolean cho biết các hàng có là bản sao của hàng trước đó hay không
    is_duplicated = index_sorted_df.duplicated(
        subset=['employeeId', 'krId'], keep='last')
    # Chỉ giữ lại các hàng cuối cùng của mỗi cặp giá trị bằng nhau
    need_add_index_df = index_sorted_df[~is_duplicated]
    # print("đây là need_add_index_df : \n",need_add_index_df)
    # thêm các kết quả đã tính toán ở trên vào cuối của mỗi kpi
    added_row = 0
    for (index, i) in zip(need_add_index_df.index, range(len(merged_sum_df))):
            df_new_record = pd.DataFrame(merged_sum_df.iloc[i, :]).T
            sorted_df = pd.concat([sorted_df.iloc[:index+added_row+1], df_new_record,
                                  sorted_df.iloc[index+added_row+1:]]).reset_index(drop=True)
            added_row += 1
    sorted_df.drop(columns=[None], axis=1, inplace=True)
    sorted_df = sorted_df.apply(lambda x: '' if x.empty else x)
    # print("đây là sorted_df mới : \n",sorted_df)

    # 1. tạo ra các dataframe chứa tên, level, tên nhóm và dataframe chưa tên các cột  (user_df)
    grouped = sorted_df.groupby(['employeeId', 'Name', 'level', 'teamName'])
    user_df = grouped.size().reset_index(name='Count')
    user_df.index.name = 'Index_column'
    user_df.drop(columns=['Count'], axis=1, inplace=True)
    # print("đây là user_df : \n",user_df)

    # Create a new DataFrame to store the column names (names_df)'
    columns_to_drop = ['employeeId', 'Name', 'level', 'teamName', 'krId']
    insert_header_name_df = sorted_df.drop(columns=columns_to_drop, axis=1)
    names_df = pd.DataFrame([insert_header_name_df.columns],
                            columns=insert_header_name_df.columns)
    # print("đây là user_df : \n",names_df)

    # 2. tạo ra một list chứa các vị trí cần add các record đó vào bằng cách tìm các vị trí đầu xuất hiện của các record
    # Tạo cột mới để xác định lần xuất hiện đầu tiên của giá trị trùng nhau
    sorted_df['FirstOccurrence'] = ~sorted_df.duplicated(subset=['employeeId'])
    # lấy lần xuất hiện đầu tiên của các giá trị trùng nhau (firstOccurrence_df)
    firstOccurrence_df = sorted_df[sorted_df['FirstOccurrence']].drop(
        columns='FirstOccurrence')
    firstOccurrence_list = firstOccurrence_df.index
    sorted_df = sorted_df.drop(columns='FirstOccurrence', axis=1)
    
    # 3. dùng openpyxl thêm các header vào các vị trí(2.) là:
    #                                      - các record(1.)
    #                                      - các record tên cột(1.)
    #                                      - Tên nhóm là header chính

    # Chuyển DataFrame thành một đối tượng Sheet bằng pandas dataframe_to_rows
    user_rows = list(dataframe_to_rows(user_df, index=False, header=False))
    if len(user_rows) != len(firstOccurrence_list):
        raise ValueError(
            "Số lượng dòng cần thêm phải bằng số dự liệu muốn thêm!")
    
    # tạo ra 1 dataframe có 3 hàng là tên các cột cần add vào sheet
    for i in range(len(user_rows)):
         names_df = pd.concat([names_df, names_df], ignore_index=True)

    # lấy vị trí các cột cần mở rộng khi align bằng openpyxl
    column_names = ['KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', et, rt, 'Note']
    column_positions = [names_df.columns.get_loc(col_name) for col_name in column_names]

    column_name_rows = list(dataframe_to_rows(names_df, index=False, header=False))
    rows = dataframe_to_rows(insert_header_name_df, index=False, header=False)

# ---------------------------------------------------------------------------------
    # tạo một sheet excel mới
    workbook = Workbook()
    sheet = workbook.active
    # Ghi dữ liệu từ DataFrame vào Workbook
    try:
        level = sorted_df['level'][0].astype(int).astype(str)
    except ValueError:
         print("Level đang không là số!")
         level = sorted_df['level'][0].astype(str)
    # Gán tiêu đề cho sheet
    header_text = "Nhóm L"+level
    sheet.cell(row=1, column=1, value=header_text)

    # Chèn các dòng vào vị trí xác định (từ dòng 2 trở đi)
    data_font = Font(name='Arial',size=11, bold=False)
    for r_idx, row in enumerate(rows, 2):
        for c_idx, value in enumerate(row, 1):
            sheet.cell(row=r_idx, column=c_idx, value=value)
            sheet.cell(row=r_idx, column=c_idx, value=value).font = data_font

    # thêm các dòng thông tin người dung và title của các trường vào sheet, đồng thời thêm màu, sửa font
    light_blue_fill = PatternFill(start_color='B8CCE4', end_color='B8CCE4', fill_type='solid')
    dark_blue_fill = PatternFill(start_color='365072', end_color='365072', fill_type='solid')
    title_font = Font(name='Arial',size=11, bold=True)
    
    added_sheet_row = 0
    for insert_index, row_user_data,row_column_name in zip(firstOccurrence_list, user_rows,column_name_rows):       
        user_insert = insert_index+added_sheet_row+2
        title_insert = insert_index+added_sheet_row+3
        sheet.insert_rows(user_insert, 1)
        sheet.insert_rows(title_insert, 1)
        for col_idx_user,user_value in enumerate(row_user_data, 1):
            sheet.cell(row=user_insert, column=col_idx_user, value=user_value)
            sheet.cell(row=user_insert, column=col_idx_user).fill = light_blue_fill
            sheet.cell(row=user_insert, column=col_idx_user).font = title_font
        for col_idx,column_name_value in enumerate(row_column_name,1):
            sheet.cell(row=title_insert, column=col_idx, value=column_name_value)
            sheet.cell(row=title_insert, column=col_idx).fill = dark_blue_fill
            sheet.cell(row=title_insert, column=col_idx).font = title_font


        if(insert_index!=0):
             blank_insert = insert_index+added_sheet_row+2
             sheet.insert_rows(blank_insert, 1) 
             added_sheet_row+=3       
        else:
             added_sheet_row+=2

    # Thiết lập tăng kích cỡ header
    for cell in sheet['1']:
	    cell.font = Font(size=16, bold=True)
    # Thiết lập tự động xuống dòng cho tất cả các ô
    for row in sheet.iter_rows(min_row=1, max_row=1):
        for cell in row:
            # Thiết lập tự động align vào giữa cho toàn bộ text trong sheet
            cell.alignment = Alignment(wrap_text=True,horizontal='center', vertical='center')
            
    # Thiết lập tự động tăng kích thước các cột
    # for col in sheet.columns:
    #     max_length = 0
    #     for cell in col:
    #         try:
    #             if len(str(cell.value)) > max_length:
    #                 max_length = len(cell.value)
    #         except:
    #             pass
    #     adjusted_width = (max_length + 2) * 1.2
    #     sheet.column_dimensions[col[0].column_letter].width = adjusted_width

    # Đặt viền cho các cell
    border = Border(left=Side(border_style='thin', color='000000'),
                    right=Side(border_style='thin', color='000000'),
                    top=Side(border_style='thin', color='000000'),
                    bottom=Side(border_style='thin', color='000000'))
    # Loop through each worksheet in the workbook
    for sheet in workbook.worksheets:
        # Loop through each row in the worksheet
        for row in sheet.iter_rows():
            # Loop through each cell in the row
            for cell in row:
                # Set wrap_text to True to automatically wrap text
                cell.alignment = openpyxl.styles.Alignment(wrapText=True)
                # thêm viền
                cell.border = border

        # Auto-adjust row height for all rows in the worksheet
        for row in sheet.iter_rows():
            sheet.row_dimensions[row[0].row].auto_size = True
    
            
    # Define a dictionary to store the desired column widths
    # column_widths = {'KR phòng': 20, 'KR team': 20, 'KR cá nhân': 20, 'Note': 20}  

    # Update the column widths
    for index in column_positions:
        print("index can tang do rong:",index+1)
        # đoạn này index +1 là vì vào sheet excel các index tính từ 1 chứ không còn là 0 như ở dataframe
        column_letter = openpyxl.utils.get_column_letter(index+1)
        sheet.column_dimensions[column_letter].width = 30
        
    # Đọc nội dung của sheet thành DataFrame
    data = sheet.values
    columns = next(data)  # Lấy tên cột từ dòng đầu tiên
    final_df = pd.DataFrame(data, columns=columns)  
    print("đây là excel file cuối : \n",final_df)

    # Lưu Workbook
    workbook.close()
    workbook.save(file_path)



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


