"""
Name: Database
Author: Ran Perry
"""

import redis
import random
from Utils.Event import Event


class DB:
    """
    Class of a general redis database containing many useful functions
    """
    db = None
    onUpdate = None

    @classmethod
    def add_update_event(cls, update_event):
        """
        Adds an update event in case the db gets updated
        :param update_event: update event to add
        """
        cls.onUpdate += update_event

    @classmethod
    def remove_update_event(cls, update_event):
        """
        Removes an update event
        :param update_event: update event to remove
        """
        cls.onUpdate -= update_event

    @classmethod
    def get(cls, id: str):
        """
        Gets value from the database of the specified id
        :param id: id to get value of
        :return: Value or None
        """
        if id is None: return None
        if id in cls.get_all_ids():
            db_object = cls.db.hgetall(id)
            return {k.decode(): db_object[k].decode() for k in db_object}
        return None

    @classmethod
    def get_id(cls, **kwargs):
        """
        Gets the id of a value by supplying keyword arguments that lie within the value
        :param kwargs: kwargs to look for
        :return: The found id or None
        """
        for key in cls.db.scan_iter():
            if all(str(kwargs[k]) == cls.get(key.decode()).get(k, None) for k in kwargs.keys()):
                return key.decode()
        return None

    @classmethod
    def get_all(cls):
        """
        Gets all of the values in the database and returns them
        :return: All values in database
        """
        return [{**cls.get(obj_id), **{'id': f'{obj_id}'}} for obj_id in cls.get_all_ids()]

    @classmethod
    def get_all_ids(cls):
        """
        Gets all the ids in the database and returns them
        :return: All ids in database
        """
        return [obj_id.decode() for obj_id in cls.db.scan_iter()]

    @classmethod
    def exists(cls, id=None, **kwargs):
        """
        Check if a value exists for an id or for an dict within the value
        :param id: id to check for
        :param kwargs: kwargs to check for
        :return: bool whether a value has been found
        """
        if id: return id in cls.get_all_ids()
        return bool(cls.get_id(**kwargs))

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new value with a randomized id
        :param kwargs: value to create
        :return: id of the new value
        """
        id = random.getrandbits(32)
        while id in cls.get_all_ids(): id = random.getrandbits(32)
        cls.set_dict_with_pipeline(id, **kwargs)
        return id

    @classmethod
    def set(cls, id: str, **kwargs):
        """
        Sets new parameters within the value of a specified id
        :param id: id of value wished to be changed
        :param kwargs: changes to value
        :return: whether function has succeeded
        """
        res = cls.set_dict_with_pipeline(id, **kwargs)
        return res

    @classmethod
    def delete(cls, id: str):
        """
        Deletes the value of a specified id
        :param id: id of value wished to be deleted
        :return: whether function has succeeded
        """
        res = cls.db.delete(id)
        return res

    @classmethod
    def set_dict_with_pipeline(cls, id, **kwargs):
        """
        Sets/Creates new parameters within the value of a specified id
        :param id: id of value wished to be changed/added
        :param kwargs: changes to value/value itself
        :return: whether function has succeeded
        """
        if not id or not kwargs:
            return False
        with cls.db.pipeline() as pipe:
            success = all([pipe.hset(id, k, v) for k, v in kwargs.items()])
            pipe.execute()
        cls.update()
        return success

    @classmethod
    def clear(cls):
        """
        Clears database
        """
        cls.db.flushall()
        cls.update()

    @classmethod
    def update(cls):
        """
        Calls update event
        """
        cls.onUpdate()

    @staticmethod
    def clear_all():
        """
        Clears all databases
        """
        UserDB.clear()
        GameDB.clear()
        UserDB.update()
        GameDB.update()

    @classmethod
    def __str__(cls):
        """
        :return: String representation of database
        """
        ret_str = f'{cls.__name__} Contains:\n'
        for obj_id in cls.get_all_ids():
            ret_str += f"\tAt key '{obj_id}' --> {cls.get(obj_id)}\n"
        return ret_str


class UserDB(DB):
    db = redis.Redis()
    onUpdate = Event()


class GameDB(DB):
    db = redis.Redis(db=1)
    onUpdate = Event()

