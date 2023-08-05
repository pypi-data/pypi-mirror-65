import numpy as np
import pandas as pd
import json
import os
import io
from datetime import datetime
from ..core.sections import Section
from .slns import SLN

def run_check(sec_dir="data_sec", sln_dir="data_sln", res_dir="data_res", types=None, groups=None):
    '''
    check ULS strength (NTC-2018).
        sec_dir = directory where design section files (.json) saved;
        sln_dir = directory where sln (from sofistik) files (.json) saved;
        res_dir = directory where to save the resutls;
        types   = list of types  of sln to be checked [default=None, check all];
        groups  = list of groups of sln to be checked [default=None, check all].
    '''
    try:
        sec_index = json.load(open(f"{sec_dir}/_index.json","r"))
    except:
        print(f"{sec_dir}/_index.json not valid!")
        raise
    try:
        sln_index = json.load(open(f"{sln_dir}/_index.json","r"))
    except:
        print(f"{sln_dir}/_index.json not valid!")
        raise
    # ----------
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    # ----------
    print("\nchecking cross sections of sln...")
    sln_f = pd.DataFrame(sln_index["sln"]).T
    # ----
    # filterring
    sln_f = sln_f.loc[(sln_f["forces"]>0) & (sln_f["ID"].isin(sec_index["sec"]["ID"])),:]
    sln_checked = []
    sln_summary = []
    for ind,row in sln_f.iterrows():
        # --- read data
        sln_data = json.load(open(f"{sln_dir}/{row['file']}","r"))
        _ind = sec_index["sec"]["ID"].index(row["ID"])
        sec_data = json.load(open(f"{sec_dir}/{sec_index['sec']['file'][_ind]}","r"))
        # --- assemble cross sections to SLN
        # print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] ...", end="\r", flush=True)
        sln = SLN().from_dict(sln_data)
        sln.type  = sec_data["type"]
        if sec_data["grp"]>=0:
            sln.group = sec_data["grp" ]
            for sec in sln.sections:
                sec["ref_nq"] = sln.group
        else:
            sln.group = int(sln.sections[0]["ref_nq"]/100)
        for i,sec in enumerate(sln.sections):
            if (types is None or sln.type in types) and (groups is None or sec["ref_nq"] in groups):
                if sec["id"]>=0:
                    if sec_data[sec["name"]] is not None:
                        sec.update(sec_data[sec["name"]])
                        sln.has_sections = True
        # --- checks
        if sln.has_sections:
            sln.check(groups=groups)
            rho_max = max([r['rho'] for r in sln.results])
            if rho_max<=1:
                print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] -> {rho_max:5.3f}", end="\r", flush=True)
            else:
                print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] -> {rho_max:5.3f}")
            filename = f'{res_dir}/{sln.id}.json'
            with open(filename,"w") as f:
                json.dump(sln.__dict__, f, indent=4)
            sln_checked += [f'{sln.id}.json']
            sln_summary += [{"id":sln.id, "sec":sln.name, "type":sln.type, "group":sln.group, "sum":sln.summary}]
    print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] completed.")
    # ----
    print("saving results...")
    sum_df = pd.DataFrame({
        "SLN"  : [ss["id"]    for ss in sln_summary], 
        "sec"  : [ss["sec"]   for ss in sln_summary],
        "type" : [ss["type"]  for ss in sln_summary],
        "group": [ss["group"] for ss in sln_summary]
    })
    sum_df["rho_max"] = 0
    sum_df["LC"     ] = 0
    sum_df["station"] = 0
    sum_df["weak"   ] = "flexure"
    for i,ss in enumerate(sln_summary):
        df = pd.DataFrame(ss["sum"])
        df["rho"] = df[["rho_flexure","rho_shear"]].max(axis=1)
        rho = df["rho"].max()
        ind = df.loc[df["rho"]==rho].index[0]
        sum_df.loc[i,"rho_max"] = rho
        sum_df.loc[i,"LC"     ] = df.loc[ind, "LC"].item()
        sum_df.loc[i,"station"] = df.loc[ind, "station"].item()
        sum_df.loc[i,"weak"   ] = "flexure" if df.loc[ind, "rho_flexure"].item()==rho else "shear"

    log={
        "date": f"{datetime.today():%d/%m/%Y}",
        "time": f"{datetime.now():%H:%M:%S}",
        "sln": sln_checked,
        "summary":sum_df.to_dict('list')
    }
    with open(f"{res_dir}/_summary.json", "w") as f:
            json.dump(log,f,indent=4)
    print("done.")

