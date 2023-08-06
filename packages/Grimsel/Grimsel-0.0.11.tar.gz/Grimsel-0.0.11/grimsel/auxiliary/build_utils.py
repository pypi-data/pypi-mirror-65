#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 15:46:30 2019

@author: user
"""

import grimsel.auxiliary.sqlutils.aux_sql_func as aql
import grimsel_config as config

db = 'storage2'


sqlc = aql.SqlConnector(db, user=config.PSQL_USER,
                        password=config.PSQL_PASSWORD,
                        host=config.PSQL_HOST,
                        port=config.PSQL_PORT)



def yr_getter(par, data_type=False, rnge=range(2015, 2050 + 1, 5)):
    return [par + i if not data_type else (par + i, data_type)
            for i in [''] + ['_yr' + str(ii) for ii
            in rnge if not ii == 2015]]

def init_table(*args, **kwargs):
    con_cur = sqlc.get_pg_con_cur()
    print(con_cur, args, kwargs)
    return aql.init_table(*args, **kwargs, con_cur=con_cur)


def init_sql_tables(sc, db):

    tb_name = 'def_profile'
    cols = [('pf_id', 'SMALLINT'), ('pf', 'VARCHAR'), ('primary_nd', 'VARCHAR')]
    pk = ['pf_id']
    unique = ['pf']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
               pk=pk, unique=unique, db=db)

    tb_name = 'def_pp_type'
    cols = [('pt_id',' SMALLINT'),
            ('pt',' varchar(20)'),
            ('pp_broad_cat', 'varchar(100)'),
            ('color', 'VARCHAR(7)')]
    pk = ['pt_id']
    unique = ['pt']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'def_fuel'
    cols = [('fl_id', 'SMALLINT'), ('fl', 'varchar(20)'),
            ('co2_int', 'DOUBLE PRECISION'),
            ('is_ca', 'SMALLINT'),
            ('is_constrained', 'SMALLINT'),
            ('color', 'VARCHAR(7)')]
    pk = ['fl_id']
    unique = ['fl']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'def_encar'
    cols = [('ca_id', 'SMALLINT'),
            ('fl_id', 'SMALLINT', sc + '.def_fuel(fl_id)'),
            ('ca', 'VARCHAR(2)')]
    pk = ['ca_id']
    unique = ['ca']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'def_node'
    cols = [('nd_id', 'SMALLINT'),
            ('nd', 'VARCHAR(10)'),
            ('color', 'VARCHAR(7)')] + yr_getter('price_co2', 'DOUBLE PRECISION')
    pk = ['nd_id']
    unique = ['nd']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'node_encar'
    cols = [('nd_id', 'SMALLINT', sc + '.def_node(nd_id)'),
            ('ca_id', 'SMALLINT', sc + '.def_encar(ca_id)'),
            ('dmnd_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
            ('grid_losses', 'DOUBLE PRECISION'),
            ('grid_losses_absolute', 'DOUBLE PRECISION'),
            ] + yr_getter('dmnd_sum', 'DOUBLE PRECISION')
    pk = ['nd_id', 'ca_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
               pk=pk, unique=unique, db=db)


    tb_name = 'def_month'
    cols = [('mt_id',' SMALLINT'),
            ('month_min_hoy',' SMALLINT'),
            ('month_weight',' SMALLINT'),
            ('mt',' VARCHAR(3)')]
    pk = ['mt_id']
    unique = ['name']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'def_week'
    cols = [('wk_id',' SMALLINT'),
            ('wk',' SMALLINT'),
            ('week_weight', 'SMALLINT')]
    pk = ['wk_id']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'def_plant'
    cols = [('pp_id',' SMALLINT'), ('pp',' VARCHAR(20)'),
            ('nd_id',' SMALLINT', sc + '.def_node(nd_id)'),
            ('fl_id',' SMALLINT', sc + '.def_fuel(fl_id)'),
            ('pt_id',' SMALLINT', sc + '.def_pp_type(pt_id)'),
            ('set_def_pr',' SMALLINT'),
            ('set_def_cain',' SMALLINT'),
            ('set_def_ror',' SMALLINT'),
            ('set_def_pp',' SMALLINT'), ('set_def_st',' SMALLINT'),
            ('set_def_hyrs',' SMALLINT'),
            ('set_def_chp',' SMALLINT'),
            ('set_def_add',' SMALLINT'),
            ('set_def_rem',' SMALLINT'),
            ('set_def_sll',' SMALLINT'),
            ('set_def_curt',' SMALLINT'),
            ('set_def_lin',' SMALLINT'),
            ('set_def_scen',' SMALLINT'),
            ('set_def_winsol',' SMALLINT'),
            ('set_def_tr', 'SMALLINT'),
            ('set_def_peak', 'SMALLINT')]
    pk = ['pp_id']
    unique = ['pp']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'plant_month'
    cols = [('mt_id',' SMALLINT', sc + '.def_month(mt_id)'),
            ('pp_id',' SMALLINT', sc + '.def_plant(pp_id)'),
            ('hyd_erg_bc','DOUBLE PRECISION')]
    pk = ['mt_id', 'pp_id']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'profsupply'
    cols = [('supply_pf_id',' SMALLINT', sc + '.def_profile(pf_id)'),
            ('hy', 'NUMERIC(6,2)'),
            ('value','NUMERIC(9,8)')]
    pk = ['supply_pf_id', 'hy']
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
               pk=pk, unique=unique, db=db)

    tb_name = 'plant_encar'
    cols = [('pp_id',' SMALLINT', sc + '.def_plant(pp_id)'),
            ('ca_id',' SMALLINT', sc + '.def_encar(ca_id)'),
            ('supply_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
            ('pp_eff','DOUBLE PRECISION'),
            ('erg_max','DOUBLE PRECISION'),
            ('discharge_duration','DOUBLE PRECISION'),
            ('st_lss_rt','DOUBLE PRECISION'),
            ('st_lss_hr','DOUBLE PRECISION'),
            ('factor_lin_0', 'DOUBLE PRECISION'),
            ('factor_lin_1','DOUBLE PRECISION'),
            ('cap_avlb', 'DOUBLE PRECISION'),
            ('vc_ramp','DOUBLE PRECISION'),
            ('vc_om','DOUBLE PRECISION'),
           ] + (yr_getter('cap_pwr_leg', 'DOUBLE PRECISION')
             +  yr_getter('erg_chp', 'DOUBLE PRECISION'))
    pk = ['pp_id', 'ca_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'plant_encar_scenarios'
    cols = [('pp_id',' SMALLINT', sc + '.def_plant(pp_id)'),
            ('ca_id',' SMALLINT', sc + '.def_encar(ca_id)'),
            ('scenario', 'VARCHAR'),
           ] + (yr_getter('cap_pwr_leg', 'DOUBLE PRECISION'))
    pk = ['pp_id', 'ca_id', 'scenario']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'imex_comp'
    cols = [('nd_id', 'SMALLINT', sc + '.def_node(nd_id)'),
            ('nd_2_id', 'SMALLINT', sc + '.def_node(nd_id)'),
            ] + yr_getter('erg_trm', 'DOUBLE PRECISION', [2015])
    pk = ['nd_id', 'nd_2_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'profdmnd'
    cols = [('dmnd_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
            ('hy', 'NUMERIC(6,2)')] + yr_getter('value', 'NUMERIC(18,9)', [2015])
    pk = ['hy', 'dmnd_pf_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'profchp'
    cols = [('nd_id', 'SMALLINT', sc + '.def_node(nd_id)'),
            ('ca_id', 'SMALLINT', sc + '.def_encar(ca_id)'),
            ('hy', 'SMALLINT'), ('value', 'DOUBLE PRECISION')]
    pk = ['hy', 'nd_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'profinflow'
    cols = [('pp_id', 'SMALLINT', sc + '.def_plant(pp_id)'),
            ('ca_id', 'SMALLINT', sc + '.def_encar(ca_id)'),
            ('hy', 'SMALLINT'), ('value', 'DOUBLE PRECISION')]
    pk = ['hy', 'pp_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'profprice'
    cols = [('hy', 'NUMERIC(6,2)'),
            ('price_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
           ] + yr_getter('value', 'DOUBLE PRECISION', [2015])
    pk = ['hy', 'price_pf_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'fuel_node_encar'
    cols = ([('fl_id', 'SMALLINT', sc + '.def_fuel(fl_id)'),
             ('nd_id', 'SMALLINT', sc + '.def_node(nd_id)'),
             ('ca_id', 'SMALLINT', sc + '.def_encar(ca_id)'),
             ('pricesll_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
             ('pricebuy_pf_id', 'SMALLINT', sc + '.def_profile(pf_id)'),
             ('is_chp', 'SMALLINT'),
             ] + yr_getter('erg_inp', 'DOUBLE PRECISION')
               + yr_getter('vc_fl', 'DOUBLE PRECISION'))
    pk = ['fl_id', 'nd_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
               pk=pk, unique=unique, db=db)

    tb_name = 'fuel_node_encar_scenarios'
    cols = ([('fl_id', 'SMALLINT', sc + '.def_fuel(fl_id)'),
             ('nd_id', 'SMALLINT', sc + '.def_node(nd_id)'),
             ('ca_id', 'SMALLINT', sc + '.def_encar(ca_id)'),
             ('scenario', 'VARCHAR'),
             ] + yr_getter('erg_inp', 'DOUBLE PRECISION'))
    pk = ['fl_id', 'nd_id', 'scenario']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    # table with monthly parameter modifiers
    tb_name = 'parameter_month'
    cols = ([('set_1_name', 'VARCHAR'), # from {'nd_id', 'fl_id', 'pp_id'}
             ('set_2_name', 'VARCHAR'), # from {'nd_id', 'fl_id', 'pp_id'}
             ('set_1_id', 'SMALLINT'),
             ('set_2_id', 'SMALLINT'),
             ('mt_id',' SMALLINT', sc + '.def_month(mt_id)'),
             ('parameter', 'VARCHAR'), # the parameter this applies to
             ('mt_fact', 'NUMERIC(10,9)'),
             ('mt_fact_others', 'NUMERIC(10,9)'),
             ])
    pk = ['parameter', 'set_1_id', 'set_2_id', 'mt_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)

    tb_name = 'node_connect'
    cols = [('nd_id', 'SMALLINT', sc + '.def_node (nd_id)'),
            ('nd_2_id', 'SMALLINT', sc + '.def_node (nd_id)'),
            ('ca_id', 'SMALLINT', sc + '.def_encar (ca_id)'),
            ('mt_id', 'SMALLINT', sc + '.def_month(mt_id)'),
            ('cap_trme_leg', 'DOUBLE PRECISION'),
            ('cap_trmi_leg', 'DOUBLE PRECISION'),
            ]
    pk = ['nd_id', 'nd_2_id', 'mt_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)


    tb_name = 'hydro'
    cols = [('pp_id',' SMALLINT', sc + '.def_plant(pp_id)'),
            ('min_erg_mt_out_share', 'DOUBLE PRECISION'),
            ('max_erg_mt_in_share', 'DOUBLE PRECISION'),
            ('min_erg_share', 'DOUBLE PRECISION')]
    pk = ['pp_id']
    unique = []
    init_table(tb_name=tb_name, cols=cols, schema=sc, ref_schema=sc,
                   pk=pk, unique=unique, db=db)
