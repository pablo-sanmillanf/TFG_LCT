# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x5d\
\x00\
\x00\x04\xe1\x78\x9c\xad\x93\xd1\x6e\x83\x20\x14\x86\xef\x4d\x7c\
\x07\x12\x6f\xb6\x44\x97\xda\xd9\x1a\xf1\x29\x9a\x3d\x01\x08\x2a\
\x99\x05\x87\xb4\x75\x5b\xf6\xee\x3b\x8a\x6e\x36\xa6\xab\x6b\xea\
\x0d\xf2\x03\xff\xe1\x7c\xe7\xb0\x7b\xa9\x04\xe3\x1a\xe3\x42\x2b\
\x75\xe4\xb8\x54\x5a\x7c\x28\x69\x48\x85\x3e\x5d\x87\x2a\xdd\x2d\
\xa2\xb0\x6e\x51\xa3\x60\x27\xf2\x28\xa5\x29\x2c\x90\xec\x15\x4e\
\x1c\x24\xc3\xe8\x54\x0a\xc3\x41\x2b\xb9\x28\x4a\x03\x9b\x57\x75\
\x9b\x8e\x67\x03\x4d\x98\x38\x34\x18\x45\xbd\xf8\xe5\x3a\xae\xb3\
\x1b\x63\x36\x07\x1a\xd4\xa4\x98\x45\x9d\x98\xbf\x55\x42\x72\xa2\
\x8b\xce\x86\x4b\xf3\xd0\x86\x18\xad\x7c\xf4\x6e\x07\xf8\xda\xb5\
\x15\x60\x08\x7d\xd7\xe9\xa4\xc6\xa8\x1a\x44\xe4\x6d\xb7\xdc\x1f\
\x66\x61\x77\xf3\xfc\x31\x5d\xee\xfe\xb4\xf6\x7b\xf3\xf0\x82\x39\
\xd8\x4d\xcc\x37\x1b\x6b\x3e\x07\x16\xc7\xf1\x4d\x70\x08\x63\xd7\
\xe0\x78\x79\x9e\xdf\x37\x68\x49\x24\xab\xfe\x59\x0f\x0b\x6c\xd5\
\xd3\xb2\xb0\xce\x58\x01\x2a\xce\xc7\x3a\x00\xa9\x2c\xcb\xfe\x24\
\x75\x12\xcc\x94\xa0\x3f\xf7\xd7\xdb\x43\x2c\x21\x83\x1e\x73\xb0\
\x9e\x4a\x54\x19\xa3\xf6\x3f\xea\x2d\xc9\xc1\xef\x91\xeb\xbb\xa4\
\x08\x95\xf8\x4d\x91\x31\x76\x21\xc5\x28\x8a\x6e\x7e\x1a\x98\x89\
\x86\xd0\x8a\xb3\x59\x1b\x0c\x6f\xd2\xba\x66\xaa\x52\x10\xd4\x4b\
\x92\x64\x49\x4f\x5d\x76\x85\xaa\x2d\x73\x9d\x73\x5d\xe4\x79\x06\
\x86\x10\xb2\x04\x4c\x67\x58\x43\x16\x42\x16\xb6\x27\x86\xd6\x1e\
\xb5\xb1\x29\x06\x19\x8e\x7e\x03\xcf\x99\x83\x63\
"

qt_resource_name = b"\
\x00\x06\
\x07\xac\x02\xc3\
\x00\x73\
\x00\x74\x00\x79\x00\x6c\x00\x65\x00\x73\
\x00\x06\
\x07\xa2\xfa\xc2\
\x00\x73\
\x00\x6c\x00\x69\x00\x64\x00\x65\x00\x72\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x12\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x12\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x87\x52\x79\xde\x54\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
