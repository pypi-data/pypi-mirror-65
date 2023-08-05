# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
from nwae.utils.sec.AccessToken import AccessTokenSharedsecretChallenge, generate_random_string


class Authenticate:
    
    @staticmethod
    def generate_challenge_string(n):
        return generate_random_string(n=n)

    def __init__(
            self,
            shared_secret,
            challenge,
            test_challenge
    ):
        self.shared_secret = shared_secret
        self.challenge = challenge
        self.test_challenge = test_challenge
        return

    def verify_totp_otp(
            self
    ):
        return AccessTokenSharedsecretChallenge(
            shared_secret  = self.shared_secret,
            challenge      = self.challenge,
            test_challenge = self.test_challenge
        ).verify_totp_otp()

    def verify_totp_style(
            self,
            tolerance_secs = 10
    ):
        return AccessTokenSharedsecretChallenge(
            shared_secret  = self.shared_secret,
            challenge      = self.challenge,
            test_challenge = self.test_challenge
        ).verify_totp_style(
            tolerance_secs = 10
        )
    
    def verify(
            self
    ):
        return AccessTokenSharedsecretChallenge(
            shared_secret  = self.shared_secret,
            challenge      = self.challenge,
            test_challenge = self.test_challenge
        ).verify()
