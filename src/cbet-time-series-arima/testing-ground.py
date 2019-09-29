import os
import datetime
import time

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go

# pydata stack
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


my_db=URL(drivername='mysql+pymysql',username='root',password="Zsaxdcqw12!",host='localhost',database='rebirth',query={'read_default_file':'~/.my.cnf'})

conn=create_engine(my_db)


def fetch_data(q):
    """
    Utility function to run queries given a query.
    @param return : query result.

    """
    result = pd.read_sql(
        sql=q,
        con=conn
    )
    return result

def get_mil_sec_diff():
    """ Return Global Milli Second Dictionary. Values are Instance Rate Objects """
    mili_sec_query=(
        f'''
        select timestampdiff(microsecond,mi.eventdate,ir.timestamp),ir.rate 
        from (select * from marketinstance where result='WINNER' limit 20) mi 
        left join (select 
                   distinct * 
                   from instancerate 
                   where instanceid in 
                   (
                        select instanceid
                        from marketinstance
                        where result='WINNER'
                    ) 
                ) ir
        on mi.instanceid=ir.instanceid; 
        '''
    )
    mili_sec_df=fetch_data(mili_sec_query)

    return mili_sec_df
if __name__ == '__main__':
    print(get_mil_sec_diff())