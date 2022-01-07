import React, { useState } from "react"
import {
    Button
} from "@chakra-ui/react"

 
  export default function ButtonGetStoryTree() {
    const [storyTree, setStoryTree] = useState("")
    const tryGetStoryTree = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/story",
                {
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                setStoryTree(response["data"])
                console.log(await response["data"].json());
            } else {
                console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured getting story tree: ${error}`)
        }
    }

    const renderButtonGetStoryTree =(
        <Button colorScheme="blue" className="flex_button" onClick={tryGetStoryTree}>
            get tree
        </Button>
    )

    return (
        renderButtonGetStoryTree    
  )
}