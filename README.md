# Deutsche Bahn Train Delay Analysis

## Final Data Visualization Project — Summer 2026

**Author:** SHAIK KHAJA SOHAIL HUSSAIN  
**Matriculation number:** 82022509  
**Subject:** DATA VISUALIZATION

---

## Project Overview

This project analyses Deutsche Bahn train-service records to investigate when,
where and which types of trains experienced the most delays across major German
railway stations.

The analysis examines delay frequency and delay severity using station,
train-category, date, scheduled time, platform and disruption-reason
information.

The final project contains:

- a Jupyter notebook containing data preparation and exploratory analysis;
- ten analytical questions answered using Plotly visualisations;
- an interactive Streamlit dashboard;
- a PDF presentation summarising the main findings;
- the original and processed datasets.

---

## Project Objective

The main objective is to answer the following question:

> How do train delays differ by station, train category, time, sampled date and
> recorded disruption reason across major German railway stations?

The project distinguishes between:

- **Delay frequency:** the percentage of services marked as delayed.
- **Delay severity:** the number of minutes by which a service was delayed.
- **Service volume:** the number of train-service records available for each
  station or category.

---

## Dataset

**Dataset title:** Trains and Delays Deutsche Bahn

**Dataset uploader:** Santiago Ravotti

**Underlying source:** Deutsche Bahn station-board information

**Dataset file:** `trains_db_hbfs.csv`

**File format:** CSV

**Licence:** CC0 — Public Domain

**Dataset page:**  
https://www.kaggle.com/datasets/santiagoravotti/trains-and-delays-deutsche-bahn

**Underlying Deutsche Bahn source:**  
https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn

---

## Dataset Scope

The uploaded CSV contains:

- **77,146 raw records**
- **9 original columns**
- **20 German main railway stations**
- **8 sampled dates**
- **34,254 raw records marked as delayed**
- approximately **44.4% of raw records marked as delayed**

The dates represented in the downloaded file are:

- 20 July 2024
- 21 July 2024
- 22 July 2024
- 23 July 2024
- 24 July 2024
- 25 July 2024
- 1 September 2024
- 2 September 2024

The results therefore describe the eight dates represented in this file and
should not be interpreted as a complete annual assessment of Deutsche Bahn.

---

## Unit of Observation

Each row represents one train service recorded at one major German railway
station at a scheduled time.

---

## Original Variables

The original dataset contains the following columns:

| Column | Description |
|---|---|
| `date` | Date of the train-service record |
| `Hbf` | Main railway station |
| `scheduled_time` | Scheduled arrival or departure time |
| `expected_time` | Updated expected time |
| `train_model` | Train category, service code and service number |
| `route` | Destination or route information |
| `platform` | Recorded platform |
| `real_time_due_to_delay` | Real-time information, including time and possible disruption text |
| `has_delay` | Delay indicator: 1 means delayed and 0 means not delayed |

---

## Data Preparation

The original CSV is preserved unchanged inside `data/raw`.

The following preparation steps are completed in the Jupyter notebook:

1. Create a working copy of the original dataset.
2. Identify and remove exact duplicate rows.
3. Rename `Hbf` to `station`.
4. Standardise inconsistent station names.
5. Convert the date field into datetime format.
6. Combine dates and scheduled times into complete timestamps.
7. Extract usable real-time values from the mixed text field.
8. Calculate actual delay duration in minutes.
9. Correct time calculations for services passing midnight.
10. Extract scheduled hour, weekday and day type.
11. Extract train-service codes from `train_model`.
12. Group services into:
    - Long-distance
    - Regional
    - S-Bahn
    - Bus or replacement service
    - Other
13. Identify records mentioning platform changes.
14. Extract recorded disruption reasons following `Grund:`.
15. Save the prepared dataset as:

`data/processed/trains_db_hbfs_cleaned.csv`

A total of **670 exact duplicate rows** were identified, leaving **76,476
records** after duplicate removal.

---

## Analytical Questions

### Question 1

Which stations recorded the highest delay rates, and how did this relate to
their service volume?

### Question 2

Which broad train-service groups had the highest delay rates?

### Question 3

How did delay rates change by scheduled hour for different train groups?

### Question 4

Which station and train-group combinations were the most delay-prone?

### Question 5

Did weekday and weekend delay patterns differ between train groups?

### Question 6

When a delayed service had usable real-time information, how severe was the
delay for each train group?

### Question 7

Which stations experienced the longest typical and severe delays?

### Question 8

Which sampled dates combined high delay rates with long average delays?

### Question 9

Which commonly recorded disruption reasons were associated with the longest
delays?

