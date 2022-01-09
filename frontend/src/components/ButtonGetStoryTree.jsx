import React, { useContext} from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"
 
export default function ButtonGetStoryTree() {

    function parseNodes(currentNode,newTree,children){
        //get keys in this node
        console.log(`keys in object:${Object.keys(currentNode)}`);  
        // the key is what we have to access to get to the node jammy goodness
        Object.keys(currentNode).forEach((nodeKey)=>{
            console.log(`Processing node key:${nodeKey}`);  
            // now check for children
            if (currentNode[nodeKey]["children"]){
                console.log(`${currentNode[nodeKey]["children"].length} children for ${nodeKey} recursive call`);
                currentNode[nodeKey]["children"].forEach((child) =>
                    parseNodes(child,newTree,children)
                )
                console.log(`finished children of ${nodeKey} we should write the parent now and empty the children array?`);
                newTree = Object.assign(newTree,{ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}, "children": children})
                //children.length = 0
            } else {
                console.log(`no children for ${nodeKey} adding to children object`);
                //Object.assign(children,{ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}})
                children.push({ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}})

                console.log(children);
            }
            console.log("next node");
            newTree = Object.assign(newTree,{ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}, "children": children})
            console.log(newTree);
            //children = []
        })    


        return newTree 
    }

    function convertTree(inputTree){
        let newTree ={}
        
        console.log("storyTree starts here:");

        newTree = parseNodes(inputTree,{},[])

        console.log(newTree);        

        return newTree

            // return { name: "top node", attributes: {text: "hi"}, children: [{name: "bollock 1", attributes:{text:"hairy"}},{name: "bollock 2", attributes:{text:"smooth"}}]}
        }

        const dummydata = 
            {
            "cfff3cc8-6c6c-11ec-b8ff-f01898e87167": {
                "children": [
                {
                    "e318bba4-6c6c-11ec-b8ff-f01898e87167": {
                    "data": { "text": "Unused 1" }
                    }
                },
                {
                     "zzzzbba4-6c6c-11ec-b8ff-f01898e871xx": {
                    "children": [
                        {
                            "item 3" :{ 
                                "data": {"text" : "beermats"}
                            }
                        }
                    ],
                    "data": { "text": "Unused 1" }
                    }                   
                },
                {
                    "f5a3d0f6-6c6c-11ec-b8ff-f01898e87167": {
                    "data": { "text": "unused 2" }
                    }
                }
                ],
                "data": { "text": "None" }
            }
}


    const {storyTree, setStoryTree} = useContext(StoryTreeContext)
    const tryGetStoryTree = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/story",
                {
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                const result = await response.json()
                console.log(`storyTree:${JSON.stringify(result.data.story)}`)
                //setStoryTree(result.data.story)
                //setStoryTree(convertTree(result.data.story))
                setStoryTree(convertTree(dummydata))

            } else {
                console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured getting story tree: ${error}`)
        }
    }

    const renderButtonGetStoryTree =(
        <StoryTreeContext.Provider value = {storyTree}>
        <Button colorScheme="blue" className="flex_button" onClick={tryGetStoryTree}>
            get tree
        </Button>
        </StoryTreeContext.Provider>
    )

    return (
        renderButtonGetStoryTree    
  )
}