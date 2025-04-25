# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.

## Project Overview

My project delivered a lightweight Flask web application that lets users enter any address or place.It uses Mapbox’s Geocoding API to convert that input into coordinates, and then finds the nearest MBTA stop (with wheelchair-accessibility info) via the MBTA V3 API. Key features include a reusable `mbta_helper.py` module with URL‐builder, geocoding, and stop‐lookup functions. Beyond the basic requirements, I added a “view request URL” link for transparency, improved error handling with custom templates, and alerts for a polished UI.

## Reflection

### Development process  
I structured my work by first building and testing each API integration separately, then unifying them in `mbta_helper.py`, and finally wiring everything into Flask routes.Print-debug tests provided py AI prevented misformatted URLs and helped debug my 403 errors quickly.

### Learning  
This project deepened my understanding of Flask routing, template rendering, and environment-driven configuration.I learned to navigate API docs, build dynamic URLs, and handle error cases. ChatGPT helped for scaffolding and troubleshooting—especially around `.env` setup which ended up being very simple but was challenging at the beginning. Going forward, ill embrace test-driven development, early UI wireframing, and continuous integration to streamline future projects.
 
