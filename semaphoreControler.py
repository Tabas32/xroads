import paho.mqtt.client as mqtt


def setUpMqtt():
    broker_address = "192.168.100.151"
    #
    client = mqtt.Client("dmytro_broker")  # name of broker
    client.connect(broker_address)  # ip adress broker

    return client


previousResult = None


def sendComand(client, status):
    result = status.index(max(status))
    if result is not previousResult:
        if result == 0:
            client.publish("semaphore", "[1, 0, 0, 0]")
        elif result == 1:
            client.publish("semaphore", "[0, 1, 0, 0]")  # send to semaphore
        elif result == 2:
            client.publish("semaphore", "[0, 0, 1, 0]")  # send to semaphore
        elif result == 3:
            client.publish("semaphore", "[0, 0, 0, 1]")  # send to semaphore
        else:
            result = -1
    return result
