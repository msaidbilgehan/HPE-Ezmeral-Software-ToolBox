#!/bin/bash

# ------------- system commands used by this script --------------------
ID=/usr/bin/id;
ECHO=/bin/echo;
RSYNC=/usr/bin/rsync;

# ------------- file locations -----------------------------------------
BACKUP_SOURCE_DIR=/opt/mapr;
SNAPSHOT_RW=/root/snapshot;

# make sure we're running as root
if (( `$ID -u` != 0 )); then { $ECHO "Sorry, must be root. Exiting..."; exit; } fi

# Check if a parameter is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <backup_number>"
    exit 1
fi

BACKUP_NUM=$1

# Restore each backup from the specified number to 0
for ((i=BACKUP_NUM; i>=0; i--))
do
    if [ -d $SNAPSHOT_RW/daily.$i ]; then
        $ECHO "Restoring from backup daily.$i..."
        $RSYNC -av --delete $SNAPSHOT_RW/daily.$i/ $BACKUP_SOURCE_DIR/
    else
        $ECHO "Backup daily.$i not found!"
    fi
done

$ECHO "Restore completed."
