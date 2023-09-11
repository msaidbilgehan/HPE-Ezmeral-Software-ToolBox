#!/bin/bash

# Kaynak ve hedef dizinleri tanımlayalım
SOURCE="/opt/mapr/"
BACKUP_DIR="/home/mapr/backup"

# Eğer hedef dizini yoksa oluşturalım
if [ ! -d "$BACKUP_DIR" ]; then
    echo "$BACKUP_DIR does not exist. Creating..."
    mkdir -p $BACKUP_DIR
fi

# İlk tam yedeğin yolu
FULL_BACKUP="$BACKUP_DIR/full"

# Eğer ilk tam yedek yoksa, tam yedek alalım
if [ ! -d "$FULL_BACKUP" ]; then
    echo "Full backup does not exist. Creating full backup..."
    sudo rsync -aAX $SOURCE $FULL_BACKUP
fi

# Yedekleme için tarih bazlı bir klasör adı oluşturalım
DATE=$(date +%Y%m%d)
BACKUP_PATH="$BACKUP_DIR/$DATE"

# Differential yedekleme yapalım
echo "Running rsync for differential backup..."
sudo rsync -aAX --compare-dest=$FULL_BACKUP/ $SOURCE $BACKUP_PATH

echo "Backup completed to $BACKUP_PATH"
