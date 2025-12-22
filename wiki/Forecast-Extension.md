# Forecast: Kenya EO Decisions

**Forecast** is a Chrome Extension designed to empower non-technical decision-makers in Kenya to use Earth Observation (EO) data efficiently. It translates complex satellite imagery into simple, question-driven indicators and actionable policy recommendations.

## Overview

-   **Target Audience**: County Governors, Policymakers, Agricultural Principals.
-   **Goal**: Provide answers, not just data.
-   **Core Philosophy**: "Explain decision impact, not just the situation."

## Key Features

### 1. Simple Indicators
Instead of raw spectral bands, we display easy-to-understand scores:
-   **Vegetation Health**: 0-100 Score (NDVI based).
-   **Flood Risk**: Low / Moderate / High / Severe.
-   **Status Badges**: Color-coded (Green for Good, Red for Danger).

### 2. Natural Language Insights
We convert data into plain English sentences:
-   *Before*: "NDVI anomaly -0.12"
-   *After*: "Vegetation in this area has declined by 12 percent in the past 3 months."

### 3. Action-Oriented Recommendations
The system suggests concrete next steps:
-   "Immediate irrigation support needed."
-   "Clear drainage channels immediately."

### 4. Interactive Timeline
A slider allows users to visualize trends over the past 6 months to spot emerging droughts or flood patterns.

## Architecture

The extension is built using standard Web Technologies:
-   **Frontend**: HTML5, CSS3 (Google Material Design tokens).
-   **Components**: Custom JS Classes (`InsightCard`, `TimeSlider`) & Google Maps Extended Component Library.
-   **Data Layer**: `GEEService` (Currently mocked) simulating Google Earth Engine responses for Kenyan regions.

### Critical Files
-   `manifest.json`: Extension configuration (Manifest V3).
-   `src/popup.html`: Main interface.
-   `src/services/gee-service.js`: Mock data provider.

## Installation & Usage

1.  **Clone the Repository**: Ensure you have the `packages/forecast` directory.
2.  **Load in Chrome**:
    *   Go to `chrome://extensions/`
    *   Enable **Developer mode**.
    *   Click **Load unpacked**.
    *   Select `packages/forecast`.
3.  **Run**: Click the Forecast icon in the toolbar.
4.  **Test Regions**: Search for the following to see different scenarios:
    *   **"Kitui"**: Warning state (Drought risk).
    *   **"Garissa"**: Danger state (Severe drought).
    *   **"Kisumu"**: Danger state (High flood risk).
    *   **"Kenya"**: Default view.

## Future Roadmap
-   **Real GEE Integration**: Connect `gee-service.js` to actual Google Earth Engine API.
-   **Interactive Map**: Fully integrate the Google Maps JavaScript API for the map view.
-   **PDF Reports**: Generate downloadable "Policy Decks".
