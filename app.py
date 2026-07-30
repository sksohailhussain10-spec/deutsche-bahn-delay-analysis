from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="Deutsche Bahn Delay Dashboard",
    page_icon="🚆",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    data_path = Path(
        "data/processed/trains_db_hbfs_cleaned.csv"
    )

    data = pd.read_csv(data_path)

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data["hour"] = pd.to_numeric(
        data["hour"],
        errors="coerce"
    )

    data["has_delay"] = pd.to_numeric(
        data["has_delay"],
        errors="coerce"
    )

    data["actual_delay_minutes"] = pd.to_numeric(
        data["actual_delay_minutes"],
        errors="coerce"
    )

    data["platform_change"] = (
        data["platform_change"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )

    return data


try:
    clean = load_data()

except FileNotFoundError:
    st.error(
        "The cleaned dataset could not be found. "
        "Make sure this file exists: "
        "data/processed/trains_db_hbfs_cleaned.csv"
    )
    st.stop()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🚆 Deutsche Bahn Train Delay Dashboard")

st.write(
    "Explore how train delays varied by station, train group, "
    "scheduled hour and sampled date across major German "
    "railway stations."
)

st.info(
    "The dataset covers eight sampled dates. The dashboard "
    "does not represent a complete annual assessment of "
    "Deutsche Bahn performance."
)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("Dashboard filters")

all_stations = sorted(
    clean["station"].dropna().unique()
)

all_train_groups = sorted(
    clean["train_group"].dropna().unique()
)

all_day_types = sorted(
    clean["day_type"].dropna().unique()
)

all_dates = sorted(
    clean["date"].dropna().dt.date.unique()
)


selected_stations = st.sidebar.multiselect(
    "Station",
    options=all_stations,
    default=all_stations
)

selected_train_groups = st.sidebar.multiselect(
    "Train group",
    options=all_train_groups,
    default=all_train_groups
)

selected_day_types = st.sidebar.multiselect(
    "Day type",
    options=all_day_types,
    default=all_day_types
)

selected_dates = st.sidebar.multiselect(
    "Sampled date",
    options=all_dates,
    default=all_dates,
    format_func=lambda value: value.strftime(
        "%d %B %Y"
    )
)

hour_range = st.sidebar.slider(
    "Scheduled hour",
    min_value=0,
    max_value=23,
    value=(0, 23)
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered = clean[
    clean["station"].isin(selected_stations)
    & clean["train_group"].isin(
        selected_train_groups
    )
    & clean["day_type"].isin(
        selected_day_types
    )
    & clean["date"].dt.date.isin(
        selected_dates
    )
    & clean["hour"].between(
        hour_range[0],
        hour_range[1]
    )
].copy()


if filtered.empty:
    st.warning(
        "No records match the selected filters. "
        "Please change one or more filters."
    )
    st.stop()


# ---------------------------------------------------------
# MAIN METRICS
# ---------------------------------------------------------

total_services = len(filtered)

delayed_services = int(
    filtered["has_delay"].sum()
)

delay_rate = (
    filtered["has_delay"].mean() * 100
)

median_delay = filtered.loc[
    (
        filtered["has_delay"] == 1
    )
    & filtered["actual_delay_minutes"].notna(),
    "actual_delay_minutes"
].median()

platform_changes = int(
    filtered["platform_change"]
    .fillna(False)
    .sum()
)


metric1, metric2, metric3, metric4, metric5 = (
    st.columns(5)
)

metric1.metric(
    "Recorded services",
    f"{total_services:,}"
)

metric2.metric(
    "Delayed services",
    f"{delayed_services:,}"
)

metric3.metric(
    "Delay rate",
    f"{delay_rate:.1f}%"
)

if pd.notna(median_delay):
    metric4.metric(
        "Median delay",
        f"{median_delay:.1f} min"
    )
else:
    metric4.metric(
        "Median delay",
        "Not available"
    )

metric5.metric(
    "Platform changes",
    f"{platform_changes:,}"
)

st.divider()


# ---------------------------------------------------------
# DASHBOARD TABS
# ---------------------------------------------------------

overview_tab, station_tab, time_tab, operations_tab = (
    st.tabs([
        "Overview",
        "Stations",
        "Time patterns",
        "Operational issues"
    ])
)


# ---------------------------------------------------------
# TAB 1 — OVERVIEW
# ---------------------------------------------------------

with overview_tab:

    st.subheader(
        "Delay performance by train group"
    )

    group_stats = (
        filtered.groupby(
            "train_group",
            as_index=False
        )
        .agg(
            total_services=(
                "has_delay",
                "size"
            ),
            delayed_services=(
                "has_delay",
                "sum"
            ),
            delay_rate=(
                "has_delay",
                "mean"
            )
        )
    )

    group_stats["delay_rate_pct"] = (
        group_stats["delay_rate"] * 100
    )

    group_stats = group_stats.sort_values(
        "delay_rate_pct"
    )

    fig_group = px.bar(
        group_stats,
        x="delay_rate_pct",
        y="train_group",
        orientation="h",
        text=group_stats[
            "delay_rate_pct"
        ].map(
            lambda value: f"{value:.1f}%"
        ),
        hover_data={
            "total_services": ":,",
            "delayed_services": ":,",
            "delay_rate_pct": ":.1f"
        },
        title=(
            "Long-distance services show the "
            "highest delay rate in the full sample"
        )
    )

    fig_group.update_layout(
        template="plotly_white",
        xaxis_title="Delayed services (%)",
        yaxis_title="",
        showlegend=False
    )

    fig_group.update_xaxes(
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig_group,
        width="stretch"
    )

    st.caption(
        "The chart updates whenever the sidebar "
        "filters are changed."
    )


# ---------------------------------------------------------
# TAB 2 — STATIONS
# ---------------------------------------------------------

with station_tab:

    st.subheader(
        "Station delay rate and service volume"
    )

    station_stats = (
        filtered.groupby(
            "station",
            as_index=False
        )
        .agg(
            total_services=(
                "has_delay",
                "size"
            ),
            delayed_services=(
                "has_delay",
                "sum"
            ),
            delay_rate=(
                "has_delay",
                "mean"
            )
        )
    )

    station_stats["delay_rate_pct"] = (
        station_stats["delay_rate"] * 100
    )

    station_stats = station_stats[
        station_stats["total_services"] >= 20
    ].copy()

    station_stats = station_stats.sort_values(
        "delay_rate_pct",
        ascending=False
    ).head(15)

    fig_station = px.scatter(
        station_stats,
        x="total_services",
        y="delay_rate_pct",
        size="total_services",
        text="station",
        hover_data={
            "delayed_services": ":,",
            "delay_rate_pct": ":.1f",
            "total_services": ":,"
        },
        title=(
            "Station delay rates differ even among "
            "stations with similar service volumes"
        )
    )

    fig_station.update_traces(
        textposition="top center"
    )

    fig_station.update_layout(
        template="plotly_white",
        xaxis_title=(
            "Number of recorded services"
        ),
        yaxis_title=(
            "Delayed services (%)"
        )
    )

    fig_station.update_yaxes(
        range=[0, 100],
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig_station,
        width="stretch"
    )

    st.subheader(
        "Stations with the longest typical delays"
    )

    station_duration = (
        filtered[
            (
                filtered["has_delay"] == 1
            )
            & filtered[
                "actual_delay_minutes"
            ].notna()
        ]
        .groupby(
            "station",
            as_index=False
        )
        .agg(
            delayed_records=(
                "actual_delay_minutes",
                "size"
            ),
            median_delay=(
                "actual_delay_minutes",
                "median"
            )
        )
    )

    station_duration = station_duration[
        station_duration[
            "delayed_records"
        ] >= 20
    ].sort_values(
        "median_delay"
    ).tail(12)

    if not station_duration.empty:

        fig_duration = px.bar(
            station_duration,
            x="median_delay",
            y="station",
            orientation="h",
            text=station_duration[
                "median_delay"
            ].map(
                lambda value: f"{value:.1f} min"
            ),
            hover_data={
                "delayed_records": ":,",
                "median_delay": ":.1f"
            },
            title=(
                "Median actual delay by station"
            )
        )

        fig_duration.update_layout(
            template="plotly_white",
            xaxis_title=(
                "Median actual delay (minutes)"
            ),
            yaxis_title=""
        )

        st.plotly_chart(
            fig_duration,
            width="stretch"
        )

    else:
        st.info(
            "There are not enough usable delay-duration "
            "records for the selected filters."
        )


# ---------------------------------------------------------
# TAB 3 — TIME PATTERNS
# ---------------------------------------------------------

with time_tab:

    st.subheader(
        "Delay rates by scheduled hour"
    )

    hourly_stats = (
        filtered.groupby(
            [
                "hour",
                "train_group"
            ],
            as_index=False
        )
        .agg(
            total_services=(
                "has_delay",
                "size"
            ),
            delay_rate=(
                "has_delay",
                "mean"
            )
        )
    )

    hourly_stats["delay_rate_pct"] = (
        hourly_stats["delay_rate"] * 100
    )

    fig_hour = px.line(
        hourly_stats,
        x="hour",
        y="delay_rate_pct",
        color="train_group",
        markers=True,
        hover_data={
            "total_services": ":,",
            "delay_rate_pct": ":.1f"
        },
        title=(
            "Delay rates change across the day "
            "and differ by train group"
        )
    )

    fig_hour.update_layout(
        template="plotly_white",
        xaxis_title=(
            "Scheduled departure hour"
        ),
        yaxis_title=(
            "Delayed services (%)"
        ),
        legend_title_text=""
    )

    fig_hour.update_xaxes(
        dtick=1
    )

    fig_hour.update_yaxes(
        range=[0, 100],
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig_hour,
        width="stretch"
    )

    st.subheader(
        "Comparison of the sampled dates"
    )

    date_stats = (
        filtered.groupby(
            "date",
            as_index=False
        )
        .agg(
            total_services=(
                "has_delay",
                "size"
            ),
            delay_rate=(
                "has_delay",
                "mean"
            ),
            mean_actual_delay=(
                "actual_delay_minutes",
                "mean"
            )
        )
    )

    date_stats["delay_rate_pct"] = (
        date_stats["delay_rate"] * 100
    )

    date_stats["date_label"] = (
        date_stats["date"].dt.strftime(
            "%d %b"
        )
    )

    fig_date = px.scatter(
        date_stats,
        x="mean_actual_delay",
        y="delay_rate_pct",
        size="total_services",
        text="date_label",
        hover_data={
            "total_services": ":,",
            "delay_rate_pct": ":.1f",
            "mean_actual_delay": ":.1f",
            "date_label": False
        },
        title=(
            "Delay frequency and average delay "
            "identify different difficult dates"
        )
    )

    fig_date.update_traces(
        textposition="top center"
    )

    fig_date.update_layout(
        template="plotly_white",
        xaxis_title=(
            "Mean actual delay (minutes)"
        ),
        yaxis_title=(
            "Delayed services (%)"
        )
    )

    st.plotly_chart(
        fig_date,
        width="stretch"
    )


# ---------------------------------------------------------
# TAB 4 — OPERATIONAL ISSUES
# ---------------------------------------------------------

with operations_tab:

    st.subheader(
        "Recorded disruption reasons"
    )

    reason_data = filtered[
        filtered["delay_reason"].notna()
        & filtered[
            "actual_delay_minutes"
        ].notna()
    ].copy()

    reason_stats = (
        reason_data.groupby(
            "delay_reason",
            as_index=False
        )
        .agg(
            records=(
                "delay_reason",
                "size"
            ),
            median_delay=(
                "actual_delay_minutes",
                "median"
            )
        )
    )

    reason_stats = reason_stats[
        reason_stats["records"] >= 10
    ].copy()

    reason_stats = (
        reason_stats
        .sort_values(
            "median_delay",
            ascending=False
        )
        .head(12)
        .sort_values(
            "median_delay"
        )
    )

    if not reason_stats.empty:

        fig_reason = px.bar(
            reason_stats,
            x="median_delay",
            y="delay_reason",
            orientation="h",
            text=reason_stats[
                "median_delay"
            ].map(
                lambda value: f"{value:.1f} min"
            ),
            hover_data={
                "records": ":,",
                "median_delay": ":.1f"
            },
            title=(
                "Some less-common disruption reasons "
                "produce particularly severe delays"
            )
        )

        fig_reason.update_layout(
            template="plotly_white",
            xaxis_title=(
                "Median actual delay (minutes)"
            ),
            yaxis_title=""
        )

        st.plotly_chart(
            fig_reason,
            width="stretch"
        )

    else:
        st.info(
            "There are not enough recorded reasons "
            "for the selected filters."
        )

    st.subheader(
        "Recorded platform changes"
    )

    platform_stats = (
        filtered.groupby(
            "station",
            as_index=False
        )
        .agg(
            total_services=(
                "platform_change",
                "size"
            ),
            platform_changes=(
                "platform_change",
                "sum"
            )
        )
    )

    platform_stats[
        "platform_change_rate_pct"
    ] = (
        platform_stats[
            "platform_changes"
        ]
        / platform_stats[
            "total_services"
        ]
        * 100
    )

    platform_stats = (
        platform_stats[
            platform_stats[
                "total_services"
            ] >= 20
        ]
        .sort_values(
            "platform_change_rate_pct"
        )
        .tail(12)
    )

    if not platform_stats.empty:

        fig_platform = px.bar(
            platform_stats,
            x="platform_change_rate_pct",
            y="station",
            orientation="h",
            text=platform_stats[
                "platform_change_rate_pct"
            ].map(
                lambda value: f"{value:.1f}%"
            ),
            hover_data={
                "total_services": ":,",
                "platform_changes": ":,"
            },
            title=(
                "Recorded platform-change rates "
                "vary substantially by station"
            )
        )

        fig_platform.update_layout(
            template="plotly_white",
            xaxis_title=(
                "Services with a platform change (%)"
            ),
            yaxis_title=""
        )

        st.plotly_chart(
            fig_platform,
            width="stretch"
        )


# ---------------------------------------------------------
# CONCLUSIONS AND LIMITATIONS
# ---------------------------------------------------------

st.divider()

st.subheader("Main interpretation")

st.write(
    "Long-distance services generally show the weakest "
    "reliability in the available sample. Station rankings "
    "also change depending on whether performance is measured "
    "using delay rate or actual delay duration."
)

st.subheader("Limitations")

st.write(
    "The dataset covers eight sampled dates rather than a "
    "complete year. Actual delay duration is available only "
    "when a usable real-time value could be extracted."
)