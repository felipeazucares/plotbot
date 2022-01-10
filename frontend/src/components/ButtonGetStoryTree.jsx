import React, { useContext} from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"
 
export default function ButtonGetStoryTree() {


        function truncateReplace(str, numWords) {
        // helper function to convert text into a node name
            return str.split(" ").splice(0,numWords).join(" ").replace(" ","_");
        }

        function returnNode2(newObj,currentTree){
            //recurse tree returned from mongo to d3_react_tree - RawNodeDatum format
            let currentKey = Object.keys(currentTree)[0]
            const objName = truncateReplace(currentTree[currentKey].data.text,3)
            newObj= {_id: currentKey, name: objName, attributes: {text:currentTree[currentKey].data.text},children:[]}
            console.log("current item:" + currentKey);
            if (currentTree[currentKey].children){
                console.log("children detected creating newObj.children=[]");
                currentTree[currentKey]["children"].forEach((child) =>{
                    console.log("processing child:" + Object.keys(child)[0]);
                    newObj.children.push(returnNode2(newObj,child))
                })
            }
            else {
                console.log("no children for :" + currentKey);
                console.log("returning newObj:" + JSON.stringify(newObj));
                return newObj
            }
            return newObj
        }


    function convertTree(inputTree){

        const newTree = returnNode2({}, inputTree)
        console.log(newTree);        

        return newTree

        }

        const dummydata = 
            {
            "root_key": {
                "children": [
                    {
                        "child_1_key": {
                            "data": { "text": "first unused piece of text" }
                        },
                    },
                    {
                        "child_2_key": {
                            "children": [
                                {
                                    "grandchild_1_key" :{ 
                                        "data": {"text" : "I liked the beermats in the old pub much the best."}
                                    }
                                }
                            ],
                            "data": { "text": "Second unused piece of text" }
                        }                   
                    },
                    {
                        "child-3_key": {
                            "data": { "text": "third unused piece of text" }
                        }
                    }
                ],
            "data": {"text": "Rooty"},
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