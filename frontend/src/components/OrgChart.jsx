import React, { useContext, useState} from "react"
import Tree from "react-d3-tree"
import './custom-tree.css'
import { useCenteredTree } from "./Helpers";
import { StoryTreeContext } from "../App"


export default function OrgChartTree() {
  const {storyTree, setStoryTree} = useContext(StoryTreeContext)
  const [translate, containerRef] = useCenteredTree()

  const [text,setText] = useState("")

  const renderNodeWithCustomEvents = ({nodeDatum,toggleNode,handleNodeClick}) => (
    <g>
    <circle r="10" onClick={() => handleNodeClick(nodeDatum)} />
    <text fill="blue" strokeWidth="0" x="15" onClick={toggleNode}>
      {nodeDatum.name}
    </text>
    {/* {nodeDatum.attributes?.text && (
      <text fill="grey" x="20" y="20" strokeWidth="0">
        {nodeDatum.attributes?.text}
      </text>
    )} */}
  </g>
);

const tryGetText = async (parent_id,promptText) => {
      const payload={
                  "prompt": promptText,
                  "temperature": 0.71234132
              }
      //get last sentence from text provided

      try{            
          const response = await fetch("http://localhost:9000/text",{method:"post", body: JSON.stringify(payload), credentials:"include", headers: {"Content-Type": "application/json"}})
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
          const response = await fetch(`http://localhost:9000/story/?parent_id=${parent_id}`,{method:"post", body: JSON.stringify(text), credentials:"include", headers: {"Content-Type": "application/json"}})
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

        try{            
          const response = await fetch("http://localhost:9000/text",{method:"post", body: JSON.stringify(payload), credentials:"include", headers: {"Content-Type": "application/json"}})
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
          const response = await fetch(`http://localhost:9000/story/?parent_id=${parent_id}`,{method:"post", body: JSON.stringify(text), credentials:"include", headers: {"Content-Type": "application/json"}})
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

        try{            
          const response = await fetch("http://localhost:9000/text",{method:"post", body: JSON.stringify(payload), credentials:"include", headers: {"Content-Type": "application/json"}})
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
          const response = await fetch(`http://localhost:9000/story/?parent_id=${parent_id}`,{method:"post", body: JSON.stringify(text), credentials:"include", headers: {"Content-Type": "application/json"}})
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

  const handleNodeClick = (nodeDatum) => {
    if (nodeDatum.children.length===0){
      tryGetText(nodeDatum._id,nodeDatum.attributes.text)
    }
}

  return (
    // `<Tree />` will fill width/height of its container; in this case `#treeWrapper`.
    <StoryTreeContext.Provider value={storyTree}>
    <div id="treeWrapper"style={{height: "60vh"}} ref={containerRef}>
      <Tree data={storyTree} 
      orientation="vertical" 
      rootNodeClassName="node_root"
      branchNodeClassName="node_branch"
      leafNodeClassName="node_leaf"
      translate={translate}
      renderCustomNodeElement={(rd3tProps) =>
        renderNodeWithCustomEvents({ ...rd3tProps, handleNodeClick })
      }      
        />
    </div>
    </StoryTreeContext.Provider>
  )
}