# ------------------------------------
# html report generation
# ------------------------------------
css_style = '''
<style type="text/css">
    html * {
        font-family: consolas;
    }
    body {
        font-size: 10pt;
    }
    h1 {font-size: 13pt; }
    h2 {font-size: 12pt; background: #E8E8E8; page-break-before: always;}
    h3 {font-size: 12pt; }
    h4 {font-size: 11pt; }
    h5 {font-size: 10pt; font-style: italic;}
    h6 {font-size: 10pt; }
    table {
        font-size: 10pt;
        border: none;
        text-align: right;
    }
    caption {
        text-align: left;
    }
    thead, th {
        font-weight: bold;
    }
    th, td {
        width: 60px;
        overflow: hidden;
        white-space: nowrap;
    }
    @media print {
		h2 {page-break-before: always;}
	}
</style>
'''

# ------------------------------------
# DataFrame to html functions
# ------------------------------------
def html_summary_table(df, rho_cols=None, max_cols=10, max_rows=50):
    '''
    convert DataFrame to html tables
        rho_cols = values to be formatted and highlight for max
        max_cols = max columns in one sub-table
        max_rows = max rows (of all sub-tables) in one page (for printing pdf)
    '''
    ntab = int(np.ceil(len(df.columns)/max_cols)) # number of tables
    html = ""
    if rho_cols is None:
        rho_cols=df.columns
    rmax = df[rho_cols].replace(to_replace="-",value=-1).max().max()
    df.index.name = df.index.name or " "
    # print(f"max rho = {rmax:5.3}")
    ntpp = max(1, int(np.floor(max_rows/(len(df)+3)))) # tables per pages
    for i in range(ntab):
        df1 = df.iloc[:, (i*max_cols):(min(len(df.columns), (i+1)*max_cols))]
        if i>1 and i%ntpp==0:
            html += "<p style='page-break-before:always;'></p><br>\n" 
        html += "<table>\n"
        html += f"<caption>tab.{i+1}/{ntab}</caption>\n"
        # ---- headers
        html += "<thead>\n"
        if isinstance(df1.columns[0], tuple):
            for j in range(len(df1.columns[0])):
                html += f"<tr><th>{df1.index.name if j==0 else ' '}</th>"
                nc = 1
                for k in range(len(df1.columns)):
                    h1 = df1.columns[k][j]
                    if k<len(df1.columns)-1:
                        h2 = df1.columns[k+1][j]
                        if h1==h2:
                            nc+=1
                        else:
                            html += f"<th colspan={nc}>{h1}</th>"
                            nc = 1
                    else:
                        html += f"<th colspan={nc}>{h1}</th>"
                html += "</tr>\n"
        else:
            html += f"<tr><th>{df1.index.name}</th>"
            for j in range(len(df1.columns)):
                html += f"<th>{df1.columns[j]}</th>"
            html += "</tr>\n"
        html += "</thead>\n"
        # ----
        for ind,_ in df1.iterrows():
            html += f"<tr><td style='font-weight:bold;'>{ind}</td>\n"
            for j in range(len(df1.columns)):
                val = df1.loc[ind,df1.columns[j]]
                if val=='-' or pd.isna(val):
                    html += "<td>-</td>"
                else:
                    if df1.columns[j] in rho_cols:
                        rho = float(val)
                        attr = ''
                        if rho==rmax:
                            attr += f'font-weight:bold;text-decoration:underline;'
                            # attr = f'background-color:red;color:white;'
                        if rho>1:
                            attr += f'color:red;'
                        html += f"<td style={attr}>{rho:5.3f}</td>"
                    else:
                        html += f"<td>{val}</td>"
            html += "</tr>\n"
        html += "</table><br>\n"
    return html
