#!/bin/bash
start_date="2025-01-01"
end_date="2025-01-31"

current_date="$start_date"
while [[ "$current_date" < "$end_date" || "$current_date" == "$end_date" ]]; do
    echo "python3 crawler.py --date "$current_date" --output "$current_date""
    python3 crawler.py --date "$current_date" --output "$current_date"
    # Increment the date (this example uses GNU date)
    current_date=$(date -I -d "$current_date + 1 day")
done
