import plotly_express as px
import plotly.graph_objs as go


def plot_grouped_bar_chart(df, colors):
    fig = px.bar(df, x=df.index, y=df.columns,
                color_discrete_sequence=colors*len(df),
                barmode='group')
    fig.update_layout(legend_title_text="Pokemon", xaxis_title="Stat", yaxis_title="Value")

    return fig


def plot_scatter_line_chart(df, colors):
    point_plot=[
                go.Scatter(x=df.index, y=df.iloc[:,0], name=df.columns[0], line=dict(color=colors[0])),
                go.Scatter(x=df.index, y=df.iloc[:,1], name=df.columns[1], line=dict(color=colors[1]))
                ]
                
                
    fig = go.Figure(data=point_plot)
    fig.update_layout(legend_title_text="Pokemon", xaxis_title="Stat", yaxis_title="Value")

    return fig