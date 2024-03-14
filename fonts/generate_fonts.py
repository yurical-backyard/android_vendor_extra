#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project

import os
import shutil

OVERLAY_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/overlays"
FONT_FILES_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/font_files"
METADATA_ALIASES = ['', 'thin', 'light', 'medium', 'black']

# "<user-facing name>": { "family": "<font family name>", "translations": { "<language code>": "<localized user-facing name" } },
# Language code: See https://developer.android.com/guide/topics/resources/providing-resources#AlternativeResources
# Example: "Noto Sans": { "family": "noto-sans", "translations": { "ko": "본고딕" } },
FONTS = {
    "Apple SD Gothic Neo": { "family": "apple-sd-gothic-neo", "translations": { "ko": "Apple SD 산돌고딕 Neo" } },
    "Google Sans": { "family": "google-sans", "body-postfix": "-text" },
    "Inter": { "family": "inter", "body-postfix": "-text" },
    "Nanum Square Neo": { "family": "nanum-square-neo", "translations": { "ko": "나눔스퀘어 네오" } },
    "Wanted Sans": { "family": "wanted-sans" },
}

# Android.bp license
ANDROID_BP_LICENSE_TEMPLATE = """/*
 * SPDX-License-Identifier: Apache-2.0
 * SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project
 */

"""

# Android.bp RRO
ANDROID_BP_RRO_TEMPLATE = """runtime_resource_overlay {{
    name: "FontExtra{apk_name}Overlay",
    theme: "FontExtra{apk_name}",
    product_specific: true,
{required_string}
    overrides: [
        "fonts_customization.xml",
        "FontLatoOverlay",
        "FontRubikOverlay",
        "FontGoogleSansOverlay",
        "FontHarmonySansOverlay",
        "FontInterOverlay",
        "FontManropeOverlay",
        "FontUrbanistOverlay",
    ],
}}
"""

# Android.bp font files
ANDROID_BP_FONT_FILES_TEMPLATE = """prebuilt_font {{
    name: "{font_file}",
    src: "{font_file}",
    product_specific: {product_specific},
}}
"""

# AndroidManifest.xml
ANDROID_MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!--
     SPDX-License-Identifier: Apache-2.0
     SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project
-->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.android.theme.font.{pkg_name}">

    <overlay
        android:targetPackage="android"
        android:category="android.theme.customization.font"
        android:priority="1" />

    <application
        android:label="@string/font_{pkg_name}_overlay"
        android:hasCode="false">
        <meta-data
            android:name="android.theme.customization.REQUIRED_SYSTEM_FONTS"
            android:value="{metadata_string}" />
    </application>

</manifest>
"""

# config.xml
CONFIG_XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!--
     SPDX-License-Identifier: Apache-2.0
     SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project
-->
<resources>

    <!-- Name of a font family to use for body text. -->
    <string name="config_bodyFontFamily" translatable="false">{font_name_body}</string>

    <!-- Name of a font family to use for medium body text. -->
    <string name="config_bodyFontFamilyMedium" translatable="false">{font_name_body}-medium</string>

    <!-- Name of a font family to use for headlines. If empty, falls back to platform default -->
    <string name="config_headlineFontFamily" translatable="false">{font_name}</string>

    <!-- Name of the font family used for system surfaces where the font should use medium weight -->
    <string name="config_headlineFontFamilyMedium" translatable="false">{font_name}-medium</string>

    <!-- Name of a font family to use as light font. For theming purpose. This is an additional change. -->
    <string name="config_lightFontFamily" translatable="false">{font_name}-light</string>

    <!-- Name of a font family to use as regular font. For theming purpose. This is an additional change. -->
    <string name="config_regularFontFamily" translatable="false">@string/config_bodyFontFamily</string>

</resources>
"""

# strings.xml
STRINGS_XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!--
     SPDX-License-Identifier: Apache-2.0
     SPDX-FileCopyrightText: Copyright 2021 The Proton AOSP Project
-->
<resources>

    <string name="font_{pkg_name}_overlay">{user_name}</string>

</resources>
"""

def main():
    for user_name, font_dict in FONTS.items():
        font_dir=f"{FONT_FILES_DIR}/{font_dict.get('family')}"

        required_string = []
        if(os.path.isdir(font_dir)):
            required_string.append("    required: [")

            with open(f"{font_dir}/Android.bp", "w+") as f:
                f.write(ANDROID_BP_LICENSE_TEMPLATE)

            for file in os.listdir(font_dir):
                if file.endswith(".otf") or file.endswith(".ttf"):
                    print(file)
                    product_specific = "true" if os.path.isfile(f"{font_dir}/product.flag") else "false"
                    required_string.append(f"        \"{file}\",")

                    with open(f"{font_dir}/Android.bp", "a") as f:
                        f.write(ANDROID_BP_FONT_FILES_TEMPLATE.format(font_file=file, product_specific=product_specific))

            required_string.append("    ],")

        pkg_apk_name = user_name.replace(" ", "").replace("+", "Plus")
        pkg_name = user_name.lower().replace(" ", "_").replace("+", "plus_")
        apk_name = f"FontExtra{pkg_apk_name}Overlay"
        pkg_dir = f"{OVERLAY_DIR}/{apk_name}"
        font_family = font_dict.get('family')

        print(apk_name)
        shutil.rmtree(pkg_dir, ignore_errors=True)

        xml_dir = f"{pkg_dir}/res/values"
        os.makedirs(xml_dir, exist_ok=True)

        with open(f"{xml_dir}/config.xml", "w+") as f:
            f.write(CONFIG_XML_TEMPLATE.format(font_name=font_family, font_name_body=f"{font_family}{font_dict.get('body-postfix', '')}"))

        with open(f"{xml_dir}/strings.xml", "w+") as f:
            f.write(STRINGS_XML_TEMPLATE.format(pkg_name=pkg_name, user_name=user_name))

        if (font_dict.get('translations')):
            for lang_name, font_name in font_dict.get('translations').items():
                translation_dir = f"{pkg_dir}/res/values-{lang_name}"
                os.makedirs(translation_dir, exist_ok=True)
                with open(f"{translation_dir}/strings.xml", "w+") as f:
                    f.write(STRINGS_XML_TEMPLATE.format(pkg_name=pkg_name, user_name=font_name))

        with open(f"{pkg_dir}/Android.bp", "w+") as f:
            f.write(ANDROID_BP_LICENSE_TEMPLATE)
            f.write(ANDROID_BP_RRO_TEMPLATE.format(apk_name=pkg_apk_name, required_string="\n".join(required_string)))

        metadata_string = ','.join([font_family if alias == '' else f"{font_family}-{alias}" for alias in METADATA_ALIASES])
        if font_dict.get('body-postfix'):
            font_family += font_dict.get('body-postfix')
            metadata_string += ',' + ','.join([font_family if alias == '' else f"{font_family}-{alias}" for alias in METADATA_ALIASES])
        with open(f"{pkg_dir}/AndroidManifest.xml", "w+") as f:
            f.write(ANDROID_MANIFEST_TEMPLATE.format(pkg_name=pkg_name, metadata_string=metadata_string))

if __name__ == '__main__':
    main()
