# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

# Inherit main Makefile
$(call inherit-product, vendor/extra/configs/main.mk)

# Inherit prebuilts Makefile
$(call inherit-product, vendor/extra/configs/prebuilts.mk)

# Inherit font Makefile
$(call inherit-product, vendor/extra/configs/fonts.mk)

# Inherit Microsoft Makefile
$(call inherit-product, vendor/aospa/prebuilt/microsoft/packages.mk)
