import pandas
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

def ozon(file, file_2, period):
    data = pd.read_excel(file)  # загружаем файл начислений
    data1 = data
    data['Дата начисления'] = data['Дата начисления'].astype(str)
    max_date = data['Дата начисления'].max()
    min_date = data['Дата начисления'].min()
    sebes = pd.read_excel(file_2)
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
    # data = pretty_html_table.build_table(data, 'green_light')
    hranenie = data1[
        (data1['Тип начисления'] == 'Услуга размещения товаров на складе')]
    logistica = data1[
        (data1['Тип начисления'] == 'Доставка покупателю')]
    vozvrati = data1[(data1['Тип начисления'] == 'Получение возврата, отмены, невыкупа от покупателя') | (
                data1['Тип начисления'] == 'Доставка и обработка возврата, отмены, невыкупа')]
    rekla = data1[
        (data1['Тип начисления'] == 'Услуги продвижения товаров')]
    reklama = -rekla['Итого'].sum()
    hran = -hranenie['Итого'].sum()

    logistica = logistica[['Артикул', 'Количество',
                           'Обработка отправления (Drop-off/Pick-up) (разбивается по товарам пропорционально количеству в отправлении)',
                           'Обработка возврата', 'Обратная логистика',
                           'Обработка отмененного или невостребованного товара (разбивается по товарам в отправлении в одинаковой пропорции)',
                           'Логистика',
                           'Последняя миля (разбивается по товарам пропорционально доле цены товара в сумме отправления)']]
    vozvrati = vozvrati[['Артикул', 'Количество', 'Итого']]

    cols = [
        'Обработка отправления (Drop-off/Pick-up) (разбивается по товарам пропорционально количеству в отправлении)',
        'Обработка возврата', 'Обратная логистика',
        'Обработка отмененного или невостребованного товара (разбивается по товарам в отправлении в одинаковой пропорции)',
        'Логистика', 'Последняя миля (разбивается по товарам пропорционально доле цены товара в сумме отправления)']
    logistica['Итого'] = logistica[cols].sum(axis=1)

    cols = [2, 3, 4, 5, 6, 7]
    logistica.drop(logistica.columns[cols], axis=1, inplace=True)
    DOP = data.loc[data['Итого'] < 0]
    PROD = data.loc[data['Итого'] > 0]

    PROD['USLUGI_SUM'] = ((USLUGI['Итого'].sum()) / (PROD['Итого'].sum())) * -1
    PROD['BEZ USLUG'] = PROD['Итого'] - (PROD['Итого'] * PROD['USLUGI_SUM'])

    PROD = PROD.merge(kolvo, on='Номер отправления или идентификатор услуги')
    PROD = PROD.loc[PROD['Итого'] > 20]

    PROD['vozv'] = (DOP['Итого'].sum() / PROD['Итого'].sum())
    PROD['total_all'] = PROD['BEZ USLUG'] + PROD['vozv'] * PROD['Итого']
    PROD['total'] = PROD['total_all'] / PROD['Количество']
    df_concat = PROD
    df_concat['zakupka'] = df_concat['Артикул'].map(sebes.set_index('Артикул поставщика')['zakupka'])
    df_concat['Дата транзакции'] = max_date
    df_concat = df_concat.dropna()
    dataframe = df_concat[['Артикул', 'Дата транзакции', 'Количество', 'Итого', 'total_all', 'zakupka']]

    dataframe['Налог'] = (dataframe['total_all'] * 0.07)

    dataframe['Прибыль'] = dataframe['total_all'] - dataframe['Налог'] - (
                dataframe['zakupka'] * dataframe['Количество'])
    dataframe['Маркетплейс'] = 'OZ'

    dataframe = dataframe.rename(
        columns={'Количество': 'Кол-во', 'Артикул': 'SKU', 'Итого': 'К перечислению', 'total_all': 'Выручка',
                 'zakupka': 'Закупка'})
    dataframe['Прибыль за шт.'] = dataframe['Прибыль'] / dataframe['Кол-во']
    dataframe_1 = dataframe[
        ['SKU', 'Дата транзакции', 'Кол-во', 'К перечислению', 'Выручка', 'Закупка', 'Налог', 'Прибыль', 'Маркетплейс',
         'Прибыль за шт.']]
    # ВЕРХНИЕ БЛОКИ МЕТРИК
    kolvo_zakazov = df_concat['Количество'].sum()
    kolvo_vozvrat = data1[
        (data1['Тип начисления'] == 'Доставка и обработка возврата, отмены, невыкупа')]['Количество'].sum()
    kolvo_tovarov = data1[
        (data1['Тип начисления'] == 'Доставка покупателю')]['Количество'].sum()
    obrat_logistica = data1[
        (data1['Тип начисления'] == 'Доставка и обработка возврата, отмены, невыкупа')]['Количество'].sum()
    viruchka = df_concat['total_all'].sum()
    EBITDA = dataframe_1['Прибыль'].sum()
    ZAKUPKA = dataframe_1['Закупка'].sum()
    ROI = round(EBITDA / ZAKUPKA * 100, 2)
    blocks = {
        "orders": kolvo_zakazov,
        "revenue": viruchka,
        "returns": kolvo_vozvrat,
        "profit": EBITDA,
        "roi": ROI,
        "purchase": ZAKUPKA
    }
    print(blocks)

    # НИЖНИЙ БЛОК ABC АНАЛИЗА
    dataset = dataframe
    dashboard_data = dataset.groupby(['SKU'])[
        'К перечислению', 'Кол-во', 'Выручка', 'Закупка', 'Прибыль'].sum().reset_index()
    dashboard_data['ROI'] = round((dashboard_data['Прибыль'] / dashboard_data['Закупка']) * 100, 2)

    dashboard_data = dashboard_data.sort_values(by='Прибыль', ascending=False)
    dashboard_data = dashboard_data.rename(columns={'К перечислению': 'Продажи', 'Прибыль': 'EBITDA'})

    return dashboard_data, blocks, dataframe_1


