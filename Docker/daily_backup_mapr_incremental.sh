#!/bin/bash

echo "Mapr mount point is on /opt/mapr/"

SOURCE="/opt/mapr/"
BACKUP_DIR="/home/mapr/backup"

### To check if it's not exists
if [ ! -d "$BACKUP_DIR" ];
then 
	echo -e "$BACKUP_DIR not exits. Creating...\n"
    mkdir $BACKUP_DIR
fi

DATE=$(date +%Y%m%d)
BACKUP_PATH="$BACKUP_DIR/$DATE"

# Create incremental backup
echo -e "Running: 'rsync -aAX --link-dest=$BACKUP_DIR/latest $SOURCE $BACKUP_PATH'\n"
sudo rsync -aAX --link-dest=$BACKUP_DIR/latest $SOURCE $BACKUP_PATH

# Update the 'latest' symlink
rm -rf $BACKUP_DIR/latest
ln -s $BACKUP_PATH $BACKUP_DIR/latest

# Limit the number of backups
MAX_BACKUPS=7
echo -e "Running: 'find $BACKUP_DIR -maxdepth 1 -type d -name '20*' | sort -r | tail -n +$(($MAX_BACKUPS + 1)) | xargs rm -rf'\n"
find $BACKUP_DIR -maxdepth 1 -type d -name '20*' | sort -r | tail -n +$(($MAX_BACKUPS + 1)) | xargs rm -rf
