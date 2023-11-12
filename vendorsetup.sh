#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2024 Yurical <yurical1g@gmail.com>

# Override host metadata to make builds more reproducible and avoid leaking info
export BUILD_USERNAME=nobody
export BUILD_HOSTNAME=android-build

# ABI compatibility checks fail for several reasons:
#   - The update to Clang 12 causes some changes, but no breakage has been
#     observed in practice.
#   - Switching to zlib-ng changes some internal structs, but not the public
#     API.
#
# We may fix these eventually by updating the ABI specifications, but it's
# likely not worth the effort for us because of how many repos are affected.
# We would need to fork a lot of extra repos (thus increasing maintenance
# overhead) just to update the ABI specs.
#
# For now, just skip the ABI checks to fix build errors.
export SKIP_ABI_CHECKS=true

# Apply patches
if [[ "${APPLY_PATCH}" == "true" ]]; then
    echo -e "\033[32m[INFO]: Applying patches...\033[0m"
    manifest_branch="$(git -C "$(gettop)"/.repo/manifests branch -r --list 'origin*' | xargs echo -n | sed -e 's/origin\///g')"
    patches_path="$(gettop)"/vendor/extra/patches/"${manifest_branch}"

    if [[ ! -d "${patches_path}" ]]; then
        return 0 2>/dev/null
        builtin exit 0
    fi

    for chain_name in "${patches_path}"/*; do
        chain_name="${chain_name##*/}"
        chain_path="${patches_path}/${chain_name}"

        echo -e "\033[32m[INFO]: Patchset: ${chain_name}...\033[0m"
        for project_name in "${chain_path}"/*; do
            project_name="${project_name##*/}"
            project_path="${project_name}"

            underscores="$(grep -o "_" <<<"${project_path}" | wc -l)"
            slashes=0

            while [[ "${slashes}" -le "${underscores}" ]]; do
                project_path="$(sed 's/_/\//' <<<"${project_path}")"
                if [[ -d "$(gettop)"/"${project_path}" ]]; then
                    echo -e "\033[32m - Path: ${project_path}\033[0m"
                    cd "$(gettop)"/"${project_path}" || exit
                    if ! git -c "apply.whitespace=nowarn" am "${chain_path}"/"${project_name}"/*.patch --quiet --no-gpg-sign; then
                        echo -e "\033[31m[ERROR]: Patch failed!\033[0m"
                        git am --abort &> /dev/null
                        return 1 2>/dev/null
                        builtin exit 1
                    else
                        break 1
                    fi
                else
                    ((slashes++))
                fi

                if [[ "${slashes}" -gt "${underscores}" ]]; then
                    echo -e "\033[31m[ERROR]: No source directory found!\033[0m"
                    return 1 2>/dev/null
                    builtin exit 1
                fi
            done
        done
    done

    # Return to source rootdir
    croot
fi
