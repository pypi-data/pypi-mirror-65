import pika, json  # type: ignore


class Worker:
    def __init__(self, uuid, rabbit_host, callback, args_names):
        self.uuid = uuid
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=uuid)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=uuid, on_message_callback=self.on_request)
        self.callback = callback
        self.args_names = args_names

    def start(self):
        try:
            # Your normal block of code

            print(" [x] En attente de requêtes")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("\nDéconnection")
            self.channel.stop_consuming()

    def on_request(self, ch, method, props, body):
        print(" [x] Processing request")
        list_args = json.loads(body.decode())
        dict_args = {}
        index = 0
        for arg in list_args:
            dict_args[self.args_names[index]] = arg
            index += 1
        try:
            response = json.dumps({"data": self.callback(dict_args), "status": "ok"})

        except Exception as inst:
            print(inst)
            response = json.dumps({"status": "error"})
        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=str(response),
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [X] End of processing")