### Question 10

At which stations were platform changes recorded most often, and how much
delay accompanied them?

---

## Visualisation Approach

All final visualisations are created using **Plotly**.

The visualisations use:

- clean white backgrounds;
- colour-vision-deficiency-safe colours;
- limited and purposeful use of colour;
- takeaway-based chart titles;
- clear axis titles and measurement units;
- direct labels and annotations where useful;
- reduced gridlines and unnecessary visual clutter;
- interactive hover information.

The visualisations are explanatory rather than purely exploratory. Each chart
is designed to answer one analytical question and communicate one main
finding.

---

## Main Findings

### 1. Station delay rates varied substantially

München Hbf recorded the highest delay rate in the available sample at
approximately **90.1%**.

It was followed by:

- Münster (Westf) Hbf — approximately **67.6%**
- Bielefeld Hbf — approximately **60.7%**

The comparison also showed that service volume alone did not explain the
differences between stations.

### 2. Long-distance services performed worst

Long-distance services recorded the highest delay rate at approximately
**75.6%**.

The approximate delay rates by broad train group were:

- Long-distance — **75.6%**
- Regional — **51.6%**
- S-Bahn — **36.9%**
- Bus or replacement services — **13.1%**

### 3. Long-distance delays were also more severe

Among delayed records with usable real-time information, the median delay was:

- Long-distance — approximately **10 minutes**
- Regional — approximately **3 minutes**
- Bus or replacement services — approximately **3 minutes**
- S-Bahn — approximately **2 minutes**

Long-distance services therefore performed poorly in both delay frequency and
delay duration.

### 4. Delay frequency and severity identified different problem areas

München Hbf had the highest delay rate, but Bielefeld Hbf and Bonn Hbf had
longer typical delay durations.

The approximate median delay durations were:

- Bielefeld Hbf — **9 minutes**
- Bonn Hbf — **8 minutes**
- Münster (Westf) Hbf — **7 minutes**

This demonstrates that delay rate and delay duration should be analysed
separately.

### 5. Operational reasons had unequal effects

Recorded disruption reasons such as delays originating abroad and train
diversions were associated with particularly long typical delays.

The most frequent operational issue was not necessarily the issue associated
with the longest delay.

### 6. Platform-change frequency and delay severity did not always move together

Some stations recorded platform changes frequently but with relatively short
associated delays. Other stations recorded fewer platform changes, but those
changes were associated with longer delays.

---

## Overall Conclusion

The analysis shows that Deutsche Bahn reliability cannot be assessed using one
measure alone.

Long-distance services were the weakest-performing category because they
experienced both frequent and comparatively severe delays. However, station
rankings changed depending on whether performance was measured using delay
rate, median delay or severe-delay percentiles.

The findings demonstrate the importance of analysing station, service type,
time, delay duration and operational reason together rather than relying only
on total delayed-service counts.

---

## Limitations

This project has the following limitations:

- The downloaded file contains only eight sampled dates.
- The results should not be treated as a complete annual assessment.
- Actual delay duration can only be calculated when a usable real-time value
  is available.
- The `real_time_due_to_delay` column contains a mixture of times and German
  text.
- Some real-time records are missing.
- Train groups are derived from service-code prefixes and simplify some
  operator-specific categories.
- The analysis uses the supplied `has_delay` classification.
- A train may appear at multiple stations as part of its route.
- The results identify associations and patterns but do not establish
  causation.

---

## Interactive Streamlit Dashboard

The Streamlit dashboard presents a selected subset of the strongest findings.

It allows users to explore the data using filters such as:

- station;
- train group;
- sampled date;
- scheduled hour;
- weekday or weekend;
- delay status.

**Live dashboard:**  
 
https://deutsche-bahn-delay-analysis-7rj2tgss6za6aykj3zjnjr.streamlit.app

---

## GitHub Repository

The complete source code, notebook, dataset information and presentation are
available in the public GitHub repository.

**GitHub repository:**  
## GitHub Repository

The complete source code, notebook, datasets and dashboard files are available
in the public GitHub repository.

**GitHub repository:**  
https://github.com/sksohailhussain10-spec/deutsche-bahn-delay-analysis

---

## Project Structure

```text
Final_Data_Visualization_Project/
│
├── data/
│   ├── raw/
│   │   └── trains_db_hbfs.csv
│   │
│   └── processed/
│       └── trains_db_hbfs_cleaned.csv
│
├── images/
│   ├── exported visualisations
│   └── dashboard screenshots
│
├── final_analysis.ipynb
├── notebook_export.html
├── app.py
├── requirements.txt
├── README.md
└── presentation.pdf
