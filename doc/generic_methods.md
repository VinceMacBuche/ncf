# Permissions type recursion
* *bundle name:* permissions_type_recursion
## parameters
* path
* mode
* owner
* group
* type
* recursion
## class result
* permissions_path

# File ensure lines in section
* *bundle name:* file_ensure_lines_in_section_present
## parameters
* file
* section
* content_tab
## class result
* file_ensure_lines_in_section_present_file

# Logger for Rudder
* *bundle name:* logger_rudder
## parameters
* message
* class_prefix
## class result
* logger_rudder_class_prefix

# File replace lines
* *bundle name:* file_replace_lines
## parameters
* file
* line
* replacement
## class result
* file_replace_lines_file

# Service restart
* *bundle name:* service_restart
## parameters
* service_name
## class result
* service_restart_service_name

# Service check running ps
* *bundle name:* service_check_running_ps
## parameters
* service_regex
## class result
* service_check_running_service_regex

# Permissions recurse
* *bundle name:* permissions_recurse
## parameters
* path
* mode
* owner
* group
## class result
* permissions_path

# Service ensure stopped
* *bundle name:* service_ensure_stopped
## parameters
* service_name
## class result
* service_ensure_stopped_service_name

# File copy from local source recurse
* *bundle name:* file_copy_from_local_source_recursion
## parameters
* source
* destination
* recursion
## class result
* file_copy_from_local_source_destination

# Service stop
* *bundle name:* service_stop
## parameters
* service_name
## class result
* service_stop_service_name

# File check exists
* *bundle name:* file_check_exists
## parameters
* file_name
## class result
* file_check_exists_file_name

# Service reload
* *bundle name:* service_reload
## parameters
* service_name
## class result
* service_reload_service_name

# Command execution
* *bundle name:* command_execution
## parameters
* command_name
## class result
* command_execution_command_name

# File from template
* *bundle name:* file_from_template
## parameters
* source_template
* destination
## class result
* file_from_template_destination

# Package verify
* *bundle name:* package_verify
## parameters
* package_name
## class result
* package_install_package_name

# Permissions dirs
* *bundle name:* permissions_dirs
## parameters
* path
* mode
* owner
* group
## class result
* permissions_path

# File ensure lines absent
* *bundle name:* file_ensure_lines_absent
## parameters
* file
* lines
## class result
* file_ensure_lines_absent_file

# Service check running
* *bundle name:* service_check_running
## parameters
* service_name
## class result
* service_check_running_service_name

# Package install
* *bundle name:* package_install
## parameters
* package_name
## class result
* package_install_package_name

# File copy from remote source recurse
* *bundle name:* file_copy_from_remote_source_recursion
## parameters
* source
* destination
* recursion
## class result
* file_copy_from_remote_source_destination

# File ensure lines present
* *bundle name:* file_ensure_lines_present
## parameters
* file
* lines
## class result
* file_ensure_lines_present_file

# File ensure block present
* *bundle name:* file_ensure_block_present
## parameters
* file
* block
## class result
* file_ensure_block_present_file

# File template expand
* *bundle name:* file_template_expand
## parameters
* tml_file
* target_file
* mode
* owner
* group
## class result
* file_template_expand_target_file

# Create symlink (optional overwriting)
* *bundle name:* file_create_symlink_enforce
## parameters
* source
* destination
* enforce
## class result
* file_create_symlink_destination

# Package install version
* *bundle name:* package_install_version
## parameters
* package_name
* package_version
## class result
* package_install_package_name

# Create symlink
* *bundle name:* file_create_symlink
## parameters
* source
* destination
## class result
* file_create_symlink_destination

# File ensure block in section
* *bundle name:* file_ensure_block_in_section
## parameters
* file
* section_start
* section_end
* block
## class result
* file_ensure_block_in_section_file

# File copy from remote source
* *bundle name:* file_copy_from_remote_source
## parameters
* source
* destination
## class result
* file_copy_from_remote_source_destination

# File copy from local source
* *bundle name:* file_copy_from_local_source
## parameters
* source
* destination
## class result
* file_copy_from_local_source_destination

# Permissions dirs recurse
* *bundle name:* permissions_dirs_recurse
## parameters
* path
* mode
* owner
* group
## class result
* permissions_path

# Package verify version
* *bundle name:* package_verify_version
## parameters
* package_name
* package_version
## class result
* package_install_package_name

# Package remove
* *bundle name:* package_remove
## parameters
* package_name
## class result
* package_remove_package_name

# Permissions recurse
* *bundle name:* permissions
## parameters
* path
* mode
* owner
* group
## class result
* permissions_path

# Service start
* *bundle name:* service_start
## parameters
* service_name
## class result
* service_start_service_name

# Service ensure running
* *bundle name:* service_ensure_running
## parameters
* service_name
## class result
* service_ensure_running_service_name

# Create symlink (force overwrite)
* *bundle name:* file_create_symlink_force
## parameters
* source
* destination
## class result
* file_create_symlink_destination

# Package install version compare
* *bundle name:* package_install_version_cmp
## parameters
* package_name
* version_comparator
* package_version
* action
## class result
* package_install_package_name

