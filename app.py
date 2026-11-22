import csv
import io
from datetime import date, datetime

import streamlit as st

from roti_counter import CSV_FIELDS, DATA_PATH, load_records, save_records, suggested_rotis


st.set_page_config(page_title="Jhelum Roti Counter", page_icon="🫓", layout="wide")

st.sidebar.markdown("## Jhelum Mess\nRoti Counter · NIT Srinagar")
page = st.sidebar.radio("Navigate", ["Dashboard", "Records"], label_visibility="collapsed")
st.sidebar.caption("Records are stored locally in data.csv.")

st.markdown("#### JHELUM MESS · NIT SRINAGAR")
st.title(page)
st.caption(date.today().strftime("%A, %d %B %Y"))

try:
    records = load_records()
except (OSError, ValueError, csv.Error) as error:
    st.error(f"Could not load meal observations: {error}")
    st.stop()


def show_dashboard() -> None:
    total = len(records)
    students_total = sum(int(row["students_eaten"]) for row in records)
    cooked_total = sum(int(row["rotis_cooked"]) for row in records)
    left_total = sum(int(row["rotis_left"]) for row in records)
    avg_students = round(students_total / total) if total else 0
    avg_cooked = round(cooked_total / total) if total else 0
    waste_rate = left_total / cooked_total * 100 if cooked_total else 0

    metric_cols = st.columns(4)
    metric_cols[0].metric("Meal records", total)
    metric_cols[1].metric("Avg. students", avg_students, "per meal")
    metric_cols[2].metric("Avg. rotis cooked", avg_cooked, "per meal")
    metric_cols[3].metric("Leftover rate", f"{waste_rate:.1f}%")

    entry_col, forecast_col = st.columns([1.45, 1])
    with entry_col:
        st.subheader("Record a meal")
        with st.form("meal_record_form", clear_on_submit=True):
            first, second = st.columns(2)
            meal_date = first.date_input("Date", value=date.today())
            meal = second.selectbox("Meal", ["Lunch", "Dinner"])
            day_type = first.selectbox("Day type", ["Weekday", "Weekend"])
            meal_time = second.time_input(
                "Meal time",
                value=datetime.strptime("13:00" if meal == "Lunch" else "20:00", "%H:%M").time(),
            )
            students = first.number_input("Students served", min_value=1, step=1, value=150)
            cooked = second.number_input("Rotis cooked", min_value=1, step=1, value=500)
            left = first.number_input("Rotis left over", min_value=0, step=1, value=0)
            ran_out = second.selectbox("Did rotis run out?", ["No", "Yes"])
            ran_out_time = st.text_input("Time they ran out (optional)", placeholder="e.g. 13:35")
            note = st.text_input("Notes (optional)")
            submitted = st.form_submit_button("Save observation", type="primary")

        if submitted:
            if left > cooked:
                st.error("Rotis left over cannot exceed the number cooked.")
            elif ran_out == "Yes" and left > 0:
                st.error("If rotis ran out, enter 0 for rotis left over.")
            else:
                new_record = {
                    "date": meal_date.isoformat(),
                    "meal": meal,
                    "time_noted": meal_time.strftime("%H:%M"),
                    "spot": "Jhelum Mess",
                    "day_type": day_type,
                    "students_eaten": int(students),
                    "rotis_cooked": int(cooked),
                    "rotis_left": int(left),
                    "ran_out": ran_out,
                    "ran_out_time": ran_out_time.strip(),
                    "note": note.strip(),
                }
                try:
                    save_records([*records, new_record])
                except OSError as error:
                    st.error(f"Could not save this observation: {error}")
                else:
                    st.success("Observation saved.")
                    st.rerun()

    with forecast_col:
        st.subheader("Prepare for the next meal")
        forecast_meal = st.selectbox("Forecast meal", ["Lunch", "Dinner"], key="forecast_meal")
        forecast_day = st.selectbox("Day type", ["Weekday", "Weekend"], key="forecast_day")
        expected = st.number_input(
            "Expected students", min_value=1, step=1, value=150, key="forecast_students"
        )
        amount, sample_count = suggested_rotis(
            records, forecast_meal, forecast_day, int(expected)
        )
        st.markdown("### Suggested preparation")
        st.metric("Rotis", f"{amount:,}")
        st.caption(
            f"Based on {sample_count} similar meal record(s), with a 5% buffer. "
            "Treat this as a guide; a meal that ran out may have unmet demand."
        )

    st.subheader("Recent demand")
    recent = sorted(records, key=lambda row: row["date"])[-10:]
    if recent:
        maximum = max(int(row["rotis_cooked"]) for row in recent) or 1
        label_col, cooked_col, consumed_col = st.columns([1, 2, 2])
        label_col.markdown("**Meal**")
        cooked_col.markdown("**Cooked**")
        consumed_col.markdown("**Consumed**")
        for row in recent:
            cooked = int(row["rotis_cooked"])
            consumed = cooked - int(row["rotis_left"])
            label_col, cooked_col, consumed_col = st.columns([1, 2, 2])
            label_col.write(f'{row["date"][5:]} {row["meal"]}')
            cooked_col.progress(cooked / maximum, text=f"{cooked} rotis")
            consumed_col.progress(consumed / maximum, text=f"{consumed} rotis")
    else:
        st.info("Save a meal observation to see demand here.")


def show_records() -> None:
    st.subheader("All observations")
    if not records:
        st.info("There are no meal observations yet.")
        return
    ordered = sorted(records, key=lambda row: (row["date"], row["time_noted"]), reverse=True)
    columns = ["Date", "Meal", "Students", "Cooked", "Left", "Consumed", "Ran out", "Notes"]
    header = st.columns([1.2, 0.8, 0.8, 0.8, 0.6, 0.9, 0.8, 2])
    for column, label in zip(header, columns):
        column.markdown(f"**{label}**")
    for row in ordered:
        values = [
            row["date"],
            row["meal"],
            int(row["students_eaten"]),
            int(row["rotis_cooked"]),
            int(row["rotis_left"]),
            int(row["rotis_cooked"]) - int(row["rotis_left"]),
            row["ran_out"],
            row["note"] or "—",
        ]
        cells = st.columns([1.2, 0.8, 0.8, 0.8, 0.6, 0.9, 0.8, 2])
        for cell, value in zip(cells, values):
            cell.write(value)

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=CSV_FIELDS)
    writer.writeheader()
    writer.writerows(ordered)
    st.download_button(
        "Download observations as CSV",
        data=csv_buffer.getvalue(),
        file_name="roti_observations.csv",
        mime="text/csv",
    )


if page == "Dashboard":
    show_dashboard()
else:
    show_records()
