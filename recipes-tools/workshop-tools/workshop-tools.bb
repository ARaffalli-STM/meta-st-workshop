DESCRIPTION = "Additional scripts for the workshop"
SECTION = "extras"
LICENSE = "CLOSED"
PR = "1.0"

FILESEXTRAPATHS_append := "${THISDIR}/${PN}"

SRC_URI += "file://read_sensor.sh"
SRC_URI += "file://51-wireless.network"
SRC_URI += "file://wpa_supplicant/*"

FILES_${PN} += "/home/root/read_sensor.sh"
FILES_${PN} += "/lib/systemd/network/51-wireless.network"
FILES_${PN} += "/etc/wpa_supplicant/*"

do_compile() {
}

do_install() {
	install -d ${D}/home/root/ 
	install -d ${D}/lib/systemd/network/ 
	install -m 0755 ${WORKDIR}/read_sensor.sh ${D}/home/root/read_sensor.sh
	install -m 0755 ${WORKDIR}/51-wireless.network ${D}/lib/systemd/network/51-wireless.network
	install -d ${D}/etc/wpa_supplicant/
	install -m 0644 ${WORKDIR}/wpa_supplicant/* ${D}/etc/wpa_supplicant/
}

RDEPENDS_${PN} = "bash"
