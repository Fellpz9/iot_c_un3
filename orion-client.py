import requests
import json

class OrionClient:
    def __init__(self, host="localhost", port=1026):
        self.base_url = f"http://{host}:{port}/v2"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def create_entity(self, entity_id, entity_type, attributes):
        """Create a new entity in Orion Context Broker."""
        url = f"{self.base_url}/entities"
        payload = {
            "id": entity_id,
            "type": entity_type,
            **attributes
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.status_code == 201

    def get_entity(self, entity_id, entity_type=None):
        """Retrieve an entity from Orion Context Broker."""
        url = f"{self.base_url}/entities/{entity_id}"
        params = {"type": entity_type} if entity_type else None
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else None

    def update_entity_attributes(self, entity_id, attributes):
        """Update entity attributes in Orion Context Broker."""
        url = f"{self.base_url}/entities/{entity_id}/attrs"
        response = requests.patch(url, headers=self.headers, json=attributes)
        return response.status_code == 204

    def subscribe(self, description, entities, notification_url, attributes=None):
        """Create a subscription in Orion Context Broker."""
        url = f"{self.base_url}/subscriptions"
        payload = {
            "description": description,
            "subject": {
                "entities": entities,
                "condition": {
                    "attrs": attributes if attributes else []
                }
            },
            "notification": {
                "http": {
                    "url": notification_url
                },
                "attrs": attributes if attributes else []
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.status_code == 201

# Example usage
if __name__ == "__main__":
    client = OrionClient()
    
    # Create a temperature sensor entity
    sensor_data = {
        "temperature": {
            "value": 23.4,
            "type": "Float"
        },
        "humidity": {
            "value": 60,
            "type": "Integer"
        }
    }
    
    client.create_entity(
        entity_id="Room1Sensor",
        entity_type="Sensor",
        attributes=sensor_data
    )
    
    # Retrieve the entity
    entity = client.get_entity("Room1Sensor")
    print("Retrieved entity:", json.dumps(entity, indent=2))