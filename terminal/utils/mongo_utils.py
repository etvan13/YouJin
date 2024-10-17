# utils/mongo_utils.py

from pymongo import MongoClient
import os

class MongoDBClient:
    def __init__(self, uri=None, db_name='chatbot_db'):
        """
        Initializes the MongoDB client, connecting to the specified URI and database.
        """
        # Use the provided URI or default to localhost
        self.uri = uri or 'mongodb://localhost:27017/'
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]
        self.collection = self.db['conversation_blocks']
    
    def insert_conversation_block(self, coordinate, block, universe=0, additional_data=None):
        """
        Inserts a conversation block at the specified coordinate, with an optional universe and additional data.
        """
        document = self.collection.find_one({'coordinate': coordinate})
        new_block = {'block': block, 'universe': universe}
        
        # Merge any additional data into the block if provided
        if additional_data:
            new_block.update(additional_data)
        
        if document:
            # Coordinate exists, append the new block to the existing document
            self.collection.update_one(
                {'coordinate': coordinate},
                {'$push': {'blocks': new_block}}
            )
        else:
            # Coordinate does not exist, create a new document for this coordinate
            new_document = {
                'coordinate': coordinate,
                'blocks': [new_block]
            }
            self.collection.insert_one(new_document)
    
    def get_conversation_blocks(self, coordinate):
        """
        Retrieves all conversation blocks stored at the specified coordinate.
        """
        document = self.collection.find_one({'coordinate': coordinate})
        if document:
            return document.get('blocks', [])
        else:
            return []
    
    def update_coordinate(self, coordinate_data):
        """
        Placeholder for updating the coordinate state in the database.
        """
        # This method can be extended if you plan to store coordinates separately.
        pass
    
    def save_coordinate_state(self, coordinate_data):
        """
        Saves the current coordinate state to the database.
        """
        self.db['coordinate_state'].update_one(
            {'_id': 'current_state'},
            {'$set': coordinate_data},
            upsert=True  # Inserts the document if it doesn't exist
        )
    
    def load_coordinate_state(self):
        """
        Loads the saved coordinate state from the database, if it exists.
        """
        document = self.db['coordinate_state'].find_one({'_id': 'current_state'})
        if document:
            return document
        else:
            return None

    def close_connection(self):
        """
        Closes the MongoDB client connection.
        """
        self.client.close()
