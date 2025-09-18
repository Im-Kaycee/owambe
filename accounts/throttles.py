# accounts/throttles.py
from rest_framework.throttling import ScopedRateThrottle

class LoginThrottle(ScopedRateThrottle):
    scope = 'login'

class RegisterThrottle(ScopedRateThrottle):
    scope = 'register'

class ChangePasswordThrottle(ScopedRateThrottle):
    scope = 'change_password'