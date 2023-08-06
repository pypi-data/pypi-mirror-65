import pandas as pd
import math

def analyze(file1, file2, out_file):
    data1 = pd.read_excel(file1, 'Cajas')
    data2 = pd.read_excel(file2)

    result = []
    used_indexes = []
    error_count = 0

    i = 0
    for val1 in data1['Material']:
        j = 0
        aux_res = ''
        for val2 in data2['Producto: Gastro']:
            if not (math.isnan(int(val1[2:])) or math.isnan(float(val2))):
                if (not (j in used_indexes)) and (int(val1[2:]) == int(val2)) and (float(data1['Peso/Cantidad'][i]) == float(data2['Kilos'][j])):
                    aux_res = data2['Código de Barras'][j]
                    used_indexes.append(j)
                    j = j - 1
                    break
            j = j + 1
        result.append(aux_res)
        if aux_res == '':
            error_count = error_count + 1
        i = i + 1

    df = pd.DataFrame({'Codigo de barras': result})
    data1 = data1.join(df)

    writer = pd.ExcelWriter(out_file)
    data1.to_excel(writer, 'Sheet1', index = False)
    writer.save()

    for k in used_indexes:
        data2.drop(k, inplace = True)

    writer = pd.ExcelWriter(file2)
    data2.to_excel(writer)

    print(error_count)
