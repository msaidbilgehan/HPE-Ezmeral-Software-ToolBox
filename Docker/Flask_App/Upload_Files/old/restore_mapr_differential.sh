#!/bin/bash

# Kaynak (yedek) ve hedef (geri yükleme yapılacak yer) dizinlerini tanımlayalım
BACKUP_DIR="/home/mapr/backup"
DESTINATION="/opt/mapr/"

# Parametre olarak verilen backup numarasını (tarih) alalım
DATE=$1

# Eğer DATE parametresi boşsa, kullanıcıya bir hata mesajı gösterelim ve scripti sonlandıralım
if [ -z "$DATE" ]; then
    echo "Error: Please provide a backup number (date) as a parameter."
    echo "Usage: ./restore_script.sh 20230905"
    exit 1
fi

# Geri yükleme yapılacak yedeğin yolu
RESTORE_PATH="$BACKUP_DIR/$DATE"

# Yedeğin var olup olmadığını kontrol edelim
if [ ! -d "$RESTORE_PATH" ]; then
    echo "Backup for the date $DATE does not exist. Exiting..."
    exit 1
fi

# Tam yedeği geri yükle
echo "Restoring full backup..."
sudo rsync -aAX $BACKUP_DIR/full/ $SOURCE

# rsync ile yedeği geri yükleyelim
echo "Restoring from $RESTORE_PATH to $DESTINATION..."
sudo rsync -aAX $RESTORE_PATH/ $DESTINATION

echo "Restore completed from $RESTORE_PATH to $DESTINATION"
