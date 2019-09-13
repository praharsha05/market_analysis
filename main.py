from pandas_datareader import data
from datetime import datetime
from bokeh.plotting import figure, show, output_file

starttime = datetime(2019,1,1)
endtime = datetime(2019,3,10)

df = data.DataReader(name="GOOG",data_source="yahoo",start=starttime,end=endtime)
def inc_dec(c,o):
    if c>o:
        value="increase"
    elif c<o:
        value = "decrease"
    else: value = "equal"
    return value

df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close,df.Open)]

df["Middle"] = (df.Close + df.Open)/2
df["Height"] = abs(df.Close - df.Open)

p = figure(x_axis_type="datetime", width=600, height=300,sizing_mode="scale_height")
p.title.text="candlestick chart"

p.grid.grid_line_alpha=0.3

hours_ms = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low)

p.rect(df.index[df.Status=="increase"], df.Middle[df.Status=="increase"],
      hours_ms, df.Height[df.Status=="increase"],fill_color="green", line_color="black")

p.rect(df.index[df.Status=="decrease"], df.Middle[df.Status=="decrease"],
      hours_ms, df.Height[df.Status=="decrease"],fill_color="red", line_color="black")
p.line(df.index,df["Close"],color = "green")

output_file("candlestick.html")
show(p)