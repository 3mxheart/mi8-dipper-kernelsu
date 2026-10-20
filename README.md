# Mi 8 (dipper) KernelSU

适配小米 8 官方 MIUI V12.5.2.0.QEACNXM（Android 10）的非 GKI 内核。

## 当前版本

- Linux 4.9.186，KernelSU v0.9.5 / 11872。
- WLAN 与音频驱动内建，避免与原厂 vendor 模块的 ABI 不匹配。
- 已在一台 dipper 上临时启动、刷入 boot 并重启验证。
- Wi-Fi 开启并连接正常；用户确认 KernelSU 显示“工作中”、扬声器有声。
- 第三方应用 root 授权、KernelSU 模块及其他硬件功能尚未逐项验证。
- 本次源码中的 embed_ksud.c 为上游归档 stub（ksud_size=0），不能将管理器“工作中”视为模块系统已验证。

## 下载与使用

从 Releases 下载 `ksu-boot.img`、管理器 APK 和 `SHA256SUMS.txt`。
仅在匹配系统且已解锁 bootloader 的 dipper 使用；先自行备份 boot。

```sh
fastboot boot ksu-boot.img
# 确认自己的设备各项功能正常后：
fastboot flash boot ksu-boot.img
fastboot reboot
```

回退时刷回自己设备的原始 boot 备份。

镜像 SHA256：
`91E6A79249875E6185459F518821530257483EBF78A551F160114BECE36AF225`

## 对应源码与构建

Release 附带 `kernel-source.tar.gz`，包含本次构建的修改后源码与 `.config`；`source-manifest.json` 列出归档源文件。
源码保留各文件的许可证声明，内核许可见 COPYING。

来源：
- [MiCode dipper-q-oss](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/tree/dipper-q-oss)，基线提交 `dcfb1676925aec83b06ae04fd8ca989ced75067c`。
- [LineageOS sdm845 lineage-17.0](https://github.com/LineageOS/android_kernel_xiaomi_sdm845/tree/lineage-17.0)：qcacld-3.0、qca-wifi-host-cmn、fw-api、techpack/audio；下载时分支 HEAD 为 `94cd5896ddd5dbbf76f5976dd6ff8db6f5e74712`。
- [KernelSU v0.9.5](https://github.com/tiann/KernelSU/tree/v0.9.5)。

本次环境：Windows、MSYS2、GNU Make 4.2.1、Android NDK r21e Clang 9、MSYS GCC host tools。
`build-ksu-wlan-full.sh` 和 `clang-kernel` 保留实际构建参数。脚本中的 `/m` 是本地工作区映射，复现时需按环境调整路径并提供相同工具链；脚本输出目录 `artifacts/build` 须预先创建。Linux 环境的独立复现未验证。

主要变更：集成 KSU、WLAN、音频；处理 Windows 头文件路径和符号链接；WLAN 链接使用 response file；移除迁到 techpack 的旧音频构建目标。完整修改已包含在源码附件。

构建输出为 `arch/arm64/boot/Image.gz-dtb`。使用 `pack_boot.py` 将它与匹配 MIUI 的原始 boot 头和 ramdisk 打包：

```sh
python pack_boot.py boot-original.img kernel-dipper/arch/arm64/boot/Image.gz-dtb ksu-boot.img
```

发布镜像使用上述已验证系统的 boot 头和 ramdisk。源码归档不含工具链、手机日志或个人备份。
