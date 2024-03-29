# Chainlink External Adapter as an MQTT Relay

![Lint and unit testing](https://github.com/Briojas/CL-EA-MQTT-Client/workflows/Lint%20and%20unit%20testing/badge.svg)

This template shows basic usecases of a Chainlink external adapter connecting a hybrid smart contract to an MQTT broker for data acquisition, distribution, or processing. It can be ran locally or in Docker.

## **Setup**

1. Download and unzip the repository.
2. Install dependencies:
   ```
   pipenv install
   ```
3. Populate [bridges.json](https://github.com/Briojas/CL-EA-MQTT-Client/blob/master/bridges.json) file with MQTT broker connection info:
   - **'name'**: Label describing the broker bridge
   - **'host'**: Domain name or IP address of the broker
   - **'port'**: Unsecure (e.g. 1883) or secure (e.g. 8883) broker port number
   - **'user'**: Username for logging into private brokers
   - **'key'**: Password for logging into private broker
   - **'env'**: Flags if the 'host', 'user', and 'key' values are .env file variable names
4. Create '.env' file with any private broker data.

   - Be sure the variable names created match those listed in the JSON file:

   ```
   JSON File:
   "host": "PRIVATE_BROKER_DOMAIN"

   .env File:
   PRIVATE_BROKER_DOMAIN = some.broker.domain
   ```

5. Docker:
   - 'build' to update container
   - 'container create' to name and build container
   - 'start' to run container
   ```
   docker build . -t cl-ea-mqtt-relay
   docker container create -it --name cl-ea-mqtt-relay -p 8080:8080 cl-ea-mqtt-relay
   docker start cl-ea-mqtt-relay
   ```
6. Setup the [node bridge](https://docs.chain.link/docs/node-operators/).
   - be sure to set the bridge URL to its docker-container ip (ex: http://172.17.0.X:8080:8080) if hosting adapter on the same machine as the node
7. Create the [node job](https://docs.chain.link/docs/jobs/).
   - See [oracleJobs](https://github.com/Briojas/CL-EA-MQTT-Client/tree/master/oracleJobs) directory for TOML examples utilizing this bridge.
8. Submit [basic requests](https://docs.chain.link/docs/architecture-request-model/) via a hybrid smart contract.

## **Baked-in Actions**

- **Publish** - Posts a payload to the Brokers defined on a topic specified with a quality of service level given.
- **Subscribe** - Gets a payload from the Brokers defined on a topic specified with a quality of service level given
- **Script** - Pulls a file from IPFS at the CID given for more advanced and custom processing specified by the subtask given

### Inputs table:

| action            | topic             | qos                      | payload      | retain          |
| ----------------- | ----------------- | ------------------------ | ------------ | --------------- |
| **publish**[^1]   | address in Broker | quality of service level | data         | store on Broker |
| **subscribe**[^1] | address in Broker | quality of service level | ignored      | ignored         |
| **ipfs**          | subtask specified | ignored                  | IPFS CID[^2] | ignored         |

[^1]: [HiveMQ: MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
[^2]: [IPFS URL with hash](https://docs.ipfs.io/how-to/address-ipfs-on-web/)

## **Development**

### New Actions

- Build new actions by appending new public methods to the end of the [Bridge](https://github.com/Briojas/CL-EA-MQTT-Client/blob/master/bridge.py) class.
- Expand custom functionaliy by adding private methods.

```python
  class Bridge(object):
    ...
    def foo(self, data): #New action named 'foo', callable by a hybrid smart contract

      #access data fed to bridge driectly from the hybrid smart contract
      bar1 = data['topic']
      bar2 = data['qos']
      bar3 = data['payload']
      bar4 = data['retain']

      #utilize exsiting actions
        #publishing to a topic
      pubData = {'topic':'/someTopic/someInteger','qos':0,'payload':12,'retain':True}
      self.publish(pubData)

        #subscribing to, and getting data published on, a topic:
      subData = {'topic':'/otherTopic/specificData','qos':0}
      self.subscribe(subData)
      specificData = self.__get_data_from(subData['topic']) #grab data from subbed topic

        #executing script stored IPFS
      ipfsData = {'topic': 'script', 'payload': 'bafybeidcuj7x347s2ekyicsu2udaime4dzwf7v5qob446pfspx3j765n7m'}
      self.ipfs(ipfsData)

      #utilize new internal functions
      self.__bar_processing(bar1, bar2, bar3, bar4)

    def __bar_processing(self, bar1, bar2, bar3, bar4): #Internal processing function
      #customized processing here
```

### Testing

```
pipenv run pytest
```

### Management

- Installing new packages:

```
pipenv install PYPI-package-name
```

- Locking packages:

```
pipenv lock -r > requirements.txt
```
