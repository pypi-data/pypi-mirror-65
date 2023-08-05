#!/bin/sh
# Finding ID:	RHEL-07-020640
# Version:	RHEL-07-020640_rule
# SRG ID:	SRG-OS-000480-GPOS-00227
# Finding Level:	medium
# 
# Rule Summary:
#	All local interactive user home directories defined in the
#	/etc/passwd file must exist.
#
# CCI-000366 
#    NIST SP 800-53 :: CM-6 b 
#    NIST SP 800-53A :: CM-6.1 (iv) 
#    NIST SP 800-53 Revision 4 :: CM-6 b 
#
#################################################################
# Standard outputter function
diag_out() {
   echo "${1}"
}

diag_out "----------------------------------------"
diag_out "STIG Finding ID: RHEL-07-020640"
diag_out "   All local interactive user home"
diag_out "   directories defined in the"
diag_out "   /etc/passwd file must exist."
diag_out "----------------------------------------"
