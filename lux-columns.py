#!/usr/bin/python3
import gi, grp, os, pwd, stat
gi.require_version('Nautilus', '4.0')
from gi.repository import GObject, Nautilus
from datetime import datetime
from pathlib import Path
from typing import List

class LuxColumnsAsync(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
	def get_columns(self):
		uidColumn = Nautilus.Column(
				name = 'NautilusPython::lux_uid_column',
				attribute = 'lux_uid',
				label = 'UID',
				description = 'The file\'s UID',
			)
		uidColumn.props.xalign = 1.0 # right align

		gidColumn = Nautilus.Column(
				name = 'NautilusPython::lux_gid_column',
				attribute = 'lux_gid',
				label = 'GID',
				description = 'The file\'s GID',
			)
		gidColumn.props.xalign = 1.0 # right align

		# exists in Nautilus, but with "(You)" added for own user; this version is just the username
		userColumn = Nautilus.Column(
				name = 'NautilusPython::lux_user_column',
				attribute = 'lux_user',
				label = 'User',
				description = 'The file\'s owner',
			)

		# already exists in Nautilus
		#groupColumn = Nautilus.Column(
		#		name = 'NautilusPython::lux_group_column',
		#		attribute = 'lux_group',
		#		label = 'Group',
		#		description = 'The file\'s group',
		#	),

		uidGidColumn = Nautilus.Column(
				name = 'NautilusPython::lux_uid_gid_column',
				attribute = 'lux_uid_gid',
				label = 'UID:GID',
				description = 'The file\'s UID and GID',
			)

		userGroupColumn = Nautilus.Column(
				name = 'NautilusPython::lux_user_group_column',
				attribute = 'lux_user_group',
				label = 'User:Group',
				description = 'The file\'s owner and group',
			)

		fullPathColumn = Nautilus.Column(
				name = 'NautilusPython::lux_full_path_column',
				attribute = 'lux_full_path',
				label = 'Full Path',
				description = 'The file\'s path, with symlink target if available',
			)

		symlinkPathColumn = Nautilus.Column(
				name = 'NautilusPython::lux_symlink_path_column',
				attribute = 'lux_symlink_path',
				label = 'Symlink Path',
				description = 'Shows target if file is a symlink',
			)

		createdSortableColumn = Nautilus.Column(
				name = 'NautilusPython::lux_created_sortable_column',
				attribute = 'lux_created_sortable',
				label = 'Created Date',
				description = 'File\'s created date in sortable format: strftime(%F %T)',
			)

		modifiedSortableColumn = Nautilus.Column(
				name = 'NautilusPython::lux_modified_sortable_column',
				attribute = 'lux_modified_sortable',
				label = 'Modified Date',
				description = 'File\'s modified date in sortable format: strftime(%F %T)',
			)

		accessedSortableColumn = Nautilus.Column(
				name = 'NautilusPython::lux_accessed_sortable_column',
				attribute = 'lux_accessed_sortable',
				label = 'Accessed Date',
				description = 'File\'s accessed date in sortable format: strftime(%F %T)',
			)

		mimeTypeColumn = Nautilus.Column(
				name = 'NautilusPython::lux_mime_type_column',
				attribute = 'lux_mime_type',
				label = 'MIME Type',
				description = 'The file\'s mime-type',
			)

		return [
			uidColumn,
			gidColumn,
			userColumn,
			#groupColumn,
			uidGidColumn,
			userGroupColumn,
			fullPathColumn,
			symlinkPathColumn,
			createdSortableColumn,
			modifiedSortableColumn,
			accessedSortableColumn,
			mimeTypeColumn,
		]

	def update_file_info(self, file):
		# Get file's path
		path: str = file.get_location().get_path()
		mimeType: str = file.get_mime_type()

		# Get file info
		fileInfo = os.lstat(path)
		# Get file user info
		userInfo = pwd.getpwuid(fileInfo.st_uid)
		# Get file group info
		groupInfo = grp.getgrgid(fileInfo.st_gid)

		symlink: str = ''
		if stat.S_ISLNK(fileInfo.st_mode):
			# Get symlink target
			symlink = str(Path(path).resolve())
			path += ' -> ' + symlink

		# File dates
		createdDate: datetime = datetime.fromtimestamp(fileInfo.st_ctime)
		modifiedDate: datetime = datetime.fromtimestamp(fileInfo.st_mtime)
		accessedDate: datetime = datetime.fromtimestamp(fileInfo.st_atime)

		# Assign the column values
		file.add_string_attribute('lux_uid', str(fileInfo.st_uid))
		file.add_string_attribute('lux_gid', str(fileInfo.st_gid))
		file.add_string_attribute('lux_uid_gid', "{0}:{1}".format(fileInfo.st_uid, fileInfo.st_gid))
		file.add_string_attribute('lux_user', userInfo.pw_name)
		#file.add_string_attribute('lux_group', groupInfo.gr_name)
		file.add_string_attribute('lux_user_group', "{0}:{1}".format(userInfo.pw_name, groupInfo.gr_name))

		file.add_string_attribute('lux_full_path', path)
		file.add_string_attribute('lux_symlink_path', symlink)

		file.add_string_attribute('lux_created_sortable', createdDate.strftime('%F %T'))
		file.add_string_attribute('lux_modified_sortable', modifiedDate.strftime('%F %T'))
		file.add_string_attribute('lux_accessed_sortable', accessedDate.strftime('%F %T'))

		file.add_string_attribute('lux_mime_type', mimeType)
