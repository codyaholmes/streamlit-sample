import streamlit as st
import duckdb
from data.taxi_trips import load_trips

st.title("Taxi Insights")


# Load taxi trip data
base_df = load_trips()
base_df.columns = [col.title().replace("_", " ") for col in base_df.columns]
df = base_df.copy()

# -----------------------------------------------------------------------------
# DATE PICKER
# -----------------------------------------------------------------------------

date_pickers_ctr = st.container(horizontal=True)

MIN_DATE_PICKUP = base_df["Pickup"].min()
MAX_DATE_PICKUP = base_df["Pickup"].max()
MIN_DATE_DROPOFF = base_df["Dropoff"].min()
MAX_DATE_DROPOFF = base_df["Dropoff"].max()

start_datetime_taxis = date_pickers_ctr.datetime_input(
    label="StartDate (Pickup)",
    value=MIN_DATE_PICKUP,
    min_value=MIN_DATE_PICKUP,
    max_value=MAX_DATE_PICKUP,
    format="YYYY-MM-DD",
    key="start_datetime_taxis",
)

end_datetime_taxis = date_pickers_ctr.datetime_input(
    label="End Date (Dropoff)",
    value=MAX_DATE_DROPOFF,
    min_value=MIN_DATE_DROPOFF,
    max_value=MAX_DATE_DROPOFF,
    format="YYYY-MM-DD",
    key="end_datetime_taxis",
)


# -----------------------------------------------------------------------------
# DROPDOWNS
# -----------------------------------------------------------------------------

borough_dropdowns = st.container(horizontal=True)

PICKUP_BOROUGHS = df["Pickup Borough"].unique()
DROPOFF_BOROUGHS = df["Dropoff Borough"].unique()

pickup_borough_selection = borough_dropdowns.multiselect(
    label="Pickup Borough",
    options=PICKUP_BOROUGHS,
    default=None,
    placeholder="No selection is all",
)

dropoff_borough_selection = borough_dropdowns.multiselect(
    label="Dropoff Borough",
    options=DROPOFF_BOROUGHS,
    default=None,
    placeholder="No selection is all",
)

# Handle empty selections for the query
if len(pickup_borough_selection) == 0:
    pickup_borough_selection = PICKUP_BOROUGHS.tolist()
if len(dropoff_borough_selection) == 0:
    dropoff_borough_selection = DROPOFF_BOROUGHS.tolist()


# -----------------------------------------------------------------------------
# FILTER THE DF COPY FOR VISUALIZATION
# -----------------------------------------------------------------------------

filtering_query = """
SELECT *
FROM df
WHERE Pickup >= $start_date
    AND DropOff <= $end_date
    AND "Pickup Borough" IN $pickup_boroughs
    AND "Dropoff Borough" IN $dropoff_boroughs;
"""

df = duckdb.execute(
    filtering_query,
    {
        "start_date": start_datetime_taxis,
        "end_date": end_datetime_taxis,
        "pickup_boroughs": pickup_borough_selection,
        "dropoff_boroughs": dropoff_borough_selection,
    },
).df()


# -----------------------------------------------------------------------------
# METRICS GROUP
# -----------------------------------------------------------------------------

metrics, raw_data, pg_info = st.tabs(["Metrics", "Raw Data", "Page Info"])

# Metric Calculations
total_passengers = df["Passengers"].sum()
total_fare = df["Fare"].sum()
total_distance = df["Distance"].sum()
total_tips = df["Tip"].sum()

with metrics:
    metrics_row1 = st.container(horizontal=True)
    metrics_row1.metric("Total Passengers", f"{total_passengers:,.0f}", border=True)
    metrics_row1.metric("Total Fares", f"${total_fare:,.0f}", border=True)

    # -------------------------------------------------------------------------
    # BOROUGH PICKUP/DROPOFF AGG TABLE GROUP
    # -------------------------------------------------------------------------

    title_info_ctr = st.container(horizontal_alignment="center")

    with title_info_ctr.popover("🤔 Table Tips!", type="tertiary"):
        st.markdown("""
        - Hover over a column to find information about this metric.
        - Click a column to sort ascendingly/descendingly. (Click multiple times to swap the method.)
        - Data can be exported or made full screen by using the icons in the top right.
        """)

    borough_agg_ctr = st.container(horizontal=True)

    borough_agg_query = """
    SELECT
        "Pickup Borough"
        , "Dropoff Borough"
        , COUNT(*) AS "Trips"
        , SUM(Passengers) AS "Passengers"
        , SUM(Fare) AS "Fares"
        , SUM(Tip) AS "Tips"
    FROM df
    GROUP BY ALL;
    """

    borough_agg_df = duckdb.execute(borough_agg_query).df()
    borough_agg_df["ATT"] = borough_agg_df["Tips"] / borough_agg_df["Trips"]

    borough_agg_col_config = {
        "Trips": st.column_config.NumberColumn(
            help="The amount of taxi trips.", format="localized"
        ),
        "Passengers": st.column_config.NumberColumn(
            help="The total amount of passengers taxied.", format="localized"
        ),
        "Fares": st.column_config.NumberColumn(
            help="The total amount of taxi fares (in U.S. dollars).",
            format="dollar",
        ),
        "Tips": st.column_config.NumberColumn(
            help="The total amount of tips from customers (in U.S. dollars).",
            format="dollar",
        ),
        "ATT": st.column_config.NumberColumn(
            help="The Average Tip per Trip (ATT) amount.", format="dollar"
        ),
    }

    borough_agg_ctr.dataframe(
        borough_agg_df, hide_index=True, column_config=borough_agg_col_config
    )


with raw_data:
    st.dataframe(df, hide_index=True)
    st.write(f"{len(df):,.0f} row{'s' if len(df) != 1 else ''}")


with pg_info:
    st.markdown("""
### Overview
This dashboard provides an interactive view of NYC taxi trip activity. Use the filters at the top of the page to analyze trips between pickup and dropoff boroughs over a selected date range.

The dashboard updates all metrics and tables automatically based on your selected filters.

### Developer
**Cody Holmes**  
(915) 929-3006  
[codyaholmes@outlook.com](mailto:codyaholmes@outlook.com)  
*Reporting and Analytics*, Trace3
""")
