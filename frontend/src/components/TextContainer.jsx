import React, { useContext, useState, useEffect} from "react"
import { StoryTreeContext,StoryTextContext } from "../App"
import { Container } from '@chakra-ui/react'

export default function TextContainer() {
    const {storyText, setStoryText} = useContext(StoryTextContext)
    const {storyTree, setStoryTree} = useContext(StoryTreeContext)

    // go and get the story from the API

    useEffect(() => {
    const tryGetStoryText = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/text",
                {
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                const result = await response.json()
                console.log(`storyText:${JSON.stringify(result.data.text)}`)
                setStoryText(result.data.text)

            } else {
                console.error(`get /text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured getting story text: ${error}`)
        }
    }

    // document.body.style.background = {background};
    tryGetStoryText()},[setStoryText,storyTree]);    

return (
    <div>
        {storyText}
    </div>
  );
}