from typing import Union

import click
import numpy as np
import pandas as pd

from smf2db.api.report_util import format_io_processors, format_alias_management_groups, format_logical_control_units, \
    format_common_storage_summary, format_common_storage_detail, format_private_storage_summary, \
    format_private_storage_detail
from smf2db.api.util import setdatetime, converttolist, col_to_frame, to_int, is_bit_set
from smf2db.db_models.smf78_model import (Smf78Comn, Smf78Ioq, Smf78Iop, Smf78Amg, Smf78Cha, Smf78Lcu,
                                          Smf78Chap, Smf78Pvt, Smf78Pvsp)


def build_pro(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """Build the dataframe for RMF Product Section which will be uploaded to smf73_pro table.

    Args:
        df: The master dataframe which is created from the JSON file.

    Returns:
        The dataframe for the RMF product section or None if csc is not found in the database.
    """
    set_datetime = np.vectorize(setdatetime)
    df_pro = pd.concat([df['header'].apply(pd.Series),
                        df['smf78pro'].apply(pd.Series)],
                       axis=1).rename(
        columns={'sysId': 'smf78sid',
                 'sysInd': 'smf78flg', 'recType': 'smf_type'})
    df_pro['csc'] = np.nan
    df_pro['smf78sid'] = df_pro['smf78sid'].str.strip()
    df_pro['smf78ist'] = pd.to_datetime(df_pro['smf78ist'])
    df_pro['smf78gie'] = pd.to_datetime(df_pro['smf78gie'])
    df_pro['smf78int'] = pd.to_timedelta(df_pro['smf78int']) / np.timedelta64(1, 's')
    df_pro['smf78lgo'] = pd.to_timedelta(df_pro['smf78lgo']) / np.timedelta64(1, 'h')
    df_pro['datetime'] = set_datetime(df_pro['smf78ist'])
    df_pro['smf78flg'] = df_pro['smf78flg'].apply(lambda x: int(str(x), 16))
    df_pro['smf78fla'] = df_pro['smf78fla'].apply(lambda x: int(str(x), 16))
    df_pro['smf78prf'] = df_pro['smf78prf'].apply(lambda x: int(str(x), 16))
    df_pro['smf78srl'] = df_pro['smf78srl'].apply(lambda x: int(str(x), 16))
    df_pro['speed_boost'] = df_pro['smf78fla'].apply(lambda x: is_bit_set(x, 16, 10))
    df_pro['ziip_boost'] = df_pro['smf78fla'].apply(lambda x: is_bit_set(x, 16, 9))
    df_pro['smf_type'] = df_pro['smf_type'].astype(str) + '.' + df_pro['subType'].astype(str)
    df_pro = df_pro.set_index(
        ['datetime', 'smf78ist', 'smf78iet', 'smf_type', 'csc', 'smf78sid', 'smf78int', 'smf78sam'])
    return df_pro


def build_comn(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Virtual Storage Common Storage Data Section which will be uploaded to smf78_comn table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Virtual Storage Common Storage Data section.
    """
    if 'r782comn' in df.columns:
        df_comn = col_to_frame(df[df.index.get_level_values('smf_type') == '78.2'], 'r782comn', df_pro_idx)
        rename_dict = {}
        for col in df_comn.columns:
            if '.' in col:
                if 'r7822' in col:
                    rename_dict[col] = col.replace('r782', 's').replace('.', '_')
                else:
                    rename_dict[col] = col.replace('r782', '').replace('.', '_')
        df_comn = df_comn.rename(columns=rename_dict)
        df_comn['r782flg'] = df_comn['r782flg'].apply(lambda x: int(str(x), 16))
        df_comn['r782pa'] = df_comn['r782pa'].str[2:]
        df_comn['r782epa'] = df_comn['r782epa'].str[2:]
        df_comn['r782ca'] = df_comn['r782ca'].str[2:]
        df_comn['r782eca'] = df_comn['r782eca'].str[2:]
        df_comn['r782mla'] = df_comn['r782mla'].str[2:]
        df_comn['r782emla'] = df_comn['r782emla'].str[2:]
        df_comn['r782fla'] = df_comn['r782fla'].str[2:]
        df_comn['r782efla'] = df_comn['r782efla'].str[2:]
        df_comn['r782pla'] = df_comn['r782pla'].str[2:]
        df_comn['r782elpa'] = df_comn['r782elpa'].str[2:]
        df_comn['r782sa'] = df_comn['r782sa'].str[2:]
        df_comn['r782esa'] = df_comn['r782esa'].str[2:]
        df_comn['r782na'] = df_comn['r782na'].str[2:]
        df_comn['r782ena'] = df_comn['r782ena'].str[2:]
        df_comn['r782ruca'] = df_comn['r782ruca'].str[2:]
        df_comn['r782eruca'] = df_comn['r782eruca'].str[2:]
        df_comn['r782rucd'] = df_comn['r782flg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_csak = pd.DataFrame(df_comn['r782csak'].tolist(), index=df_comn.index)
        df_s227k = pd.DataFrame(df_comn['r782227k'].tolist(), index=df_comn.index)
        df_s228k = pd.DataFrame(df_comn['r782228k'].tolist(), index=df_comn.index)
        df_s231k = pd.DataFrame(df_comn['r782231k'].tolist(), index=df_comn.index)
        df_s241k = pd.DataFrame(df_comn['r782241k'].tolist(), index=df_comn.index)
        df_comn = pd.concat([df_comn.drop(columns=['r782csak', 'r782227k', 'r782228k', 'r782231k', 'r782241k']),
                             pd.json_normalize(df_csak[0]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_0', 'vsdbntme': 'csak_vsdbntme_0',
                                          'vsdbmax': 'csak_vsdbmax_0',
                                          'vsdbxtme': 'csak_vsdbxtme_0', 'vsdbtotl': 'csak_vsdbtotl_0',
                                          'vsdamin': 'csak_vsdamin_0',
                                          'vsdantme': 'csak_vsdantme_0', 'vsdamax': 'csak_vsdamax_0',
                                          'vsdaxtme': 'csak_vsdaxtme_0',
                                          'vsdatotl': 'csak_vsdatotl_0'}),
                             pd.json_normalize(df_csak[1]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_1', 'vsdbntme': 'csak_vsdbntme_1',
                                          'vsdbmax': 'csak_vsdbmax_1',
                                          'vsdbxtme': 'csak_vsdbxtme_1', 'vsdbtotl': 'csak_vsdbtotl_1',
                                          'vsdamin': 'csak_vsdamin_1',
                                          'vsdantme': 'csak_vsdantme_1', 'vsdamax': 'csak_vsdamax_1',
                                          'vsdaxtme': 'csak_vsdaxtme_1',
                                          'vsdatotl': 'csak_vsdatotl_1'}),
                             pd.json_normalize(df_csak[2]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_2', 'vsdbntme': 'csak_vsdbntme_2',
                                          'vsdbmax': 'csak_vsdbmax_2',
                                          'vsdbxtme': 'csak_vsdbxtme_2', 'vsdbtotl': 'csak_vsdbtotl_2',
                                          'vsdamin': 'csak_vsdamin_2',
                                          'vsdantme': 'csak_vsdantme_2', 'vsdamax': 'csak_vsdamax_2',
                                          'vsdaxtme': 'csak_vsdaxtme_2',
                                          'vsdatotl': 'csak_vsdatotl_2'}),
                             pd.json_normalize(df_csak[3]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_3', 'vsdbntme': 'csak_vsdbntme_3',
                                          'vsdbmax': 'csak_vsdbmax_3',
                                          'vsdbxtme': 'csak_vsdbxtme_3', 'vsdbtotl': 'csak_vsdbtotl_3',
                                          'vsdamin': 'csak_vsdamin_3',
                                          'vsdantme': 'csak_vsdantme_3', 'vsdamax': 'csak_vsdamax_3',
                                          'vsdaxtme': 'csak_vsdaxtme_3',
                                          'vsdatotl': 'csak_vsdatotl_3'}),
                             pd.json_normalize(df_csak[4]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_4', 'vsdbntme': 'csak_vsdbntme_4',
                                          'vsdbmax': 'csak_vsdbmax_4',
                                          'vsdbxtme': 'csak_vsdbxtme_4', 'vsdbtotl': 'csak_vsdbtotl_4',
                                          'vsdamin': 'csak_vsdamin_4',
                                          'vsdantme': 'csak_vsdantme_4', 'vsdamax': 'csak_vsdamax_4',
                                          'vsdaxtme': 'csak_vsdaxtme_4',
                                          'vsdatotl': 'csak_vsdatotl_4'}),
                             pd.json_normalize(df_csak[5]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_5', 'vsdbntme': 'csak_vsdbntme_5',
                                          'vsdbmax': 'csak_vsdbmax_5',
                                          'vsdbxtme': 'csak_vsdbxtme_5', 'vsdbtotl': 'csak_vsdbtotl_5',
                                          'vsdamin': 'csak_vsdamin_5',
                                          'vsdantme': 'csak_vsdantme_5', 'vsdamax': 'csak_vsdamax_5',
                                          'vsdaxtme': 'csak_vsdaxtme_5',
                                          'vsdatotl': 'csak_vsdatotl_5'}),
                             pd.json_normalize(df_csak[6]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_6', 'vsdbntme': 'csak_vsdbntme_6',
                                          'vsdbmax': 'csak_vsdbmax_6',
                                          'vsdbxtme': 'csak_vsdbxtme_6', 'vsdbtotl': 'csak_vsdbtotl_6',
                                          'vsdamin': 'csak_vsdamin_6',
                                          'vsdantme': 'csak_vsdantme_6', 'vsdamax': 'csak_vsdamax_6',
                                          'vsdaxtme': 'csak_vsdaxtme_6',
                                          'vsdatotl': 'csak_vsdatotl_6'}),
                             pd.json_normalize(df_csak[7]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_7', 'vsdbntme': 'csak_vsdbntme_7',
                                          'vsdbmax': 'csak_vsdbmax_7',
                                          'vsdbxtme': 'csak_vsdbxtme_7', 'vsdbtotl': 'csak_vsdbtotl_7',
                                          'vsdamin': 'csak_vsdamin_7',
                                          'vsdantme': 'csak_vsdantme_7', 'vsdamax': 'csak_vsdamax_7',
                                          'vsdaxtme': 'csak_vsdaxtme_7',
                                          'vsdatotl': 'csak_vsdatotl_7'}),
                             pd.json_normalize(df_csak[8]).rename(
                                 columns={'vsdbmin': 'csak_vsdbmin_8', 'vsdbntme': 'csak_vsdbntme_8',
                                          'vsdbmax': 'csak_vsdbmax_8',
                                          'vsdbxtme': 'csak_vsdbxtme_8', 'vsdbtotl': 'csak_vsdbtotl_8',
                                          'vsdamin': 'csak_vsdamin_8',
                                          'vsdantme': 'csak_vsdantme_8', 'vsdamax': 'csak_vsdamax_8',
                                          'vsdaxtme': 'csak_vsdaxtme_8',
                                          'vsdatotl': 'csak_vsdatotl_8'}),
                             pd.json_normalize(df_s227k[0]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_0', 'vsdbntme': 's227k_vsdbntme_0',
                                          'vsdbmax': 's227k_vsdbmax_0',
                                          'vsdbxtme': 's227k_vsdbxtme_0', 'vsdbtotl': 's227k_vsdbtotl_0'}),
                             pd.json_normalize(df_s227k[1]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_1', 'vsdbntme': 's227k_vsdbntme_1',
                                          'vsdbmax': 's227k_vsdbmax_1',
                                          'vsdbxtme': 's227k_vsdbxtme_1', 'vsdbtotl': 's227k_vsdbtotl_1'}),
                             pd.json_normalize(df_s227k[2]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_2', 'vsdbntme': 's227k_vsdbntme_2',
                                          'vsdbmax': 's227k_vsdbmax_2',
                                          'vsdbxtme': 's227k_vsdbxtme_2', 'vsdbtotl': 's227k_vsdbtotl_2'}),
                             pd.json_normalize(df_s227k[3]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_3', 'vsdbntme': 's227k_vsdbntme_3',
                                          'vsdbmax': 's227k_vsdbmax_3',
                                          'vsdbxtme': 's227k_vsdbxtme_3', 'vsdbtotl': 's227k_vsdbtotl_3'}),
                             pd.json_normalize(df_s227k[4]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_4', 'vsdbntme': 's227k_vsdbntme_4',
                                          'vsdbmax': 's227k_vsdbmax_4',
                                          'vsdbxtme': 's227k_vsdbxtme_4', 'vsdbtotl': 's227k_vsdbtotl_4'}),
                             pd.json_normalize(df_s227k[5]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_5', 'vsdbntme': 's227k_vsdbntme_5',
                                          'vsdbmax': 's227k_vsdbmax_5',
                                          'vsdbxtme': 's227k_vsdbxtme_5', 'vsdbtotl': 's227k_vsdbtotl_5'}),
                             pd.json_normalize(df_s227k[6]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_6', 'vsdbntme': 's227k_vsdbntme_6',
                                          'vsdbmax': 's227k_vsdbmax_6',
                                          'vsdbxtme': 's227k_vsdbxtme_6', 'vsdbtotl': 's227k_vsdbtotl_6'}),
                             pd.json_normalize(df_s227k[7]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_7', 'vsdbntme': 's227k_vsdbntme_7',
                                          'vsdbmax': 's227k_vsdbmax_7',
                                          'vsdbxtme': 's227k_vsdbxtme_7', 'vsdbtotl': 's227k_vsdbtotl_7'}),
                             pd.json_normalize(df_s227k[8]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_8', 'vsdbntme': 's227k_vsdbntme_8',
                                          'vsdbmax': 's227k_vsdbmax_8',
                                          'vsdbxtme': 's227k_vsdbxtme_8', 'vsdbtotl': 's227k_vsdbtotl_8'}),
                             pd.json_normalize(df_s227k[9]).rename(
                                 columns={'vsdbmin': 's227k_vsdbmin_all', 'vsdbntme': 's227k_vsdbntme_all',
                                          'vsdbmax': 's227k_vsdbmax_all',
                                          'vsdbxtme': 's227k_vsdbxtme_all', 'vsdbtotl': 's227k_vsdbtotl_all'}),
                             pd.json_normalize(df_s228k[0]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_0', 'vsdbntme': 's228k_vsdbntme_0',
                                          'vsdbmax': 's228k_vsdbmax_0',
                                          'vsdbxtme': 's228k_vsdbxtme_0', 'vsdbtotl': 's228k_vsdbtotl_0'}),
                             pd.json_normalize(df_s228k[1]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_1', 'vsdbntme': 's228k_vsdbntme_1',
                                          'vsdbmax': 's228k_vsdbmax_1',
                                          'vsdbxtme': 's228k_vsdbxtme_1', 'vsdbtotl': 's228k_vsdbtotl_1'}),
                             pd.json_normalize(df_s228k[2]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_2', 'vsdbntme': 's228k_vsdbntme_2',
                                          'vsdbmax': 's228k_vsdbmax_2',
                                          'vsdbxtme': 's228k_vsdbxtme_2', 'vsdbtotl': 's228k_vsdbtotl_2'}),
                             pd.json_normalize(df_s228k[3]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_3', 'vsdbntme': 's228k_vsdbntme_3',
                                          'vsdbmax': 's228k_vsdbmax_3',
                                          'vsdbxtme': 's228k_vsdbxtme_3', 'vsdbtotl': 's228k_vsdbtotl_3'}),
                             pd.json_normalize(df_s228k[4]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_4', 'vsdbntme': 's228k_vsdbntme_4',
                                          'vsdbmax': 's228k_vsdbmax_4',
                                          'vsdbxtme': 's228k_vsdbxtme_4', 'vsdbtotl': 's228k_vsdbtotl_4'}),
                             pd.json_normalize(df_s228k[5]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_5', 'vsdbntme': 's228k_vsdbntme_5',
                                          'vsdbmax': 's228k_vsdbmax_5',
                                          'vsdbxtme': 's228k_vsdbxtme_5', 'vsdbtotl': 's228k_vsdbtotl_5'}),
                             pd.json_normalize(df_s228k[6]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_6', 'vsdbntme': 's228k_vsdbntme_6',
                                          'vsdbmax': 's228k_vsdbmax_6',
                                          'vsdbxtme': 's228k_vsdbxtme_6', 'vsdbtotl': 's228k_vsdbtotl_6'}),
                             pd.json_normalize(df_s228k[7]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_7', 'vsdbntme': 's228k_vsdbntme_7',
                                          'vsdbmax': 's228k_vsdbmax_7',
                                          'vsdbxtme': 's228k_vsdbxtme_7', 'vsdbtotl': 's228k_vsdbtotl_7'}),
                             pd.json_normalize(df_s228k[8]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_8', 'vsdbntme': 's228k_vsdbntme_8',
                                          'vsdbmax': 's228k_vsdbmax_8',
                                          'vsdbxtme': 's228k_vsdbxtme_8', 'vsdbtotl': 's228k_vsdbtotl_8'}),
                             pd.json_normalize(df_s228k[9]).rename(
                                 columns={'vsdbmin': 's228k_vsdbmin_all', 'vsdbntme': 's228k_vsdbntme_all',
                                          'vsdbmax': 's228k_vsdbmax_all',
                                          'vsdbxtme': 's228k_vsdbxtme_all', 'vsdbtotl': 's228k_vsdbtotl_all'}),
                             pd.json_normalize(df_s231k[0]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_0', 'vsdbntme': 's231k_vsdbntme_0',
                                          'vsdbmax': 's231k_vsdbmax_0',
                                          'vsdbxtme': 's231k_vsdbxtme_0', 'vsdbtotl': 's231k_vsdbtotl_0'}),
                             pd.json_normalize(df_s231k[1]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_1', 'vsdbntme': 's231k_vsdbntme_1',
                                          'vsdbmax': 's231k_vsdbmax_1',
                                          'vsdbxtme': 's231k_vsdbxtme_1', 'vsdbtotl': 's231k_vsdbtotl_1'}),
                             pd.json_normalize(df_s231k[2]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_2', 'vsdbntme': 's231k_vsdbntme_2',
                                          'vsdbmax': 's231k_vsdbmax_2',
                                          'vsdbxtme': 's231k_vsdbxtme_2', 'vsdbtotl': 's231k_vsdbtotl_2'}),
                             pd.json_normalize(df_s231k[3]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_3', 'vsdbntme': 's231k_vsdbntme_3',
                                          'vsdbmax': 's231k_vsdbmax_3',
                                          'vsdbxtme': 's231k_vsdbxtme_3', 'vsdbtotl': 's231k_vsdbtotl_3'}),
                             pd.json_normalize(df_s231k[4]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_4', 'vsdbntme': 's231k_vsdbntme_4',
                                          'vsdbmax': 's231k_vsdbmax_4',
                                          'vsdbxtme': 's231k_vsdbxtme_4', 'vsdbtotl': 's231k_vsdbtotl_4'}),
                             pd.json_normalize(df_s231k[5]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_5', 'vsdbntme': 's231k_vsdbntme_5',
                                          'vsdbmax': 's231k_vsdbmax_5',
                                          'vsdbxtme': 's231k_vsdbxtme_5', 'vsdbtotl': 's231k_vsdbtotl_5'}),
                             pd.json_normalize(df_s231k[6]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_6', 'vsdbntme': 's231k_vsdbntme_6',
                                          'vsdbmax': 's231k_vsdbmax_6',
                                          'vsdbxtme': 's231k_vsdbxtme_6', 'vsdbtotl': 's231k_vsdbtotl_6'}),
                             pd.json_normalize(df_s231k[7]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_7', 'vsdbntme': 's231k_vsdbntme_7',
                                          'vsdbmax': 's231k_vsdbmax_7',
                                          'vsdbxtme': 's231k_vsdbxtme_7', 'vsdbtotl': 's231k_vsdbtotl_7'}),
                             pd.json_normalize(df_s231k[8]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_8', 'vsdbntme': 's231k_vsdbntme_8',
                                          'vsdbmax': 's231k_vsdbmax_8',
                                          'vsdbxtme': 's231k_vsdbxtme_8', 'vsdbtotl': 's231k_vsdbtotl_8'}),
                             pd.json_normalize(df_s231k[9]).rename(
                                 columns={'vsdbmin': 's231k_vsdbmin_all', 'vsdbntme': 's231k_vsdbntme_all',
                                          'vsdbmax': 's231k_vsdbmax_all',
                                          'vsdbxtme': 's231k_vsdbxtme_all', 'vsdbtotl': 's231k_vsdbtotl_all'}),
                             pd.json_normalize(df_s241k[0]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_0', 'vsdbntme': 's241k_vsdbntme_0',
                                          'vsdbmax': 's241k_vsdbmax_0',
                                          'vsdbxtme': 's241k_vsdbxtme_0', 'vsdbtotl': 's241k_vsdbtotl_0'}),
                             pd.json_normalize(df_s241k[1]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_1', 'vsdbntme': 's241k_vsdbntme_1',
                                          'vsdbmax': 's241k_vsdbmax_1',
                                          'vsdbxtme': 's241k_vsdbxtme_1', 'vsdbtotl': 's241k_vsdbtotl_1'}),
                             pd.json_normalize(df_s241k[2]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_2', 'vsdbntme': 's241k_vsdbntme_2',
                                          'vsdbmax': 's241k_vsdbmax_2',
                                          'vsdbxtme': 's241k_vsdbxtme_2', 'vsdbtotl': 's241k_vsdbtotl_2'}),
                             pd.json_normalize(df_s241k[3]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_3', 'vsdbntme': 's241k_vsdbntme_3',
                                          'vsdbmax': 's241k_vsdbmax_3',
                                          'vsdbxtme': 's241k_vsdbxtme_3', 'vsdbtotl': 's241k_vsdbtotl_3'}),
                             pd.json_normalize(df_s241k[4]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_4', 'vsdbntme': 's241k_vsdbntme_4',
                                          'vsdbmax': 's241k_vsdbmax_4',
                                          'vsdbxtme': 's241k_vsdbxtme_4', 'vsdbtotl': 's241k_vsdbtotl_4'}),
                             pd.json_normalize(df_s241k[5]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_5', 'vsdbntme': 's241k_vsdbntme_5',
                                          'vsdbmax': 's241k_vsdbmax_5',
                                          'vsdbxtme': 's241k_vsdbxtme_5', 'vsdbtotl': 's241k_vsdbtotl_5'}),
                             pd.json_normalize(df_s241k[6]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_6', 'vsdbntme': 's241k_vsdbntme_6',
                                          'vsdbmax': 's241k_vsdbmax_6',
                                          'vsdbxtme': 's241k_vsdbxtme_6', 'vsdbtotl': 's241k_vsdbtotl_6'}),
                             pd.json_normalize(df_s241k[7]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_7', 'vsdbntme': 's241k_vsdbntme_7',
                                          'vsdbmax': 's241k_vsdbmax_7',
                                          'vsdbxtme': 's241k_vsdbxtme_7', 'vsdbtotl': 's241k_vsdbtotl_7'}),
                             pd.json_normalize(df_s241k[8]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_8', 'vsdbntme': 's241k_vsdbntme_8',
                                          'vsdbmax': 's241k_vsdbmax_8',
                                          'vsdbxtme': 's241k_vsdbxtme_8', 'vsdbtotl': 's241k_vsdbtotl_8'}),
                             pd.json_normalize(df_s241k[9]).rename(
                                 columns={'vsdbmin': 's241k_vsdbmin_all', 'vsdbntme': 's241k_vsdbntme_all',
                                          'vsdbmax': 's241k_vsdbmax_all',
                                          'vsdbxtme': 's241k_vsdbxtme_all', 'vsdbtotl': 's241k_vsdbtotl_all'})], axis=1)
        datetime_cols = list(set([column.name for column in Smf78Comn.__table__.columns if
                                  'DATETIME' in str(column.type)]) - {'smf78ist', 'datetime'})
        for col in datetime_cols:
            df_comn[col] = pd.to_datetime(df_comn[col], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df_comn = df_comn.copy().reset_index()[Smf78Comn.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Comn.__table__.primary_key.columns.values()])
    else:
        df_comn = pd.DataFrame(columns=Smf78Comn.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Comn.__table__.primary_key.columns.values()])
    return df_comn


def build_pvt(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Virtual Storage Private Area Data Section which will be uploaded to smf78_pvt table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Virtual Storage Private Area Data section.
    """
    if 'r782pvt' in df.columns:
        df_pvt = col_to_frame(df[df.index.get_level_values('smf_type') == '78.2'], 'r782pvt', df_pro_idx)
        rename_dict = {}
        for col in df_pvt.columns:
            if '.' in col:
                rename_dict[col] = col.replace('r782', '').replace('.', '_')
        df_pvt = df_pvt.rename(columns=rename_dict)
        df_pvt['r782flgs'] = df_pvt['r782flgs'].apply(lambda x: int(str(x), 16))
        df_pvt['r782actv'] = df_pvt['r782flgs'].apply(lambda x: is_bit_set(x, 16, 0))
        df_pvt['r782term'] = df_pvt['r782flgs'].apply(lambda x: is_bit_set(x, 16, 1))
        df_pvt['r782glch'] = df_pvt['r782flgs'].apply(lambda x: is_bit_set(x, 16, 2))
        df_pvt['r782invl'] = df_pvt['r782flgs'].apply(lambda x: is_bit_set(x, 16, 3))
        df_pvt['r782shra'] = df_pvt['r782flgs'].apply(lambda x: is_bit_set(x, 16, 4))
        df_pvt['r782urab'] = df_pvt['r782urab'].str[2:]
        df_pvt['r782uraa'] = df_pvt['r782uraa'].str[2:]
        datetime_cols = list(set([column.name for column in Smf78Pvt.__table__.columns
                                  if 'DATETIME' in str(column.type)]) - {'smf78ist', 'datetime'})
        for col in df_pvt.columns:
            if col in datetime_cols:
                df_pvt[col] = pd.to_datetime(df_pvt[col], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df_pvt = df_pvt.reset_index()[Smf78Pvt.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Pvt.__table__.primary_key.columns.values()])
    else:
        df_pvt = pd.DataFrame(columns=Smf78Pvt.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Pvt.__table__.primary_key.columns.values()])
    return df_pvt


def build_pvsp(df: pd.DataFrame, df_pvt: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Virtual Storage Private Area Subpool Section which will be uploaded to smf78_pvsp table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pvt: The dataframe of Virtual Storage Private Area Data section.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the Virtual Storage Private Area Subpool section.
    """
    convert_to_list = np.vectorize(converttolist)
    def _df_pvsp(pvsp_idx):
        try:
            pvsp = df_x.loc[pvsp_idx]
            return pvsp.to_dict()
        except KeyError:
            return {}

    get_df_pvsp = np.vectorize(_df_pvsp)
    if 'r782pvsp' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '78.2')].reset_index()['r782pvsp'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z['r782pvsp'] = convert_to_list(z['r782pvsp'])
        x = z.explode('r782pvsp').reset_index()
        x['pvsp_idx'] = x.groupby(['smf78sid', 'datetime', 'smf78ist', 'smf78iet']).cumcount() + 1
        x.set_index(['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'pvsp_idx'], inplace=True)
        df_x = pd.json_normalize(x['r782pvsp']).set_index(x.index).rename(
            columns={'r782spd.vsdbntme': 'spd_vsdbntme', 'r782spd.vsdbxtme': 'spd_vsdbxtme',
                     'r782spd.vsdbmin': 'spd_vsdbmin', 'r782spd.vsdbmax': 'spd_vsdbmax', 'r782spd.vsdbtotl': 'spd_vsdbtotl'})
        df_x['spd_vsdbntme'] = pd.to_datetime(df_x['spd_vsdbntme'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df_x['spd_vsdbxtme'] = pd.to_datetime(df_x['spd_vsdbxtme'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df_pvsp = df_pvt[df_pvt['r782subn'] > 0].copy().reset_index().set_index(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r782jobn'])[['r782subi', 'r782subn']]
        df_pvsp['pvsp_cnt'] = df_pvsp.r782subn - df_pvsp.r782subi + 1
        df_pvsp = df_pvsp.reindex(df_pvsp.index.repeat(df_pvsp.pvsp_cnt))
        df_pvsp['pvsp_idx'] = df_pvsp.groupby(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r782jobn']
                                              ).cumcount() + df_pvsp['r782subi']

        df_pvsp = df_pvsp.reset_index().set_index(['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'pvsp_idx'])
        df_pvsp['pvsp'] = get_df_pvsp(df_pvsp.index)
        df_pvsp = pd.concat([df_pvsp,
                             pd.json_normalize(df_pvsp['pvsp']).set_index(df_pvsp.index)],
                            axis=1).drop(columns=['pvsp'])
        df_pvsp = df_pvsp.reset_index()[Smf78Pvsp.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Pvsp.__table__.primary_key.columns.values()])
    else:
        df_pvsp = pd.DataFrame(columns=Smf78Pvsp.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Pvsp.__table__.primary_key.columns.values()])
    return df_pvsp


def build_ioq(df: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for I/O Queuing global data which will be uploaded to smf78_ioq table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The dataframe for the I/O queuing global section.
    """
    if 'r783gd' in df.columns:
        df_ioq = col_to_frame(df[df.index.get_level_values('smf_type') == '78.3'], 'r783gd', df_pro_idx).rename(
            columns={'r783tok.r783tdt': 'r783tdt', 'r783tok.r783ttm': 'r783ttm'})
        df_ioq['r783gflg'] = df_ioq['r783gflg'].apply(lambda x: int(str(x), 16))
        df_ioq['r783gflx'] = df_ioq['r783gflx'].apply(lambda x: int(str(x), 16))
        df_ioq['r783cfl'] = df_ioq['r783cfl'].apply(lambda x: int(str(x), 16))
        df_ioq['data_invalid_ch_failure'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ioq['diagnose_failed'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ioq['store_primary_not_supported'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ioq['dcm_hw_supported'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 3))
        df_ioq['dcm_managed_ch'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 4))
        df_ioq['iop_util_data_supported'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 5))
        df_ioq['command_response_time_supported'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 6))
        df_ioq['transfer_ready_disabled_aval'] = df_ioq['r783gflg'].apply(lambda x: is_bit_set(x, 8, 7))
        df_ioq['alias_management_aval'] = df_ioq['r783gflx'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ioq['eadm_compression_aval'] = df_ioq['r783gflx'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ioq['scm_aval'] = df_ioq['r783gflx'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ioq['config_changed'] = df_ioq['r783cfl'].apply(lambda x: is_bit_set(x, 8, 0))
        df_ioq['config_changed_since_ipl'] = df_ioq['r783cfl'].apply(lambda x: is_bit_set(x, 8, 1))
        df_ioq['ipl_iodf'] = df_ioq['r783cfl'].apply(lambda x: is_bit_set(x, 8, 2))
        df_ioq['io_config_token_valid'] = df_ioq['r783cfl'].apply(lambda x: is_bit_set(x, 8, 3))
        df_ioq['multi_ch_subsys_allowed'] = df_ioq['r783cfl'].apply(lambda x: is_bit_set(x, 8, 4))
        df_ioq = df_ioq.set_index(
            [col.name for col in Smf78Ioq.__table__.primary_key.columns.values()])
    else:
        df_ioq = pd.DataFrame(columns=Smf78Ioq.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Ioq.__table__.primary_key.columns.values()])
    return df_ioq


def build_iop(df_ioq: pd.DataFrame) -> pd.DataFrame:
    """Build the dataframe for Input Output Processor (IOP) data which will be uploaded to smf78_iop table.

    Args:
        df_ioq: The dataframe of the I/O queuing global section.

    Returns:
        The dataframe for the Input Output Processor (IOP) data.
    """
    if df_ioq.shape[0] > 0:
        df_iop = col_to_frame(df_ioq, 'r783iqd', df_ioq.reset_index().set_index(
            ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'smf78int', 'iop_util_data_supported']).index)#.rename(
            # columns={'r783iqsm': 'entries_iop_queue'})
        df_iop['r783iqid'] = df_iop['r783iqid'].str[2:]
        df_iop['r783iflg'] = df_iop['r783iflg'].apply(lambda x: int(str(x), 16))
        df_iop['iop_installed'] = df_iop['r783iflg'].apply(lambda x: is_bit_set(x, 8, 0))
        df_iop['iopac'] = df_iop['r783iqct'] / df_iop['smf78int']
        df_iop['r783iipb'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783iipb'], np.nan)
        df_iop['r783iipi'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783iipi'], np.nan)
        df_iop['r783iifs'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783iifs'], np.nan)
        df_iop['r783ipii'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783ipii'], np.nan)
        df_iop['r783icpb'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783icpb'], np.nan)
        df_iop['r783idpb'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783idpb'], np.nan)
        df_iop['r783icub'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783icub'], np.nan)
        df_iop['r783idvb'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783idvb'], np.nan)
        df_iop['iopipb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    df_iop['r783iipb'] * 100 / (df_iop['r783iipb'] + df_iop['r783iipi']), np.nan)
        df_iop['iopecb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    df_iop['r783iecb'] * 100 / (df_iop['r783iipb'] + df_iop['r783iipi']), np.nan)
        df_iop['iopscb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    df_iop['r783iscb'] * 100 / (df_iop['r783iipb'] + df_iop['r783iipi']), np.nan)
        df_iop['iopipi'] = np.where(df_iop.iop_util_data_supported == 1,
                                    df_iop['r783iipi'] * 100 / (df_iop['r783iipb'] + df_iop['r783iipi']), np.nan)
        df_iop['iorifs'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783iifs'] / df_iop['smf78int'],
                                    np.nan)
        df_iop['iorpii'] = np.where(df_iop.iop_util_data_supported == 1, df_iop['r783ipii'] / df_iop['smf78int'],
                                    np.nan)
        df_iop['iopalb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    ((df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop['r783icub'] + df_iop[
                                        'r783idvb']) * 100 /
                                     (df_iop['r783iifs'] + df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop[
                                         'r783icub'] + df_iop['r783idvb'])), np.nan)
        df_iop['iopchb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    (df_iop['r783icpb'] * 100 / (
                                                df_iop['r783iifs'] + df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop[
                                            'r783icub'] +
                                                df_iop['r783idvb'])), np.nan)
        df_iop['iopdpb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    (df_iop['r783idpb'] * 100 / (
                                                df_iop['r783iifs'] + df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop[
                                            'r783icub'] +
                                                df_iop['r783idvb'])), np.nan)
        df_iop['iopcub'] = np.where(df_iop.iop_util_data_supported == 1,
                                    (df_iop['r783icub'] * 100 / (
                                                df_iop['r783iifs'] + df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop[
                                            'r783icub'] +
                                                df_iop['r783idvb'])), np.nan)
        df_iop['iopdvb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    (df_iop['r783idvb'] * 100 / (
                                                df_iop['r783iifs'] + df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop[
                                            'r783icub'] +
                                                df_iop['r783idvb'])), np.nan)
        df_iop['ionalb'] = np.where(df_iop.iop_util_data_supported == 1,
                                    (df_iop['r783icpb'] + df_iop['r783idpb'] + df_iop['r783icub'] + df_iop[
                                        'r783idvb']) / df_iop['r783iifs'], np.nan)
        df_iop['ionchb'] = df_iop['r783icpb'] / df_iop['r783iifs']
        df_iop['iondpb'] = df_iop['r783idpb'] / df_iop['r783iifs']
        df_iop['ioncub'] = df_iop['r783icub'] / df_iop['r783iifs']
        df_iop['iondvb'] = df_iop['r783idvb'] / df_iop['r783iifs']
        df_iop['iopql'] = (df_iop['r783iqsm'] - df_iop['r783iqct']) / df_iop['r783iqct']
        df_iop = df_iop.reset_index()[Smf78Iop.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Iop.__table__.primary_key.columns.values()])
    else:
        df_iop = pd.DataFrame(columns=Smf78Iop.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Iop.__table__.primary_key.columns.values()])
    return df_iop


def update_ioq(df_ioq: pd.DataFrame, df_iop: pd.DataFrame) -> pd.DataFrame:
    """Update the I/O queuing dataframe based on the data from IOP dataframe.

    Args:
        df_ioq: The dataframe of the I/O queuing global section.
        df_iop: The dataframe of the Input Output Processor (IOP) data section.

    Returns:
        The dataframe for the I/O queuing global section.
    """
    if df_iop.shape[0] > 0:
        agg_iop = {'iop_installed': 'last', 'r783iqsm': 'sum', 'r783iqct': 'sum', 'r783iipb': 'sum',
                   'r783iipi': 'sum', 'r783iifs': 'sum', 'r783ipii': 'sum', 'r783icpb': 'sum', 'r783idpb': 'sum',
                   'r783icub': 'sum', 'r783idvb': 'sum', 'r783iscb': 'sum', 'r783iecb': 'sum',
                   'r783iflg': 'last'}
        df_iop_gp = df_iop.groupby(['smf78sid', 'datetime', 'smf78ist', 'smf78iet']).agg(agg_iop)
        df_ioq = pd.concat([df_ioq.reset_index().set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet']), df_iop_gp], axis=1)
        df_ioq['iopac'] = df_ioq['r783iqct'] / df_ioq['smf78int']
        df_ioq['iopipb'] = df_ioq['r783iipb'] * 100 / (df_ioq['r783iipb'] + df_ioq['r783iipi'])
        df_ioq['iopecb'] = df_ioq['r783iecb'] * 100 / (df_ioq['r783iipb'] + df_ioq['r783iipi'])
        df_ioq['iopscb'] = df_ioq['r783iscb'] * 100 / (df_ioq['r783iipb'] + df_ioq['r783iipi'])
        df_ioq['iopipi'] = df_ioq['r783iipi'] * 100 / (df_ioq['r783iipb'] + df_ioq['r783iipi'])
        df_ioq['iorifs'] = df_ioq['r783iifs'] / df_ioq['smf78int']
        df_ioq['iorpii'] = df_ioq['r783ipii'] / df_ioq['smf78int']
        df_ioq['iopalb'] = ((df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] + df_ioq['r783idvb']) * 100 /
                            (df_ioq['r783iifs'] + df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] + df_ioq[
                                'r783idvb']))
        df_ioq['iopchb'] = (df_ioq['r783icpb'] * 100 / (
                    df_ioq['r783iifs'] + df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] +
                    df_ioq['r783idvb']))
        df_ioq['iopdpb'] = (df_ioq['r783idpb'] * 100 / (
                    df_ioq['r783iifs'] + df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] +
                    df_ioq['r783idvb']))
        df_ioq['iopcub'] = (df_ioq['r783icub'] * 100 / (
                    df_ioq['r783iifs'] + df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] +
                    df_ioq['r783idvb']))
        df_ioq['iopdvb'] = (df_ioq['r783idvb'] * 100 / (
                    df_ioq['r783iifs'] + df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] +
                    df_ioq['r783idvb']))
        df_ioq['ionalb'] = (df_ioq['r783icpb'] + df_ioq['r783idpb'] + df_ioq['r783icub'] + df_ioq['r783idvb']) / df_ioq[
            'r783iifs']
        df_ioq['ionchb'] = df_ioq['r783icpb'] / df_ioq['r783iifs']
        df_ioq['iondpb'] = df_ioq['r783idpb'] / df_ioq['r783iifs']
        df_ioq['ioncub'] = df_ioq['r783icub'] / df_ioq['r783iifs']
        df_ioq['iondvb'] = df_ioq['r783idvb'] / df_ioq['r783iifs']
        df_ioq['iopql'] = (df_ioq['r783iqsm'] - df_ioq['r783iqct']) / df_ioq['r783iqct']
        df_ioq = df_ioq.reset_index()[Smf78Ioq.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Ioq.__table__.primary_key.columns.values()])
    return df_ioq


