import pandas as pd
import plotly.graph_objects as go

from config import PLATFORM_COLORS, PLATFORM_ORDER, VIEW_ORDER

TEMPLATE = "plotly_white"

LAYOUT_FONT = dict(family="Inter, Segoe UI, sans-serif", size=14, color="#1f2937")


def auroc_bar(df: pd.DataFrame, score_col: str, title: str, y_label: str,
              ci_low_col: str | None = None, ci_high_col: str | None = None) -> go.Figure:
    fig = go.Figure()
    for platform in PLATFORM_ORDER:
        sub = df[df["platform"] == platform]
        error_y = None
        if ci_low_col and ci_high_col and ci_low_col in sub.columns:
            err_plus = sub[ci_high_col] - sub[score_col]
            err_minus = sub[score_col] - sub[ci_low_col]
            error_y = dict(type="data", symmetric=False, array=err_plus, arrayminus=err_minus,
                            visible=True, color="#4b5563", thickness=1.3)
        fig.add_trace(go.Bar(
            x=sub["view"],
            y=sub[score_col],
            name=platform,
            marker_color=PLATFORM_COLORS[platform],
            text=sub[score_col].round(3),
            textposition="outside",
            error_y=error_y,
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


def platform_significance_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of the AUROC gap per view, annotated with the unpaired DeLong
    test P value, so the reader can see at a glance which platform gaps are
    statistically confirmed rather than assumed from the point estimates alone."""
    colors = ["#16a34a" if sig else "#9ca3af" for sig in df["significant_at_0.05"]]
    labels = [
        f"P {'< 0.001' if p < 0.001 else f'= {p:.3f}'}"
        for p in df["p_value"]
    ]
    fig = go.Figure(go.Bar(
        x=df["view"],
        y=df["difference"],
        marker_color=colors,
        text=labels,
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>AUROC gap (high-end − low-end): %{y:.3f}<br>"
            "%{text}<extra></extra>"
        ),
    ))
    fig.update_layout(
        template=TEMPLATE,
        title="Is the platform gap real? Unpaired DeLong test per view",
        yaxis=dict(title="AUROC difference (high-end − low-end)"),
        xaxis=dict(title="Cardiac view"),
        font=LAYOUT_FONT,
        height=380,
        margin=dict(t=70, b=50, l=60, r=30),
        annotations=[dict(
            text="green = P < 0.05 (statistically significant)   gray = not significant",
            xref="paper", yref="paper", x=0, y=1.12, showarrow=False,
            font=dict(size=12, color="#6b7280"),
        )],
    )
    return fig


def participant_flow_funnel(df: pd.DataFrame) -> go.Figure:
    stages = df[df["stage"].isin(["screened", "enrolled", "training_set"])]
    excluded_n = df[df["stage"].str.startswith("excluded_")]["n"].sum()
    fig = go.Figure(go.Funnel(
        y=["Screened for eligibility", "Excluded before enrolment", "Enrolled (final dataset)"],
        x=[int(df.loc[df["stage"] == "screened", "n"].iloc[0]),
           int(excluded_n),
           int(df.loc[df["stage"] == "enrolled", "n"].iloc[0])],
        marker=dict(color=["#2563eb", "#ef4444", "#f97316"]),
        textinfo="value+percent initial",
    ))
    fig.update_layout(
        template=TEMPLATE,
        title="Participant flow (STARD-style)",
        font=LAYOUT_FONT,
        height=380,
        margin=dict(t=70, b=30, l=140, r=30),
    )
    return fig


def baseline_table(df: pd.DataFrame) -> go.Figure:
    label_map = {
        "age_years": "Age, years", "male_sex_pct": "Male sex, n (%)",
        "bmi_kgm2": "Body mass index, kg/m²", "hypertension_pct": "Hypertension, n (%)",
        "diabetes_mellitus_pct": "Diabetes mellitus, n (%)",
        "coronary_artery_disease_pct": "Coronary artery disease, n (%)",
        "atrial_fibrillation_pct": "Atrial fibrillation, n (%)",
        "lvef_pct": "LVEF, %", "lv_end_diastolic_diameter_mm": "LV end-diastolic diameter, mm",
        "lv_end_systolic_diameter_mm": "LV end-systolic diameter, mm",
        "left_atrial_diameter_mm": "Left atrial diameter, mm",
        "non_hf_pct": "Non-HF, n (%)", "hfpef_pct": "HFpEF, n (%)", "hfref_pct": "HFrEF, n (%)",
    }
    rows = df.copy()
    rows["characteristic"] = rows["characteristic"].map(label_map).fillna(rows["characteristic"])
    fig = go.Figure(go.Table(
        header=dict(
            values=["<b>Characteristic</b>", "<b>Overall (n=254)</b>", "<b>Non-HF (n=104)</b>",
                    "<b>HF (n=150)</b>", "<b>P value</b>"],
            fill_color="#f97316", font=dict(color="white", size=13), align="left", height=32,
        ),
        cells=dict(
            values=[rows["characteristic"], rows["overall_n254"], rows["non_hf_n104"],
                    rows["hf_n150"], rows["p_value"]],
            fill_color=[["#fff7ed", "#ffffff"] * (len(rows) // 2 + 1)],
            align="left", height=28, font=dict(size=12),
        ),
    ))
    fig.update_layout(template=TEMPLATE, title="Table 1. Baseline demographic and clinical characteristics",
                       font=LAYOUT_FONT, height=520, margin=dict(t=60, b=20, l=10, r=10))
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
