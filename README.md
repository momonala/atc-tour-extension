# Against the Compass Tour Chrome Extension and Google Calendar Updater Service

## Chrome Extension
Filters away tours your not interested in, provides the discounted price, and defaults the view to the table view on `https://expeditions.againstthecompass.com/tours/`

To install locally: 

1. Go to [`chrome://extensions/`](chrome://extensions/)
2. enable Developer mode
3. and click on "Load unpacked" on the top left.
4. Select this directory containing your extension files.
5. Under the "ATC tour filter" extension that just loaded, go to "details"
6. Enable "Pin to toolbar"

## Google Calendar Updater Service
Runs a cron job with python-schedule that updates events in your Google Calendar for tours you are interested in. Execute with `main.py` or `schedule.py` service.

Installation:
```
conda create -n against_the_compass_tour_extension python=3.12 -y
pip install poetry
poetry install
```

Create a google_application_credentials.json file with the appropriate scopes (see values.py).