def build_lcu(df: pd.DataFrame, df_ioq_idx: pd.Index) -> pd.DataFrame:
    """Build the dataframe for Logical Control Unit data which will be uploaded to smf78_lcu table.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_ioq_idx: The index of the I/O queuing dataframe.

    Returns:
        The dataframe for the Logical Control Unit data.
    """
    if 'r783ds' in df.columns:
        df_lcu = col_to_frame(df[df.index.get_level_values('smf_type') == '78.3'], 'r783ds', df_ioq_idx)
        df_lcu['r783dst'] = df_lcu['r783dst'].apply(lambda x: int(str(x), 16))
        df_lcu['r783dstx'] = df_lcu['r783dstx'].apply(lambda x: int(str(x), 16))
        df_lcu['r783id2'] = df_lcu['r783id2'].str[2:]
        df_lcu['no_hw_measurement'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 0))
        df_lcu['dynamically_changed'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 1))
        df_lcu['dynamically_added'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 2))
        df_lcu['config_change_attempt'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 3))
        df_lcu['lcu_has_dcm_ch'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 4))
        df_lcu['path_attr_valid'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 5))
        df_lcu['lcu_has_hyperpav'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 6))
        df_lcu['lcu_has_superpav'] = df_lcu['r783dst'].apply(lambda x: is_bit_set(x, 8, 7))
        df_lcu['lcu_has_ficon'] = df_lcu['r783dstx'].apply(lambda x: is_bit_set(x, 8, 0))
        df_lcu['connect_time_invalid'] = df_lcu['r783dstx'].apply(lambda x: is_bit_set(x, 8, 1))
        df_lcu['disconnect_time_invalid'] = df_lcu['r783dstx'].apply(lambda x: is_bit_set(x, 8, 2))
        df_lcu['r783cbtm'] = pd.to_timedelta(df_lcu['r783cbtm']) / np.timedelta64(1, 's')
        df_lcu['r783cmrm'] = pd.to_timedelta(df_lcu['r783cmrm']) / np.timedelta64(1, 's')
        df_lcu['r783dctm'] = pd.to_timedelta(df_lcu['r783dctm']) / np.timedelta64(1, 's')
        df_lcu['r783ddtm'] = pd.to_timedelta(df_lcu['r783ddtm']) / np.timedelta64(1, 's')
        df_lcu['r783csst'] = pd.to_timedelta(df_lcu['r783csst']) / np.timedelta64(1, 's')
        df_lcu['csc'] = np.nan
        df_lcu = df_lcu.set_index(
            [col.name for col in Smf78Lcu.__table__.primary_key.columns.values()])
    else:
        df_lcu = pd.DataFrame(columns=Smf78Lcu.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Lcu.__table__.primary_key.columns.values()])
    return df_lcu


