import React, {useContext} from "react"
import {
    Button
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"
 
export default function ButtonRestart() {

    const {storyTree, setStoryTree} = useContext(StoryTreeContext)
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

        //now add a single node in to begon with

        
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