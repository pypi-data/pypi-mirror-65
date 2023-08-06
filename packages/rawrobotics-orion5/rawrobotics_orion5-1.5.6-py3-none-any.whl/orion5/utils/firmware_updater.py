import serial
import struct
import time


OLD_BYTE = 0x69
NEW_BYTE = 0x22


def get_firmware_file(filename, byte):
    BLOCK_SIZE = 524
    blocks = []

    if byte == OLD_BYTE:
        bootloader_version = 1
    elif byte == NEW_BYTE:
        bootloader_version = 3

    filename = filename.replace('*', '{:02d}'.format(bootloader_version))

    # read blocks from file
    with open(filename, "rb") as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if len(block) != BLOCK_SIZE:
                break
            blocks.append(block)

    # 16 bit number indicating how many blocks to expect
    num_blocks = len(blocks)

    # 32 bit firmware version number
    version_number = int(filename.split('_')[-2])
    print(filename, version_number)

    return blocks, num_blocks, version_number


def signal_update(s, callback=None):
    s.write(bytes([240, 240, 66, 3, 13, 1, 0, 177, 251]))
    s.close()
    if callback is not None:
        callback('Waiting for Orion5 reboot', 0, 0)


def update(s=None, filename='', callback=None, output=False):
    # state 0 - waiting for micro to send 'ready packet'
    # state 1 - wait for micro to request blocks
    state = 0

    if callback is not None:
        callback('Hold middle button for 2s', 0, 100)

    while True:
        if state == 0:
            # wait for ready packet
            if s.in_waiting > 0:
                byte = struct.unpack('B', s.read(1))[0]

                if byte == NEW_BYTE:
                    s.write(struct.pack('B', NEW_BYTE))
                    time.sleep(0.1)
                    while s.in_waiting > 0:
                        s.read(1)

                if byte == OLD_BYTE or byte == NEW_BYTE:
                    if output:
                        print("Ready packet recieved")

                    blocks, num_blocks, version_number = get_firmware_file(filename, byte)

                    # write 32 bit version number
                    for i in range(4):
                        s.write(struct.pack('B', (version_number >> (i*8)) & 0xFF))
                    # write 16 bit number of blocks value
                    s.write(struct.pack('B', (num_blocks & 0xFF)))
                    s.write(struct.pack('B', (num_blocks & 0xFF00) >> 8))
                    state = 1
                    if callback is not None:
                        callback('Release middle button', 0, num_blocks)

        elif state == 1:
            # wait for request packet
            if s.in_waiting >= 2:
                # packet indicates which block index was requested
                block_index = ((struct.unpack('B', s.read(1))[0] & 0xFF) << 8)
                block_index |= (struct.unpack('B', s.read(1))[0] & 0xFF)

                # check if finish flag recieved or error in block index
                if (block_index == 0xFFFF):
                    if output:
                        print("Finish flag recieved")
                    break
                elif (block_index < 0 or block_index > num_blocks-1):
                    if output:
                        print("Request index error")
                    break

                # send the appropriate block with index as header
                s.write(struct.pack('B', (block_index & 0xFF)) + struct.pack('B', (block_index & 0xFF00) << 8) + blocks[block_index])

                if callback is not None:
                    callback('Writing firmware...', block_index+1, num_blocks)
                if output:
                    print(block_index, '-', str(int((block_index+1)*100/float(num_blocks))) + '%')

    if callback is not None:
        callback('Done', num_blocks, num_blocks)
    if output:
        print("Finished")

    s.close()