def update_lcu_hpav(df: pd.DataFrame, df_lcu: pd.DataFrame, df_pro_idx: pd.Index) -> pd.DataFrame:
    """Update the dataframe for Logical Control Unit if HyperPAV/SuperPAV Data section exist in the master dataframe.

    Args:
        df: The master dataframe which is created from the JSON file.
        df_lcu: The dataframe of the Logical Control Unit
        df_pro_idx: The index of the RMF product section dataframe.

    Returns:
        The modified dataframe for the Logical Control Unit data.
    """
    convert_to_list = np.vectorize(converttolist)
    if 'r783hpav' in df.columns:
        z = df[(df.index.get_level_values('smf_type') == '78.3')].reset_index()['r783hpav'].to_frame().set_index(
            df_pro_idx)
        z.dropna(how='all', inplace=True)
        z = z.reset_index().reset_index().set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'index'])
        z['r783hpav'] = convert_to_list(z['r783hpav'])
        x = z.explode('r783hpav').reset_index()
        x['r783hix'] = x.groupby(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'index']).cumcount() + 1
        x.set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'index', 'r783hix'], inplace=True)
        df_hpav = pd.json_normalize(x['r783hpav']).set_index(x.index)
        df_hpav['r783hcu'] = df_hpav['r783hcu'].str[2:]
        df_lcu = df_lcu.reset_index().set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'index', 'r783hix'])
        df_lcu = df_lcu.join(df_hpav)
        df_lcu = df_lcu.reset_index().set_index(
            [col.name for col in Smf78Lcu.__table__.primary_key.columns.values()])
    return df_lcu


