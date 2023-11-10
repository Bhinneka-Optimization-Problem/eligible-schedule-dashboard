import numpy as np
import pandas as pd

def set_statuses(row):
    load_x = row['load_factor_x']
    load_y = row['load_factor_y']
    if pd.isna(row['load_factor_y']): #klo null berarti gaada keberangkatan balik, cek aja originnya
        if load_x < 40:
            return "Batal"
        elif load_x >=70:
            return "Jalan"
        else:
            return "Jalan Bersyarat"
    else: #klo ga null, artinya ada keberangkatan balik, harus dicek keduanya
        if (load_x<40) & (load_y<40):
            return "Batal"
        elif (load_x>=70) & (load_y>=70):
            return "Jalan"
        else:
            return "Jalan Bersyarat"

def eligible_schedule(origin:str,destination:str,dayoftheweek:str=["Today","Monday","Tuesday","Wednesday","Thursday",'Friday','Saturday','Sunday']):
    # import 
    df_prejadwal = pd.read_csv('prejadwal.csv')
    df_nomainkey = df_prejadwal.copy()
    df_nomainkey.drop(columns=['main_key','duration'],inplace=True)
    df_nomainkey.drop_duplicates(inplace=True)
    if dayoftheweek == "Today":
        df_nomainkey_today = df_nomainkey[df_nomainkey['dayofweek']==pd.Timestamp.today().day_name()].copy()
    elif dayoftheweek in ["Monday","Tuesday","Wednesday","Thursday",'Friday','Saturday','Sunday']:
        df_nomainkey_today = df_nomainkey[df_nomainkey['dayofweek']==dayoftheweek].copy()
    else:
        raise TypeError('The input of "dayoftheweek" is not valid. Try one of these values: \n["Today","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]')
    df_nomainkey_today.drop(columns='dayofweek',inplace=True)
    origin_a = origin
    destination_b = destination
    condition_origin = df_nomainkey_today['origin'] == origin_a
    condition_destination = df_nomainkey_today['destination'] == destination_b
    condition_origin2 = df_nomainkey_today['origin'] == destination_b
    condition_destination2 = df_nomainkey_today['destination'] == origin_a
    df_a_to_b = df_nomainkey_today[condition_origin & condition_destination]
    df_b_to_a = df_nomainkey_today[condition_origin2 & condition_destination2]
    df_a_b_a = pd.merge(df_a_to_b,df_b_to_a,left_on='arrival_time',right_on='origin_period',how='left')
    df_a_b_a['status'] = df_a_b_a.apply(set_statuses, axis=1)
    df_a_b_a.drop(columns=['tomorrow?_x','tomorrow?_y','origin_period_y','origin_y'],inplace=True)
    return df_a_b_a

def all_eligible_schedule(origin:str,dayoftheweek:str=["Today","Monday","Tuesday","Wednesday","Thursday",'Friday','Saturday','Sunday'],show:str=['detail','compact']):
    df_routes=pd.read_csv('routes.csv')
    df_jadwal_origin = pd.DataFrame([])
    for destination in df_routes[df_routes['origin']==origin]['destination'].unique():
        df_jadwal_origin = pd.concat([df_jadwal_origin,eligible_schedule(origin,destination,dayoftheweek)])
    df_jadwal_origin.reset_index(inplace=True,drop=True)
    if show == 'compact':
        return df_jadwal_origin[['origin_period_x','origin_name_x','arrival_time_x','destination_name_x', 'minimal_n_departures_x','status',]]
    elif show == 'detail':
        return df_jadwal_origin
    else:
        raise TypeError('"show" parameter should be str either "compact" or "detail".')