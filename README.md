# Russo-Ukrainian Airstrike Analysis: Patterns, Impact & Prediction

This project delves into the Russo-Ukrainian conflict using open-source data to identify patterns, analyze the impact of various events, and predict fatality occurrences. Through extensive data analysis, geospatial visualizations, and machine learning models, we aim to provide insights into the conflict's dynamics.

## Project Overview

We analyze conflict events and missile/UAV strikes to understand their distribution, intensity, and consequences, with a particular focus on civilian targeting and fatalities. The project culminates in an interactive 3D map visualizing regional attack intensity and individual strike fatalities.

## Data Sources

Two primary datasets were utilized:

*   **ACLED Data (Armed Conflict Location & Event Data Project)**: Provides granular information on conflict events, actors, locations (latitude/longitude), event types, and associated fatalities across Ukraine.
*   **Missile/UAV Attack Data**: Detailed records of launched and destroyed missiles and unmanned aerial vehicles, including their models, categories (missile/UAV), and targets.

## Methodology

Our analytical approach involved several stages:

1.  **Exploratory Data Analysis (EDA)**: Initial examination of data distributions, event timelines, and regional concentrations of conflict and attacks.
2.  **Geospatial Analysis**: Creation of 2D and 3D interactive maps to visualize conflict hotspots, fatality locations, and regional attack intensities. K-Means clustering was applied to latitude and longitude to create geospatial features for modeling.
3.  **Feature Engineering**: Development of temporal features (month, day of week, day of year) and integration of geospatial clusters into the dataset.
4.  **Predictive Modeling**: Employed a two-tiered modeling approach:
    *   **Lasso Regression**: Used to predict the number of fatalities for events where fatalities occur, identifying key influencing factors.
    *   **Logistic Regression & Random Forest Classifier**: Used to predict the likelihood of an event resulting in any fatalities (binary classification: fatalities > 0 or = 0). These models help understand the drivers behind fatal versus non-fatal incidents.

## Key Findings

*   The conflict involves a significant number of events, with over **6,000 recorded incidents** and **over 10,000 fatalities** across the datasets.
*   Intense conflict activity is concentrated in specific regions, particularly **Donetsk and Luhansk**, which account for a substantial percentage of all strikes, leading to disproportionate impacts and a higher likelihood of casualties there.
*   Missile and UAV data indicate an overall destruction rate of over **70%** for launched projectiles, highlighting strong defensive capabilities.
*   A notable proportion (over **50%**) of ACLED conflict events are recorded with zero fatalities, suggesting varied incident impacts.
*   **Geospatial location** and **temporal factors** (where and when events occur) are crucial determinants of conflict severity and casualty counts, as confirmed by our predictive models.
*   The **Shahed-136/131** UAV model is a prominent component of the attacks, representing a significant percentage of all launched projectiles.

## Broader Implications & Future Work

Our findings can inform:

*   **Humanitarian Aid**: Directing resources to high-risk areas based on predicted fatality patterns.
*   **Policy & Defense**: Developing more effective defense strategies and resource allocation by understanding attack types and locations.
*   **Conflict Monitoring**: Contributing to early warning systems for escalating violence.

Future work could involve integrating more diverse data sources (e.g., economic indicators, social media sentiment), exploring advanced deep learning models for spatio-temporal predictions, and refining models to predict specific types of casualties or damages.

## Interactive 3D Map (Streamlit App)

An interactive 3D map is available, built using PyDeck and Streamlit, showcasing regional attack intensity and individual fatality strikes across Ukraine. The map allows for exploration of conflict hotpots and the severity of events.

**Access the live Streamlit app here:** [https://ukraine-3d-map-nt7et2c3m46k2boo2vqnfd.streamlit.app/](https://ukraine-3d-map-nt7et2c3m46k2boo2vqnfd.streamlit.app/)

### How to Run the Streamlit App Locally

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure `requirements.txt` contains `pandas`, `geopandas`, `pydeck`, `matplotlib`, `streamlit`, `scikit-learn`, `statsmodels`, `seaborn`, `IPython`)*

3.  **Save the Streamlit application file:**

    The Streamlit application code has been exported to `ukraine_3d_map.py` (or similar). Make sure this file is in your cloned repository.

4.  **Run the Streamlit app:**

    ```bash
    streamlit run ukraine_3d_map.py
    ```

    This will open the interactive 3D map in your web browser.