def build_cha(df_cs: pd.DataFrame) -> tuple:
    """Build the dataframes of the channel path data.

    Args:
        df_cs: The dataframe of the I/O Queuing Configuration Control section.

    Returns:
        The dataframe of the channel path data.
        The dataframe of the Alias Managment Group member's channel path data.
    """
    convert_2_int = np.vectorize(to_int)
    if df_cs.shape[0] > 0:
        df_cha = col_to_frame(df_cs, 'r783cpd', df_cs.index)
        df_cha['r783cpst'] = df_cha['r783cpst'].apply(lambda x: int(str(x), 16))
        df_cha['r783cpxf'] = df_cha['r783cpxf'].apply(lambda x: int(str(x), 16))
        df_cha['r783cpid'] = df_cha['r783cpid'].str[2:]
        df_cha['ch_path_installed'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cha['ch_path_online'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cha['ch_path_varied'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 2))
        df_cha['ch_path_offline'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 3))
        df_cha['vary_path_action'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 4))
        df_cha['ch_path_data_invalid'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 5))
        df_cha['ch_path_dcm'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 6))
        df_cha['chpid_manipulated'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 7))
        df_cha['r783cu1'] = df_cha['r783cu1'].str[2:]
        df_cha['r783cu2'] = df_cha['r783cu2'].str[2:]
        df_cha['r783cu3'] = df_cha['r783cu3'].str[2:]
        df_cha['r783cu4'] = df_cha['r783cu4'].str[2:]
        df_cha['r783cbt'] = pd.to_timedelta(df_cha['r783cbt']) / np.timedelta64(1, 's')
        df_cha['r783cmr'] = pd.to_timedelta(df_cha['r783cmr']) / np.timedelta64(1, 's')
        df_cha['extended_io_measurement1'] = df_cha['r783cpxf'].apply(lambda x: is_bit_set(x, 8, 0))
        df_cha['extended_io_measurement2'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 1))
        df_cha['first_transfer_ready_disabled'] = df_cha['r783cpst'].apply(lambda x: is_bit_set(x, 8, 2))
        # df_cha['path_attributes'] = flag_loc(df_cha['r783cpat'], 0)
        df_cha['r783cpat'] = convert_2_int(df_cha['r783cpat'])
        df_cha['iocbt'] = df_cha.r783cbt * 1000 / df_cha.r783pt
        df_cha['iocmr'] = df_cha.r783cmr * 1000 / df_cha.r783pt
        df_cha['iotmdinh'] = (df_cha['r783ctmw'] - df_cha['r783ctrd']) / df_cha['r783ctmw']
        df_cha['ioart'] = df_cha['r783pt'] / df_cha['smf78int']
        df_cha['total_requests'] = df_cha['r783pt'] + df_cha['r783dpb'] + df_cha['r783cub']
        df_cha['iocub'] = df_cha['r783cub'] * 100 / df_cha['total_requests']
        df_cha['iodpb'] = df_cha['r783dpb'] * 100 / df_cha['total_requests']
        df_cha['iocbt'] = df_cha['r783cbt'] * 1000 / df_cha['r783pt']
        df_cha['iocmr'] = df_cha['r783cmr'] * 1000 / df_cha['r783pt']
        chap_cols = [col.name for col in Smf78Cha.__table__.primary_key.columns.values()] + ['r783amgs']
        df_chap = df_cha[(df_cha.ch_path_installed == 1) & (df_cha.alias_management_aval == 1)][
            chap_cols].drop_duplicates()
        df_cha = df_cha.reset_index()[Smf78Cha.__table__.columns.keys()].set_index(
            [col.name for col in Smf78Cha.__table__.primary_key.columns.values()])
    else:
        df_cha = pd.DataFrame(columns=Smf78Cha.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Cha.__table__.primary_key.columns.values()])
        df_chap = pd.DataFrame(columns=Smf78Chap.__table__.columns.keys()).set_index(
            [col.name for col in Smf78Chap.__table__.primary_key.columns.values()])
    return df_cha, df_chap


