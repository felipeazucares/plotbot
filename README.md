# Hairy Plotter

DEV.TO Hackathon Project - interactive fiction generation using the FARM stack: fastAPI, aitextgen library, MongoDB Atlas and React.
My submission to the MongoDB Atlas Hackathon on DEV.

---

### Overview of My Submission

Generate your own fiction by collaborating with an AI to steer the story as it unfolds. Amaze your friends! Terrify your enemies! Make people you don't know exclaim, "oh, that's mildly interesting."

## Installation

This app uses oAuth2, so you will _need_ redis installed on your machine on the defaul port 6379. Follow the instructions here: https://docs.redis.com/latest/rs/installing-upgrading/

Once you have confirmed your Redis installation is up and running, from terminal create a directory and git clone this repo into it.

You'll now need to install the pre-reqs for the frontend (React) and the backend (Python-fastapi).

1. Open a terminal session and complete the following steps
2. `$ cd frontend`
3. `$ npm install`
4. Once this is complete:
5. `$ cd ./backend`
6. `$ pip install -r requirements.txt`
7. This should install all the required components

## Startup

Start the backend
From the terminal complete the following

1. `$ cd <your directory>/backend`
2. `$ python main.py`
3. Your server should now be running on http://localhost:9000

start the frontend

1. `$ cd <your directory>/frontend`
2. `$ npm start`
3. You front end will be running on http://localhost:3000

## Usage

Click on `Start Here` and the story is initialised with an an initial preset scene.

![App screenshot showing initial scene node](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v7vvuwmf45ushce0mna9.png)

From then on it's up to you.

Mouse over this first node in the story tree to reveal the text comprising the scene. This also displays the story so far in the story pane to the right of the story tree.

![App screenshot hovering over the initial scene node to reveal its content](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9pbuglapy5jdkotmwh8t.png)

Click on the first node. The AiTextGen library will generate three follow up scenes based on the one you've just selected. These will appear as children of this first node in the tree.

![Video showing first nodes being generated](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sy61lrrl4uz0mmb4w9fm.gif)

![App screenshot showing three new scene nodes beneath the initial one](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b68hap371i9iiw3zfij6.png)

![Video showing story text updated as selected nodes generate children](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wnk42kct8ota5r1z9dh5.gif)

The story panel on the right keeps track of what your total story looks like based on the scenes you've selected.

![App screenshot showing the complete generated text in the story panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/98h9gvt2r5vkmn8wpafb.png)

Mouse over each of these new scenes to see which one appeals to you the most to pursue, then click on that one too. The selected scene is added to your story and three more scenes will be generated, and you can just keep going.

![Video hovering over each scene node to examine its text](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n9c1htyh0dqf9b7x28jo.gif)

![App screenshot examining the text of a follow up scene](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7w0lzik1cd3vc57rquag.png)

The creativity slider at the bottom of the screen allows you to ramp up the tangential-ness of the scenes generated, so play with it to find a setting that works for you. (Hint: lower settings sometimes cause repetitiveness, higher settings launch into non sequiturs)

![app screenshot of creativity slider settings from Walter Cronkite to Nic cage](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/suhr0mkrwszk9hthmxu0.png)

![App screen showing several scenes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vw4u6rro9nvwg4vdzw3v.png)

Happy with your story?

AWESOME! Copy it out mail it to yourself, send it to your mum or share it where ever you like.

Got a pig in a poke instead? No problem. Most AI generated stories are a load of doggy do, (generally only about 10% hang together). Simply click `Start Here` button and start all over again.

Just for curiosity's sake here's the one I generated for this post:

---

> "Harry Potter peered over his spectacles. He waved his magic wand and solemnly chanted the words of the spell. 'Indominus Petronus!' he cried with a final flourish. There was an almighty bang and a griffin appeared in a puff of smoke. 'Hello, Harry Potter,' the griffin said. 'Hey, do you mind if I touch this?' 'No, Sir,' said Harry. 'Let me take a look. Tell me what you're doing, then I'll tell you what to do." Harry was able to hear the griffin's voice echoing through the halls, and the griffin said, "Oh, Harry Potter, I've got something good to do. If I can see some good in you, I'll make you something good." The griffin smiled, and Harry nodded. The griffin turned on its side, and the Great Hall was illuminated. It was dark, and the darkness caught Harry's attention."

---

This submission comprises an API lovingly crafted with #fastAPI, uses a tree structure constructed using Treelib to connect each scene and features a UI thrown together with #React (It's the first time I've used this library so, it was a learning experience to say the least).

### Submission Category:

Choose your own adventure

### Link to Code

https://github.com/felipeazucares/plotbot

### Additional Resources / Info

This repo makes extensive use of the following brilliant libraries:

- fastAPI (https://fastapi.tiangolo.com)
- AITextGen (https://docs.aitextgen.io/)
- Treelib (https://treelib.readthedocs.io/en/latest/)
- React-d3-tree https://www.npmjs.com/package/react-d3-tree?activeTab=readme
- Chakra-UI (https://chakra-ui.com/)
