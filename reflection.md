# Reflection: Jhelum Mess Roti Counter

## Why I chose this problem

During my visit to Jhelum Mess at NIT Srinagar, I started thinking about a small but important daily decision: how many rotis should be prepared for lunch and dinner? If the kitchen prepares too few, some students may not get enough. If it prepares too many, good food may be left over. I wanted to explore whether keeping simple records could help the mess staff make a more informed estimate without adding unnecessary work to their routine.

## What I learned from the visit

Speaking with Abdul Qayoom, the butler, and Mohammad Mukhtar, the cook, helped me look beyond the number of rotis prepared. The number of students eating can change from one meal to another, so the real challenge is estimating demand before the meal. I also realised that a useful record should capture more than leftovers: it should include attendance, meal type, whether rotis ran out, and when that happened.

This changed how I thought about the problem. A meal with no leftovers does not automatically mean the quantity was exactly right; rotis might have run out before everyone had eaten. Recording both shortages and leftovers is important for understanding demand more fairly.

## What I built

I made a Python app with Streamlit so meal records can be entered through a straightforward interface. It shows a few summaries, keeps a records table, and estimates a preparation quantity using similar meals and a small buffer. I chose a simple interface because the tool should support the staff's existing work rather than make it harder.

Building the app also helped me see how a practical idea turns into a set of concrete questions: which details should be recorded, how should similar meals be compared, and how should a suggestion be presented so it is useful but not mistaken for a guarantee?

## Limitations and what I still need to do

The app's starter CSV contains 20 example observations. They are useful for trying the interface and forecast, but they should not be treated as verified records of actual meals. I need to check the entries against real observations and replace or correct any examples before drawing conclusions about Jhelum Mess. I also need to collect records over a longer period, including different weekdays and weekends.

The current forecast is only a basic estimate from past records. If a meal ran out, the recorded number eaten may understate the actual demand. Attendance can also change unexpectedly. The suggestion should therefore be treated as a starting point for the staff, not as an instruction or a promise that there will be enough rotis.

## My next steps

- Confirm how the mess currently estimates meal quantities and what information is practical for staff to record.
- Gather and verify real observations across lunch and dinner on different days.
- Keep shortages and leftovers distinct in the data, and review how they affect the estimate.
- Ask the mess staff whether the form and forecast are clear and quick enough to use.
- Improve the forecast only after there is enough reliable data to justify a change.

This project has taught me that a useful tool does not need to be complicated. It needs to reflect the real situation, use trustworthy records, and fit the people who may use it. My aim is to make the roti counter a helpful aid for the mess, while treating the staff's experience and the limits of the data with care.
