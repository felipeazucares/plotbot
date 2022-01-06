import React, { useState } from "react"
import {
    Button
} from "@chakra-ui/react"

 
  export default function ButtonGetStoryTree() {
    const [storyTree, setStoryTree] = useState("")
    const tryGetStoryTree = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/story", {headers: 
            {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIkMmIkMTIka3NlTVR6ZnV6L1h3MjdtTnIxNjhKT1Z4UWVHL2hiVU8vMko2VDR2eGUvei9meVhZQUozVS4iLCJzY29wZXMiOlsic3Rvcnk6cmVhZGVyIiwic3Rvcnk6d3JpdGVyIl0sImV4cCI6MTY0MTQ4MzQyNX0.C905Gdp16SHgNMP7URo_-w2mR0JmH-KfikryXZKDEtU"}, 
            credentials: "include"
        },)
            if (response.status===200 && response.statusText==="OK"){
                setStoryTree(response["data"])
                console.log(response.body.data);
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