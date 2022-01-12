import React, {useContext, useEffect} from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"


export default function ButtonRestart() {

    const {storyTree, setStoryTree} = useContext(StoryTreeContext)

    function returnNode2(newObj,currentTree, count){
        count = count + 1
        //recurse tree returned from mongo to d3_react_tree - RawNodeDatum format
        let currentKey = Object.keys(currentTree)[0]
        //const objName = truncateReplace(currentTree[currentKey].data.text,3)
        if(currentTree[currentKey].children){
            newObj= {_id: currentKey, name: count, attributes: {text:currentTree[currentKey].data.text},children:[]}
        }
        else {
            
            newObj= {_id: currentKey, name: count, attributes: {text:currentTree[currentKey].data.text}}
        }
        console.log("current item:" + currentKey);
        if (currentTree[currentKey].children){
            console.log("children detected creating newObj.children=[]");
            currentTree[currentKey]["children"].forEach((child) =>{
                console.log("processing child:" + Object.keys(child)[0]);
                newObj.children.push(returnNode2(newObj,child, count))
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

        const newTree = returnNode2({}, inputTree,0)
        console.log(newTree);        
        return newTree

        }


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
                    setStoryTree(convertTree(result.data.story))

                } else {
                    console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
                }
            }
            catch(error){
                console.error(`Exception occured getting story tree: ${error}`)
            }
        }


    const tryRestart = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/save",
                {   method: "DELETE",
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                const result = await response.json()
                console.log(`${JSON.stringify(result.data)}`)
                //setStoryTree({})
            } else {
                console.error(`DELETE/saves failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured deletiing saved story tree: ${error}`)
        }

        //now add a single node with default text to begin with
        const textPayload = {
            text: "Harry Potter peered over his spectacles. He waved his magic wand and solemnly chanted the words of the spell. 'Indominus Petronus!' he cried with a final flourish. There was an almighty bang and a griffin appeared in a puff of smoke. 'Hello, Harry Potter,' the griffin said."
        }
        try{            
            const response = await fetch(`http://localhost:9000/story/?parent_id=`,{method:"post", body: JSON.stringify(textPayload), credentials:"include", headers: {"Content-Type": "application/json"}})
            if (response.status===200 && response.statusText==="OK"){
            console.log("save text to db")
            const result = await response.json()
            console.log(`returned text: ${JSON.stringify(result)}`)
            await tryGetStoryTree()
            } else {
            console.error(`Save text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured saving text: ${error}`)
        }
        

    }

    const renderButtonRestart =(
        <StoryTreeContext.Provider value = {storyTree}>
        <Button colorScheme="blue" className="flex_button" onClick={tryRestart}>
            Start Here
        </Button>
        </StoryTreeContext.Provider>
    )

    return (
        renderButtonRestart    
  )
}