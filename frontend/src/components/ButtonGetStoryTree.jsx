import React, { useContext, useState } from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"
 
  export default function ButtonGetStoryTree() {
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
                setStoryTree(result.data.story)

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