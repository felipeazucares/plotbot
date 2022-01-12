import React, { useContext, useState, useEffect} from "react"
import Tree from "react-d3-tree"
import './custom-tree.css'
import { useCenteredTree } from "./Helpers";
import { StoryTreeContext } from "../App"
import { Spinner } from '@chakra-ui/react'
import { Tooltip } from '@chakra-ui/react'


export default function OrgChartTree() {
  const {storyTree, setStoryTree} = useContext(StoryTreeContext)
  const [translate, containerRef] = useCenteredTree()
  const [text,setText] = useState("")
  const [isLoading, setLoading] = useState(false);
  const [isBackgroundDim,setIsBackgroundDim] = useState(false)
  const [status,setStatus] = useState("")
  


  const showSpinner = () => {
    setLoading(currentIsLoaded => !currentIsLoaded)
  };

        function returnNode2(newObj,currentTree, count){
          count = count + 1
            //recurse tree returned from mongo to d3_react_tree - RawNodeDatum format
            let currentKey = Object.keys(currentTree)[0]
            //const objName = truncateReplace(currentTree[currentKey].data.text,3)
            newObj= {_id: currentKey, name: count, attributes: {text:currentTree[currentKey].data.text},children:[]}
            console.log("current item:" + currentKey);
            if (currentTree[currentKey].children){
                console.log("children detected creating newObj.children=[]");
                currentTree[currentKey]["children"].forEach((child) =>{
                    console.log("processing child:" + Object.keys(child)[0]);
                    newObj.children.push(returnNode2(newObj,child, count))
                })
            }
            else {
                console.log("no children for :" + currentKey);
                console.log("returning newObj:" + JSON.stringify(newObj));
                return newObj
            }
            return newObj
        }


    function convertTree(inputTree){

        const newTree = returnNode2({}, inputTree,0)
        console.log(newTree);        
        return newTree

        }


    const tryGetStoryTree = async () => 
    {
        try{            
            const response = await fetch("http://localhost:9000/story",
                {
                    credentials:"include"
                 })
            if (response.status===200 && response.statusText==="OK"){
                const result = await response.json()
                console.log(`storyTree:${JSON.stringify(result.data.story)}`)
                setStoryTree(convertTree(result.data.story))

            } else {
                console.error(`get /story failed with status:${response.status} - ${response.statusText}`)
            }
        }
        catch(error){
            console.error(`Exception occured getting story tree: ${error}`)
        }
    }


    
    const tryGetText = async (parent_id,promptText) => {
   
      //get the last complete sentence from the prompt
      const endOfPenultimateSentence = promptText.substring(1,promptText.length-1).lastIndexOf(".")
      console.log(`promptText: ${promptText}`)
      console.log(`end of text: ${endOfPenultimateSentence}`)
      promptText=promptText.substring(endOfPenultimateSentence+2,promptText.length)
      console.log(`last sentence promptText: ${promptText}`)
      const payload={
        "prompt": promptText,
        "temperature": 0.71234132
      }

      //get last sentence from text provided
      
      try{            
        showSpinner(true)

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
      showSpinner(false)
      
    }
    
    const renderNodeWithCustomEvents = ({nodeDatum,toggleNode,handleNodeClick}) => (
      <Tooltip label={nodeDatum.attributes?.text}>
        <g>
        <circle r="10" style={{}} onClick={() => handleNodeClick(nodeDatum)} onMouseEnter={()=>handleHover()}/>
        <text fill="grey" strokeWidth="0" x="15" onClick={toggleNode}>
          {nodeDatum.name}

        </text>
        {/* {nodeDatum.attributes?.text && (
          <text fill="grey" x="20" y="20" strokeWidth="0">
            {nodeDatum.attributes?.text}
          </text>
        )} */}
      </g>
    </Tooltip>
  )
    const handleNodeClick = async (nodeDatum) => {
      if (nodeDatum.children.length===0){
        setIsBackgroundDim(true)
        setStatus("thinking")
        await tryGetText(nodeDatum._id,nodeDatum.attributes.text)
        await tryGetStoryTree()
        await tryGetText(nodeDatum._id,nodeDatum.attributes.text)
        await tryGetStoryTree()
        await tryGetText(nodeDatum._id,nodeDatum.attributes.text)
        await tryGetStoryTree()
        setIsBackgroundDim(false)
        setStatus("")
      }
    }

  const handleHover = () => {
    
  }

  //render component on load
  useEffect(() => {
    // document.body.style.background = {background};
    tryGetStoryTree()},[]);

  return (
    // `<Tree />` will fill width/height of its container; in this case `#treeWrapper`.
    <StoryTreeContext.Provider value={storyTree}>
    <div id="treeWrapper"style={{height: "60vh"}} ref={containerRef} className={isBackgroundDim ? 'background-grey' : 'background-white'}>
      <Tree data={storyTree}
      orientation="vertical" 
      rootNodeClassName="node_root"
      branchNodeClassName="node_branch"
      leafNodeClassName="node_leaf"
      enableLegacyTransitions="true"
      transitionDuration="2000"
      // onNodeMouseOver={window.alert("eh")}
      translate={translate}
      renderCustomNodeElement={(rd3tProps) =>
        renderNodeWithCustomEvents({ ...rd3tProps, handleNodeClick })
      }  
        />
    </div>

    {isLoading && <Spinner id="loader"
      thickness='20px'
      speed='2s'
      emptyColor='gray.200'
      color='blue.500'
      size='xl'></Spinner>}
    </StoryTreeContext.Provider>
  )
}