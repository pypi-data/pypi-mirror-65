#!/usr/bin/python3

import os, string

class QEMUException(Exception):
	pass


class QEMUWrapperException(QEMUException):
	pass


qemu_arch_settings = {
	'riscv-64bit': {
		'qemu_binary': 'qemu-riscv64',
		'qemu_cpu': 'sifive-u54',
		'hexstring': [ '7f454c460201010000000000000000000200f3', '7f454c460201010000000000000000000300f3' ]
	},
	'arm-64bit': {
		'qemu_binary': 'qemu-aarch64',
		'qemu_cpu': 'cortex-a53',
		'hexstring': [ '7f454c460201010000000000000000000200b7', '7f454c460201010000000000000000000300b7' ]
	},
	'arm-32bit': {
		'qemu_binary': 'qemu-arm',
		'qemu_cpu': 'cortex-a7',
		'hexstring': [ '7f454c46010101000000000000000000020028', '7f454c46010101000000000000000000030028' ]
	}
}

native_support = {
	'x86-64bit': ['x86-32bit'],
	'x86-32bit': [],
	'arm-64bit': ['arm-32bit'],
	'arm-32bit': []
}


def compile_wrapper(qemu_arch):
	"""
	Compiles a QEMU wrapper using gcc. Will raise QEMUWrapperException if any error is encountered along the way.
	:param qemu_arch: arch to build for -- should be 'arm-64bit' or 'arm-32bit' at the moment.
	:return: None
	"""
	wrapper_code = """#include <string.h>
#include <unistd.h>

int main(int argc, char **argv, char **envp) {{
	char *newargv[argc + 3];

	newargv[0] = argv[0];
	newargv[1] = "-cpu";
	newargv[2] = "{qemu_cpu}";

	memcpy(&newargv[3], &argv[1], sizeof(*argv) * (argc -1));
	newargv[argc + 2] = NULL;
	return execve("/usr/local/bin/{qemu_binary}", newargv, envp);
}}
	"""
	if not os.path.exists(wrapper_storage_path):
		try:
			os.makedirs(wrapper_storage_path)
		except PermissionError:
			raise QEMUWrapperException("Unable to create path to store wrappers: %s" % wrapper_storage_path)
	try:
		with open(os.path.join(wrapper_storage_path, "qemu-%s-wrapper.c" % qemu_arch), "w") as f:
			f.write(wrapper_code.format(**qemu_arch_settings[qemu_arch]))
		retval = os.system("cd {wrapper_path}; gcc -static -O2 -s -o qemu-{qemu_arch}-wrapper qemu-{qemu_arch}-wrapper.c".format(wrapper_path=wrapper_storage_path, qemu_arch=qemu_arch))
		if retval != 0:
			raise QEMUWrapperException("Compilation failed.")
	except (IOError, PermissionError) as e:
		raise QEMUWrapperException(str(e))


# Where our stuff will look for qemu binaries:
qemu_binary_path = "/usr/bin"

# Where our code will try to store our compiled qemu wrappers:
wrapper_storage_path = "/usr/share/fchroot/wrappers"

def native_arch_desc():
	uname_arch = os.uname()[4]
	if uname_arch in ["x86_64", "AMD64"]:
		host_arch = "x86-64bit"
	elif uname_arch in ["x86", "i686", "i386"]:
		host_arch = "x86-32bit"
	else:
		raise QEMUException("Arch of %s not recognized." % uname_arch)
	return host_arch

def qemu_path(arch_desc):
	return os.path.join(qemu_binary_path, qemu_arch_settings[arch_desc]['qemu_binary'].lstrip("/"))

def qemu_exists(arch_desc):
	return os.path.exists(qemu_path(arch_desc))

def wrapper_path(arch_desc):
	return os.path.join(wrapper_storage_path, 'qemu-%s-wrapper' % arch_desc)

def wrapper_exists(arch_desc):
	return os.path.exists(wrapper_path(arch_desc))

def supported_binfmts(native_arch_desc=None):
	if native_arch_desc is None:
		return set(qemu_arch_settings.keys())
	else:
		# TODO: return supported QEMU arch_descs specific to a native arch_desc.
		return set()

def get_arch_of_binary(path):
	hexstring = get_binary_hexstring(path)
	for arch_desc, arch_settings in qemu_arch_settings.items():
		if hexstring in arch_settings['hexstring']:
			return arch_desc
	return None

def get_binary_hexstring(path):
	chunk_as_hexstring = ""
	with open(path, 'rb') as f:
		for x in range(0, 19):
			chunk_as_hexstring += f.read(1).hex()
	return chunk_as_hexstring


def escape_hexstring(hexstring):
	to_process = hexstring
	to_output = ""
	while len(to_process):
		ascii_value = chr(int(to_process[:2], 16))
		to_process = to_process[2:]
		if ascii_value in set(string.printable):
			to_output += ascii_value
		else:
			to_output += "\\x" + "{0:02x}".format(ord(ascii_value))
	return to_output


def is_binfmt_registered(arch_desc):
	return os.path.exists("/proc/sys/fs/binfmt_misc/" + arch_desc)


def register_binfmt(arch_desc, wrapper_bin):
	if not os.path.exists(wrapper_bin):
		raise QEMUWrapperException("Error: wrapper binary %s not found.\n" % wrapper_bin)
	if arch_desc not in qemu_arch_settings:
		raise QEMUWrapperException("Error: arch %s not recognized. Specify one of: %s.\n" % (arch_desc, ", ".join(supported_binfmts())))
	hexcount = 0
	for hexstring in qemu_arch_settings[arch_desc]['hexstring']:
		local_arch_desc = arch_desc if hexcount == 0 else "%s-%s" % ( arch_desc, hexcount )
		if os.path.exists("/proc/sys/fs/binfmt_misc/%s" % local_arch_desc):
			sys.stderr.write("Warning: binary format %s already registered in /proc/sys/fs/binfmt_misc.\n" % local_arch_desc)
		try:
			with open("/proc/sys/fs/binfmt_misc/register", "w") as f:
				chunk_as_hexstring = hexstring
				mask_as_hexstring = "fffffffffffffffcfffffffffffffffffeffff"
				mask = int(mask_as_hexstring, 16)
				chunk = int(chunk_as_hexstring, 16)
				out_as_hexstring = hex(chunk & mask)[2:]
				f.write(":%s:M::" % local_arch_desc)
				f.write(escape_hexstring(out_as_hexstring))
				f.write(":")
				f.write(escape_hexstring(mask_as_hexstring))
				f.write(":/usr/local/bin/%s" % os.path.basename(wrapper_bin))
				f.write(":C\n")
		except (IOError, PermissionError) as e:
			raise QEMUWrapperException("Was unable to write to /proc/sys/fs/binfmt_misc/register.")
		hexcount += 1
# vim: ts=4 sw=4 noet
