import pandas as pd
import os

def analyzeResults(file_path=None):
    if file_path is None:
        results_files = [f for f in os.listdir("results") if f.endswith(".csv")]
        file_name = sorted(results_files)[-1]
        file_path = os.path.join("results", file_name)

    df = pd.read_csv(file_path)

    best_per_instance = df.groupby('instance')['obj_value'].max()

    deviations = []
    for _, row in df.iterrows():
        best = best_per_instance[row['instance']]
        dev = ((best - row['obj_value']) / best) * 100
        deviations.append(dev)
    df['deviation'] = deviations
    
    avg_dev = df.groupby('alpha')['deviation'].mean()
    df['is_best'] = df.apply(lambda x: x['obj_value'] == best_per_instance[x['instance']], axis=1)
    best_count = df.groupby('alpha')['is_best'].sum()

    return best_count, avg_dev


def writeExcel(best_count, avg_dev, date_time, max_time):
    if not os.path.exists("results/analyzed"):
        os.makedirs("results/analyzed")
    writer = pd.ExcelWriter(f'results/analyzed/{date_time}-max_time-{int(max_time)}.xlsx', engine='xlsxwriter')
    workbook = writer.book
    
    header_format = workbook.add_format({
        'bold': True,
        'font_color': 'white',
        'bg_color': '#0066cc',
        'align': 'center',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'align': 'center',
        'border': 1
    })
    
    pct_format = workbook.add_format({
        'align': 'center',
        'border': 1,
        'num_format': '0.00%'
    })

    alphas = best_count.index.tolist()
    data = []
    
    header_row = ['Metric']
    for alpha in alphas:
        header_row.append(f'α = {alpha:.1f}')
    data.append(header_row)
    
    best_row = ['Best Solutions Found']
    for alpha in alphas:
        best_row.append(best_count[alpha])
    data.append(best_row)
    
    dev_row = ['Average Deviation']
    for alpha in alphas:
        dev_row.append(avg_dev[alpha] / 100)
    data.append(dev_row)

    worksheet = workbook.add_worksheet('Results')
    
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center'
    })
    worksheet.merge_range(0, 0, 0, len(alphas), f'GRASP Analysis Results (Max Time: {max_time}s)', title_format)
    
    for row in range(len(data)):
        for col in range(len(data[row])):
            if row == 0:
                worksheet.write(row + 1, col, data[row][col], header_format)
            elif col == 0:
                worksheet.write(row + 1, col, data[row][col], cell_format)
            else:
                if row == 2:
                    worksheet.write(row + 1, col, data[row][col], pct_format)
                else:
                    worksheet.write(row + 1, col, data[row][col], cell_format)
    
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, len(alphas), 12)
    
    writer.close()