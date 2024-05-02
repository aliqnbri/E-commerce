import redis
from django.conf import settings


def redis_client():
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                               password=settings.REDIS_PASS, decode_responses=True)
    return redis_client





# class OTPSingleton:
#     _instance = None
#     _redis_client = None

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
#                                password=settings.REDIS_PASS, db=settings.REDIS_DB, decode_responses=True)
#         return cls._instance

#     def generate_otp(self, email):
#         otp = ''.join(random.choices('0123456789', k=6))
#         self._redis_client.setex(email, time=300, value=otp)
#         return otp

#     def validate_otp(self, email, user_input_otp):
#         stored_otp = self._redis_client.get(email)
#         if stored_otp is None:
# #             return False
#         else:
#             correct_otp = stored_otp.decode('utf-8')
#             self._redis_client.delete(email)
#             return user_input_otp == correct_otp

# # Usage example:
# otp_singleton = OTPSingleton()
# email = '+1234567890'
# otp = otp_singleton.generate_otp(email)

# # Validate the OTP
# is_valid = otp_singleton.validate_otp(email, '123456')
# print(is_valid)