# SHRP2 Travel Time Reliability Dashboard (Colorado)
Explore the impacts of work zones, incidents, extreme weather, and special events on travel time reliability in Colorado.

## Overview
This dashboard was developed by Navjoy Inc. in partnership with the Colorado Department of Transportation (CDOT) as part of the Strategic Highway Research Program 2 (SHRP2).

Navjoy compiled travel time data for corridors with four sources of non-recurring congestion: active work zones, traffic incidents, special events, and severe weather. Travel time data were compiled from the RITIS Probe Data Analytics Massive Data Downloader, and impact dates, locations, and subtypes were compiled from various CDOT databases.

This dashboard allows users to select up to two variables for comparison using violin plots, a summary table, and cumulative distribution functions. Users may apply various filters to the data set to narrow their results and improve performance. 

For more information on CDOT's implementation of SHRP2, see the report included in this repository. 
## Technologies
* Python 3.7.4
* Dash 1.16.0
* Heroku 
### Libraries
* plotly 4.9.0
* dash-core-components 1.12.0
* dash-html-components 1.1.1
* pandas 1.1.2
* datetime 4.3
* numpy 1.18.2

## Launch
This project can be viewed at https://shrp2-dashboard.herokuapp.com/

## Acknowledgments 
All code written by Stewart LaPan. The SHRP2 final report was composed by Justin Healey and Devin Joslin. Special thanks to Ethan Alexander and Marc Russell for their data collection efforts, and to Emily Gerson and Jim MacCrea for their assistance with editing and formatting of the final report.