def round_values(values, to_int=True):
    table_result = []
    for row in values:
        row_result = []
        for value in row:
            if isinstance(value, float):
                value = round(value, 2)
                if to_int:
                    value = int(value)
            row_result.append(value)
        table_result.append(row_result)
    return table_result


def yandex(united, mp_services, netting, sebes, period):

    sebes = pd.read_excel(sebes)
    data_bonus = pd.read_excel(netting, sheet_name='Отчёт о платежном поручении', skiprows=1)

    # data_bonus = data_bonus.loc[data_bonus['Источник транзакции'] == ('Платёж за скидку по баллам Яндекс Плюса'  'Платёж за скидку маркетплейса')]
    data_bonus = data_bonus.loc[data_bonus['Тип заказа'] == 'Продажа физлицу']
    # data_bonus = data_bonus[['Модели работы','Названия магазинов','Номер заказа','Ваш SKU','Название товара','Количество','Сумма транзакции, руб.','Дата транзакции']]
    data_bonus = data_bonus[['Номер заказа', 'Количество', 'Сумма транзакции, руб.']]
    data_bonus = data_bonus.groupby(['Номер заказа']).sum()
    data_bonus = data_bonus.loc[data_bonus['Сумма транзакции, руб.'] != 0]

    vozvrat = pd.read_excel(united, sheet_name='Отчёт о платежном поручении', skiprows=1)

    vozvrat = vozvrat.loc[vozvrat['Источник транзакции'] == 'Возврат платежа покупателя']
    vozvrat = vozvrat[['Номер заказа', 'Ваш SKU', 'Количество', 'Сумма транзакции, руб.']]
    vozvrat = vozvrat.rename(columns={'Номер заказа': 'Заказ'})
    vozvrat = vozvrat.reset_index(drop=True)
    list_vozv = vozvrat['Заказ'].tolist()

    data_tranzact = pd.read_excel(united, sheet_name='Отчёт о платежном поручении', skiprows=1)

    data_tranzact = data_tranzact.loc[(data_tranzact['Источник транзакции'] == 'Платёж покупателя')]
    data_tranzact = data_tranzact[
        ['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Название товара', 'Количество',
         'Сумма транзакции, руб.', 'Дата транзакции']]
    data_tranzact = data_tranzact.sort_values(by=['Номер заказа'], ascending=True)
    data_tranzact = data_tranzact.fillna(0)
    data_tranzact = data_tranzact.loc[~data_tranzact['Номер заказа'].isin(list_vozv)]
    data_tranzact = data_tranzact.reset_index(drop=True)

    dostavka = pd.merge(data_tranzact, data_bonus, on=['Номер заказа'], how='left')
    dostavka = dostavka.fillna(0)
    dostavka['цена за шт'] = (dostavka['Сумма транзакции, руб._x'] + dostavka['Сумма транзакции, руб._y']) / dostavka[
        'Количество_x']
    dostavka['Итого платеж'] = dostavka['цена за шт'] * dostavka['Количество_x']
    list_dostavka = dostavka['Номер заказа']

    dostavka['Дата транзакции'] = pd.to_datetime(dostavka['Дата транзакции'], infer_datetime_format=True)
    max_date = dostavka['Дата транзакции'].max()
    min_date = dostavka['Дата транзакции'].min()
    max_date = max_date.date()
    min_date = min_date.date()
    max_date = max_date.strftime('%d/%m/%y')
    min_date = min_date.strftime('%d/%m/%y')
    data_vitrina = pd.read_excel(mp_services,
                                 sheet_name='Размещение товаров на витрине', skiprows=4)
    data_vitrina = data_vitrina.drop(index=[0, 1])
    data_reklama = pd.read_excel(mp_services, sheet_name='Буст продаж', skiprows=1)
    data_dostavka = pd.read_excel(mp_services, sheet_name='Доставка покупателю',
                                  skiprows=1)
    data_eqva = pd.read_excel(mp_services, sheet_name='Перевод платежа', skiprows=1)
    data_obrabotka = pd.read_excel(mp_services,
                                   sheet_name='Обработка заказов в СЦ или ПВЗ', skiprows=1)
    data_hranenie = pd.read_excel(mp_services,
                                  sheet_name='Хранение невыкупов и возвратов', skiprows=1)
    data_loyal = pd.read_excel(mp_services, sheet_name='Программа лояльности и отзывы',
                               skiprows=1)
    data_dostavka = data_dostavka[
        ['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Количество, шт.', 'Стоимость услуги, руб.']]
    data_vitrina = data_vitrina[['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Количество, шт.',
                                 'Стоимость услуги (гр.46=гр. 34-гр.36+гр.41+гр.43-гр.44-гр.45), руб.']]
    data_reklama = data_reklama[
        ['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Количество, шт.', 'Постоплата, руб.']]
    data_loyal = data_loyal[
        ['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Количество, шт.', 'Стоимость услуги, руб.']]
    data_reklama = data_reklama.rename(columns={'Постоплата, руб.': 'Стоимость услуги, руб.'})
    data_eqva = data_eqva[
        ['Модели работы', 'Названия магазинов', 'Номер заказа', 'Ваш SKU', 'Тариф на перевод, % от оплаченной суммы',
         'Стоимость услуги, руб.']]
    data_eqva = data_eqva.rename(columns={'Тариф на перевод, % от оплаченной суммы': 'Количество, шт.'})
    data_obrabotka = data_obrabotka[['Номер заказа', 'Тариф за заказ или отправление, руб.']]
    data_dostavka_group = data_dostavka.groupby(['Номер заказа', 'Ваш SKU'])[
        'Стоимость услуги, руб.'].sum().reset_index()

    data_vitrina = data_vitrina.rename(
        columns={'Стоимость услуги (гр.46=гр. 34-гр.36+гр.41+гр.43-гр.44-гр.45), руб.': 'Стоимость услуги, руб.'})
    df_dostavka = data_dostavka.loc[data_dostavka['Номер заказа'].isin(list_dostavka)]
    df_dostavka = df_dostavka.groupby(['Номер заказа', 'Ваш SKU'])[
        'Количество, шт.', 'Стоимость услуги, руб.'].sum().reset_index()
    df_vitrina = (data_vitrina.loc[data_vitrina['Номер заказа'].isin(list_dostavka)]).reset_index(drop=True)
    df_reklama = (data_reklama.loc[data_reklama['Номер заказа'].isin(list_dostavka)]).reset_index(drop=True)
    df_loyal = (data_loyal.loc[data_loyal['Номер заказа'].isin(list_dostavka)]).reset_index(drop=True)
    df_eqva = (data_eqva.loc[data_eqva['Номер заказа'].isin(list_dostavka)]).reset_index(drop=True)
    df_obrabotka = (data_obrabotka.loc[data_obrabotka['Номер заказа'].isin(list_dostavka)]).reset_index(drop=True)

    dostavka = dostavka.rename(
        columns={'Ваш SKU': 'SKU', 'Количество_y': 'Кол-во бонусы', 'Сумма транзакции, руб._y': 'Платеж бонусами',
                 'Количество_x': 'Кол-во', 'Сумма транзакции, руб._x': 'Платеж'})
    unit = dostavka.merge(df_dostavka, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Стоимость услуги, руб.': 'Доставка'}, inplace=True)
    unit = unit.merge(df_vitrina, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Стоимость услуги, руб.': 'Витрина'}, inplace=True)
    unit = unit.merge(df_reklama, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Стоимость услуги, руб.': 'Реклама'}, inplace=True)
    unit = unit.merge(df_loyal, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Стоимость услуги, руб.': 'Лояльность'}, inplace=True)
    unit = unit.merge(df_eqva, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Стоимость услуги, руб.': 'Эквайринг'}, inplace=True)
    unit = unit.merge(df_obrabotka, left_on='Номер заказа', right_on='Номер заказа', how='outer')
    unit.rename(columns={'Тариф за заказ или отправление, руб.': 'Обработка'}, inplace=True)
    unit = unit.fillna(0)
    unit = unit.drop(
        ['Модели работы', 'Названия магазинов', 'Количество, шт.', 'Ваш SKU', 'Модели работы_x', 'Названия магазинов_x',
         'Ваш SKU_y', 'Количество, шт._x', 'Модели работы_y', 'Названия магазинов_y', 'Количество, шт._y', 'Ваш SKU_x'],
        axis=1)
    unit['Итоговый Перевод'] = unit['Итого платеж'] - unit['Доставка'] - unit['Витрина'] - unit['Лояльность'] - unit[
        'Обработка'] - unit['Реклама'] - unit['Эквайринг']

    no_dostavka = data_dostavka.loc[~data_dostavka['Номер заказа'].isin(list_dostavka)]
    no_dostavka = no_dostavka.groupby(['Номер заказа', 'Ваш SKU'])[
        'Количество, шт.', 'Стоимость услуги, руб.'].sum().reset_index()
    no_dostavka = no_dostavka[['Ваш SKU', 'Стоимость услуги, руб.']]
    no_vitrina = data_vitrina.loc[~data_vitrina['Номер заказа'].isin(list_dostavka)]
    no_vitrina = no_vitrina[['Ваш SKU', 'Стоимость услуги, руб.']]
    no_reklama = data_reklama.loc[~data_reklama['Номер заказа'].isin(list_dostavka)]
    no_reklama = no_reklama[['Ваш SKU', 'Стоимость услуги, руб.']]
    no_loyal = data_loyal.loc[~data_loyal['Номер заказа'].isin(list_dostavka)]
    no_loyal = no_loyal[['Ваш SKU', 'Стоимость услуги, руб.']]
    no_eqva = data_eqva.loc[~data_eqva['Номер заказа'].isin(list_dostavka)]
    no_eqva = no_eqva[['Ваш SKU', 'Стоимость услуги, руб.']]
    no_obrabotka = data_obrabotka.loc[~data_obrabotka['Номер заказа'].isin(list_dostavka)]
    no_obrabotka = no_obrabotka[['Номер заказа', 'Тариф за заказ или отправление, руб.']]

    no_sales_costs = pd.concat([no_dostavka, no_vitrina, no_reklama, no_loyal, no_eqva]).reset_index()
    unit = unit.rename(columns={'SKU': 'Ваш SKU'})

    unit['Обработка %'] = no_obrabotka['Тариф за заказ или отправление, руб.'].sum() / unit['Итоговый Перевод'].sum()
    unit['Хранение общее %'] = data_hranenie['Стоимость услуги, руб.'].sum() / unit['Итоговый Перевод'].sum()
    unit['Иные расходы, %'] = no_sales_costs['Стоимость услуги, руб.'].sum() / unit['Итоговый Перевод'].sum()
    unit['Итого'] = unit['Итоговый Перевод'] - (unit['Обработка %'] * unit['Итоговый Перевод']) - (
                unit['Иные расходы, %'] * unit['Итоговый Перевод']) - (
                                unit['Хранение общее %'] * unit['Итоговый Перевод'])
    df_concat = unit
    df_concat['zakupka'] = df_concat['Ваш SKU'].map(sebes.set_index('Артикул поставщика')['zakupka'])
    df_concat['Дата транзакции'] = period
    df_concat = df_concat.dropna()
    dataframe = df_concat[['Ваш SKU', 'Дата транзакции', 'Кол-во', 'Итого платеж', 'Итого', 'zakupka']]

    dataframe['Налог'] = (dataframe['Итого'] * 0.07)

    dataframe['Прибыль'] = dataframe['Итого'] - dataframe['Налог'] - (dataframe['zakupka'] * dataframe['Кол-во'])
    dataframe['Маркетплейс'] = 'YM'

    dataframe = dataframe.rename(
        columns={'Ваш SKU': 'SKU', 'Итого платеж': 'К перечислению', 'Итого': 'Выручка', 'zakupka': 'Закупка'})
    dataframe['Прибыль за шт.'] = dataframe['Прибыль'] / dataframe['Кол-во']
    dataframe_1 = dataframe[
        ['SKU', 'Дата транзакции', 'Кол-во', 'К перечислению', 'Выручка', 'Закупка', 'Налог', 'Прибыль', 'Маркетплейс',
         'Прибыль за шт.']]
    # ВЕРХНИЕ БЛОКИ МЕТРИК
    kolvo_zakazov = len(df_concat)
    kolvo_vozvrat = vozvrat['Количество'].sum()
    kolvo_tovarov = dataframe['Кол-во'].sum()
    viruchka = df_concat['Итого'].sum()
    EBITDA = dataframe_1['Прибыль'].sum()
    ZAKUPKA = dataframe_1['Закупка'].sum()

    # НИЖНИЙ БЛОК ABC АНАЛИЗА
    dataset = dataframe
    dashboard_data = dataset.groupby(['SKU'])[
        'К перечислению', 'Кол-во', 'Выручка', 'Закупка', 'Прибыль'].sum().reset_index()
    dashboard_data['ROI'] = round((dashboard_data['Прибыль'] / dashboard_data['Закупка']) * 100, 2)
    ROI = round(EBITDA / ZAKUPKA * 100, 2)
    dashboard_data = dashboard_data.sort_values(by='Прибыль', ascending=False)
    dashboard_data = dashboard_data.rename(columns={'К перечислению': 'Продажи', 'Прибыль': 'EBITDA'})

    blocks = {
        "orders": kolvo_zakazov,
        "revenue": viruchka,
        "returns": kolvo_vozvrat,
        "profit": EBITDA,
        "roi": ROI,
        "purchase": ZAKUPKA
    }
    print(blocks)
    return dashboard_data, blocks, dataframe_1
