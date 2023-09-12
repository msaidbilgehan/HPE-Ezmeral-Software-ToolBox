#!/bin/bash
# ----------------------------------------------------------------------
# mikes handy rotating-filesystem-snapshot utility
# http://www.mikerubel.org/computers/rsync_snapshots/#Extensions
# ----------------------------------------------------------------------
# this needs to be a lot more general, but the basic idea is it makes
# rotating backup-snapshots of $BACKUP_SOURCE_DIR whenever called
# ----------------------------------------------------------------------

unset PATH	# suggestion from H. Milz: avoid accidental use of $PATH

# ------------- system commands used by this script --------------------
ID=/usr/bin/id;
SUDO=/usr/bin/sudo;
ECHO=/bin/echo;

MOUNT=/bin/mount;
RM=/bin/rm;
MV=/bin/mv;
CP=/bin/cp;
TOUCH=/bin/touch;

RSYNC=/usr/bin/rsync;


# ------------- file locations -----------------------------------------

BACKUP_SOURCE_DIR=/opt/mapr;
SNAPSHOT_DIR=/root/snapshot;


# ------------- the script itself --------------------------------------

# make sure we're running as root
if (( `$ID -u` != 0 )); then { $ECHO "Sorry, must be root.  Exiting..."; exit; } fi

if [ ! -d "$SNAPSHOT_DIR" ] ; then			\
	$SUDO mkdir -p "$SNAPSHOT_DIR" ;	\
fi;

# attempt to remount the RW mount point as RW; else abort
# $ECHO "Attempting to update permissions as writable for $SNAPSHOT_DIR..."
# if [ ! -w "$SNAPSHOT_DIR" ]; then
# 	$SUDO chmod -R u+w $SNAPSHOT_DIR
#     $ECHO "$SNAPSHOT_DIR is now writable "
# else
#     $ECHO "No need to add write permission. $SNAPSHOT_DIR is already writable"
# fi


# rotating snapshots of $BACKUP_SOURCE_DIR

# step 1: delete the oldest snapshot, if it exists:
$ECHO "Deleting the oldest snapshot, if they exist..."
if [ -d $SNAPSHOT_DIR/daily.7 ] ; then			\
	$RM -rf $SNAPSHOT_DIR/daily.7 ;				\
fi ;

# step 2: shift the middle snapshots(s) back by one, if they exist
$ECHO "Shifting the middle snapshots(s) back by one, if they exist..."
if [ -d $SNAPSHOT_DIR/daily.6 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.6 $SNAPSHOT_DIR/daily.7 ;	\
fi;
if [ -d $SNAPSHOT_DIR/daily.5 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.5 $SNAPSHOT_DIR/daily.6 ;	\
fi;
if [ -d $SNAPSHOT_DIR/daily.4 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.4 $SNAPSHOT_DIR/daily.5 ;	\
fi;
if [ -d $SNAPSHOT_DIR/daily.3 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.3 $SNAPSHOT_DIR/daily.4 ;	\
fi;
if [ -d $SNAPSHOT_DIR/daily.2 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.2 $SNAPSHOT_DIR/daily.3 ;	\
fi;
if [ -d $SNAPSHOT_DIR/daily.1 ] ; then			\
	$MV $SNAPSHOT_DIR/daily.1 $SNAPSHOT_DIR/daily.2 ;	\
fi;

# step 3: make a hard-link-only (except for dirs) copy of the latest snapshot,
# if that exists
$ECHO "Making a hard-link-only (except for dirs) copy of the latest snapshot, if they exist..."
if [ -d $SNAPSHOT_DIR/daily.0 ] ; then			\
	$CP -al $SNAPSHOT_DIR/daily.0 $SNAPSHOT_DIR/daily.1 ;	\
fi;

# step 4: rsync from the system into the latest snapshot (notice that
# rsync behaves like cp --remove-destination by default, so the destination
# is unlinked first.  If it were not so, this would copy over the other
# snapshot(s) too!
$ECHO "Running rsync..."
$RSYNC								\
	-va --delete					\
	--perms --owner --group			\
	$BACKUP_SOURCE_DIR $SNAPSHOT_DIR/daily.0 ;

# step 5: update the mtime of daily.0 to reflect the snapshot time
$ECHO "Updating the mtime of daily.0 to reflect the snapshot time"
$TOUCH $SNAPSHOT_DIR/daily.0 ;

# and thats it for $BACKUP_SOURCE_DIR.

# now remount the RW snapshot mountpoint as readonly

# $ECHO "Attempting to update permissions as read-only for $SNAPSHOT_DIR..."
# if [ -e "$SNAPSHOT_DIR" ] && [ -w "$SNAPSHOT_DIR" ]; then
# 	$SUDO chmod -R a-w $SNAPSHOT_DIR
#     $ECHO "$SNAPSHOT_DIR is now read-only "
# else
#     $ECHO "No need to remove append-write permissions. $SNAPSHOT_DIR is already read-only"
# fi
