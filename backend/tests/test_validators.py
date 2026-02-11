from app.utils.validators import validate_imei, validate_cnic, validate_mobile, validate_password, validate_username


class TestIMEIValidation:
    def test_valid_imei(self):
        assert validate_imei("490154203237518") is True

    def test_valid_imei_2(self):
        assert validate_imei("356938035643809") is True

    def test_invalid_imei_wrong_checksum(self):
        assert validate_imei("490154203237519") is False

    def test_invalid_imei_too_short(self):
        assert validate_imei("49015420323") is False

    def test_invalid_imei_too_long(self):
        assert validate_imei("4901542032375189") is False

    def test_invalid_imei_letters(self):
        assert validate_imei("49015420323751a") is False

    def test_invalid_imei_empty(self):
        assert validate_imei("") is False


class TestCNICValidation:
    def test_valid_cnic(self):
        assert validate_cnic("12345-6789012-3") is True

    def test_invalid_cnic_no_dashes(self):
        assert validate_cnic("1234567890123") is False

    def test_invalid_cnic_wrong_format(self):
        assert validate_cnic("1234-56789012-3") is False

    def test_invalid_cnic_empty(self):
        assert validate_cnic("") is False


class TestMobileValidation:
    def test_valid_mobile(self):
        assert validate_mobile("03001234567") is True

    def test_valid_mobile_03xx(self):
        assert validate_mobile("03111234567") is True

    def test_invalid_mobile_no_03(self):
        assert validate_mobile("04001234567") is False

    def test_invalid_mobile_too_short(self):
        assert validate_mobile("0300123456") is False

    def test_invalid_mobile_too_long(self):
        assert validate_mobile("030012345678") is False


class TestPasswordValidation:
    def test_valid_password(self):
        assert validate_password("TestPass123") is None

    def test_too_short(self):
        assert validate_password("Abc1") is not None

    def test_no_uppercase(self):
        assert validate_password("testpass123") is not None

    def test_no_lowercase(self):
        assert validate_password("TESTPASS123") is not None

    def test_no_digit(self):
        assert validate_password("TestPassWord") is not None


class TestUsernameValidation:
    def test_valid_username(self):
        assert validate_username("testuser") is None

    def test_too_short(self):
        assert validate_username("ab") is not None

    def test_special_chars(self):
        assert validate_username("test@user") is not None

    def test_underscores_ok(self):
        assert validate_username("test_user") is None
