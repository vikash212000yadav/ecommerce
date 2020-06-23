
"""
from .models import DeliveryInfo


class DeliveryInfoService:

    @staticmethod
    def delete_by_user(user):
        try:
            user.deliveryinfo.delete()
            return True
        except DeliveryInfo.DoesNotExist:
            return False

"""