FILESEXTRAPATHS_append := ":${THISDIR}/${PN}"
KERNEL_CONFIG_FRAGMENTS_append += "${WORKDIR}/fragments/5.10/fragment-ext4-fs-security.config"
SRC_URI_append = " file://5.10/fragment-ext4-fs-security.config;subdir=fragments "
