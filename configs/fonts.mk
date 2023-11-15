# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project

# fonts_customization.xml
PRODUCT_COPY_FILES += \
	vendor/extra/fonts/fonts_customization.xml:$(TARGET_COPY_OUT_PRODUCT)/etc/fonts_customization.xml

# Overlays for UI font styles
PRODUCT_PACKAGES += \
	FontExtraNanumSquareNeoOverlay
