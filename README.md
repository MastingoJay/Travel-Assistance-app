# Travel-Assistance-App

## Project Overview

This project is a web-based Travel Assistance Application that provides AI-generated travel itineraries enhanced with:

- Real-time weather information

- Destination images

Users can select a destination, duration, and travel style, and receive a full trip plan including daily activities, recommended hotels, and practical travel tips.

The system integrates real APIs: OpenWeatherMap (weather), and Pexels API (images). AI-generated itineraries are displayed dynamically for an interactive experience.

## Features

- Dynamic Itinerary Generation – AI generates day-by-day plans

- Weather Condition – Shows current weather at the destination

- Travel Tips – Practical advice for travelers

- Responsive UI – Works on desktop and mobile

## Screenshots

Landing Page

![](https://github.com/MastingoJay/Travel-Assistance-app/blob/main/HOME%20PAGE.png)

Trip Generation Example

![](https://github.com/MastingoJay/Travel-Assistance-app/blob/main/HOME%20PAGE1.png)

Weather + Image Section

![](https://github.com/MastingoJay/Travel-Assistance-app/blob/main/ACTION.png)

Itenary

![](https://github.com/MastingoJay/Travel-Assistance-app/blob/main/ACTION1.png)

## Technical Architecture

- Frontend: HTML + Bootstrap + JavaScript

- APIs Integrated:

  - Weather: OpenWeatherMap

  - Images: Pexels API

- AI Integration: /generate endpoint handles itinerary generation

## Installation & Usage

### Clone the repository

```bash
git clone <repo-url>
cd travel-assistance-app
```

### Frontend

- Open index.html in a browser

- Enter your API keys in the script section:

``` bash
const PEXELS_API_KEY = "YOUR_PEXELS_API_KEY";
const WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_KEY";
```

### Backend

Ensure an AI endpoint (/generate) is running for itinerary generation

Can be FastAPI, Flask, or other AI service

## Deployment

- Frontend: Deploy on Netlify, Vercel, or GitHub Pages

- Backend: Deploy separately (Render, Railway, or Fly.io)

- Ensure CORS is enabled so frontend can communicate with backend

Example Deployment Links

Frontend: http://127.0.0.1:5000

### Example Queries

- "Plan a 3-day mid-range trip to Nairobi"

- "Suggest hotels in Mombasa"

- "What is the weather in Mount Kenya?"

- "Best local restaurants and activities in Zanzibar"

All results are dynamically generated with real weather, and images.

## Repository Structure

``` bash
index.html           # Main HTML frontend
static/              # Images and CSS files
script.js            # JavaScript for API calls and itinerary logic
```
































































