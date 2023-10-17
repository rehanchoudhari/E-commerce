

def get_listing_image(instance, filename):
    return 'user_{0}/listing/{1}'.format(instance.seller.user.id, filename)