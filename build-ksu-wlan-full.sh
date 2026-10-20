#!/bin/bash
cd /m/kernel-dipper
export PATH=/m/tools/bin:/m/tools/ndk/android-ndk-r21e/toolchains/llvm/prebuilt/windows-x86_64/bin:/mingw64/bin:$PATH
export LC_ALL=C
/m/tools/make421/bin/make -j16 ARCH=arm64 CC=/m/tools/bin/clang-kernel CLANG_TRIPLE=aarch64-linux-gnu CROSS_COMPILE=aarch64-linux-android- GCC_TOOLCHAIN_DIR= GCC_TOOLCHAIN= HOSTCFLAGS=-fcommon LD=aarch64-linux-android-ld AR=aarch64-linux-android-ar NM=aarch64-linux-android-nm OBJCOPY=aarch64-linux-android-objcopy OBJDUMP=aarch64-linux-android-objdump STRIP=aarch64-linux-android-strip HOSTCC=/usr/bin/gcc HOSTCXX=/usr/bin/g++ HOSTLD=/usr/bin/ld Image.gz-dtb > /m/artifacts/build/ksu-wlan-full-build.log 2>&1
echo "$?" > /m/artifacts/build/ksu-wlan-full.exit
