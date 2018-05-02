
# Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
#
# Copyright (C) 2016-2017 Deep Cognition Labs, Skiva Technologies Inc.
#
# All rights reserved.

from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import (ProviderAccount,
                                                  AuthAction)
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.app_settings import QUERY_EMAIL

class Scope(object):
    EMAIL = 'email'
    PROFILE = 'profile'

class DeepCognitionAccount(ProviderAccount):

    def get_avatar_url(self):
        return self.account.extra_data.get('avatar_url')

    def to_str(self):
        dflt = super(DeepCognitionAccount, self).to_str()
        return self.account.extra_data.get('user_login', dflt)


class DeepCognitionProvider(OAuth2Provider):
    id = 'deepcognition'
    name = 'DeepCognition'
    account_class = DeepCognitionAccount

    def get_default_scope(self):
        scope = [Scope.PROFILE]
        if QUERY_EMAIL:
            scope.append(Scope.EMAIL)
        return scope

    def extract_uid(self, data):
        return str(data['ID'])

    def extract_common_fields(self, data):
        return dict(username=data.get('user_login'),
                    first_name=data.get('display_name'),
                    email=data.get('email'))

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('email')
        if email and data.get('active'):
            ret.append(EmailAddress(email=email,
                       verified=True,
                       primary=True))
        return ret


providers.registry.register(DeepCognitionProvider)