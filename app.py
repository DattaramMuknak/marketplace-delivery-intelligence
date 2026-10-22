
import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Delivery Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Support Streamlit Community Cloud secrets.
try:
    for key, value in st.secrets.items():
        if isinstance(value, (str, int, float)):
            os.environ.setdefault(key, str(value))
except Exception:
    pass

from src.auth import init_db, login_user, register_user
from src.analytics import analyze_deliveries

# --------------------------------------------------
# PROFESSIONAL UI + ANIMATIONS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --panel: #111a2e;
    --panel-hover: #17233b;
    --line: #263653;
    --text: #eef3ff;
    --muted: #9baaca;
    --blue: #7195ff;
    --cyan: #59d5e8;
    --green: #48d9a0;
    --red: #ff748e;
}

.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, rgba(65, 100, 190, .16), transparent 36%),
        radial-gradient(ellipse at 100% 12%, rgba(48, 190, 204, .08), transparent 28%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0d1528;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif;
    letter-spacing: -0.035em;
    color: var(--text);
}

p, label, .stMarkdown {
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, .75);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 2rem 2.1rem;
    margin-bottom: 1.6rem;
    border: 1px solid #2c4269;
    border-radius: 22px;
    background: linear-gradient(115deg, #182c50 0%, #14213b 52%, #102d3b 100%);
    animation: fadeUp .65s ease both;
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -60px;
    top: -110px;
    border-radius: 50%;
    border: 1px solid rgba(145, 180, 255, .24);
    box-shadow:
        0 0 0 25px rgba(145, 180, 255, .035),
        0 0 0 55px rgba(145, 180, 255, .025);
    animation: floatGlow 7s ease-in-out infinite;
    pointer-events: none;
}

.eyebrow {
    color: #9ab9ff;
    font-size: .74rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    font-weight: 700;
    margin-bottom: .7rem;
}

.hero h1 {
    font-size: clamp(1.8rem, 3vw, 2.65rem);
    font-weight: 800;
    margin: 0;
    line-height: 1.2;
}

.hero p {
    color: #b4c3e0;
    margin: .8rem 0 0 0;
    max-width: 720px;
    font-size: .98rem;
    line-height: 1.7;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(72, 217, 160, .3);
    background: rgba(72, 217, 160, .08);
    color: #8af0c4;
    padding: 7px 11px;
    border-radius: 100px;
    font-size: .76rem;
    margin-top: 1.2rem;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(72, 217, 160, .7);
}

.section-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 1.15rem;
    font-weight: 750;
    margin: 1.4rem 0 .2rem 0;
}

.section-subtitle {
    color: var(--muted);
    font-size: .88rem;
    margin-bottom: 1.2rem;
}

.kpi-card {
    padding: 1.1rem 1.2rem;
    min-height: 125px;
    border: 1px solid var(--line);
    border-radius: 17px;
    background: linear-gradient(145deg, rgba(20, 32, 55, .98), rgba(15, 24, 42, .98));
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
    animation: fadeUp .55s ease both;
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: #4e6ca1;
    box-shadow: 0 12px 30px rgba(0, 0, 0, .18);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.kpi-label {
    color: #a7b6d4;
    font-size: .82rem;
    font-weight: 500;
}

.kpi-icon {
    width: 32px;
    height: 32px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background: rgba(113, 149, 255, .12);
    font-size: 1rem;
}

.kpi-value {
    font-family: 'Manrope', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -.05em;
    color: #f4f7ff;
    margin-top: .55rem;
}

.kpi-note {
    color: #93a4c5;
    font-size: .75rem;
    margin-top: .15rem;
}

.panel {
    background: rgba(17, 26, 46, .83);
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    animation: fadeUp .6s ease both;
}

.panel-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1rem;
    font-weight: 750;
    margin-bottom: .25rem;
}

.panel-description {
    color: var(--muted);
    font-size: .81rem;
    margin-bottom: 1rem;
}

div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    padding: 1rem;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
}

div[data-testid="stMetricValue"] {
    color: var(--text);
}

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    font-weight: 650;
    transition: transform .18s ease, box-shadow .18s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(80, 125, 220, .17);
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(105deg, #547cf4, #4776dc);
    border: none;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stFileUploader"] {
    background: rgba(17, 26, 46, .65);
    border: 1px dashed #405477;
    border-radius: 14px;
    padding: .5rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid var(--line);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px 9px 0 0;
    padding: 10px 18px;
}

