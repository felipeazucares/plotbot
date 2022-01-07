import React, { useState } from "react"
import axios from "axios"
import {
    Button
} from "@chakra-ui/react"

 
  export default function ButtonGetStoryTree() {
    const [storyTree, setStoryTree] = useState("")
    const tryGetStoryTree = async () => 
    {
        // try{            
        //     const response = await fetch("http://localhost:9000/story",
        //         {
        //             credentials:"include"
        //             // headers: {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIkMmIkMTIka3NlTVR6ZnV6L1h3MjdtTnIxNjhKT1Z4UWVHL2hiVU8vMko2VDR2eGUvei9meVhZQUozVS4iLCJzY29wZXMiOltdLCJleHAiOjE2NDE1Mzk2MjJ9.IQbegXFRSt4LfeReCVUXJk6tkrYls2mhfKezK4bX-jY"},
        //         })
        //     if (response.status===200 && response.statusText==="OK"){
        //         setStoryTree(response["data"])
        //         console.log(await response["data"].json());
        //     } else {
        //         console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
        //     }
        // }
        // catch(error){
        //     console.error(`Exception occured getting story tree: ${error}`)
        // }
        const baseURL= "http://localhost:9000/story"
        const axiosConfig={
                method: 'GET',
                url: baseURL,
                withCredentials: true
        }
        try{            
            const response = await axios(axiosConfig)

            if (response.status===200 && response.statusText==="OK"){
                setStoryTree(response["data"])
                console.log(response["data"].json());
            } else {
                console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
                console.log(response);
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