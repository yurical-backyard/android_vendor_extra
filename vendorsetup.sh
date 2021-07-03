#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

# Override host metadata to make builds more reproducible and avoid leaking info
export BUILD_HOSTNAME=android-build
export BUILD_USERNAME=android-build
