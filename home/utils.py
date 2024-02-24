import pandas as pd
from pretty_html_table import pretty_html_table


def assign_kassa(row):
    BIB_SKU = ['KAR-014V1', 'AB-840122', 'ABBK4006P1LW', 'ABBK1439C6L', 'ABBK1439C8L', 'ABBK1013DP1L', 'ABBK1465PB',
               'ABBK4006P1L', 'ABBK4006P1LB', 'ABBK1492PS', 'ABBK1492PSB']
    KAI_SKU = ['KT-V-10896', 'KT-TFRB02', 'KT-9002GREEN', 'KT-6MD', 'KT-W001',
               'KT-W002', 'KT-0523', 'KT-2019083001', 'KT-1051', 'KT-CLFH01',
               'KT-MT1002', 'KT-DB061', 'KT-DB062', 'KT-SOC01', 'KT-R1ENLE',
               'KT-V1ENLE', 'KAIHTM-CS00100', 'KT-2019083002']
    ML_SKU = ['AB-B18WH', 'AB-B17WH', 'AB-JB16-2BL', 'AB-JB16-2WH', 'MPL-T0671', 'AB-EDZ03', 'AB-EDSZ08', 'MPL-BOX3WH',
              'MPL-BOX3BL', 'MPL-BOX2WH', 'MPL-BOX2BL',
              'KO-033', 'KO-201513O', 'KO-201513G', 'KT-COS01', 'KT-DESK01', 'AB-ED2001', 'KO-2100O',
              'AB-PB07WAB-PB07W', 'AB-B17W', 'AB12CHER',
              'AB15CHER', 'AB05CHER', 'AB05BLACK', 'AB-SN057', 'SM-black', '20CF', 'KAIMT0-3999', 'KO-033', 'KO-01',
              'KO-02', 'KO-0410',
              'KO-04ORGCAM', 'KO-04ORGGR', 'KO-04URBBL', 'KO-05', 'KO-09', 'KO-2084', 'KO-2100G', 'KO-2100KH',
              'KO-2100R', 'KO-2102', 'KO-210625',
              'KO-C25', 'KO-P7075', 'KT-2TABGB', 'KT-693', 'KT-A12SB', 'KT-A12SR', 'KT-A155WH50', 'KT-ADM', 'KT-COS01',
              'KT-COS02', 'KT-G013', 'KT-G08',
              'KT-G081', 'KT-G81', 'KT-G85', 'KT-G919', 'KT-G91MD', 'KT-GG015', 'KT-GOPRO50', 'KT-GP20360',
              'KT-H018FMAX', 'KT-KO20L', 'KT-P10', 'MPL-1002W', 'MPL-1085M', 'MPL-1085MB', 'MPL-27B', 'MPL-T067',
              'MPLBK1025A-T2R', 'MPLBK4050-P', 'MPLCP-200061', 'KO-04OR0', 'KO-04ORG',
              'MPLCP-200610', 'AM-138IN1URAM-138IN1UR', 'KT-ADMKT-ADM']
    RBK_SKU = ['AB-B18WH', 'AB-B18W', 'AB-B17W', 'AB-B17WH', 'AB-JB16-2WH', 'AB-JB16-2BL', 'AB-JB16-2WH ', 'AB-EDZ03',
               'AB-EDSZ08 ', 'KT-DESK01', 'AB-ED2001', 'AB15CHER', 'AB15BLACK', 'AB-EDSZ08', 'AB-EDZ03 ']
    if row['Артикул'] in ML_SKU:
        return 'MPL'
    elif row['Артикул'] in KAI_SKU:
        return 'KAITAG'
    elif row['Артикул'] in BIB_SKU:
        return 'BIBA'
    elif row['Артикул'] in RBK_SKU:
        return 'RBK'
    else:
        return 'Unknown'

def main(file):
    data = pd.read_excel(file)  # загружаем файл начислений
    data['Дата начисления'] = data['Дата начисления'].astype(str)
    max_date = data['Дата начисления'].max()
    min_date = data['Дата начисления'].min()
    # sebes = pd.read_excel('sebes.xlsx')
    data = (data.fillna(0))
    USLUGI = data.loc[data['Номер отправления или идентификатор услуги'] == 0]

    data['Номер отправления или идентификатор услуги'] = data['Номер отправления или идентификатор услуги'].str.extract(
        r'^(\d+-\d+)')

    data = data.drop(columns=['Сборка заказа',
                              'Обработка отправления (Drop-off/Pick-up) (разбивается по товарам пропорционально количеству в отправлении)',
                              'Магистраль', 'Обратная магистраль', 'Обработка возврата', 'Сборка заказа',
                              'Обработка отмененного или невостребованного товара (разбивается по товарам в отправлении в одинаковой пропорции)',
                              'Обработка невыкупленного товара', 'Индекс локализации',
                              'Последняя миля (разбивается по товарам пропорционально доле цены товара в сумме отправления)'],
                     axis=1)
    # kolvo = data[['Номер отправления или идентификатор услуги','Количество']].drop_duplicates ()
    kolvo = data[['Номер отправления или идентификатор услуги', 'Количество']]
    data = data.groupby(['Номер отправления или идентификатор услуги', 'Артикул'])['Итого'].sum().reset_index()
    kolvo = kolvo.groupby(['Номер отправления или идентификатор услуги'])['Количество'].mean().reset_index()
    data = data.loc[data['Итого'] != 0]
    data['kassa'] = data.apply(assign_kassa, axis=1)
    data = pretty_html_table.build_table(data, 'green_light')
    return data