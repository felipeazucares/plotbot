""" Database interface module for plotbot.py
"""
import os
from datetime import datetime
import motor.motor_asyncio
from treelib import Tree
from fastapi.encoders import jsonable_encoder
from api.helpers import ConsoleDisplay
from bson.objectid import ObjectId
from api.models import UserDetails, Story, AddNodeResponse


MONGO_DETAILS = os.getenv(key="MONGO_DETAILS")
DEBUG = bool(os.getenv("DEBUG", "False") == "True")
USER_COLLECTION_NAME = os.getenv(key="USER_COLLECTION_NAME")
STORY_COLLECTION_NAME = os.getenv(key="STORY_COLLECTION_NAME")


# console_display = ConsoleDisplay()

# ----------------------------------------------------
#           Functions for loading users
# ----------------------------------------------------


class UserStorage:
    """Class providing user retrieval methods"""

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.plotbot
        self.user_collection = self.database.get_collection(USER_COLLECTION_NAME)
        self.console_display = ConsoleDisplay()
        # init method attribs
        self.username = None
        self.user_details = None
        self.user_id = None

    async def get_user_details_by_username(self, username: str):
        """return the a user's details given their username - used for log in"""
        self.username = username
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"get_user_details_by_username({self.username}) called"
            )
        try:
            user_deets = await self.user_collection.find_one(
                {"username": self.username}
            )
            if user_deets is not None:
                self.user_details = UserDetails(**user_deets)
            else:
                self.user_details = None
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving user details from the database username was: {self.username}"
            )
            print(exception_object)
            raise
        return self.user_details

    async def get_user_details_by_user_id(self, user_id):
        """return the a user's details given their user_id"""
        self.user_id = user_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"get_user_details_by_account({self.user_id}) called"
            )
        try:
            user_deets = await self.user_collection.find_one({"user_id": self.user_id})
            if user_deets is not None:
                self.user_details = UserDetails(**user_deets)
            else:
                self.user_details = None
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving user details from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        return self.user_details


