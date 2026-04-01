#!/bin/bash

# organizer.sh
# Archives grades.csv with a timestamp, resets
# the workspace, and logs every operation.


GRADES_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"


#  Check if grades.csv exists before archiving

if [ ! -f "$GRADES_FILE" ]; then
    echo "Error: '$GRADES_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi


#  Check if grades.csv is empty — skip processing if it is

if [ ! -s "$GRADES_FILE" ]; then
    echo "Error: '$GRADES_FILE' is empty. Nothing to archive."
    exit 1
fi


#  Check if archive directory exists, create if not

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
else
    echo "Archive directory already exists: $ARCHIVE_DIR"
fi


#  Generate timestamp (format: YYYYMMDD-HHMMSS)

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")


#  Build the new archived filename and move it

ORIGINAL_NAME="$GRADES_FILE"
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

mv "$GRADES_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"
echo "Archived: $ORIGINAL_NAME → $ARCHIVE_DIR/$ARCHIVED_NAME"


#  Workspace Reset: create a fresh empty grades.csv

touch "$GRADES_FILE"
echo "Workspace reset: new empty '$GRADES_FILE' created."


#  Logging: append operation details to organizer.log

echo "[$TIMESTAMP] Original: $ORIGINAL_NAME | Archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"
echo "Logged operation to: $LOG_FILE"

echo ""
echo "Done!"