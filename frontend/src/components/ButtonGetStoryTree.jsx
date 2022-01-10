import React, { useContext} from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"
 
export default function ButtonGetStoryTree() {

    const deepCopyFunction = (inObject) => {
        //could refactor this to add a child beneatha given parent when supplied with current tree object
        let outObject, value, key
        console.log("deep copy called");
        if (typeof inObject !== "object" || inObject === null) {
            return inObject // Return the value if inObject is not an object
        }

        // Create an array or object to hold the values
        outObject = Array.isArray(inObject) ? [] : {}

        for (key in inObject) {
            value = inObject[key]

            // Recursively (deep) copy for nested objects, including arrays
            outObject[key] = deepCopyFunction(value)
        }
        return outObject
    }

    // function parseNodes(currentNode,newTree,children){
    //     //get keys in this node
    //     //newTree = JSON.parse(newTree)
        
    //     console.log(`Node keys in this object:${Object.keys(currentNode)}`);  
    //     console.log(`Calling routine with currentNode:${JSON.stringify(currentNode)}`);
    //     console.log(`Calling routine with newTree:${JSON.stringify(newTree)}`);
    //     console.log(`Calling routine with children:${JSON.stringify(children)}`);       
    //     // the key is what we have to access to get to the node jammy goodness
    //     Object.keys(currentNode).forEach((nodeKey)=>{
    //         console.log(`Node loop processing key:${nodeKey}`);  
    //         // now check for children
    //         if (currentNode[nodeKey]["children"]){
    //             console.log(`${currentNode[nodeKey]["children"].length} children for ${nodeKey} recursive call`);
    //             currentNode[nodeKey]["children"].forEach((child) =>{
    //                 newTree = { newTree: {"name" : nodeKey, "children": children} }
    //                 parseNodes(child,newTree,children)
    //             })
    //             console.log(`Finished collecting children of ${nodeKey}: ${JSON.stringify(children)}`);
    //             // need a deep copy of the object involved 
    //             //newTree = Object.assign(newTree, { "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}, "children": children})
    //             console.log("newTree after collecting children:"+JSON.stringify(newTree));
    //             //children.length = 0
                
    //         } else {
    //             console.log(`${nodeKey} is a leaf node. Processing leaf and pushing ${nodeKey} & ${currentNode[nodeKey]['data']['text']} to children object`);
    //             //Object.assign(children,{ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}})
    //             // console.log(`pushing this to array:${ {'name': nodeKey, 'attributes': {text:currentNode[nodeKey]['data']['text']}}`);
    //             children.push({ "name": nodeKey, "attributes": {text:currentNode[nodeKey]["data"]["text"]}})
    //             console.log(`children array contains:${JSON.stringify(children)}`);
    //             return children
    //         }
    //         //newTree["children"] = children
    //     })    

    //     return newTree 
    // }

        function returnNode2(newObj,currentTree){
            // get key for all nodes
            let currentKey = Object.keys(currentTree)[0]
            newObj= {"name": currentKey, "children":[]}
            console.log("current item:" + currentKey);
            if (currentTree[currentKey].children){
                console.log("children detected creating newObj.children=[]");
                //newObj.children=[]
                currentTree[currentKey]["children"].forEach((child) =>{
                    console.log("processing child:" + Object.keys(child)[0]);
                    newObj.children.push(returnNode2(newObj,child))
                })
            }
            else {
                console.log("no children for :" + currentKey);
                console.log("returning object" + JSON.stringify(newObj));
                return newObj
            }
            return newObj
        }


    function convertTree(inputTree){
        let newTree ={}
        
        newTree = returnNode2({},inputTree)
        console.log(newTree);        

        return newTree

        }

        const dummydata = 
            {
            "root_key": {
                "children": [
                    {
                        "child_1_key": {
                            "data": { "text": "Unused 1" }
                        },
                    },
                    {
                        "child_2_key": {
                            "children": [
                                {
                                    "grandchild_1_key" :{ 
                                        "data": {"text" : "beermats"}
                                    }
                                }
                            ],
                            "data": { "text": "Unused 2" }
                        }                   
                    },
                    {
                        "child-3_key": {
                            "data": { "text": "unused " }
                        }
                    }
                ],
            "data": "Rooty",
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