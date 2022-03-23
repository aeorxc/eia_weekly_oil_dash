from pathlib import Pathimport pandas as pdfrom commodplot import jinjautils as jufrom excel_scraper import excel_scraperfrom oilanalytics.utils import chartutils as cufileloc = 'https://ir.eia.gov/wpsr/psw09.xls'eia_url = 'https://www.eia.gov/opendata/qb.php?sdid=PET.%s.W'sheets_to_parse = [    'Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6', 'Data 7', 'Data 8', 'Data 9', 'Data 10', 'Data 11',    'Data 14', 'Data 16']def report_symbols() -> dict:    """    Get a list of all the symbols in the Weekly Report    :return:    """    ex = excel_scraper.read_excel_file(fileloc)    symbols = {}    for tab in sheets_to_parse:        if 'Data' in tab:            d = ex.parse(tab, skiprows=[0]).head(1).iloc[0].to_dict()            symbols = {**symbols, **d}    return symbolsdef read_report() -> pd.DataFrame:    """    Read all the timeseries in the report    :return:    """    ex = excel_scraper.read_excel_file(fileloc)    dfs = []    for tab in sheets_to_parse:        if 'Data' in tab:            d = ex.parse(tab, skiprows=[0, 2], index_col=0)            d = d['2000':]            # if tab in ['Data 1', 'Data 2', 'Data 6']:            d = d / 1000            if tab == 'Data 14':                # d.rename(columns={'WDIRPUS2':'WDIRPUS2_4wk', 'WKJRPUS2':'WKJRPUS2_4wk'}, inplace=True)                d.rename(columns={'WDIRPUS2': 'WDIRPUS2_4wk'}, inplace=True)                d = d['WDIRPUS2_4wk']            if tab == 'Data 16':                d.rename(columns={'W_EPOOXE_YOP_NUS_MBBLD': 'W_EPOOXE_YOP_NUS_MBBLD_4wk'}, inplace=True)                d = d['W_EPOOXE_YOP_NUS_MBBLD_4wk']            dfs.append(d)    res = pd.concat(dfs, axis=1)    res['Gas Yield'] = (res['W_EPM0F_YPR_NUS_MBBLD'] / res['WCRRIUS2']) * 100    res['Non Oxy Yield'] = ((res['W_EPM0F_YPR_NUS_MBBLD'] - res['W_EPOOXE_YOP_NUS_MBBLD']) / res['WCRRIUS2']) * 100    res['Dist Yield'] = (res['WDIRPUS2'] / res['WCRRIUS2']) * 100    return resdef gen_page(title: str, template: str, out_loc: str, report_data: pd.DataFrame = None):    data = {'name': title, 'title': title, 'eia_url': eia_url}    if report_data is None:        report_data = read_report()    data['report'] = report_data    template_loc = (Path(__file__).resolve().parent / 'templates' / template)    return ju.render_html(data, template_loc, out_loc, template_globals={'cu': cu})def gen_summary_charts(out_loc, report_data=None):    data = {'name': 'DOE Weekly Quick Report', 'title': 'DOE Weekly Quick', 'eia_url': eia_url}    if report_data is None:        report_data = read_report()    data['report'] = report_data    return ju.render_html(data, 'doe_weekly_summary.html', out_loc, template_globals={'cu': cu})if __name__ == '__main__':    gen_page(title='DOE Weekly Quick Report', template=('doe_weekly_summary.html'),             out_loc=r'dist/index.html')    # gen_page(title='DOE Weekly Quick Report - Refineries', template='doe_weekly_refineries.html',    #          out_loc=r'..\dist\refineries.aspx')    # gen_page(title='DOE Weekly Quick Report - Distillates', template='doe_weekly_distillates.html',    #          out_loc=r'..\dist\distillates.aspx')    # gen_page(title='DOE Weekly Quick Report - Jet', template='doe_weekly_jet.html',    #          out_loc=r'..\dist\jet.aspx')    # gen_page(title='DOE Weekly Quick Report - Fuel', template='doe_weekly_fuel.html',    #          out_loc=r'..\dist\fuel.aspx')    # gen_page(title='DOE Weekly Quick Report - LPG', template='doe_weekly_lpg.html',    #          out_loc=r'..\dist\lpg.aspx')    # gen_page(title='DOE Weekly Quick Report - Ethanol', template='doe_weekly_ethanol.html',    #          out_loc=r'..\dist\ethanol.aspx')    # gen_page(title='DOE Weekly Quick Report - Crude', template='doe_weekly_crude.html',    #          out_loc=r'..\dist\crude.aspx')    # gen_page(title='DOE Weekly Quick Report - Gasoline', template='doe_weekly_gasoline.html',    #          out_loc=r'..\dist\gasoline.aspx')