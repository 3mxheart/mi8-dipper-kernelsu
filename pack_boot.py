import hashlib
import struct
import sys
from pathlib import Path


def align(value: int, page: int) -> int:
    return (value + page - 1) // page * page


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: pack_boot.py <original-boot> <new-kernel> <output>")

    source = Path(sys.argv[1])
    kernel_path = Path(sys.argv[2])
    output = Path(sys.argv[3])

    original = source.read_bytes()
    if original[:8] != b"ANDROID!":
        raise SystemExit("not an Android boot image")

    kernel_size = struct.unpack_from("<I", original, 8)[0]
    ramdisk_size = struct.unpack_from("<I", original, 16)[0]
    second_size = struct.unpack_from("<I", original, 24)[0]
    page_size = struct.unpack_from("<I", original, 36)[0]
    header_version = struct.unpack_from("<I", original, 40)[0]

    if header_version not in (0, 1):
        raise SystemExit(f"unsupported header version: {header_version}")

    kernel_offset = page_size
    ramdisk_offset = kernel_offset + align(kernel_size, page_size)
    second_offset = ramdisk_offset + align(ramdisk_size, page_size)

    ramdisk = original[ramdisk_offset:ramdisk_offset + ramdisk_size]
    second = original[second_offset:second_offset + second_size]
    if len(ramdisk) != ramdisk_size or len(second) != second_size:
        raise SystemExit("truncated original boot image")

    kernel = kernel_path.read_bytes()
    if not kernel:
        raise SystemExit("new kernel is empty")

    header = bytearray(original[:page_size])
    struct.pack_into("<I", header, 8, len(kernel))
    struct.pack_into("<I", header, 16, len(ramdisk))
    struct.pack_into("<I", header, 24, len(second))

    # AOSP boot image ID is SHA1 over payloads and their 32-bit sizes.
    digest = hashlib.sha1()
    for payload in (kernel, ramdisk, second):
        digest.update(payload)
        digest.update(struct.pack("<I", len(payload)))
    header[576:608] = digest.digest() + b"\x00" * (32 - digest.digest_size)

    packed = bytearray()
    packed.extend(header)
    for payload in (kernel, ramdisk, second):
        packed.extend(payload)
        packed.extend(b"\x00" * (align(len(payload), page_size) - len(payload)))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(packed)
    print(
        f"kernel={len(kernel)} ramdisk={len(ramdisk)} second={len(second)} "
        f"image={len(packed)} sha1={digest.hexdigest()}"
    )


if __name__ == "__main__":
    main()
