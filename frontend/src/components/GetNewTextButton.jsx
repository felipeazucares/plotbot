import React, { useState } from "react"
import {
    Button,
} from "@chakra-ui/react"


export default function GetNewTextButton() {

    const [text,setText] = useState("")
    const payload={
                "prompt": "It was cold outside, but not as cold as Peter felt in his heart.",
                "temperature": 0.71234132
            }
    const tryGetText = async () => 
    {

        try{            
            const response = await fetch("http://localhost:9000/text",{method:"post", body: JSON.stringify(payload), credentials:"include", headers: {"Content-Type": "application/json"}})
            if (response.status===200 && response.statusText==="OK"){
                console.log("get text")
                const result = await response.json()
                console.log(`returned text: ${JSON.stringify(result)}`)
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


    const RenderGetNewTextButton =(
        <Button colorScheme="blue" className="flex_button" onClick={tryGetText}>
           get text
        </Button>
    )

    return (
        RenderGetNewTextButton    
  )
}