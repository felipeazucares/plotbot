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
            const response = await fetch("http://localhost:8450/text",{method:"post", body: JSON.stringify(payload), credentials:"include", headers: {"Content-Type": "application/json"}})
            if (response.status===200 && response.statusText==="OK"){
                console.log("get text")
                const result = await response.json()
                console.log(`result:${JSON.stringify(result)}`)
                setText(await result.data)
                // setUser(username)
            } else {
                console.error(`generating text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured generating text: ${error}`)
        }
        console.log(`text:${JSON.stringify(text)}`);
        // no that we have the text add it onto the the last item in the tree
        try{            
            const response = await fetch("http://localhost:8450/story/?parent_id=1976c33e-6c6e-11ec-b1ed-f01898e87167",{method:"post", body: JSON.stringify(text), credentials:"include", headers: {"Content-Type": "application/json"}})
            if (response.status===200 && response.statusText==="OK"){
                console.log("save text to db")
                const result = await response.json()
                console.log(`returned text: ${JSON.stringify(result)}`)
                // setUser(username)
            } else {
                console.error(`save text failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured saving text: ${error}`)
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