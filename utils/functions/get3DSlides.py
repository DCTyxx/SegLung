import numpy as np
import plotly.graph_objects as go

def buildPdbPage(volume):
    volume.reverse()
    r, c = volume[0].shape
    lenImage = len(volume)
    zLen = (lenImage-1)/10

    fig = go.Figure(
        # The ‘frames’ property is a tuple of instances of Frame
        frames=[
            go.Frame(
                # A list of traces this frame modifies. The format is identical to the normal trace definition.
                # Construct a new Surface object
                data=go.Surface(
                    # The data the describes the coordinates of the surface is set in z. Data in z should be a 2D list.
                    # Z 用于构建空白的立体空间 参数为：（z坐标轴）*image.size()
                    z=(zLen - k * 0.1) * np.ones((r, c)),
                    # Sets the surface color values, used for setting a color scale independent of z
                    # 用于独立设计Z的表面颜色
                    # np.flipud: 沿0轴翻转颜色的顺序（最后呈现为一边的颜色柱）
                    surfacecolor=np.flipud(volume[lenImage-1 - k]),
                    # 设计了颜色的下界
                    cmin=0,
                    # 设计了颜色的上界
                    cmax=255
                ),
                name=str(k)  # you need to name the frame for the animation to behave properly
            )
            for k in range(lenImage)])

    # 汇入图片
    # Add data to be displayed before animation starts
    fig.add_trace(
        go.Surface(
            z=zLen * np.ones((r, c)),
            # 这边设计了模块的初始值
            surfacecolor=np.flipud(volume[lenImage-1]),
            # 设计颜色属性
            colorscale='Gray',
            cmin=0,
            cmax=255,
            # why?
            # colorbar=dict(thickness=20, ticklen=4)
        ))

    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

    # 构建滑块
    sliders = [
        {
            "pad": {"b": 5, "t": 30},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], frame_args(0)],
                    "label": str(k),
                    "method": "animate",
                }
                for k, f in enumerate(fig.frames)
            ],
        }
    ]

    # Layout 布局
    fig.update_layout(
        width=350,
        height=350,
        # autosize = True,
        scene=dict(
            zaxis=dict(range=[-0.1, zLen+0.1], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),
        ),
        sliders=sliders,
        showlegend = False,
        margin_b=0,
        margin_l=0,
        margin_t = 0,
        margin_r = 0,
    )

    return fig