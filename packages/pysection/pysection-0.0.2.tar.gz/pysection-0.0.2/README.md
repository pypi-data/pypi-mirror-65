# Introduction
ULS Checks (NTC-2018) on RC sections based on FEM database.

# Example
## imports
`import os`   
`from pysection import *`
## data sheets files
- design cross sections   
`xls_sec = '20_007_map_sezioni.xlsx'`
- data from sofistik FEM   
`xls_fem = '20_007_data_sofistik.xlsx'`

## directories for saving data
`rep_dir = '20_007_test'`   
`if not os.path.exists(rep_dir):`   
`    os.mkdir(rep_dir)`   
`sec_dir = f"{rep_dir}/data_sec"`   
`sln_dir = f"{rep_dir}/data_sln"`   
`res_dir = f"{rep_dir}/data_res"`   

## read design sections
`get_sec(src=xls_sec, sec_dir=sec_dir)`

## read fem data
- first read or update from xlsx file   
`get_sln(src=xls_fem, sln_dir=sln_dir)`   
- read existing hdf file   
`get_sln(src=f"{sln_dir}/data.h5", sln_dir=sln_dir)`   

## run check
`run_check(sec_dir=sec_dir, sln_dir=sln_dir, res_dir=res_dir)`

## generate report
- save report of all checks summary tables in html   
`report_summary(res_dir=res_dir, rep_dir=rep_dir)`   
- create report for single selected sln checks in html   
`report_single(res_dir=res_dir, rep_dir=rep_dir, sln_id=1574)`   

## view of results
`create_view(sln_dir=sln_dir, res_dir=res_dir, title="Viale Europa", view_html=f"{rep_dir}/view1.html")`