def update_lcu_cha(df_lcu: pd.DataFrame, df_cha: pd.DataFrame) -> pd.DataFrame:
    df_cha_gp2 = df_cha.reset_index().rename(columns={'r783id1': 'r783id2'}).groupby(
        ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783id2']).agg(
        {'r783cun': 'first', 'r783cu1': 'first', 'r783cu2': 'first', 'r783cu3': 'first', 'r783cu4': 'first',
         'r783pt': 'sum', 'r783dpb': 'sum', 'r783cub': 'sum', 'r783cbt': 'sum', 'r783cmr': 'sum'})
    df_lcu = pd.concat([df_lcu.reset_index().set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783id2']),
                        df_cha_gp2], axis=1)
    df_lcu['r783cu4'] = np.where(df_lcu['r783cun'] < 4, np.nan, df_lcu['r783cu4'])
    df_lcu['r783cu3'] = np.where(df_lcu['r783cun'] < 3, np.nan, df_lcu['r783cu3'])
    df_lcu['r783cu2'] = np.where(df_lcu['r783cun'] < 2, np.nan, df_lcu['r783cu2'])
    df_lcu['iocss'] = df_lcu['r783csst'] * 1000 / df_lcu['r783pt']
    df_lcu['ioart'] = df_lcu['r783pt'] / df_lcu['smf78int']
    df_lcu['total_requests'] = df_lcu['r783pt'] + df_lcu['r783dpb'] + df_lcu['r783cub']
    df_lcu['iocub'] = df_lcu['r783cub'] * 100 / df_lcu['total_requests']
    df_lcu['iodpb'] = df_lcu['r783dpb'] * 100 / df_lcu['total_requests']
    df_lcu['iocbt'] = df_lcu['r783cbt'] * 1000 / df_lcu['r783pt']
    df_lcu['iocmr'] = df_lcu['r783cmr'] * 1000 / df_lcu['r783pt']
    df_lcu['ioctr'] = df_lcu['r783qct'] / df_lcu['smf78int']
    df_lcu['iodlq'] = (df_lcu['r783qsm'] - df_lcu['r783qct']) / df_lcu['r783qct']
    if 'r783hnai' in df_lcu.columns:
        df_lcu['iohwait'] = np.where((df_lcu['lcu_has_hyperpav'] == 1) | (df_lcu['lcu_has_superpav'] == 1),
                                     df_lcu['r783hnai'] / df_lcu['r783htio'], np.nan)
        df_lcu['iohmax'] = np.where((df_lcu['lcu_has_hyperpav'] == 1) | (df_lcu['lcu_has_superpav'] == 1),
                                    df_lcu['r783haiu'] + df_lcu['r783xhbc'], np.nan)
        df_lcu['iohdmax'] = np.where((df_lcu['lcu_has_hyperpav'] == 1) | (df_lcu['lcu_has_superpav'] == 1),
                                     df_lcu['r783hcad'], np.nan)
        df_lcu['iohioqc'] = np.where((df_lcu['lcu_has_hyperpav'] == 1) | (df_lcu['lcu_has_superpav'] == 1),
                                     df_lcu['r783hioq'], np.nan)
        df_lcu['ioxsareq'] = df_lcu['r783xauc'] / df_lcu['r783xanc']
        df_lcu['ioxuahrq'] = df_lcu['r783xnhc'] / df_lcu['r783xanc']
        df_lcu['ioxcqd'] = df_lcu['r783xcqd'] / df_lcu['r783xanc']
        df_lcu['ioxiuac'] = df_lcu['r783xciu'] / df_lcu['r783xanc']
        df_lcu['ioxabc'] = df_lcu['r783xabc'] / df_lcu['smf78int']
        df_lcu['ioxhcba'] = df_lcu['r783xhbc']
        df_lcu['ioxalc'] = df_lcu['r783xalc'] / df_lcu['smf78int']
        df_lcu['ioxhcla'] = df_lcu['r783xhlc']
    else:
        df_lcu['r783hcu'], df_lcu['r783hnai'], df_lcu['r783htio'], df_lcu['r783haiu'], df_lcu['r783hcad'], \
        df_lcu['r783hioq'], df_lcu['r783xanc'], df_lcu['r783xauc'], df_lcu['r783xnhc'], df_lcu['r783xabc'],\
        df_lcu['r783xcbc'], df_lcu['r783xhbc'], df_lcu['r783xalc'], df_lcu['r783xclc'], df_lcu['r783xhlc'],\
        df_lcu['r783xnag'], df_lcu['r783xcqd'], df_lcu['r783xciu'] = np.nan, np.nan, np.nan, np.nan, np.nan,\
                                                                     np.nan, np.nan, np.nan, np.nan, np.nan,\
                                                                     np.nan, np.nan, np.nan, np.nan, np.nan,\
                                                                     np.nan, np.nan, np.nan
        df_lcu['iohwait'] = np.nan
        df_lcu['iohmax'] = np.nan
        df_lcu['iohdmax'] = np.nan
        df_lcu['iohioqc'] = np.nan
        df_lcu['ioxsareq'] = np.nan
        df_lcu['ioxuahrq'] = np.nan
        df_lcu['ioxcqd'] = np.nan
        df_lcu['ioxiuac'] = np.nan
        df_lcu['ioxabc'] = np.nan
        df_lcu['ioxhcba'] = np.nan
        df_lcu['ioxalc'] = np.nan
        df_lcu['ioxhcla'] = np.nan
    df_lcu = df_lcu.reset_index()[Smf78Lcu.__table__.columns.keys()].set_index(
        [col.name for col in Smf78Lcu.__table__.primary_key.columns.values()])
    return df_lcu


