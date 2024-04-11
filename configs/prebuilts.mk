# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

# Auxio
PRODUCT_PACKAGES += \
    Auxio

# Material Files
PRODUCT_PACKAGES += \
    MaterialFiles

# Next Player
PRODUCT_PACKAGES += \
    NextPlayer

ifeq ($(TARGET_PRODUCT), aospa_asphalt)
ifeq ($(PRIVATE_BUILD), true)
BOARD_PREBUILT_DTBIMAGE_DIR := device/lenovo/asphalt-kernel/dtbs-private
endif
endif
