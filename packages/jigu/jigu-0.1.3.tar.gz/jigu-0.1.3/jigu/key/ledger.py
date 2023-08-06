try:
    import hid
    from btchip.btchipComm import HIDDongleHIDAPI, DongleWait
    from btchip.btchip import btchip
    from btchip.btchipUtils import (
        compress_public_key,
        format_transaction,
        get_regular_input_script,
        get_p2sh_input_script,
    )
    from btchip.bitcoinTransaction import bitcoinTransaction
    from btchip.btchipFirmwareWizard import checkFirmware, updateFirmware
    from btchip.btchipException import BTChipException

    BTCHIP = True
    BTCHIP_DEBUG = False
except ImportError:
    BTCHIP = False

from jigu.key import LUNA_COIN_TYPE, Key, derive_child, derive_root


class LedgerClient:

    BNC_CLA = 0xBC
    BNC_INS_GET_VERSION = 0x00
    BNC_INS_PUBLIC_KEY_SECP256K1 = 0x01
    BNC_INS_SIGN_SECP256K1 = 0x02
    BNC_INS_SHOW_ADDR_SECP256K1 = 0x03
    BNC_INS_GET_ADDR_SECP256K1 = 0x04
    SUCCESS_CODE = 0x9000

    CHUNK_SIZE = 250

    def __init__(self, dongle):
        self._dongle = dongle

    def get_btchip_device(self, device):
        ledger = False
        if device.product_key[0] == 0x2581 and device.product_key[1] == 0x3B7C:
            ledger = True
        if device.product_key[0] == 0x2581 and device.product_key[1] == 0x4B7C:
            ledger = True
        if device.product_key[0] == 0x2C97:
            if device.interface_number == 0 or device.usage_page == 0xFFA0:
                ledger = True
            else:
                return None  # non-compatible interface of a Nano S or Blue
        dev = hid.device()
        dev.open_path(device.path)
        dev.set_nonblocking(True)
        return HIDDongleHIDAPI(dev, ledger, BTCHIP_DEBUG)

    def _parse_hd_path(self, path):
        if len(path) == 0:
            return bytearray([0])
        result = []
        elements = path.split("/")
        if len(elements) > 10:
            raise BTChipException("Path too long")
        for pathElement in elements:
            element = re.split("'|h|H", pathElement)
            if len(element) == 1:
                writeUint32LE(int(element[0]), result)
            else:
                writeUint32LE(0x80000000 | int(element[0]), result)
        return bytearray([len(elements)] + result)

    def get_public_key(self) -> str:
        """Gets the public key from the Ledger app that is currently open on the device.
        .. code:: python
            public_key = client.get_public_key()
        :return: API Response
        .. code:: python
            '<public_key>'
        """
        dongle_path = self._parse_hd_path("44'/330'/0'/0/0")
        apdu = [
            self.BNC_CLA,
            self.BNC_INS_PUBLIC_KEY_SECP256K1,
            0x00,
            0x00,
            len(dongle_path),
        ]
        apdu.extend(dongle_path)
        response = self._exchange(apdu)

        return response[0 : 1 + 64]


a = LedgerClient(getDongle(debug=True))
a.get_public_key()
