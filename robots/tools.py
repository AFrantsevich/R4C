import io

import xlsxwriter


def prepare_data_for_ex(data_to):
    model = data_to[0].model
    data_from = {}
    tmp = {}
    for i in data_to:
        if model != i.model:
            data_from[model] = tmp
            model = i.model
            tmp = {}
        if i.model == model:
            tmp[i.version] = tmp.get(i.version, 0) + 1
    data_from[model] = tmp
    return data_from


def export_to_excel(date_to_wr):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    bold = workbook.add_format({"bold": True})
    col = 0
    for item in date_to_wr.items():
        worksheet = workbook.add_worksheet(item[0])
        worksheet.write("A1", "Модель", bold)
        worksheet.write("B1", "Версия", bold)
        worksheet.write("C1", "Количество за неделю", bold)
        row = 1
        for data in item[1].items():
            worksheet.write(row, col, item[0])
            worksheet.write(row, col + 1, data[0])
            worksheet.write(row, col + 2, data[1])
            row += 1

    workbook.close()
    output.seek(0)
    return output
