import os

import pytz
import aws2summary
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

seoul = pytz.timezone('Asia/Seoul')

def min_max_date(folder_path):
    csv_list = os.listdir(folder_path)
    csv_list = [int(filename.split('.')[0]) for filename in csv_list]
    max_value = str(max(csv_list))
    min_value = str(min(csv_list))

    min_date = datetime(int(min_value[:4]), int(min_value[4:6]), int(min_value[6:]))
    max_date = datetime(int(max_value[:4]), int(max_value[4:6]), int(max_value[6:]))

    max_date1 = max_date - timedelta(days=1)
    max_date2 = max_date

    return min_date, max_date1, max_date2

def week_temp_line(df):
    # fig = px.line(df, x='datetime', y='temp', title='Temperature Over Time')
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()

    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['temp'], name='temp')])
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})

    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == max_temp]['datetime'].values[0])],
                             y=[max_temp],
                             mode='markers',
                             marker=dict(size=10, color='red'),
                             name='최고기온'))
    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == min_temp]['datetime'].values[0])],
                             y=[min_temp],
                             mode='markers',
                             marker=dict(size=10, color='blue'),
                             name='최저기온'))
    fig.update_layout(title_text=f'{df["datetime"].min().date()} ~ {df["datetime"].max().date()}')

    return fig


def week_humid_line(df):
    # fig = px.line(df, x='datetime', y='humid', title='humiderature Over Time')
    max_humid = df['hum'].max()
    min_humid = df['hum'].min()

    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['hum'], name='humid')])
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})
    fig.update_layout(title_text=f'{df["datetime"].min().date()} ~ {df["datetime"].max().date()}')
    return fig

def week_temphumid_line(df):
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["datetime"], y=df['temp'], mode='lines', name='temp', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df["datetime"], y=df["hum"], name='hum', mode='lines', yaxis='y2', marker=dict(color='orange')))
    fig.update_layout(yaxis=dict(title='온도(℃)'))
    fig.update_layout(yaxis2=dict(title='습도(%)', overlaying='y', side='right', showgrid=False))
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(range=[0, 100], tick0=0, dtick=10, secondary_y=True)
    fig.update_layout(title_text=f'{df["datetime"].min().date()} ~ {df["datetime"].max().date()}')
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})

    return fig

def week_rad_line(df):
    df['cumsum_rad'] = df.groupby('date')['rad'].cumsum()
    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['cumsum_rad'], name='hum')])
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})
    fig.update_layout(title_text='누적광량')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='누적광량(W/m²)')

    return fig


def day_temp_line(df):
    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['temp'], name='temp')])
    fig.update_layout(title_text='온도')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='온도(℃)')

    return fig

def day_humid_line(df):
    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['hum'], name='hum')])
    fig.update_layout(title_text='습도')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='습도(%)')

    return fig

def day_temphumid_line(df):
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["datetime"], y=df['temp'], mode='lines', name='temp', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df["datetime"], y=df["hum"], name='hum', mode='lines', yaxis='y2', marker=dict(color='orange')))
    fig.update_layout(yaxis=dict(title='온도(℃)'))
    fig.update_layout(yaxis2=dict(title='습도(%)', overlaying='y', side='right', showgrid=False))
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(range=[0, 100], tick0=0, dtick=10, secondary_y=True)

    return fig

def day_rad_line(df):
    df['cumsum_rad'] = df['rad'].cumsum()
    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['cumsum_rad'], name='hum')])
    fig.update_layout(title_text='누적광량')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='누적광량(W/m²)')

    return fig

def daily_temprain_linebar(df):

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df["날짜"], y=df['평균기온'], mode='lines', name='평균기온', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["날짜"], y=df['최저기온'], mode='lines', name='최저기온', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df["날짜"], y=df['최고기온'], mode='lines', name='최고기온', line=dict(color='red')))

    fig.add_trace(go.Bar(x=df["날짜"], y=df["강수량"], name='강수량', yaxis='y2', marker=dict(color='blue')))

    fig.update_layout(yaxis=dict(title='온도 (℃)'))

    fig.update_layout(yaxis2=dict(title='강수량', overlaying='y', side='right', showgrid=False))
    fig.update_yaxes(range=[0, 100], tick0=0, dtick=10, secondary_y=True)

    return fig

