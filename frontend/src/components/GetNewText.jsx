import React, { useState, useContext } from "react"
// import { UserContext } from '../App';
import {
    Button,
} from "@chakra-ui/react"
import { StoryTreeContext } from "../App"

  export default function getNewText() {

    const {text,setText} = useState("")

    const tryGetText = async () => 
    {

        try{            
            const response = await fetch("http://localhost:9000/text",{method:"get", credentials:"include"})
            if (response.status===200 && response.statusText==="OK"){
                console.log("get text")
                const result = await response.json()
                setText(result.data)
                // setUser(username)
            } else {
                console.error(`get a text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured loggin in: ${error}`)
        }
    }


    const renderButtonGetStoryTree =(
        // <StoryTreeContext.Provider value = {storyTree}>
        <Button colorScheme="blue" className="flex_button" onClick={tryGetText}>
            get tree
        </Button>
        // </StoryTreeContext.Provider>
    )

    return (
        renderButtonGetStoryTree    
  )
}