from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError


class PubSubPublisher:
    def __init__(self, project_id, topic_id):
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_message(self, message):
        # Message data must be a bytestring
        message_data = message.encode("utf-8")

        # Publishes a message
        try:
            # When you publish a message, the client returns a future.
            future = self.publisher.publish(self.topic_path, data=message_data)
            return future.result()  # Returns the message ID after publishing
        except GoogleAPICallError as e:
            print(f"An exception occurred when publishing to the topic: {e}")
            raise
