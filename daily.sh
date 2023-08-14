#!/bin/bash

cd /home/shawnmonk/monk/data-bot
source venv/bin/activate
/home/shawnmonk/monk/data-bot/venv/bin/python /home/shawnmonk/monk/data-bot/wiki_stocks/sp-yahoo-financials.py
aws sns publish --topic-arn "arn:aws:sns:us-east-1:904524340593:tractors" --message "Cron Ran" 
