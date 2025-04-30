from database import etp_collection
from bson.objectid import ObjectId

class EtpRepository:

    @staticmethod
    def get(id):
        etp = etp_collection.find_one({'_id': ObjectId(id)})
        if etp:
            etp['_id'] = str(etp['_id'])
        return etp

    @staticmethod
    def create(etp):
        result = etp_collection.insert_one(etp)
        etp['_id'] = str(result.inserted_id)
        return etp

    @staticmethod
    def delete(id):
        result = etp_collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0