def update_amg(df_amg: pd.DataFrame, df_lcu: pd.DataFrame, df_cha: pd.DataFrame) -> pd.DataFrame:
    df_lcu_gp = df_lcu.reset_index().groupby(
        ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs']).agg(
        {'r783qct': 'sum', 'r783qsm': 'sum', 'r783hnai': 'sum', 'r783htio': 'sum', 'iohmax': 'max', 'iohdmax': 'max',
         'iohioqc': 'max',
         'r783xanc': 'sum', 'r783xauc': 'sum', 'r783xnhc': 'sum', 'r783xcqd': 'sum', 'r783xciu': 'sum',
         'r783xabc': 'sum', 'ioxhcba': 'max',
         'r783xalc': 'sum', 'ioxhcla': 'max', 'r783csst': 'sum'})
    df_cha_gp3 = df_cha.reset_index().groupby(
        ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs']).agg(
        {'r783pt': 'sum', 'r783dpb': 'sum', 'r783cub': 'sum', 'r783cbt': 'sum', 'r783cmr': 'sum'})
    df_amg = pd.concat([df_amg.reset_index().set_index(['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs']),
                        df_lcu_gp, df_cha_gp3], axis=1)
    df_amg['ioctr'] = df_amg['r783qct'] / df_amg['smf78int']
    df_amg['iodlq'] = (df_amg['r783qsm'] - df_amg['r783qct']) / df_amg['r783qct']
    df_amg['iohwait'] = df_amg['r783hnai'] / df_amg['r783htio']
    df_amg['ioxsareq'] = df_amg['r783xauc'] / df_amg['r783xanc']
    df_amg['ioxuahrq'] = df_amg['r783xnhc'] / df_amg['r783xanc']
    df_amg['ioxcqd'] = df_amg['r783xcqd'] / df_amg['r783xanc']
    df_amg['ioxiuac'] = df_amg['r783xciu'] / df_amg['r783xanc']
    df_amg['ioxabc'] = df_amg['r783xabc'] / df_amg['smf78int']
    df_amg['ioxalc'] = df_amg['r783xalc'] / df_amg['smf78int']
    df_amg['total_requests'] = df_amg['r783pt'] + df_amg['r783dpb'] + df_amg['r783cub']
    df_amg['ioart'] = df_amg['r783pt'] / df_amg['smf78int']
    df_amg['iocub'] = df_amg['r783cub'] * 100 / df_amg['total_requests']
    df_amg['iodpb'] = df_amg['r783dpb'] * 100 / df_amg['total_requests']
    df_amg['iocbt'] = df_amg['r783cbt'] * 1000 / df_amg['r783pt']
    df_amg['iocmr'] = df_amg['r783cmr'] * 1000 / df_amg['r783pt']
    df_amg['iocss'] = df_amg['r783csst'] * 1000 / df_amg['r783pt']
    df_amg = df_amg.reset_index()[Smf78Amg.__table__.columns.keys()].set_index(
        [col.name for col in Smf78Amg.__table__.primary_key.columns.values()])
    return df_amg


