# Dreamcast Toolchains
Containers are built daily

## Containers
- `ghcr.io/cepawiel/toolchain-raw`

  Unpatched SH4+ARM Toolchain, useful for building Baremetal or Libronin Projects

- `ghcr.io/cepawiel/toolchain-kos`

  KOS Patched SH4+ARM Toolchain Only, useful when modifying KOS

- `ghcr.io/cepawiel/dreamcast-kos`

  KOS Patched SH4+ARM Toolchain with KOS, useful when modifying KOS-Ports

- `ghcr.io/cepawiel/dreamcast-ports-kos`

  KOS Patched SH4+ARM Toolchain with KOS & KOS-Ports, useful for building against a stock KOS+Ports install

## TODO:
- Build Multi-Arch Images (ARM)
- Provide Example Usage
- Build Raw Toolchains Less Often
- Add Build System for Local Usage