hr {
    border-color: var(--line);
}

.footer {
    text-align: center;
    padding: 1.5rem 0 .5rem 0;
    color: #7182a4;
    font-size: .78rem;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floatGlow {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(14px) rotate(8deg); }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# REUSABLE UI COMPONENTS
# --------------------------------------------------

def show_hero():
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">MARKETPLACE OPERATIONS · DATA ANALYTICS</div>
        <h1>Delivery Intelligence</h1>
        <p>
            Turn delivery records into actionable insights.
            Explore SLA performance, compare couriers, and understand
            delivery outcomes through a clean analytics workspace.
        </p>
        <div class="status-pill">
            <span class="status-dot"></span>
            Analytics workspace
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_section_heading(title, subtitle):
    st.markdown(
        f"""
        <div class="section-heading">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def show_kpi(label, value, note, icon):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_auth():
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR OPERATIONS WORKSPACE</div>
        <h1>Welcome to Delivery Intelligence</h1>
        <p>
            Sign in to view delivery performance, analyse courier outcomes,
            and download reports from your data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown("### Your analytics workspace")
        st.markdown(
            "- Delivery SLA performance\n"
            "- Courier scorecards and comparisons\n"
            "- Interactive charts and data exploration\n"
            "- Downloadable reports"
        )

    with right:
        login_tab, register_tab = st.tabs(
            ["Sign in", "Create account"]
        )

        with login_tab:
            with st.form("login_form"):
                email = st.text_input(
                    "Email address",
                    key="login_email",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password",
                )
                submitted = st.form_submit_button(
                    "Sign in",
                    type="primary",
                    width="stretch",
                )

            if submitted:
                ok, message, user = login_user(email, password)

                if ok:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(message)

        with register_tab:
            with st.form("register_form"):
                name = st.text_input(
                    "Full name",
                    key="reg_name",
                )
                email = st.text_input(
                    "Email address",
                    key="reg_email",
                )
                password = st.text_input(
                    "Password (minimum 8 characters)",
                    type="password",
                    key="reg_password",
                )
                confirm = st.text_input(
                    "Confirm password",
                    type="password",
                    key="reg_confirm",
                )

                submitted = st.form_submit_button(
                    "Create account",
                    type="primary",
                    width="stretch",
                )

            if submitted:
                if password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    ok, message = register_user(
                        name,
                        email,
                        password,
                    )

                    if ok:
                        st.success(
                            message + " You can now sign in."
                        )
                    else:
                        st.error(message)


def make_chart_layout(fig, height=350):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=55, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, sans-serif",
            color="#c5d1e9",
            size=12,
        ),
        title_font=dict(
            family="Manrope, sans-serif",
            size=15,
            color="#eef3ff",
        ),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="#111a2e",
            bordercolor="#354969",
            font_color="#eef3ff",
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#263653",
        tickfont=dict(color="#aab9d5"),
    )
    fig.update_yaxes(
        gridcolor="rgba(125,145,180,.12)",
        zerolinecolor="#263653",
        tickfont=dict(color="#aab9d5"),
    )
    return fig


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

try:
    init_db()
except Exception as exc:
    st.error(
        "Could not connect to MySQL. Check your database "
        "configuration in .env or Streamlit secrets."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

if "user" not in st.session_state:
    show_auth()
    st.stop()

user = st.session_state.user


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 📦 Delivery IQ")
    st.caption("Analytics workspace")
    st.divider()

    st.markdown("**YOUR ACCOUNT**")
    st.write(f"👤 {user['name']}")

    st.divider()

    section = st.radio(
        "WORKSPACE",
        ["Overview & Analytics", "Explore Data"],
        label_visibility="visible",
    )

    st.divider()

    st.markdown("**DATA SOURCE**")
    st.caption(
        "Use the provided assignment CSV or upload your own "
        "compatible delivery dataset."
    )

    st.divider()

    if st.button("↪ Sign out", width="stretch"):
        st.session_state.pop("user", None)
        st.rerun()

    st.markdown(
        '<div class="footer">Delivery Intelligence · v1.0</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# MAIN WORKSPACE
# --------------------------------------------------

show_hero()

default_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "task1_marketplace_delivery_sla_raw.csv",
)

show_section_heading(
    "Your delivery workspace",
    "Upload your data or use the sample dataset to explore delivery performance.",
)

uploaded = st.file_uploader(
    "Choose a delivery CSV file",
    type=["csv"],
    key="main_csv_upload",
    help="Upload a CSV containing delivery records.",
)

try:
    if uploaded is not None:
        raw = pd.read_csv(uploaded)
        filename = uploaded.name
    elif os.path.exists(default_path):
        raw = pd.read_csv(default_path)
        filename = os.path.basename(default_path)
    else:
        st.info(
            "Upload a delivery CSV to get started. "
            "The default assignment dataset was not found."
        )
        st.stop()

    if raw.empty:
        st.warning("The selected CSV contains no records.")
        st.stop()

    result = analyze_deliveries(raw)

except Exception as exc:
    st.error(f"Unable to analyse this CSV: {exc}")
    st.stop()


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

clean = result["clean"].copy()
summary = result["summary"].copy()
warnings = result.get("warnings", [])

if warnings:
    with st.expander(
        f"Data quality notes · {len(warnings)}",
        expanded=False,
    ):
        for warning in warnings:
            st.write(f"• {warning}")

eligible = len(clean)

if "delivery_status" not in clean.columns:
    st.error(
        "The analytics result is missing the delivery_status column. "
        "Please check src/analytics.py and the uploaded CSV."
    )
    st.stop()

on_time = int(clean["delivery_status"].eq("On Time").sum())
late = int(clean["delivery_status"].eq("Late").sum())
rate = on_time / eligible if eligible else 0.0


# --------------------------------------------------
# OVERVIEW & ANALYTICS
# --------------------------------------------------

if section == "Overview & Analytics":
    show_section_heading(
        "Performance overview",
        f"Source: {filename} · {len(raw):,} raw records",
    )

    if eligible == 0:
        st.warning(
            "No eligible delivery records were found after applying "
            "the assignment's data cleaning and SLA rules."
        )

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    with k1:
        show_kpi(
            "Eligible orders",
            f"{eligible:,}",
            "Records included in the analysis",
            "📦",
        )

    with k2:
        show_kpi(
            "On-time orders",
            f"{on_time:,}",
            "Orders meeting the SLA",
            "✓",
        )

    with k3:
        show_kpi(
            "On-time rate",
            f"{rate:.1%}",
            "Share of eligible orders",
            "↗",
        )

    with k4:
        show_kpi(
            "Late orders",
            f"{late:,}",
            "Orders missing the SLA",
            "◷",
        )

    st.markdown("")

    # Main chart row
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            '<div class="panel-title">Delivery outcomes</div>'
            '<div class="panel-description">'
            'Distribution of eligible orders by delivery status.'
            '</div>',
            unsafe_allow_html=True,
        )

        outcomes = (
            clean["delivery_status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="orders")
        )

        if not outcomes.empty:
            fig = px.pie(
                outcomes,
                names="status",
                values="orders",
                hole=0.69,
                color="status",
                color_discrete_map={
                    "On Time": "#48d9a0",
                    "Late": "#ff748e",
                },
                template="plotly_dark",
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(
                    line=dict(
                        color="#111a2e",
                        width=3,
                    )
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Orders: %{value:,}<br>"
                    "Share: %{percent}<extra></extra>"
                ),
            )

            fig = make_chart_layout(fig, 330)
            st.plotly_chart(fig, width="stretch")

        else:
            st.info("No delivery outcomes are available.")

    with right:
        st.markdown(
            '<div class="panel-title">Courier scorecard</div>'
            '<div class="panel-description">'
            'Compare courier performance using the SLA on-time rate.'
            '</div>',
            unsafe_allow_html=True,
        )

        if not summary.empty and {
            "courier",
            "on_time_rate",
        }.issubset(summary.columns):

            chart_data = summary.sort_values(
                "on_time_rate",
                ascending=True,
            ).copy()

            fig = px.bar(
                chart_data,
                x="on_time_rate",
                y="courier",
                orientation="h",
                text=chart_data["on_time_rate"].map(
                    lambda value: f"{value:.0%}"
                ),
                range_x=[0, 1],
                color="on_time_rate",
                color_continuous_scale=[
                    "#ff748e",
                    "#e9b76a",
                    "#48d9a0",
                ],
                template="plotly_dark",
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "On-time rate: %{x:.1%}<extra></extra>"
                ),
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_tickformat=".0%",
                yaxis_title="",
                xaxis_title="On-time rate",
            )

            fig = make_chart_layout(
                fig,
                max(330, 50 * len(chart_data) + 100),
            )
            st.plotly_chart(fig, width="stretch")

        else:
            st.info("Courier scorecard data is unavailable.")

    # City chart
    st.markdown("")
    st.markdown(
        '<div class="panel-title">City performance</div>'
        '<div class="panel-description">'
        'Understand where on-time and late deliveries occur.'
        '</div>',
        unsafe_allow_html=True,
    )

    if {"city", "delivery_status"}.issubset(clean.columns) and not clean.empty:
        city_data = (
            clean.groupby(["city", "delivery_status"])
            .size()
            .reset_index(name="orders")
        )

        fig = px.bar(
            city_data,
            x="city",
            y="orders",
            color="delivery_status",
            barmode="group",
            color_discrete_map={
                "On Time": "#48d9a0",
                "Late": "#ff748e",
            },
            template="plotly_dark",
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Number of orders",
        )

        fig = make_chart_layout(fig, 370)
        st.plotly_chart(fig, width="stretch")

    else:
        st.info("City-level delivery data is unavailable.")

    # Courier summary table
    st.markdown("")
    st.markdown(
        '<div class="panel-title">Courier performance details</div>'
        '<div class="panel-description">'
        'Review and download the complete courier-level summary.'
        '</div>',
        unsafe_allow_html=True,
    )

    if not summary.empty:
        display_summary = summary.copy()

        if "on_time_rate" in display_summary.columns:
            display_summary["on_time_rate"] = (
                display_summary["on_time_rate"]
                .map(lambda value: f"{value:.1%}")
            )

        st.dataframe(
            display_summary,
            width="stretch",
            hide_index=True,
        )

        st.download_button(
            "⬇ Download courier summary",
            data=summary.to_csv(index=False).encode("utf-8"),
            file_name="courier_delivery_summary.csv",
            mime="text/csv",
        )
    else:
        st.info("No courier summary is available.")

    # Assignment note
    st.markdown("")
    with st.expander("About the analysis"):
        st.write(
            "This dashboard applies the assignment's delivery SLA "
            "and data-cleaning rules through src/analytics.py. "
            "The eligible order count, on-time rate, and late-order "
            "count are calculated from the resulting cleaned dataset."
        )
        st.info(
            "A predictive ML model should only be added when there is "
            "sufficient representative historical data and a reliable "
            "evaluation process. This dashboard does not claim to "
            "predict future delivery delays."
        )


# --------------------------------------------------
# EXPLORE DATA
# --------------------------------------------------

else:
    show_section_heading(
        "Explore your dataset",
        "Inspect the source records, validate cleaned data, and export results.",
    )

    tab_raw, tab_clean, tab_summary = st.tabs(
        ["Raw data", "Eligible records", "Courier summary"]
    )

    with tab_raw:
        st.markdown("#### Uploaded dataset")
        st.caption(
            f"{len(raw):,} rows · {len(raw.columns):,} columns · {filename}"
        )

        st.dataframe(
            raw,
            width="stretch",
            hide_index=True,
        )

        st.download_button(
            "⬇ Download original dataset",
            data=raw.to_csv(index=False).encode("utf-8"),
            file_name="delivery_original_data.csv",
            mime="text/csv",
            key="download_raw",
        )

    with tab_clean:
        st.markdown("#### Eligible delivery records")
        st.caption(
            f"{len(clean):,} records after the assignment's cleaning rules."
        )

        st.dataframe(
            clean,
            width="stretch",
            hide_index=True,
        )

        st.download_button(
            "⬇ Download eligible records",
            data=clean.to_csv(index=False).encode("utf-8"),
            file_name="eligible_delivery_records.csv",
            mime="text/csv",
            key="download_clean",
        )

    with tab_summary:
        st.markdown("#### Courier summary")

        if not summary.empty:
            st.dataframe(
                summary,
                width="stretch",
                hide_index=True,
            )

            st.download_button(
                "⬇ Download courier summary",
                data=summary.to_csv(index=False).encode("utf-8"),
                file_name="courier_delivery_summary.csv",
                mime="text/csv",
                key="download_summary",
            )
        else:
            st.info("No courier summary is available.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    """
    <div class="footer">
        DELIVERY INTELLIGENCE · MARKETPLACE OPERATIONS ANALYTICS
        <br>
        Clear data. Meaningful insights. Better delivery decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
