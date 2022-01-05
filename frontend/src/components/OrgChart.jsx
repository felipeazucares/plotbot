import React, { useState, useEffect } from 'react';
import Tree from "react-d3-tree";

// This is a simplified example of an org chart with a depth of 2.
// Note how deeper levels are defined recursively via the `children` property.
const orgChart = {
  name: "Start here",
  children: [
    
    {
      name: "Option 1",
      attributes: {
        text: "There was a fire in the house and I ran down the steps to avoid it",
      },
      children: [
        {
          name: "Option 4",
          attributes: {
            text: "And I broke my leg",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
        {
          name: "Option 5",
          attributes: {
            text: "Assembly",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
        {
          name: "Option 6",
          attributes: {
            text: "Assembly",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
      ],
    },
    {
      name: "Option 2",
      attributes: {
        text: "There was a fire in the house and I called the police.",
      },
      children: [
        {
          name: "Foreman",
          attributes: {
            text: "Fabrication",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
        {
          name: "Foreman",
          attributes: {
            text: "Assembly",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
      ],
    },
    {
      name: "Option 3",
      attributes: {
        text: "There was a fire in the house and so I laughed.",
      },
      children: [
        {
          name: "Foreman",
          attributes: {
            text: "Fabrication",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
        {
          name: "Foreman",
          attributes: {
            text: "Assembly",
          },
          children: [
            {
              name: "Worker",
            },
          ],
        },
      ],
    },
  ],
};

export default function OrgChartTree() {
  return (
    // `<Tree />` will fill width/height of its container; in this case `#treeWrapper`.
    <div id="treeWrapper"style={{height: "60vh"}}>
      <Tree data={orgChart} orientation="vertical" />
    </div>
  );
}
