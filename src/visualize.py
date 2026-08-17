import pandas as pd
import plotly.graph_objects as go

from config import PLATFORM_COLORS, PLATFORM_ORDER, VIEW_ORDER

TEMPLATE = "plotly_white"

LAYOUT_FONT = dict(family="Inter, Segoe UI, sans-serif", size=14, color="#1f2937")


def auroc_bar(df: pd.DataFrame, score_col: str, title: str, y_label: str) -> go.Figure:
    fig = go.Figure()
    for platform in PLATFORM_ORDER:
        sub = df[df["platform"] == platform]
        fig.add_trace(go.Bar(
            x=sub["view"],
            y=sub[score_col],
            name=platform,
            marker_color=PLATFORM_COLORS[platform],
            text=sub[score_col].round(3),
            textposition="outside",
            hovertemplate=(
                "<b>%{x} · " + platform + "</b><br>"
                + y_label + ": %{y:.3f}<br>"
                "Accuracy: %{customdata[0]:.1f}%<br>"
                "Sensitivity: %{customdata[1]:.1f}%<br>"
                "Specificity: %{customdata[2]:.1f}%<extra></extra>"
            ),
            customdata=sub[["accuracy", "sensitivity", "specificity"]].values,
        ))
    fig.add_hline(y=0.5, line_dash="dash", line_color="#9ca3af", annotation_text="chance level (0.5)")
    fig.update_layout(
        template=TEMPLATE,
        title=title,
        barmode="group",
        yaxis=dict(title=y_label, range=[0, 1]),
        xaxis=dict(title="Cardiac view"),
        legend_title_text="Ultrasound platform",
        font=LAYOUT_FONT,
        height=460,
        margin=dict(t=70, b=50, l=60, r=30),
    )
    return fig


def platform_gap_bar(delta_df: pd.DataFrame, title: str) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=delta_df["delta"],
        y=delta_df["view"],
        orientation="h",
        marker_color=["#f97316" if v > 0 else "#2563eb" for v in delta_df["delta"]],
        text=delta_df["delta"].round(3),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>High-end minus low-end: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(
        template=TEMPLATE,
        title=title,
        xaxis=dict(title="AUROC gap (high-end − low-end)"),
        yaxis=dict(title=""),
        font=LAYOUT_FONT,
        height=340,
        margin=dict(t=70, b=50, l=90, r=30),
    )
    return fig


def rate_metrics_radar(df: pd.DataFrame, view: str) -> go.Figure:
    metrics = ["sensitivity", "specificity", "ppv", "npv", "accuracy"]
    labels = ["Sensitivity", "Specificity", "PPV", "NPV", "Accuracy"]
    fig = go.Figure()
    for platform in PLATFORM_ORDER:
        row = df[(df["view"] == view) & (df["platform"] == platform)].iloc[0]
        values = [row[m] for m in metrics]
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=platform,
            line_color=PLATFORM_COLORS[platform],
            opacity=0.75,
        ))
    fig.update_layout(
        template=TEMPLATE,
        title=f"Diagnostic profile at {view} (binary classification)",
        polar=dict(radialaxis=dict(range=[0, 100], ticksuffix="%")),
        font=LAYOUT_FONT,
        height=460,
        margin=dict(t=70, b=40, l=40, r=40),
    )
    return fig


def rate_metrics_heatmap(df: pd.DataFrame, title: str) -> go.Figure:
    df = df.copy()
    df["label"] = df["platform"].astype(str) + " · " + df["view"].astype(str)
    metrics = ["accuracy", "sensitivity", "specificity", "ppv", "npv"]
    labels = ["Accuracy", "Sensitivity", "Specificity", "PPV", "NPV"]
    z = df[metrics].values
    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels,
        y=df["label"],
        colorscale="Oranges",
        text=z.round(1),
        texttemplate="%{text}",
        hovertemplate="%{y}<br>%{x}: %{z:.1f}%<extra></extra>",
        colorbar=dict(title="%"),
    ))
    fig.update_layout(
        template=TEMPLATE,
        title=title,
        font=LAYOUT_FONT,
        height=420,
        margin=dict(t=70, b=50, l=140, r=30),
    )
    return fig
