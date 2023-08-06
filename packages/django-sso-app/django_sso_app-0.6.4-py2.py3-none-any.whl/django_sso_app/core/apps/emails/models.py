from allauth.account.models import EmailAddress as _EmailAddress


class EmailAddress(_EmailAddress):
    class Meta:
        proxy = True
