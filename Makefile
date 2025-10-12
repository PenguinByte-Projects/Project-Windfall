all:
	make -C linux -j$(nproc)
	cp linux/arch/x86/boot/bzImage iso/boot
	as --32 test.S -o test.o
	ld -m elf_i386 test.o -o test
	rm iso/boot/initramfs.cpio.zstd
	echo test | cpio -o --format=newc | zstd -3 -o iso/boot/initramfs.cpio.zstd
	grub-mkrescue -o windfall.iso iso

run:
	qemu-system-i386 -cdrom windfall.iso
