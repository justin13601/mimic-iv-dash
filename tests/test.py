##!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on May 10, 2022
@author: Justin Xu
"""

import dash
import plotly.express as px
from dash import Dash, html, dcc, dash_table
import plotly.graph_objs as go
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate

import os
import csv
import pandas as pd
import numpy as np
from google.cloud import bigquery


def load_data(path):
    filename = os.path.basename(path).strip()
    print(f'Loading {filename}...')
    df_data = pd.read_csv(path)
    print('Done.')
    return df_data


def big_query(query):
    client = bigquery.Client()
    query_job = client.query(query)  # API request
    print("The query data:")
    for row in query_job:
        # row values can be accessed by field name or index
        print("name={}, count={}".format(row[0], row["total_people"]))
    return


if __name__ == "__main__":
    df_labitems = load_data('../demo-data/D_LABITEMS.csv')
    df_labevents = load_data('../demo-data/LABEVENTS.csv')

    print("Data Loaded.")

    labitems_list = df_labitems["label"].unique()
    labitems_dict = pd.Series(df_labitems.label.values, index=df_labitems.itemid.values).to_dict()

    categories = list(set(map(lambda x: x.lower().capitalize(), df_labitems["category"].unique().tolist())))
    categories = categories + list(set(map(lambda x: x.lower().capitalize(), df_labitems["fluid"].unique().tolist())))

    target = labitems_list[4]

    for itemid, label in labitems_dict.items():
        if target == label:
            df_table = df_labevents.query(f'itemid == {itemid}')
