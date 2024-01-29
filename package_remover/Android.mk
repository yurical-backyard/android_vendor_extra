# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := package_remover
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_TAGS := optional
LOCAL_UNINSTALLABLE_MODULE := true
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_SRC_FILES := /dev/null
LOCAL_OVERRIDES_PACKAGES += \
	Abstruct \
	F-Droid \
	F-DroidPrivilegedExtension \
	OpenEUICC \
	Ripple \
	Updater
include $(BUILD_PREBUILT)