def format_78df(df: pd.DataFrame) -> dict:
    """Format smf78 JSON files to the dataframes.

    Args:
        df: JSON dataframe.

    Returns:
        A dictionary of dataframes.
    """
    dfs_dict = {'comn': pd.DataFrame(), 'pvt': pd.DataFrame(), 'pvsp': pd.DataFrame(),
                'ioq': pd.DataFrame(), 'iop': pd.DataFrame(), 'lcu': pd.DataFrame(),
                'cha': pd.DataFrame(), 'amg': pd.DataFrame(), 'chap': pd.DataFrame(),
                'pro': pd.DataFrame()}

    if 'smf78pro' not in df.columns:
        return dfs_dict
    else:
        dfs_dict['pro'] = build_pro(df)

    if dfs_dict['pro'].empty:
        # Cannot continue processing
        return dfs_dict

    df.set_index(dfs_dict['pro'].index, inplace=True)

    if '78.2' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 2 records
        dfs_dict['comn'] = build_comn(df, dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '78.2'].index)

        dfs_dict['pvt'] = build_pvt(df, dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '78.2'].index)

        if dfs_dict['pvt'].shape[0] > 0:
            dfs_dict['pvsp'] = build_pvsp(df, dfs_dict['pvt'],
                                 dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '78.2'].index)

    if '78.3' in dfs_dict['pro'].index.get_level_values('smf_type'):  # Contains subtype 3 records
        def _df_lcu(csc, sid, datetime, smf78ist, smf78iet, r783sid1):
            try:
                lcu = dfs_dict['lcu'].loc[(csc, sid, datetime, smf78ist, smf78iet, r783sid1)]
                return lcu.r783mcmn, lcu.r783mcmx, lcu.r783mcdf
            except KeyError:
                return np.nan, np.nan, np.nan

        get_df_lcu = np.vectorize(_df_lcu)

        dfs_dict['ioq'] = build_ioq(df, dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '78.3'].index)

        if dfs_dict['ioq'].shape[0] > 0:
            dfs_dict['iop'] = build_iop(dfs_dict['ioq'])

        if dfs_dict['iop'].shape[0] > 0:
            dfs_dict['ioq'] = update_ioq(dfs_dict['ioq'],
                                         dfs_dict['iop'].reset_index().drop_duplicates(
                                             subset=[col for col in Smf78Iop.__table__.columns.keys() if
                                                     col in dfs_dict['iop'].reset_index().columns],
                                             keep='first').set_index(
                                             [col.name for col in Smf78Iop.__table__.primary_key.columns.values()]))

        dfs_dict['lcu'] = build_lcu(df, dfs_dict['ioq'].reset_index().reset_index().set_index(
            ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'smf78int', 'alias_management_aval',
             'index']).index)

        if 'r783hpav' in df.columns:
            dfs_dict['lcu'] = update_lcu_hpav(df, dfs_dict['lcu'],
                                              dfs_dict['pro'][dfs_dict['pro'].index.get_level_values('smf_type') == '78.3'].index)

        if 'r783cs' in df.columns:
            df_cs = col_to_frame(df[df.index.get_level_values('smf_type') == '78.3'], 'r783cs',
                                          dfs_dict['ioq'].reset_index().set_index(
                                              ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'smf78int',
                                               'alias_management_aval']).index)
            df_cs['r783id1'] = df_cs['r783id1'].str[2:]
            df_cs['r783amgc'] = np.where(df_cs['alias_management_aval'] == 1,
                                                  df_cs['r783amgc'].str[2:], np.nan)
            df_cs['r783amgs'] = np.where(df_cs['alias_management_aval'] == 1,
                                                  df_cs['r783amgs'].str[2:], np.nan)
            df_cs['csc'] = np.nan

            dfs_dict['amg'] = df_cs[df_cs['alias_management_aval'] == 1][
                ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs', 'r783id1', 'smf78int',
                 'r783amgc']].set_index(
                [col.name for col in Smf78Amg.__table__.primary_key.columns.values()])

            if dfs_dict['amg'].shape[0] > 0:
                # update lcu's r783amgs
                dfs_dict['lcu']['r783amgs'] = dfs_dict['lcu'].index.map(dfs_dict['amg'].reset_index().set_index(
                    ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783id1'])['r783amgs'])

                dfs_dict['amg'] = dfs_dict['amg'].reset_index()[
                    ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs', 'smf78int',
                     'r783amgc']].drop_duplicates().set_index(
                    [col.name for col in Smf78Amg.__table__.primary_key.columns.values()])

            else:
                dfs_dict['lcu']['r783amgs'] = np.nan
                dfs_dict['amg'] = pd.DataFrame(columns=Smf78Amg.__table__.columns.keys()).set_index(
                    [col.name for col in Smf78Amg.__table__.primary_key.columns.values()])
            df_cs = df_cs.set_index(
                ['csc', 'smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs', 'r783id1', 'smf78int',
                 'alias_management_aval'])

            dfs_dict['cha'], dfs_dict['chap'] = build_cha(df_cs)

            if dfs_dict['cha'].shape[0] > 0:
                if dfs_dict['chap'].shape[0] > 0:
                    # update chap
                    dfs_dict['chap'] = dfs_dict['chap'].set_index(
                        ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs', 'r783cpid'])
                    agg_cha = {'smf78int': 'last', 'ch_path_installed': 'last', 'ch_path_online': 'last',
                               'ch_path_varied': 'last',
                               'ch_path_offline': 'last', 'vary_path_action': 'last',
                               'ch_path_data_invalid': 'last', 'ch_path_dcm': 'last',
                               'chpid_manipulated': 'first', 'r783cun': 'last', 'r783cu1': 'last',
                               'r783cu2': 'last', 'r783cu3': 'last', 'r783cu4': 'last',
                               'r783cub': 'sum', 'r783pt': 'sum', 'r783dpb': 'sum', 'r783cbt': 'sum',
                               'r783cmr': 'sum', 'r783sbs': 'sum',
                               'extended_io_measurement1': 'last', 'extended_io_measurement2': 'last',
                               'first_transfer_ready_disabled': 'last',
                               'r783cpat': 'last', 'r783ctmw': 'sum', 'r783ctrd': 'sum',
                               'r783cpst': 'last', 'r783cpxf': 'last'}
                    df_cha_gp = dfs_dict['cha'].reset_index().groupby(
                        ['smf78sid', 'datetime', 'smf78ist', 'smf78iet', 'r783amgs', 'r783cpid']).agg(agg_cha)
                    dfs_dict['chap'] = pd.concat([dfs_dict['chap'], df_cha_gp], axis=1)

                    dfs_dict['chap']['iotmdinh'] = (dfs_dict['chap']['r783ctmw'] - dfs_dict['chap']['r783ctrd']
                                                    ) / dfs_dict['chap']['r783ctmw']
                    dfs_dict['chap']['ioart'] = dfs_dict['chap']['r783pt'] / dfs_dict['chap']['smf78int']
                    dfs_dict['chap']['total_requests'] = (dfs_dict['chap']['r783pt'] + dfs_dict['chap']['r783dpb']
                                                          + dfs_dict['chap']['r783cub'])
                    dfs_dict['chap']['iocub'] = dfs_dict['chap']['r783cub'] * 100 / dfs_dict['chap']['total_requests']
                    dfs_dict['chap']['iodpb'] = dfs_dict['chap']['r783dpb'] * 100 / dfs_dict['chap']['total_requests']
                    dfs_dict['chap']['iocbt'] = dfs_dict['chap']['r783cbt'] * 1000 / dfs_dict['chap']['r783pt']
                    dfs_dict['chap']['iocmr'] = dfs_dict['chap']['r783cmr'] * 1000 / dfs_dict['chap']['r783pt']
                    dfs_dict['chap'] = dfs_dict['chap'].reset_index()
                    dfs_dict['chap']['r783mcmn'], dfs_dict['chap']['r783mcmx'], dfs_dict['chap']['r783mcdf'] = get_df_lcu(
                        dfs_dict['chap']['csc'], dfs_dict['chap']['smf78sid'], dfs_dict['chap']['datetime'],
                        dfs_dict['chap']['smf78ist'], dfs_dict['chap']['smf78iet'], dfs_dict['chap']['r783id1'])
                    dfs_dict['chap'] = dfs_dict['chap'][Smf78Chap.__table__.columns.keys()].set_index(
                        [col.name for col in Smf78Chap.__table__.primary_key.columns.values()])

                # update lcu
                dfs_dict['lcu'] = update_lcu_cha(dfs_dict['lcu'], dfs_dict['cha'])

            if dfs_dict['amg'].shape[0] > 0:
                dfs_dict['amg'] = update_amg(dfs_dict['amg'], dfs_dict['lcu'], dfs_dict['cha'])

    return dfs_dict


def print_ioq_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                        target_lcu: str = None) -> str:
    """Print smf78 I/O Queuing Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        target_lcu: Target LCU to print.

    Returns:
        I/O Queuing Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar

    report = ''
    for jsonfile in jsonfiles:
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 78:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_78df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue

            starting = 'ioq'

            start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf78ist >= @start_time and smf78ist <= @end_time and smf78sid == @lpar"
                         ).drop_duplicates()
            if start_tbls.empty:
                continue
            for ioq in start_tbls.to_dict('records'):
                pro = df_dict['pro'].copy().reset_index().query(
                            "smf78iet == @ioq['smf78iet'] and smf78sid == @ioq['smf78sid'] and smf_type == '78.3'"
                         ).drop_duplicates()
                lcus = df_dict['lcu'].copy().reset_index().query(
                            "smf78iet == @ioq['smf78iet'] and smf78sid == @ioq['smf78sid']"
                         ).drop_duplicates()
                iops = df_dict['iop'].copy().reset_index().query(
                            "smf78iet == @ioq['smf78iet'] and smf78sid == @ioq['smf78sid']"
                         ).drop_duplicates()
                amgs = df_dict['amg'].copy().reset_index().query(
                            "smf78iet == @ioq['smf78iet'] and smf78sid == @ioq['smf78sid']"
                         ).drop_duplicates()
                page_detail = format_io_processors(pro.to_dict('records')[0], ioq,
                                                   iops.to_dict('records'))

                if not amgs.empty:
                    chaps_list = []
                    for amg in amgs.to_dict('records'):
                        chaps = df_dict['chap'].copy().reset_index().query(
                            "smf78iet == @amg['smf78iet'] and smf78sid == @amg['smf78sid'] and r783amgs == @amg['r783amgs']"
                        ).drop_duplicates()
                        chaps_list.append(chaps.to_dict('records'))
                    page_detail += '\n'
                    page_detail += format_alias_management_groups(pro.to_dict('records')[0], ioq,
                                                                  amgs.to_dict('records'), chaps_list)
                cha_list = []
                amg_list = []
                for lcu in lcus.to_dict('records'):
                    chas = df_dict['cha'].copy().reset_index().query(
                        "smf78iet == @lcu['smf78iet'] and smf78sid == @lcu['smf78sid'] and r783id1 == @lcu['r783id2']"
                    ).drop_duplicates()
                    amg = df_dict['amg'].copy().reset_index().query(
                        "smf78iet == @lcu['smf78iet'] and smf78sid == @lcu['smf78sid'] and r783amgs == @lcu['r783amgs']"
                    ).drop_duplicates()

                    cha_list.append(chas.to_dict('records'))
                    if not amg.empty:
                        amg_list.append(amg.to_dict('records')[0])
                    else:
                        amg_list.append(None)
                page_detail += '\n'
                page_report = format_logical_control_units(ioq, pro.to_dict('records')[0],
                                                           lcus.to_dict('records'),
                                                           cha_list, amg_list,
                                                           target_lcu)
                if page_report is not None:
                    page_detail += page_report
                    report += page_detail
                    report += "\n\n"
    if report == '':
        report = "No data found."
    return report

def print_vstor_activity(jsonfiles: tuple, lpar: str, start_time_str: str, end_time_str: str,
                        report_type: str) -> str:
    """Print smf78 Virtual Storage Activity Report based on JSON files.

    Args:
        jsonfiles: JSON file or files.
        lpar: Target LPAR to print.
        start_time_str: Start time string.
        end_time_str: End time string.
        report_type: Type of report.

    Returns:
        Virtual Storage Activity report.
    """
    start_time = pd.to_datetime(start_time_str)
    end_time = pd.to_datetime(end_time_str)
    sid = lpar

    report = ''
    for jsonfile in jsonfiles:
        page_detail = ''
        with open(jsonfile) as f:
            try:
                df = pd.read_json(f)
            except ValueError:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue

            if 'header' not in df.columns or not isinstance(df.iloc[0]['header'], dict) \
                    or df.iloc[0]['header'].get('recType') is None or df.iloc[0]['header']['recType'] != 78:
                click.echo(
                    f"\nInvalid JSON file {jsonfile}. This file will be skipped.")
                continue
            try:
                df_dict = format_78df(df)
            except Exception as e:
                click.echo(f"\nUnsupported JSON file {jsonfile} with error: {str(e)}. This file will be skipped.")
                continue

            if df_dict['pro'].empty:
                click.echo(
                    f"\nThis JSON file {jsonfile} is not for this smf type. This file will be skipped.")
                # Cannot continue processing
                continue
            starting = 'comn'

            start_tbls = df_dict[starting].copy().reset_index().query(
                            "smf78ist >= @start_time and smf78ist <= @end_time and smf78sid == @lpar"
                         ).drop_duplicates()
            if start_tbls.empty:
                continue
            for comn in start_tbls.to_dict('records'):
                page_sub_detail = ''
                pro = df_dict['pro'].copy().reset_index().query(
                            "smf78iet == @comn['smf78iet'] and smf78sid == @comn['smf78sid'] and smf_type == '78.2'"
                         ).drop_duplicates()
                pro_dict = pro.to_dict('records')[0]
                if report_type == "Common Storage":
                    page_sub_detail = format_common_storage_summary(comn, pro_dict)
                    page_sub_detail += '\n\n'
                    page_sub_detail += format_common_storage_detail(comn, pro_dict)
                    page_sub_detail += '\n\n'
                else:
                    pvts = df_dict['pvt'].copy().reset_index().query(
                            "smf78iet == @pro_dict['smf78iet'] and smf78sid == @pro_dict['smf78sid']"
                         ).drop_duplicates()
                    for pvt in pvts.to_dict('records'):
                        page_sub_detail = format_private_storage_summary(pvt, comn, pro_dict)
                        pvsps = df_dict['pvsp'].copy().reset_index().query(
                            "smf78iet == @pvt['smf78iet'] and smf78sid == @pvt['smf78sid'] and r782jobn == @pvt['r782jobn']"
                         ).drop_duplicates()
                        page_sub_detail += '\n\n'
                        page_sub_detail += format_private_storage_detail(pvt, pro_dict, pvsps.to_dict('records'))
                        page_sub_detail += '\n\n'
                if page_sub_detail != '':
                    page_detail += page_sub_detail
            if page_detail != '':
                report += page_detail
    if report == '':
        report = "No data found."
    return report
