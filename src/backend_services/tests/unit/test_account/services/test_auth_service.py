from account.models import AccountModel
from account.services import AuthService


class TestAuthService:
    def test_is_email_used_no(self, auth_service: AuthService):
        result = auth_service.is_email_used("email@email.com")

        assert result is None

    def test_is_email_used_yes(
        self, auth_service: AuthService, test_customer: AccountModel
    ):
        result = auth_service.is_email_used(test_customer.email)

        assert type(result) == AccountModel
