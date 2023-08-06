class Notification(object):
    def __init__(self, message, publisher=None):
        self.message = message
        self.publisher = publisher


class Provider(object):
    def __init__(self):
        self.subscription = {}

    def subscribe(self, message, subscriber):
        self.subscription.setdefault(message, []).append(subscriber)

    def unsubscribe(self, message, subscriber):
        self.subscription[message].remove(subscriber)

    def notify(self, notification):
        for subscriber in self.subscription.setdefault(notification.message, []):
            subscriber.update(notification)

    def notify_by_queue(self, queue):
        for notification in queue:
            self.notify(notification)


class Subscriber(object):
    def update(self, notification):
        raise NotImplemented


class AdvancedSubscriber(Subscriber):
    def __init__(self, provider):
        self.provider = provider

    def update(self, notification):
        raise NotImplemented

    def subscribe(self, message):
        self.provider.subscribe(message, self)

    def unsubscribe(self, message):
        self.provider.unsubscribe(message, self)