FILESEXTRAPATHS_append := ":${THISDIR}/${PN}"
KERNEL_CONFIG_FRAGMENTS_append += "${WORKDIR}/fragments/5.10/fragment-ext4-fs-security.config"
SRC_URI_append = " file://5.10/fragment-ext4-fs-security.config;subdir=fragments "
KERNEL_CONFIG_FRAGMENTS_append += "${WORKDIR}/fragments/5.10/fragment-add-sensors-iks01a3.config"
SRC_URI_append = " file://5.10/fragment-add-sensors-iks01a3.config;subdir=fragments "

SRC_URI += " file://5.10/5.10.10/add-sensors-iks01a3.patch "