# ----------------------------------------------------
#       Functions for Story Tree CRUD ops
# ----------------------------------------------------
class StoryStorage:
    """Class for managing STory object saving and retrieval"""

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.plotbot
        self.story_collection = self.database.get_collection(STORY_COLLECTION_NAME)
        self.console_display = ConsoleDisplay()
        # init class attribs prior to use
        self.user_id = None
        self.saves = []
        self.story_to_save = None
        self.save_response = None
        self.new_save = None
        self.delete_result = None
        self.last_save = None
        self.save_id = None
        self.document_id = None
        self.story_document = None
        self.tree_id = None
        self.loaded_tree = None
        self.new_tree = None
        self.node_id = None
        self.last_save_tree = None
        self.tree = None
        self.tree_dict = None
        self.final_tree = None
        self.root_node = None
        self.payload = None
        self.children = None
        self.child_id = None
        self.name = None
        self.text = None
        self.last_save_story = None
        self.current_leaf = None
        self.new_node_id = None
        self.text_to_return = None
        self.story_text = None
        self.current_node_id = None
        self.current_node = None
        self.parent_id = None

    async def save_story(self, story: Story) -> str:
        """save the story provided to mongo db

        Args:
            user_id (str): salted hash id for user
            story (Story): wrapper containing userid, date time and tree object containing the story text and structure

        Returns:
            str: id of inserted mongodb document
        """
        self.story_to_save = Story(
            tree=story, user_id=self.user_id, date_time=datetime.utcnow()
        )
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show="save_story(story) called"
            )
        try:
            self.save_response = await self.story_collection.insert_one(
                jsonable_encoder(self.story_to_save)
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occured writing to the database"
            )
            print(exception_object)
            raise
        try:
            self.new_save = await self.story_collection.find_one(
                {"_id": ObjectId(self.save_response.inserted_id)}
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retriving details for save operation to the database _id: {self.save_response.inserted_id}"
            )
            print(exception_object)
            raise
        return str(ObjectId(self.save_response.inserted_id))

    async def return_a_save_document(self, user_id: str, document_id: str) -> Story:
        """Returns a specified story document for user in mongodb

        Args:
            user_id (str): hashed salted userid
            document_id: mongo _id of save document

        Returns:
            Story: object containing requested save doc tree
        """
        self.user_id = user_id
        self.document_id = document_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_a_save_document({self.user_id},{self.document_id}) called"
            )
        try:
            self.last_save = await self.story_collection.find_one(
                {"_id": ObjectId(self.document_id)}
            )

        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving save for user_id: {self.user_id}"
            )
            print(exception_object)
            raise
        if self.last_save is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="Save document found"
                )
            # self.last_save = Story(**self.last_save)
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No save document found"
                )
        return self.last_save

    async def return_latest_save_document(self, user_id: str) -> Story:
        """Returns latest story document or user in mongodb

        Args:
            user_id (str): hashed salted userid

        Returns:
            Story: most recent save document
        """
        self.user_id = user_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_latest_save_document({self.user_id}) called"
            )
        try:
            self.last_save = await self.story_collection.find_one(
                {"user_id": self.user_id}, sort=[("date_time", -1)]
            )

        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save for user_id: {self.user_id}"
            )
            print(exception_object)
            raise
        if self.last_save is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="Save document found"
                )
            # self.last_save = Story(**self.last_save)
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No save document found"
                )
        return self.last_save

    async def return_latest_story(self, user_id: str) -> Tree:
        """return the tree found in the latest save document

        Args:
            user_id (str): hashed salted user_id

        Returns:
            Tree: Story tree object found in latest save
        """
        self.user_id = user_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_latest_story({self.user_id}) called"
            )
        try:
            self.last_save = await self.return_latest_save_document(
                user_id=self.user_id
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        # get the tree dict from the saved document
        if self.last_save is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="Story save exists - rebuilding tree"
                )
            try:
                self.last_save_tree = self.last_save["tree"]
                self.tree = self.build_tree_from_dict(tree_dict=self.last_save_tree)
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show=f"Exception occured rebuilding tree structure from last save, last_save: {self.last_save}"
                )
                print(exception_object)
                raise
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No Story save exists - creating Tree()"
                )
            try:
                self.tree = Tree()
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show="Exception occured creating new tree"
                )
                print(exception_object)
                raise
            # I think this is breaking stuff - should it be returning a dict here? perhaps we add a format flag?
        return self.tree.to_dict(with_data=True)

    async def return_latest_story_text(self, user_id: str) -> str:
        """return the story text by traversing the latest tree

        Args:
            user_id (str): hashed salted user_id

        Returns:
            str: containing compiled text from tree object
        """
        self.user_id = user_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_latest_story_text({self.user_id}) called"
            )
        try:
            self.last_save = await self.return_latest_save_document(
                user_id=self.user_id
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        # get the tree dict from the saved document
        if self.last_save is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="Story save exists - rebuilding tree"
                )
            try:
                self.last_save_tree = self.last_save["tree"]
                self.tree = self.build_tree_from_dict(tree_dict=self.last_save_tree)
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show=f"Exception occured rebuilding tree structure from last save, last_save: {self.last_save}"
                )
                print(exception_object)
                raise
            # now recursively parse the given tree
            self.text_to_return = self.traverse_tree(
                tree=self.tree,
                story_text="",
                current_node_id=self.tree.root,
            )
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No Story save exists - creating Tree()"
                )
            try:
                self.tree = Tree()
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show="Exception occured creating new tree"
                )
                print(exception_object)
                raise
        return self.text_to_return

    def traverse_tree(self, tree: Tree, story_text: str, current_node_id: str) -> str:
        """recursive routine to traverse a given tree and concatenate text data from each node

        Args:
            tree (Tree): story tree to traverse containing data with text attribs
            story_text (str): string to results of contcatenation of all text data in tree
            current_node_id (str): current node that we are processing in tree

        Returns:
            str: string to contain contcatenation of all text data in tree
        """

        self.story_text = story_text
        self.current_node_id = current_node_id
        self.tree = tree
        self.current_node = None

        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"traverse_tree(story_text:{self.story_text},current_node_id:{self.current_node_id},tree:{self.tree}) called"
            )

        # get current node
        try:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="getting current_node"
                )
            self.current_node = self.tree.get_node(self.current_node_id)

        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occured getting current node:{self.current_node_id}"
            )
            print(exception_object)
            raise

        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"Adding text {self.current_node.data['text']} to story_text"
            )
        # add the text from the current node to the story_text string
        self.story_text = self.story_text + " " + self.current_node.data["text"]
        # check for children
        if self.tree.children(self.current_node_id):
            # loop through all children checking to see which one has children - should be only one
            for child in self.tree.children(self.current_node_id):
                if DEBUG:
                    self.console_display.show_debug_message(
                        message_to_show=f"Child detected:{child.identifier}"
                    )
                # when we find one with children we pass that to the next call of the routine
                if self.tree.children(child.identifier):
                    self.traverse_tree(
                        tree=self.tree,
                        story_text=self.story_text,
                        current_node_id=child.identifier,  # each node has only one child so far
                    )

        if DEBUG:
            self.console_display.show_debug_message(message_to_show="base case")
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"self.story_text:{self.story_text}"
            )
        return self.story_text

    async def return_a_story(self, user_id: str, document_id: str) -> Tree:
        """return the tree found in the specified save document

        Args:
            user_id (str): hashed salted user_id
            document_id (str): mongodb _id value

        Returns:
            Tree: Story tree object found in latest save
        """
        self.user_id = user_id
        self.document_id = document_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_a_story({self.user_id},{self.document_id}) called"
            )
        try:
            self.last_save = await self.return_a_save_document(
                user_id=self.user_id, document_id=self.document_id
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        # get the tree dict from the saved document
        if self.last_save is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="Story save exists - rebuilding tree"
                )
            try:
                self.last_save_tree = self.last_save["tree"]
                self.tree = self.build_tree_from_dict(tree_dict=self.last_save_tree)
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show=f"Exception occured rebuilding tree structure from last save, last_save: {self.last_save}"
                )
                print(exception_object)
                raise
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No Story tree found. Returning empty tree"
                )
            self.tree = Tree()
        return self.tree.to_dict(with_data=True)

    async def add_text_to_story_tree(
        self, text: str, user_id: str, parent_id: str
    ) -> str:
        """Creates a new tree node and adds text to its data property & saves it to db

        Args:
            text (str): text to store in the node
            user_id (str): current user id
            parent_id (str): node id of new node's parent

        Returns:
            AddNodeResponse: wrapper class containing node id, tree and document save id
        """
        self.text = text
        self.user_id = user_id
        self.parent_id = parent_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"add_text_to_story_tree({self.text},{self.user_id}) called"
            )
        try:
            self.last_save_story = await self.return_latest_story(user_id=self.user_id)
            self.last_save_story.show()
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured returning latest save story from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise

        # if DEBUG:
        #     self.console_display.show_debug_message(
        #         message_to_show=f"story root node {self.last_save_story.root}"
        #     )
        if self.last_save_story.root is not None:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"save document detected {self.last_save_story}"
                )
            # since the tree is a vertical chain there should only ever be one leaf
            self.current_leaf = self.last_save_story.leaves()
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"current leaf is: {self.current_leaf[0].identifier})"
                )
            # add the new text node
            try:
                self.new_node_id = self.last_save_story.create_node(
                    parent=self.parent_id, data={"text": self.text}
                )
            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show="Exception occured adding a node to tree"
                )
                print(exception_object)
                raise
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"adding node id:{self.new_node_id.identifier} to {self.parent_id})"
                )
        else:
            # no pre-existing save so we'll create a new node without a parent
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="No pre-existing save - adding new root node"
                )
            try:
                self.new_node_id = self.last_save_story.create_node(
                    data={"text": self.text}
                )
                if DEBUG:
                    self.console_display.show_debug_message(
                        message_to_show=f"new node added to tree:{self.new_node_id}"
                    )

            except Exception as exception_object:
                self.console_display.show_exception_message(
                    message_to_show="Exception occured creating a new tree"
                )
                print(exception_object)
                raise
        # now save the tree
        self.save_id = await self.save_story(self.last_save_story)

        return AddNodeResponse(
            new_node_id=self.new_node_id.identifier,
            document_id=self.save_id,
            story=self.last_save_story,
        )

    def build_tree_from_dict(self, tree_dict: dict) -> Tree:
        """build a Tree object from a tree dictionary object stored in a save document

        Args:
            tree_dict (dict): The tree dictionary object to convert into a Tree

        Returns:
            Tree: Story tree built from input dictionary
        """
        self.tree_dict = tree_dict
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"build_tree_from_dict({self.tree_dict}) called"
            )
        try:
            self.root_node = self.tree_dict["root"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"root node in dict is:{self.tree_dict['root']}"
                )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving root object from dict, self.tree_dict: {self.tree_dict} {exception_object}"
            )
            print(exception_object)
            raise
        # create a new tree
        try:
            self.new_tree = Tree(identifier=self.tree_dict["_identifier"])
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"new empty tree object created with id:{self.tree_dict['_identifier']}"
                )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured creating new tree with _identifier:{self.tree_dict['_identifier']} {exception_object}"
            )
            print(exception_object)
            raise

        self.final_tree = self.add_a_node(
            tree_id=self.tree_dict["_identifier"],
            loaded_tree=self.tree_dict,
            new_tree=self.new_tree,
            node_id=self.root_node,
        )
        return self.final_tree

    def add_a_node(
        self, tree_id: str, loaded_tree: dict, new_tree: Tree, node_id: str
    ) -> Tree:
        """recursive routine to add a node extracted from a loaded dict to add to a Tree

        Args:
            tree_id (str): id of the tree we're constructing
            loaded_tree (dict): dictionary object containing the nodes we want to add to the Tree
            new_tree (Tree): the Tree object we're building
            node_id (str): id of the node we want to add

        Returns:
            Tree: Story tree object we're constructing
        """
        self.tree_id = tree_id  # identifier for the tree that we're building
        self.loaded_tree = loaded_tree  # the tree structure returned from mongo
        self.new_tree = new_tree  # tree we're building
        self.node_id = node_id  # the node to add

        # get name of node that's been passed to the routine
        try:
            self.name = self.loaded_tree["_nodes"][self.node_id]["_tag"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"node tag in self.loaded_tree['_nodes'][node_id] dict is: {self.name}"
                )
        except KeyError as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred unable to find _tag for {self.loaded_tree['_nodes'][self.node_id]} in loaded_tree dict"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][node_id]['_tag']: {self.loaded_tree['_nodes'][self.node_id]['_tag']}"
            )
            print(exception_object)
            raise
        # get the id of the current node
        try:
            self.node_id = self.loaded_tree["_nodes"][self.node_id]["_identifier"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"loaded_tree['_nodes'][self.node_id][_identifier] is: {self.tree_id}"
                )
        except KeyError as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred unable to find _identifier for {self.loaded_tree['_nodes'][self.node_id]}"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][node_id]['_identifier']: {self.loaded_tree['_nodes'][self.node_id]['_identifier']}"
            )
            print(exception_object)
            raise
        # set payload for new node to what's in the current node
        try:
            self.payload = self.loaded_tree["_nodes"][self.node_id]["data"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"payload set to {self.payload}"
                )
        except KeyError as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occurred unable to get node data"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][self.node_id]['data']: {self.loaded_tree['_nodes'][self.node_id]['data']}"
            )
            print(exception_object)
            raise

        # parent (_predecessor) and children(_successors) are stored under against self.tree_id key
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"{self.node_id} _successors: {self.loaded_tree['_nodes'][self.node_id]['_successors']}"
            )
        try:
            self.children = self.loaded_tree["_nodes"][self.node_id]["_successors"][
                self.tree_id
            ]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"self.loaded_tree['_nodes'][self.node_id]['_successors'][self.tree_id] children: {self.children}"
                )
        except KeyError:
            # sometimes the _successors field has no key - so if we can't find it set to None
            self.children = None
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"key error caught: no successors key for {self.name}'s children: None"
                )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occurred retrieving the _successors field"
            )
            self.console_display.show_exception_message(
                message_to_show=f"id:{self.loaded_tree['_nodes'][self.node_id]['_identifier']}"
            )
            print(exception_object)
            raise

        if (
            self.loaded_tree["_nodes"][self.node_id]["_predecessor"][self.tree_id]
            is not None
        ):
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"creating node with - name: {self.name}, identifier: {self.node_id}, parent: {self.loaded_tree['_nodes'][self.node_id]['_predecessor'][self.tree_id]}"
                )
        else:
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="creating node with - name: {self.name}, identifier: {self.node_id}, parent: none"
                )

        try:
            self.new_tree.create_node(
                tag=self.name,
                identifier=self.node_id,
                parent=self.loaded_tree["_nodes"][self.node_id]["_predecessor"][
                    self.tree_id
                ],
                data=self.payload,
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occurred adding a node to the working tree."
            )
            self.console_display.show_exception_message(
                message_to_show=f"name: {self.name}, identifier: {self.tree_id}, data: {self.payload}"
            )
            print(exception_object)
            raise

        if self.children is not None:

            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show="recursive call"
                )
            for self.child_id in self.children:
                self.add_a_node(
                    tree_id=self.tree_id,
                    loaded_tree=self.loaded_tree,
                    new_tree=self.new_tree,
                    node_id=self.child_id,
                )

        else:
            if DEBUG:
                self.console_display.show_debug_message(message_to_show="base_case")

        return self.new_tree

    async def list_all_story_saves(self, user_id: str) -> dict:
        """return a list of all story documents for user_id

        Args:
            user_id (str): hashed salted user id string

        Returns:
            dict: containing ids of all saved documents
        """
        self.user_id = user_id
        self.saves = []
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"list_all_story_saves({self.user_id}) called"
            )
        try:
            async for save in self.story_collection.find({"user_id": self.user_id}):
                self.saves.append(str(save["_id"]))
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured returning list of all documents for user_id {self.user_id}"
            )
            print(exception_object)
            raise
        return self.saves

    async def delete_all_story_saves(self, user_id: str) -> int:
        """delete all the saved story documents for user_id

        Args:
            user_id (str): hashed salted user_id string

        Returns:
            int: count of documents deleted from database
        """
        self.user_id = user_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"delete_all_story_saves({self.user_id}) called"
            )
        try:
            self.delete_result = await self.story_collection.delete_many(
                {"user_id": self.user_id}
            )
            # delete_result object contains a deleted_count & acknowledged properties
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured deleting a save from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        return self.delete_result.deleted_count

    async def delete_a_story_save(self, user_id: str, document_id: str) -> int:
        """delete all the saved story documents for user_id

        Args:
            user_id (str): hashed salted user_id string
            document_id : id of the doc we want to delete

        Returns:
            int: count of documents deleted from database
        """
        self.user_id = user_id
        self.document_id = document_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"delete_a_story_save({self.user_id},{self.document_id}) called"
            )
        try:
            self.delete_result = await self.story_collection.delete_one(
                {"user_id": self.user_id, "_id": ObjectId(self.document_id)}
            )
            # delete_result object contains a deleted_count & acknowledged properties
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured deleting a save from the database user_id was: {self.user_id}, document_id: {self.document_id}"
            )
            print(exception_object)
            raise
        return self.delete_result.deleted_count

    async def return_specified_save_document(self, document_id: str) -> Story:
        """return a story object from a specified save document

        Args:
            document_id (str): the id of the document we want

        Returns:
            Story: story specified
        """
        self.document_id = document_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_save({self.document_id}) called"
            )
        try:
            self.story_document = await self.story_collection.find_one(
                {"_id": ObjectId(self.document_id)}
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving save from the database document_id was: {self.document_id}"
            )
            print(exception_object)
            raise
        return self.story_document

    async def return_saved_story(self, document_id: str) -> Tree:
        """load a specified save document and return contained Story tree object

        Args:
            document_id (str): save document id

        Returns:
            Tree: Story tree object extracted from save
        """
        self.document_id = document_id
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_saved_story({self.document_id}) called"
            )
        try:
            self.story_document = await self.return_specified_save_document(
                document_id=self.document_id
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.document_id}"
            )
            print(exception_object)
            raise
        # get the tree dict from the saved document
        try:
            self.story = self.story_document["tree"]
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving tree structure from last save, last_save: {self.document_id}"
            )
            print(exception_object)
            raise

        return self.build_tree_from_dict(tree_dict=self.story)