def daily_tempdiff_line(df):

    fig = go.Figure(data=[go.Scatter(x=df["날짜"], y=df['일교차'], name='일교차', mode='lines')])

    fig.update_layout(title_text='일교차')
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='일교차(℃)')

    return fig


def rain_count_pie(df):
    grouped_data = df.groupby('강수계급').size().reset_index(name='갯수')
    fig = px.pie(grouped_data, names='강수계급', values='갯수', title='강수계급별 분포',
                 hover_data=['강수계급', '갯수'])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

def text_to_degrees(text_direction):
    direction_mapping = {
        "북": 0,
        "북북동": 22.5,
        "북동": 45,
        "동북동": 67.5,
        "동": 90,
        "동남동": 112.5,
        "남동": 135,
        "남남동": 157.5,
        "남": 180,
        "남남서": 202.5,
        "남서": 225,
        "서남서": 247.5,
        "서": 270,
        "서북서": 292.5,
        "북서": 315,
        "북북서": 337.5
    }

    return direction_mapping.get(text_direction, None)

def wd_count_pie(df):
    # grouped_data = df.groupby('풍향').size().reset_index(name='갯수')
    # fig = px.pie(grouped_data, names='풍향', values='갯수', title='풍향계급별 분포',
    #              hover_data=['풍향', '갯수'])
    # fig.update_traces(textposition='inside', textinfo='percent+label')
    #
    # return fig
    df['풍향'] = df['풍향'].apply(lambda x: text_to_degrees(x))
    grouped_data = df.groupby('풍향').size().reset_index(name='갯수')
    fig = px.bar_polar(grouped_data, r='갯수', theta='풍향', title='풍향계급별 분포')
    fig.update_traces(marker=dict(color='blue'))
    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                direction='clockwise',
                period=360
            )
        )
    )
    return fig

def user_select_date(folder_path):
    min_date, max_date1, max_date2 = min_max_date(folder_path)

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Select a start date", min_value=min_date, max_value=max_date1, value=min_date, key=1)
        start_date_str = start_date.strftime('%Y%m%d')

    with col2:
        end_date = st.date_input("Select an end date", min_value=min_date, max_value=max_date2, value=max_date2, key=2)
        end_date_str = end_date.strftime('%Y%m%d')

    select_date = st.date_input("Select a date", min_value=start_date, max_value=end_date, value=end_date,
                                key=3)
    select_date_str = select_date.strftime('%Y%m%d')

    return start_date, start_date_str, end_date, end_date_str, select_date, select_date_str

def tab_vis_day(select_minute_df):
    day_temphumid = day_temphumid_line(select_minute_df)
    day_temp = day_temp_line(select_minute_df)
    day_humid = day_humid_line(select_minute_df)
    day_rad = day_rad_line(select_minute_df)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    chart_selection = st.radio("Select a chart:", ["온습도", "온도", "습도", "누적광량"], key="day_chart_selection")

    selected_chart = st.plotly_chart(day_temphumid)

    if chart_selection == "온습도":
        selected_chart.plotly_chart(day_temphumid)
    elif chart_selection == "온도":
        selected_chart.plotly_chart(day_temp)
    elif chart_selection == "습도":
        selected_chart.plotly_chart(day_humid)
    elif chart_selection == "누적광량":
        selected_chart.plotly_chart(day_rad)