# ------------------------------------
# ------------------------------------
# ------------------------------------
def report_summary(res_dir="data_res", rep_dir="", types=None, groups=None, max_cols=12, pdf=False, html_style=None):
    '''
    generate summary tables (in html file) from results.
        res_dir    = directory where results files (.json) saved, see function "run_check()";
        rep_dir    = directory where report html file to be saved;
        types      = list of types  of sln to be reported [default=None, report all];
        groups     = list of groups of sln to be reported [default=None, report all];
        max_cols   = maximum number of columns to be shown in one table (for printing page width);
        pdf        = [TODO] if convert html to pdf [default=False, not converted];
        html_style = html style string "<style type="text/css">...</style>".
    '''
    # ---- check results log
    try:
        with open(f"{res_dir}/_summary.json","r") as f:
            log = json.load(f)
    except:
        print("results not valid!")
        raise
    # -----
    if html_style is None:
        html_style = css_style
    # ----
    print("\npreparing data for report...")
    html  = "<html>\n<head>\n<title>ULS check summary</title>\n" + html_style + "</head>\n<body>\n"
    all_df = pd.DataFrame(log["summary"])
    all_df["file"] = log["sln"]
    if types is not None:
        all_df = all_df.loc[all_df["type" ].isin(types ),:]
    if groups is not None:
        all_df = all_df.loc[all_df["group"].isin(groups),:]
    for f in all_df["file"]:
        print(f"reading results of SLN {f[:-5]:>4} ...", end="\r", flush=True)
        try:
            data = json.load(open(f"{res_dir}/{f}","r"))
        except:
            data = None
        if data is not None:
            if len(data["summary"]):
                res_df = pd.DataFrame(data["summary"])
                res_df = res_df.pivot(index='LC', columns='station')
                res_df.columns = pd.MultiIndex.from_tuples([(f"s={c[1]:.3f}",c[0][4:]) for c in res_df.columns]) #.swaplevel(0, 1)
                res_df.sort_index(axis=1, level=0, inplace=True)
                # --------------
                html += f"<h2>Checks - SLN {data['id']}</h2>\n"
                html += html_summary_table(res_df, max_cols=max_cols)
    print(f"reading results of SLN {f[:-5]:>4} completed.")
    html += f"<h2>Summary</h2>\n"
    # ---
    html += f"<h3>Critical SLNs</h3>\n"
    sum_df = all_df.drop(columns=["file"])
    sum1 = sum_df.set_index("SLN")
    sum1 = sum1.loc[(sum1["rho_max"]>0.9) | (sum1["rho_max"]==sum1["rho_max"].max()),:]
    html += html_summary_table(sum1, rho_cols=["rho_max"], max_cols=8)
    html += f"<h3>Maximum by sections</h3>\n"
    idx = sum_df.groupby(['sec'])['rho_max'].transform(max) == sum_df['rho_max']
    sum2 = sum_df.loc[idx]
    sum2 = sum2[["sec","rho_max","SLN","LC","station","weak"]].set_index("sec")
    html += html_summary_table(sum2, rho_cols=["rho_max"], max_cols=8)
    html += f"<h3>Maximum by type and groups</h3>\n"
    sum3 = sum_df.groupby("type" )["rho_max"].max().to_frame()
    sum4 = sum_df.groupby("group")["rho_max"].max().to_frame()
    html += html_summary_table(sum3, rho_cols=["rho_max"], max_cols=8)
    html += html_summary_table(sum4, rho_cols=["rho_max"], max_cols=8)
    # ---
    html += "</body>\n</html>"
    with open(f"{rep_dir}/report_summary.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("html report generated.")
    # if pdf:
    #     # header = {"left":"19_038 NYCE - ULS checks", "center":"Summary Tables", "right":"[date]"}
    #     header = {"left":"ULS checks", "right":"Summary Tables"}
    #     footer = {"right":"Page [page]/[topage]"}
    #     html2pdf(html, out_file=f"{rep_dir}/report_summary.pdf", header=header, footer=footer)
    return None


def report_single(res_dir="data_res", rep_dir="", sln_id=120, pdf=False, html_style=None):
    '''
    generate report (in html file) for single sln results.
        res_dir    = directory where results files (.json) saved, see function "run_check()";
        rep_dir    = directory where report html file to be saved;
        sln_id     = sln id (file name without .json);
        pdf        = [TODO] if convert html to pdf [default=False, not converted];
        html_style = html style string "<style type="text/css">...</style>".
    '''
    if html_style is None:
        html_style = css_style
    print("\npreparing data for report...")
    filename = f"{res_dir}/{sln_id}.json"
    data = None
    try:
        with open(filename,"r") as f:
            data = json.load(f)
    except:
        print(f"data file {filename} not valid!")
        raise
    # ----
    if data is not None:
        print(f"generating report for SLN {data['id']}...")
        html  = f"<html>\n<head>\n<title>ULS checks - SLN {data['id']}</title>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>\n" 
        html += html_style + "</head>\n<body>\n"
        html += f"<h2>Structural Line {data['id']}</h2>\n"
        # --- section
        html += f"<h3>Nodes</h3>\n"
        html += f'''<table><thead><tr><td> </td>
            <td>No.  </td> <td>X [m]</td> <td>Y [m]</td> <td>Z [m]</td>
            </tr></thead> \n'''
        for sv in ["node1","node2"]:
            html += f'''<tr><td>{sv}</td> 
            <td>{data[sv]["nr"]:7.0f}</td> 
            <td>{data[sv]["x" ]:8.3f}</td> 
            <td>{data[sv]["y" ]:8.3f}</td> 
            <td>{data[sv]["z" ]:8.3f}</td> </tr>\n'''
        html += "</table>\n"
        # --- checks
        for i in range(len(data["stations"])):
            if data["results"][i]["data"]:    
                html += f"<h3>Resistance Checks - s={data['stations'][i]:5.3f}/{data['length']:6.3f}<h3>\n"
                # --- cross section
                sec = Section().from_dict(data["sections"][i])
                html += f"<h4>Cross section: {sec.name}</h4>\n"
                html += f'''<table><tr> 
                    <td>  concrete      </td>
                    <td>  f<sub>cd</sub>  = {sec.mat["fcd"]:5.2f}  MPa  </td>  
                    <td>  f<sub>cvd</sub> = {sec.mat["fcvd"]:5.2f} MPa  </td>  
                    <td>  &gamma; = {sec.mat["gamma"]}  </td> 
                    <td>  FC = {sec.mat["FC"]} </td> 
                    </tr><tr> 
                    <td>  reinforcement  </td>
                    <td>  f<sub>yd</sub>  = {sec.mrf["fyd"]:5.1f}  MPa  </td>  
                    <td>  f<sub>ywd</sub> = {sec.mrf["fywd"]:5.1f} MPa  </td>  
                    <td>  &gamma; = {sec.mrf["gamma"]}  </td> 
                    <td>  FC = {sec.mrf["FC"]} </td> 
                    </tr></table> \n'''
                fig1 = io.StringIO()
                sec.plot_geometry(fig1,rebar=True, stirr=False, z_inversed=True, figsize=(12/2.54,12/2.54))
                fig2 = io.StringIO()
                sec.plot_geometry(fig2,rebar=False, stirr=True, z_inversed=True, figsize=(12/2.54,12/2.54))
                html +='<figure>\n' + fig1.getvalue() + fig2.getvalue() + '\n<figcaption>section geometry</figcaption>\n</figure>\n'
                fig3 = io.StringIO()
                sec.plot_domains(fig3)
                html +='<figure>\n' + fig3.getvalue() + '\n<figcaption>N-M domains</figcaption>\n</figure>\n'
                # --- forces, check and results
                ff  = data["forces"][i]
                for j in range(len(ff['LC'])):
                    html += f"<h4>Checks Loadcase LC.{ff['LC'][j]}</h4>\n"
                    html += f'''
                    <h5>Design Forces</h5>
                    <table>
                    <tr> <td>N<sub>Ed</sub>   =</td> <td style="width:80px">{ff["N" ][j]:10.0f} kN </td> </tr>
                    <tr> <td>V<sub>y,Ed</sub> =</td> <td style="width:80px">{ff["VY"][j]:10.0f} kN </td> </tr>
                    <tr> <td>V<sub>z,Ed</sub> =</td> <td style="width:80px">{ff["VZ"][j]:10.0f} kN </td> </tr>
                    <tr> <td>T<sub>Ed</sub>   =</td> <td style="width:80px">{ff["MT"][j]:10.0f} kNm</td> </tr>
                    <tr> <td>M<sub>y,Ed</sub> =</td> <td style="width:80px">{ff["MY"][j]:10.0f} kNm</td> </tr>
                    <tr> <td>M<sub>z,Ed</sub> =</td> <td style="width:80px">{ff["MZ"][j]:10.0f} kNm</td> </tr>
                    </table>
                    '''
                    res = data["results"][i]["data"]
                    html += f'''
                    <h5>Flexure and Axial Loads check</h5>
                    <i> the stengths are calculated according to Clause 4.1.2.3.4, NTC-2018</i><br>
                    <i> the biaxial flexure-compression combined effect is checked according to Eq.[4.1.19], NTC-2018</i><br><br>
                    <strong>( M<sub>y,Ed</sub> / M<sub>y,Rd</sub> )<sup>&alpha;</sup> + ( M<sub>z,Ed</sub> / M<sub>z,Rd</sub> )<sup>&alpha;</sup> 
                        = {res["rho_flexure"][j]:5.3f} {"≤" if res["rho_flexure"][j]<=1 else ">"} 1 </strong><br><br>
                    where,<ul>
                    <li>M<sub>y,Rd</sub> = {res["Myd"][j]:10.0f} kNm = uniaxial flexure resistance in y-direction</li>
                    <li>M<sub>z,Rd</sub> = {res["Mzd"][j]:10.0f} kNm = uniaxial flexure resistance in z-direction</li>
                    <li>&alpha; = {res["alpha"][j]:10.2f} = index evaluated according to geometry and compression level </li>
                    </ul>
                    <em>verification {"" if res["rho_flexure"][j]<=1 else "NOT "}satisfied.</em><br><br>
                    
                    <h5>Shear and Torsion check</h5>
                    <i> the stengths are calculated according to Clause 4.1.2.3.5, NTC-2018</i><br><br>
                    <strong> max[ ( V<sub>y,Ed</sub> + V<sub>y,T</sub> ) / V<sub>y,Rd</sub>, ( V<sub>z,Ed</sub> + V<sub>z,T</sub> ) / V<sub>z,Rd</sub> ]
                        = {res["rho_shear"][j]:5.3f} {"≤" if res["rho_shear"][j]<=1 else ">"} 1</strong> <br><br>
                    where,<ul>
                    <li>V<sub>y,T</sub>  = {res["Vyt"][j]:10.0f} kN = torsion T<sub>Ed</sub> induced shear in y-direction</li>
                    <li>V<sub>z,T</sub>  = {res["Vzt"][j]:10.0f} kN = torsion T<sub>Ed</sub> induced shear in z-direction</li>
                    <li>V<sub>y,Rd</sub> = {res["Vyd"][j]:10.0f} kN = shear resistance in y-direction</li>
                    <li>V<sub>z,Rd</sub> = {res["Vzd"][j]:10.0f} kN = shear resistance in z-direction</li>
                    </ul>
                    <em>verification {"" if res["rho_shear"][j]<=1 else "NOT "}satisfied.</em><br><br>
                    '''
                # --------------
        # --------------
        sum_df = pd.DataFrame(data["summary"])
        sum_df = sum_df.pivot(index='LC', columns='station')
        sum_df.columns = pd.MultiIndex.from_tuples([(f"s={c[1]:.3f}",c[0][4:]) for c in sum_df.columns]) #.swaplevel(0, 1)
        sum_df.sort_index(axis=1, level=0, inplace=True)
        html += f"<h2>Summary of checks - SLN {data['id']}</h2>\n"
        html += html_summary_table(sum_df)
        html += "<br>\n</body>\n</html>"
        with open(f"{rep_dir}/report_SLN_{data['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"html report for SLN {data['id']} generated.")
        # if pdf:
        #     header = {"left":"ULS checks", "center":f"SLN {data['id']}", "right":"[date]"}
        #     footer = {"right":"Page [page]/[topage]"}
        #     html2pdf(html, out_file=f"{rep_dir}/report_SLN_{data['id']}.pdf", header=header, footer=footer)
    return None


def html2pdf(html_string="<html><body>No String!</body></html>", out_file="test.pdf", header={"center":"test"}, footer={"center":"[page]"}):
    import pdfkit
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')        
    options = {
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '15mm',
        'margin-bottom': '20mm',
        'margin-left': '15mm',
        'encoding': "UTF-8",
        'zoom': '1.15',
        # 'no-outline': None,
        'header-font-size': '9',
        'header-font-name': 'consolas',
        'header-spacing': '5',
        'footer-font-size': '9',
        'footer-font-name': 'consolas',  
        'footer-spacing': '5',    
    }
    if header is not None:
        options.update({f"header-{k}":header[k] for k in header.keys()})
    if footer is not None:
        options.update({f"footer-{k}":footer[k] for k in footer.keys()})

    pdfkit.from_string(html_string, out_file, configuration=config, options=options)
    # print("pdf generated.")