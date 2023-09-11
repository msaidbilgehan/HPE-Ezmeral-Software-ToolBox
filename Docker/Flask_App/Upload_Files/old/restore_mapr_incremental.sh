#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <restore_date>"
    echo "Example: $0 20230905 (This will restore up to 5th September 2023)"
    exit 1
fi

RESTORE_DATE=$1
BACKUP_DIR="/home/mapr/backup"
SOURCE="/opt/mapr/"

# Tam yedeği geri yükle
echo "Restoring full backup..."
sudo rsync -aAX $BACKUP_DIR/full/ $SOURCE

# Belirtilen tarihe kadar olan incremental yedekleri sırayla geri yükle
for BACKUP in $(ls $BACKUP_DIR | grep -E '^20' | sort); do
    if [ "$BACKUP" -le "$RESTORE_DATE" ]; then
        echo "Restoring incremental backup from $BACKUP..."
        sudo rsync -aAX $BACKUP_DIR/$BACKUP/ $SOURCE
    fi
done

echo "Incremental restore up to $RESTORE_DATE completed!"