def tab_vis_daily(minute_df, daily_df, wd_category):
    week_temphumid = week_temphumid_line(minute_df)
    week_temp = week_temp_line(minute_df)
    week_humid = week_humid_line(minute_df)
    week_rad = week_rad_line(minute_df)

    daily_tempdiff = daily_tempdiff_line(daily_df)
    daily_temprain = daily_temprain_linebar(daily_df)
    rain_pie = rain_count_pie(daily_df)
    wd_pie = wd_count_pie(wd_category)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    chart_selection = st.radio("Select a chart:", ["온습도", "온도", "습도", "누적광량"], key="daily_chart_selection")

    selected_chart = st.plotly_chart(week_temphumid)

    if chart_selection == "온습도":
        selected_chart.plotly_chart(week_temphumid)
    elif chart_selection == "온도":
        selected_chart.plotly_chart(week_temp)
    elif chart_selection == "습도":
        selected_chart.plotly_chart(week_humid)
    elif chart_selection == "누적광량":
        selected_chart.plotly_chart(week_rad)

    st.plotly_chart(daily_tempdiff)

    st.plotly_chart(daily_temprain)

    st.plotly_chart(rain_pie)

    st.plotly_chart(wd_pie)


def tab_table_summary(daily_df, dates_df, wd_category):
    st.write('요약 통계')
    st.write(daily_df)

    st.write(dates_df)

    st.write('풍향 계급')
    wd_category = wd_category.groupby(['date'])['풍향'].value_counts().reset_index(name='counts')
    wd_category = wd_category.pivot(index='date', columns='풍향', values='counts')
    wd_category = wd_category.fillna(0)
    st.write(wd_category)

def tab_table_hour(hour_df):
    show_hour_df = hour_df[['datetime', 'temp', 'hum', 'rad', 'wd', 'ws', 'rain', 'maxws', 'bv']]
    st.write(show_hour_df)

def tab_table_minute(minute_df):
    number = st.number_input("분 간격 입력", min_value=0, max_value=55, value=10, step=5, key=4)

    show_minute_df = minute_df[['datetime', 'temp', 'hum', 'rad', 'wd', 'ws', 'rain', 'maxws', 'bv']]
    show_minute_df = show_minute_df[show_minute_df['datetime'].dt.minute % number == 0]

    st.write(show_minute_df)

def tab_table_day(select_minute_df):
    number = st.number_input("분 간격 입력", min_value=0, max_value=55, value=10, step=5, key=5)
    show_select_minute_df = select_minute_df[['datetime', 'temp', 'hum', 'rad', 'wd', 'ws', 'rain', 'maxws', 'bv']]
    show_select_minute_df = show_select_minute_df[show_select_minute_df['datetime'].dt.minute % number == 0]
    st.write(show_select_minute_df)


def ready_dataframe(folder_path):
    start_date, start_date_str, end_date, end_date_str, select_date, select_date_str = user_select_date(folder_path)

    minute_df, hour_df = aws2summary.get_dataframe(start_date_str, end_date_str, folder_path)
    daily_df, wd_cate_df = aws2summary.daily_data(minute_df, hour_df)
    dates_df = aws2summary.weekly_date(daily_df)

    select_minute_df = pd.read_csv(os.path.join(folder_path, f"{select_date.strftime('%Y%m%d')}.csv"))
    select_minute_df['datetime'] = pd.to_datetime(select_minute_df['datetime'])


    daily_df['폭염일수'] = daily_df['폭염일수'].apply(lambda x: '-' if x == 0 else x)
    daily_df['강수일수'] = daily_df['강수일수'].apply(lambda x: '-' if x == 0 else x)
    daily_df['한파일수'] = daily_df['한파일수'].apply(lambda x: '-' if x == 0 else x)

    return minute_df, hour_df, daily_df, wd_cate_df, dates_df, select_minute_df


def main():
    folder_path = "./output/AWS"

    minute_df, hour_df, daily_df, wd_cate_df, dates_df, select_minute_df = ready_dataframe(folder_path)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Day Vis', 'Daily Vis', 'Summary Table', 'Hour Table', 'Minute Table', 'Day Table'])

    with tab1:
        tab_vis_day(select_minute_df)

    with tab2:
        tab_vis_daily(minute_df, daily_df, wd_cate_df)

    with tab3:
        tab_table_summary(daily_df, dates_df, wd_cate_df)

    with tab4:
        tab_table_hour(hour_df)

    with tab5:
        tab_table_minute(minute_df)

    with tab6:
        tab_table_day(select_minute_df)

if __name__ == '__main__':
    main()