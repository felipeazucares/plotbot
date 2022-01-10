import React, { useState } from "react"
import {
    Button,
} from "@chakra-ui/react"


export default function ButtonGetNewText() {

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


    const RenderButtonGetNewText =(
        <Button colorScheme="blue" className="flex_button" onClick={tryGetText}>
           get blah blah blah
        </Button>
    )

    return (
        RenderButtonGetNewText    
  )
}