# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

# Build package remover
PRODUCT_PACKAGES += package_remover

# Build adb_root
PRODUCT_PACKAGES += adb_root

# Inherit main Makefile
$(call inherit-product, vendor/extra/configs/main.mk)

# Inherit prebuilts Makefile
$(call inherit-product, vendor/extra/configs/prebuilts.mk)

# Inherit font Makefile
$(call inherit-product, vendor/extra/configs/fonts.mk)

# Inherit overlay Makefile
$(call inherit-product, vendor/extra/configs/overlay.mk)

# Inherit Microsoft Makefile
$(call inherit-product, vendor/aospa/prebuilt/microsoft/packages.mk)

# Inherit Google Makefile
ifeq ($(WITH_GMS),true)
$(call inherit-product, vendor/google/gms/config.mk)
$(call inherit-product, vendor/google/pixel/config.mk)
endif

# Additional SEPolicy
SYSTEM_EXT_PRIVATE_SEPOLICY_DIRS += \
    vendor/extra/sepolicy/private
